import cv2
import numpy as np
from logger import logger_config

class OldBookRemake:
    def __init__(self, file):
        # 要匯入的檔案名稱
        self.file = file

    def show_img(self, img):
        # 以視窗的形式展現圖片，視窗大小為圖片的一半
        # 若圖片太大，直接用cv2.imshow會以完整解析度呈現，所以改用下面的nameWindow把圖像放在裡面限制大小
        # 冷知識:在imshow顯示的時候，可以在選定的窗口中做圖片的複製(Ctrl+C)與保存(Ctrl+S)
        cv2.namedWindow("windows", 0)
        # 設定窗口大小，("名稱", x, y) x是寬度 y是高度，此處暫以縮小一半作呈現
        cv2.resizeWindow("windows", int(img.shape[1] / 2), int(img.shape[0] / 2))
        cv2.imshow("windows", img)
        cv2.waitKey()
        cv2.destroyAllWindows()

    def save_img(self, img, img_number):
        # Saving the image 儲存圖片
        # Using cv2.imwrite() method
        filename = f'OldBookRemake/OldBookRemake_page{img_number + 1}.tif'
        # img_remake[:,:,0] 0表示只取第一通道(單通道)
        cv2.imwrite(filename, img[:, :, 0], [int(cv2.IMWRITE_TIFF_RESUNIT), 2,  # 解析度單位
                                                 int(cv2.IMWRITE_TIFF_COMPRESSION), 5,  # 壓縮方式..?參數不確定
                                                 int(cv2.IMWRITE_TIFF_XDPI), 600,  # 設定水平dpi
                                                 int(cv2.IMWRITE_TIFF_YDPI), 600,  # 設定垂直dpi
                                                 ])

    def draw_approx_hull_polygon(self, img, cnts):
        # 參考自https://zhuanlan.zhihu.com/p/38739563
        img = np.copy(img)
        # 生成一張相同大小尺寸的空白圖(0..)
        # img = np.zeros(img.shape, dtype=np.uint8)

        # 藍色線段直接取等高線
        # cv2.drawContours(img, cnts, -1, (255, 0, 0), 2)  # blue
        # 綠色線段則是近似多邊形
        # epsilion = img.shape[0]/32
        # approxes = [cv2.approxPolyDP(cnt, epsilion, True) for cnt in cnts]
        # cv2.polylines(img, approxes, True, (0, 255, 0), 2)  # green
        # 紅色線段則是船殼多邊形，與綠色差別在是否"凹陷"；紅色不凹陷
        hulls = [cv2.convexHull(cnt) for cnt in cnts]
        cv2.polylines(img, hulls, True, (0, 0, 255), 2)  # red
        return img

    def draw_min_rect_circle(self, img, cnts):  # conts = contours
        img = np.copy(img)
        # img = np.zeros(img.shape, dtype=np.uint8)
        for cnt in cnts:
            x, y, w, h = cv2.boundingRect(cnt)
            # 藍色線段為正矩形
            cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)  # blue
            # # 綠色線段為"最小"矩形
            # min_rect = cv2.minAreaRect(cnt)  # min_area_rectangle
            # min_rect = np.int0(cv2.boxPoints(min_rect))
            # cv2.drawContours(img, [min_rect], 0, (0, 255, 0), 2)  # green
            # # 紅色線段為"最小"圓形
            # (x, y), radius = cv2.minEnclosingCircle(cnt)
            # center, radius = (int(x), int(y)), int(radius)  # for the minimum enclosing circle
            # img = cv2.circle(img, center, radius, (0, 0, 255), 2)  # red
        return img

    def detect_img(self, origin_img, resize_ratio, filter_size, dilate_iter):
        # 檢測圖片，思路:先將圖片做多次腐蝕，多次腐蝕會讓較小面積的文字被腐蝕掉，理論上圖片的區域會有較大的面積相連，因此不會被完全清除
        # 接下來在執行膨脹操作，目的是為了把保留下來的圖片區域膨脹回去原來大小(也可以多擴張一點，抓寬鬆)
        img = cv2.resize(origin_img, None, fx=resize_ratio, fy=resize_ratio)  # resize_ratio 縮放比率
        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        img_gray = cv2.medianBlur(img_gray, filter_size)  # filter_sieze 灰階模糊化濾波器大小
        ret, thresh = cv2.threshold(img_gray, 127, 255, cv2.THRESH_BINARY_INV)
        kernel = np.ones((3, 3), np.uint8) # 濾波核，可以調整大小，也可以指定參數
        thresh = cv2.dilate(thresh, kernel, iterations=2) # 先膨脹一次，讓有些掃圖的黑白間隙給補上
        thresh = cv2.erode(thresh, kernel, iterations=dilate_iter)  # 先腐蝕掉大部分的點
        thresh = cv2.dilate(thresh, kernel, iterations=dilate_iter+1)  # 在膨脹回原圖大小
        contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        # self.show_img(img) # 展示原圖
        return img, contours

    def img_preprocessing(self, origin_img, resize_ratio, filter_size, dilate_iter):
        img = cv2.resize(origin_img, None, fx=resize_ratio, fy=resize_ratio) # resize_ratio 縮放比率
        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        img_gray = cv2.medianBlur(img_gray, filter_size) # filter_sieze 灰階模糊化濾波器大小
        ret, thresh = cv2.threshold(img_gray, 127, 255, cv2.THRESH_BINARY_INV)
        kernel = np.ones((3, 5), np.uint8)
        thresh = cv2.dilate(thresh, kernel, iterations=dilate_iter) # dilate_iter 迭代次數
        contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        return img, contours

    def img_noise_processing(self, img, contours, min_area_size, indent):
        n = len(contours)
        contours_list = []
        clear_list = []
        for i in range(n):
            contours_list.append(i)
            area = cv2.contourArea(contours[i])
            # print(f"輪廓{i}面積 = {area}")
            M = cv2.moments(contours[i])
            cX = int(M["m10"] / M["m00"])  # 計算X方向質心
            cY = int(M["m01"] / M["m00"])  # 計算Y方向質心
            if area < min_area_size: # 測試 若面積小於一定閾值，則加入清除清單
                # cv2.circle(img, (cX, cY), 5, (0, 255, 0), -1) # 在要清除的區塊做綠點標記
                cv2.drawContours(img, contours, i, (0, 255, 0), -1)  # 在要將清除的區塊以綠色塗滿
                clear_list.append(i)
            # 直接設定四周邊界內縮距離
            if cX < indent or cX > (img.shape[1]-indent) or cY < indent or cY > (img.shape[0]-indent):
                # cv2.circle(img, (cX, cY), 10, (0, 0, 255), -1) # 在要清除的區塊做紅點標記
                cv2.drawContours(img, contours, i, (0, 0, 255), -1) # 在要將清除的區塊以紅色塗滿
                clear_list.append(i)
            """ # (封存)計算效率較低的方法，因為要取邊界所有的點和選取的面積計算距離
            for j in range(img.shape[0]): # 左邊界
                c_distance = ((0 - cX)**2 + (j - cY)**2)**0.5
                if c_distance < indent:
                    cv2.circle(img, (cX, cY), 5, (0, 255, 0), -1)
                    clear_list.append(i)
            for j in range(img.shape[0]):# 右邊界
                c_distance = ((img.shape[1] - cX) ** 2 + (j - cY) ** 2) ** 0.5
                if c_distance < indent:
                    cv2.circle(img, (cX, cY), 5, (0, 255, 0), -1)
                    clear_list.append(i)
            for j in range(img.shape[1]): # 上邊界
                c_distance = ((j - cX) ** 2 + (0 - cY) ** 2) ** 0.5
                if c_distance < indent:
                    cv2.circle(img, (cX, cY), 5, (0, 255, 0), -1)
                    clear_list.append(i)
            for j in range(img.shape[1]): # 下邊界
                c_distance = ((j - cX) ** 2 + (img.shape[0] - cY) ** 2) ** 0.5
                if c_distance < indent:
                    cv2.circle(img, (cX, cY), 5, (0, 255, 0), -1)
                    clear_list.append(i)
            """

        contours_list = set(contours_list).difference(set(clear_list))
        return contours_list

    def main(self, img_number, resize_ratio, filter_size, dilate_iter, min_area_size, indent):
        # 要處理的圖片序號
        imgs = []
        loaded, imgs = cv2.imreadmulti(self.file, img_number, 1, imgs, cv2.IMREAD_COLOR)

        for x in imgs:
            origin_img = x
            img, contours = self.detect_img(origin_img, resize_ratio, filter_size, dilate_iter)
            img = cv2.drawContours(img, contours, -1, (0, 0, 255), 5)
            self.show_img(img)
            contours_list = self.img_noise_processing(img,contours,min_area_size,indent)
            mask = np.zeros(img.shape, np.uint8)
            for i in contours_list:
                mask = cv2.drawContours(mask, contours, i, (255, 255, 255), -1)
            #
            # dst = cv2.drawContours(img, contours, -1, (255, 0, 0), 3)
            # self.show_img(dst)
            self.show_img(mask)
            mask_reverse = (np.ones(img.shape, dtype=np.uint8) * 255) - mask
            self.show_img(mask_reverse)
            mask_reverse = cv2.resize(mask_reverse, (origin_img.shape[1], origin_img.shape[0]))
            img_add = cv2.add(origin_img, mask_reverse)
            self.show_img(img_add)

            for cnt in contours: # 也許可以改用矩形包圍來處理 鏤空的案例
                x, y, w, h = cv2.boundingRect(cnt)
                # 藍色線段為正矩形
                cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), -1)
            self.show_img(img)

            # self.save_img(img_add,img_number)




if __name__ == '__main__':
    # class內填入要處理的檔案名稱
    file_name = "OldBook_CH.tif"
    OBR = OldBookRemake(file_name)

    logger_config = logger_config()
    logger = logger_config.create_logger("隨機測試")
    # 參數
    resize_ratio = 0.4  # 圖片縮放倍率
    filter_size = 3  # 灰階模糊化濾波器大小
    dilate_iter = 5  # 膨脹迭代次數
    min_area_size = 500  # 最小面積容忍閾值
    indent = 100  # 四邊內縮距離(pixel)

    # 挑幾張有代表性的圖片做測試
    img_number_list1 = [0, 2, 3, 4, 5]  # 較大字體
    img_number_list2 = [4, 7, 8, 9, 10]  # 較單純的圖片
    img_number_list3 = [11, 12, 14, 22, 30, 280, 800, 802]  # 文字+雜訊
    img_number_list4 = [215, 216, 278, 788]  # 雜訊汙染到文字(較難)
    img_number_list5 = [29, 81, 117, 421, 423, 426, 430, 432, 467, 493, 562, 613, 614, 624]  # 文字+圖片部分
    img_number_list6 = [616, 650, 666, 724, 725]  # 較淡的圖片+文字

    # for i in img_number_list2: # 測試清單 # 檢測圖片迭代次數至少要20以上
    #     OBR.main(i, resize_ratio, filter_size, 20, 200, indent)
    # 圖片部分參數
    OBR.main(7, 0.4, 3, 20, 500, 100) # 簡單圖片
    # OBR.main(432, 0.4, 3, 20, 500, 100) # 較難圖片，簍空，可用矩形補
    # OBR.main(81, 0.4, 3, 20, 500, 100)  # 較難圖片，簍空，矩形也補不完，可能還要用IOU跟Mask做對比(或統一都用IOU去算..?)

    # (81)文字部分參數，如逗點或像素數少的字(ex 一)，min_area_size建議取的保守(200)
    # OBR.main(21, 0.4, 3, 5, 200, 100)

    # 隨機測試
    # import random
    # x = random.randrange(0, 803, 1) # 從0到803隨機取整數，步伐為1
    # OBR.main(x, resize_ratio, filter_size, dilate_iter, 200, indent)
    # print(f'第{x}頁')

import cv2
import numpy as np

class OldBookRemake:
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
        loaded, imgs = cv2.imreadmulti("CHOLD.tif", img_number, 1, imgs, cv2.IMREAD_COLOR)

        for x in imgs:
            origin_img = x
            img, contours = self.img_preprocessing(origin_img, resize_ratio, filter_size, dilate_iter)
            contours_list = self.img_noise_processing(img,contours,min_area_size,indent)
            mask = np.zeros(img.shape, np.uint8)
            for i in contours_list:
                mask = cv2.drawContours(mask, contours, i, (255, 255, 255), -1)

            dst = cv2.drawContours(img, contours, -1, (255, 0, 0), 3)
            self.show_img(dst)
            self.show_img(mask)
            mask_reverse = (np.ones(img.shape, dtype=np.uint8) * 255) - mask
            self.show_img(mask_reverse)
            mask_reverse = cv2.resize(mask_reverse, (origin_img.shape[1], origin_img.shape[0]))
            img_add = cv2.add(origin_img, mask_reverse)
            self.show_img(img_add)

            img_line = self.draw_approx_hull_polygon(img, contours)
            img_rect = self.draw_min_rect_circle(img, contours)
            self.show_img(img_line)
            self.show_img(img_rect)

            self.save_img(img_add,img_number)

            """ # 嘗試用np強制將陣列內值用成0&1，再轉圖片，失敗
            x = img_add[:,:,0]/255
            x = x.astype(int)
            print(x)
            cv2.imwrite('test.tif', x)
            """

            """ # 嘗試使用PIL儲存圖片，也不太行? 位元深度有變1但dpi和壓縮方式都沒有，檔案也不小
            from PIL import Image
            img_add = Image.fromarray(img_add)
            img_add = img_add.convert('1')  # convert image to black and white
            img_add.save('OldBookRemake/result_col.tif')"""


if __name__ == '__main__':
    OBR = OldBookRemake()
    # 參數
    resize_ratio = 0.4  # 圖片縮放倍率
    filter_size = 3  # 灰階模糊化濾波器大小
    dilate_iter = 5  # 膨脹迭代次數
    min_area_size = 200  # 最小面積容忍閾值
    indent = 100  # 四邊內縮距離(pixel)

    # 挑幾張有代表性的圖片做測試
    img_number_list1 = [0, 2, 3, 4, 5] # 較大字體
    img_number_list2 = [7, 8, 9, 10] # 圖片
    img_number_list3 = [11, 12, 14, 22, 29, 30] # 文字+雜訊
    img_number_list4 = [81, 83, 85, 467, 500] # 文字+圖片部分

    # for i in img_number_list2: # 測試清單
    #     OBR.main(i, resize_ratio, filter_size, dilate_iter, min_area_size, indent)

    # 圖片部分參數
    OBR.main(0, resize_ratio, filter_size, dilate_iter, mi  n_area_size, indent)

    # (81)文字部分參數，如逗點或像素數少的字(ex 一)，min_area_size建議取的保守(200)
    # OBR.main(200, 0.4, 3, 5, 200, 100)

    # 隨機測試
    # import random
    # x = random.randrange(0, 803, 1) # 從0到803隨機取整數，步伐為1
    # OBR.main(x, resize_ratio, filter_size, dilate_iter, 200, indent)
    # print(x)

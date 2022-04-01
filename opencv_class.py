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
        # 檢測圖片；思路:先將圖片做多次腐蝕，多次腐蝕會讓較小面積的文字被腐蝕掉，理論上圖片的區域會有較大的面積相連，因此不會被完全清除
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
        return img, contours #@ img還是原圖...其實沒必要回傳，但先保留

    def img_preprocessing(self, origin_img, resize_ratio, filter_size, dilate_iter):
        # 圖像前處理；將原圖縮放->二值化->基礎模糊化->膨脹迭代->提取邊緣區塊輸出contours
        # contours包含的資料是框選到的區塊，一個區塊就是一個list
        img = cv2.resize(origin_img, None, fx=resize_ratio, fy=resize_ratio) # resize_ratio 縮放比率
        """
        # 測試功能:直接畫白線雖然可以切分開大區塊的雜訊，但可能會導致切分開的靠內的雜訊 質心落在範圍裏面
        # 會導致某些情況很好用，但某些情況不好用。也許可以考慮網狀的分割? (或是只選用左右白線或是上下白線)
        # 或是計算外框，若外框的雜訊數量仍然太多，則代表可以導入分割處理
        # cv2.line(img, (0, 50), (img.shape[1], 50), (255, 255, 255), 20) # 上白線
        # cv2.line(img, (0, img.shape[0]-50), (img.shape[1], img.shape[0]-50), (255, 255, 255), 30) # 下白線
        # cv2.line(img, (50, 0), (50, img.shape[0]-50), (255, 255, 255), 30) # 左白線
        # cv2.line(img, (img.shape[1]-50, 0), (img.shape[1]-50, img.shape[1]), (255, 255, 255), 20) # 右白線
        """
        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        img_gray = cv2.medianBlur(img_gray, filter_size) # filter_sieze 灰階模糊化濾波器大小
        ret, thresh = cv2.threshold(img_gray, 127, 255, cv2.THRESH_BINARY_INV)
        kernel = np.ones((3, 5), np.uint8)
        thresh = cv2.dilate(thresh, kernel, iterations=dilate_iter) # dilate_iter 迭代次數
        contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        return img, contours

    def img_noise_remove(self, img, contours, min_area_size, indent):
        # 雜訊處理；將前面框選出來的區塊，透過設定條件，來篩選那些是不要的雜訊
        # 兩種思路；其一透過計算面積，小於一定閾值的就清除掉。(謹慎取值，若是值設定的太激進逗點和句號可能都會消失，@也能嘗試透過數學取值，後25%的面積平均作為雜訊閾值?)
        # 其二透過計算質心，若是該區塊的質心落在指定的邊界外，則是為雜訊清除掉(要看各種案例，不曉得有沒有通則，或是透過一定的計算公式來決定取值)
        n = len(contours)
        contours_list = []
        clear_list = []
        for i in range(n):
            contours_list.append(i) # 此處只是順便建立contours的索引，因為contours是tuple不方便直接利用
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
        # contours_list和要清除的清單clear_list取差集，便可以獲得要保留的清單
        contours_list = set(contours_list).difference(set(clear_list))
        return contours_list

    def main(self, img_number, resize_ratio, filter_size, dilate_iter, min_area_size, indent):
        # img_number 是要處理的圖片序號
        # 以清單承接讀取出來的資料，其格式為(1,高度,寬度,通道數)，讀取複數圖片則為(n,高度,寬度,通道數)
        # 不一定只能用cv2.IMREAD_COLOR來讀取格式，UNCHANGED、GRAYSCALE應該也都可以
        # 但在中途的可視化還是需要以彩色呈現，因此在這邊先都以三通道圖像讀入，方便理解(後續單純執行程式的話，可以把中間很多地方優化掉)
        imgs = []
        loaded, imgs = cv2.imreadmulti(self.file, img_number, 1, imgs, cv2.IMREAD_COLOR)

        for x in imgs:
            origin_img = x
            img, contours = self.img_preprocessing(origin_img, resize_ratio, filter_size, dilate_iter)
            contours_list = self.img_noise_remove(img,contours,min_area_size,indent)
            mask = np.zeros(img.shape, np.uint8) # 先建立全黑的遮罩(也可以全白啦，思路相同)
            for i in contours_list:
                # 將要保留的區塊使用純白的色塊填滿
                mask = cv2.drawContours(mask, contours, i, (255, 255, 255), -1)
            # dst為在img基礎上畫上contours框選到的所有區塊
            # 紅色區塊和綠色區塊是img_noise_remove所標註的要清除的區域(理論上也可以複製新的圖片單獨呈現，但就都先畫在img上==)
            dst = cv2.drawContours(img, contours, -1, (255, 0, 0), 3)
            self.show_img(dst)
            self.show_img(mask) # 呈現黑底白內容物的遮罩
            mask_reverse = (np.ones(img.shape, dtype=np.uint8) * 255) - mask # 遮罩反轉(取反)
            self.show_img(mask_reverse) # 呈現白底黑內容物的遮罩 # 注意黑的值其實是0 白是255
            mask_reverse = cv2.resize(mask_reverse, (origin_img.shape[1], origin_img.shape[0])) # 遮罩resize回原圖尺寸大小
            img_add = cv2.add(origin_img, mask_reverse) # 將原圖和遮罩疊加，此時只有遮罩內為0(黑色)的區塊才會有原圖出現
            self.show_img(img_add)

            img_line = self.draw_approx_hull_polygon(img, contours) # 船型包圍的框線
            img_rect = self.draw_min_rect_circle(img, contours) # 矩形包圍的框線
            self.show_img(img_line)
            self.show_img(img_rect)

            self.save_img(img_add,img_number) # 儲存圖片 # 還有待更進一步處理

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
                        
    # for i in img_number_list2: # 測試清單
    #     OBR.main(i, resize_ratio, filter_size, dilate_iter, 200, indent)

    # 圖片部分參數，面積閾值可取500~800
    # x = 1
    # # OBR.main(x, 0.4, 3, 5, 500, 100)
    # # OBR.main(x, 1, 3, 5, 1250, 250) # 原圖處理
    # logger.info(f'圖片測試 {file_name} 第{x}頁')

    # 文字部分參數，如逗點或像素數少的字(ex 一)，min_area_size建議取的保守(200)
    # x = 759
    # OBR.main(x, 0.4, 3, 5, 200, 100)
    # logger.info(f'文字測試 {file_name} 第{x}頁')

    # 隨機測試
    # import random
    # x = random.randrange(0, 803, 1) # 從0到803隨機取整數，步伐為1
    # OBR.main(x, resize_ratio, filter_size, dilate_iter, 200, indent)
    # print(f'第{x}頁')
    # logger.info(f'隨機測試 {file_name} 第{x}頁')

    # cv2.imcount 可以讀取總頁數


    # img_test = cv2.imdecode(np.fromfile(r"C:\Users\jasper chiu\Downloads\OldBook_TWPoetry.tif", dtype=np.uint8), -1)
    # img_page = cv2.imcount(r"C:\Users\jasper chiu\Downloads\OldBook_TWPoetry.tif")
    # print(img_page)
    # print(img_test)
    # print(img_test.shape)
    # # img_write = cv2.imencode(".tif", img_test)[1].tofile(img_path)
    # OBR.show_img(img_test)

    """測試使用，嘗試以PIL讀進資料，避開cv2無法讀取中文路徑的問題"""

    from PIL import Image
    path = r"E:\JasperWork\PythonLearn\台灣現代詩史論.tif"
    def tifread(path):
        tiff = Image.open(path)
        # tiff = np.array(tiff)*255
        # print(tiff)
        images = []
        try:
            for i in range(0,10):
                tiff.seek(i)
                print(tiff.mode)
                images.append((np.array(tiff)*255).astype(np.uint8))
            return np.array(images)
        except:
            return np.array(images)


    images = tifread(path)
    print(len(images))
    print(images.shape)

    # img = cv2.cvtColor(np.array(images[0]), cv2.COLOR_RGB2BGR)

    # print(img)
    print(images[0].shape)
    OBR.show_img(images[0])


    # for i in images:
    #     OBR.show_img(i)
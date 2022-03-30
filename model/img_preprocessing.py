import cv2
import numpy as np

class ImgPreprocessing:
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
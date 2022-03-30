import cv2
import numpy as np

class ImgNoiseRemove:
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
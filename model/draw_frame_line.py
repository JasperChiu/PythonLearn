import cv2
import numpy as np

class DrawFrameLine:
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

import cv2
import numpy as np
import matplotlib.pyplot as plt

def show_img(img):
    # 以視窗的形式展現圖片，視窗大小為圖片的一半
    # 若圖片太大，直接用cv2.imshow會以完整解析度呈現，所以改用下面的nameWindow把圖像放在裡面限制大小
    cv2.namedWindow("windows", 0)
    # 設定窗口大小，("名稱", x, y) x是寬度 y是高度，此處暫以縮小一半作呈現
    cv2.resizeWindow("windows", int(img.shape[1]/2), int(img.shape[0]/2))
    cv2.imshow("windows", img)
    cv2.waitKey()
    cv2.destroyAllWindows()

img = cv2.imread("oldbook_bad.jpg")
# img.shpae -> (高,寬,通道數)
# 將圖片轉成灰度圖
img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# 將灰階圖模糊化，能先處理掉一些噪點；有用
img_gray = cv2.medianBlur(img_gray,5)
# 將圖片二值化，ret是閾值，thresh是承接二值化後的資料
# cv2.THRESH_BINARY_INV是在將其反轉，因為我們在乎的是文字的部分
# 也有自適應二值化的方法，可以嘗試https://shengyu7697.github.io/python-opencv-threshold/
ret, thresh = cv2.threshold(img_gray, 127, 255, cv2.THRESH_BINARY_INV)
# th2 = cv2.adaptiveThreshold(img_gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, 13, 2) # 自適應效果不佳

# kernel 膨脹的卷積核
kernel = np.ones((3, 5), np.uint8)
# 迭代次數表示做幾次膨脹操作，不一定做膨脹操作，但有膨脹的話會取得比較寬限，不會吃掉邊線
thresh = cv2.dilate(thresh, kernel, iterations=5)

# thresh = cv2.Canny(thresh, 128, 256) # 邊緣檢測，會取的較細連文字部分都捕捉

# cv2.findContour 接受的參數為二值圖，才能抓出等高線
contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# 以下嘗試將框選內東西令為白色
print(f"資料類型 :{type(contours)}")
n = len(contours)
print(n)
for i in range(n):
    # 迴圈計算影像框選到的面積
    M = cv2.moments(contours[i])
    area = cv2.contourArea(contours[i])
    print(f"輪廓{i}面積 = {area}")
    # 可以最後提取出最大值
# contours後的-1是取全部，可以單獨選取第n個框選目標，最後面是框線粗度
dst = cv2.drawContours(img,contours,-1,(255,0,0),3)

mask = np.zeros(img.shape, np.uint8)
dst = cv2.drawContours(mask,contours,12,(255,255,255),-1)
show_img(dst)
dst_mask = (np.ones(img.shape, dtype=np.uint8)*255) - dst
show_img(dst_mask)
img_add = cv2.add(img, dst_mask)
show_img(img_add)

def draw_approx_hull_polygon(img, cnts):
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

def draw_min_rect_circle(img, cnts):  # conts = contours
    # img = np.copy(img)
    img = np.zeros(img.shape, dtype=np.uint8)
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

# 帶入原圖和先前計算的等高線
img_line = draw_approx_hull_polygon(img, contours)
# img_rect = draw_min_rect_circle(img, contours)

# img_add = cv2.add(img, img_line) # 將兩個影像暴力疊加起來
# img_fusion = cv2.addWeighted(img, 0.5, img_line, 0.5, 0) # 將兩個影像按比例融合起來

show_img(img_line)
# show_img(img_rect)






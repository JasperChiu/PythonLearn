import cv2
import numpy as np
import matplotlib.pyplot as plt

# 練習將cv2通道轉換成plt可讀的形式
# 讀入圖片
img = cv2.imread("Lenna_(test_image).png")

# 方法一 用cv2將通道從bgr轉換成rgb，因為matplotlib是吃rgb的通道順序
plt_img1 = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

# 方法二 先用cv2將圖片通道分離，在合併回plt的格式
# cv2將圖片通道分離(亦可以用np索引的方式)
b, g, r = cv2.split(img)
# 用cv2.merge將通道合併回plt的格式(rgb)
plt_img2 = cv2.merge((r, g, b))
# 指定要展示哪張圖片
# 若用cv2讀取的圖片，沒有轉換直接用plt展示的話圖片顯示會不一樣
plt.subplot(1, 3, 1)
plt.title("origin img")
plt.imshow(img)
plt.subplot(1, 3, 2)

plt.title("plt_img1")
plt.imshow(plt_img1)
plt.subplot(1, 3, 3)

plt.title("plt_img2")
plt.imshow(plt_img2)

plt.show()



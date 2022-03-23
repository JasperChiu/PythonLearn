import cv2
import numpy as np
# 讀入圖片
img = cv2.imread("Lenna_(test_image).png")
# 生成灰色圖片
img_grey = cv2.imread("Lenna_(test_image).png", 0)

# 1. 練習顯示圖片
"""
# 展示原圖
cv2.imshow("img", img)
# 展示灰色圖片
cv2.imshow("img_grey", img_grey)
# 等待圖片的關閉
cv2.waitKey()
# 關閉所有視窗，不關閉視窗程式無法正常中止；無引數
cv2.destroyAllWindows()
# 儲存灰色圖片
cv2.imwrite("Copy.png", img_grey)
"""

# 2. 練習圖片通道處理、分離、合併等
"""
# cv2將圖片通道分離，並將三層的陣列指定以b,g,r變數來承接，cv2.split()是一個比較耗時的操作，能用Numpy索引就儘量使用索引
b, g, r = cv2.split(img)
# 推薦用 numpy 索引方式，單獨提取出藍綠紅，在cv2中便是對應第0,1,2通道
b = img[:, :, 0]
g = img[:, :, 1]
r = img[:, :, 2]
# 以下是直接用np賦值，將第一通道(藍)全部令為0
# img[:, :, 0] = 0

# 用np建立一個512*512的空陣列，指定資料型態np.uint8
# 因為cv2讀出來的資料型態是uint8，若要合併通道則須將格式轉換成相同的形式；("dtype="可以省略)
zero_array = np.zeros((512, 512), dtype=np.uint8)
# 同樣用np產生空陣列，img.shape會提取出圖片的(長,寬,通道數)，而[:2]就是取tuple的0,1位址的值
zero_array2 = np.zeros(img.shape[:2], dtype=np.uint8)
# 將分離的通道合併回去，
# img_merge = cv2.merge((b, g, r))
# 只保留藍色通道，其餘通道令為0。
img_merge = cv2.merge((b, zero_array, zero_array))
# 查看各圖片的資料型態
# print(img.dtype)
# print(b.dtype)
# print(zero_array.dtype)

cv2.imshow("img_merge", img_merge)
cv2.waitKey()
cv2.destroyAllWindows()
"""
# 3. 指定矩形內區域為指定顏色
"""
img_crop = img
# 指定區域[x,y] [0到50,50到最後](註:左上角為原點(0,0))
img_crop[0:50, 50:] = (255, 255, 255)
cv2.imshow("img_crop", img_crop)
cv2.waitKey()
cv2.destroyAllWindows()
"""
# 4. cv2.resize 縮放圖片 resize(src, dsize, dst=None, fx=None, fy=None, interpolation=None)

# 指定(寬,高)尺寸大小，直接將圖片拉伸縮放到該大小；若沒有指定插植方式則預設使用INTER_LINEAR雙線性插植
img_resize2 = cv2.resize(img, (256, 256), interpolation=cv2.INTER_NEAREST)
# 指定縮放的倍率，分為x軸和y軸(寬,高)，注意dsize部分要設定為None
img_resize1 = cv2.resize(img, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_NEAREST)

cv2.imshow("img", img)
cv2.imshow("img_size1", img_resize1)
cv2.imshow("img_size2", img_resize2)
cv2.waitKey()
cv2.destroyAllWindows()


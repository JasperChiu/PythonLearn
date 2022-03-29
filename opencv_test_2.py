import cv2
import numpy as np

def show_img(img):
    # 以視窗的形式展現圖片，視窗大小為圖片的一半
    # 若圖片太大，直接用cv2.imshow會以完整解析度呈現，所以改用下面的nameWindow把圖像放在裡面限制大小
    # 冷知識:在imshow顯示的時候，可以在選定的窗口中做圖片的複製(Ctrl+C)與保存(Ctrl+S)
    cv2.namedWindow("windows", 0)
    # 設定窗口大小，("名稱", x, y) x是寬度 y是高度，此處暫以縮小一半作呈現
    cv2.resizeWindow("windows", int(img.shape[1]/2), int(img.shape[0]/2))
    cv2.imshow("windows", img)
    cv2.waitKey()
    cv2.destroyAllWindows()
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

# 設定空的清單用來承接TIF檔的資料
imgs = []
# cv2.imreadmulti()該函數是用來一次性讀取多張圖片的
# cv2.imreadmulti()，第一個參數為讀取的檔名，第二個為第幾張圖片，第三個為一次讀取進入幾張
# 第四個為讀取方式(TIF檔先用IMREAD_COLOR讀成三通道的圖片，後續較方便理解、處理)
loaded,imgs = cv2.imreadmulti("OldBook_CH.tif", 0, 1, imgs, cv2.IMREAD_COLOR)
# for i in imgs:
#     img = cv2.resize(i, None, fx=0.4, fy=0.4)
#     img_gray = cv2.medianBlur(img,3)
#     ret, thresh = cv2.threshold(img_gray, 127, 255, cv2.THRESH_BINARY)
#     show_img(thresh)


for x in imgs:
    # 保存原始圖片，將變數x從imgs承接到的圖片資料複製給origin_img
    origin_img = x
    # 先將圖片縮小進行處理，注意img是resize過的喔
    img = cv2.resize(origin_img, None, fx=0.4, fy=0.4)
    # img.shpae -> (高,寬,通道數)
    # 將圖片轉成灰度圖
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # 將灰階圖模糊化，能先處理掉一些噪點；有用；注意濾波器開到太大旁邊的數字可能就被塗掉了
    # img_gray = cv2.medianBlur(img_gray,3)

    # 將圖片二值化，ret是閾值，thresh是承接二值化後的資料
    # cv2.THRESH_BINARY_INV是在將其反轉，因為我們在乎的是文字的部分
    # 因為後續的膨脹操作以及捕捉邊緣等高線等等方法，都是以"值"為基礎，而黑=0 白=255程式上操作都是以有值的為主
    ret, thresh = cv2.threshold(img_gray, 127, 255, cv2.THRESH_BINARY_INV)

    # 也有自適應二值化的方法，可以嘗試https://shengyu7697.github.io/python-opencv-threshold/
    # 以下為自適應二值化方法，效果不佳，推測因為原圖已經是二值化的型態，不須多此一舉
    # th2 = cv2.adaptiveThreshold(img_gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, 13, 2)

    # kernel 膨脹的卷積核
    kernel = np.ones((3, 5), np.uint8)
    # 迭代次數表示做幾次膨脹操作，不一定做膨脹操作，但有膨脹的話會取得比較寬限，不會吃掉邊線
    thresh = cv2.dilate(thresh, kernel, iterations=5)

    # 3/29 簡單重新測試cv2.Canny()，再多膨脹一兩次就能提取出更細節的邊緣
    # thresh = cv2.Canny(thresh, 128, 256) # 邊緣檢測，會取的較細連文字部分都捕捉
    # show_img(thresh)
    # thresh = cv2.dilate(thresh, kernel, iterations=2)
    # show_img(thresh)

    # cv2.findContour() 接受的參數為二值圖，才能抓出等高線
    # 第一個參數為尋找輪廓的圖像，第二個參數是輪廓的檢索模式(檢索模式可參考https://blog.csdn.net/hjxu2016/article/details/77833336)
    # cv2.RETR_EXTERNAL只檢測外輪廓，第三個參數cv2.CHAIN_APPROX_SIMPLE有壓縮水平方向、垂直方向、對角線方向的元素；
    # cv2.CHAIN_APPROX_NONE則為儲存所有輪廓點等，可以根據需要調整算法(可能會影響計算時間)
    # 計算完成會回傳兩個參數，contours為ndarray的list
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # 以下嘗試將框選內東西令為白色
    print(f"資料類型 :{type(contours)}")
    n = len(contours)
    print(n)
    contours_list = []
    clear_list = []
    for i in range(n):
        contours_list.append(i) # 將contours資料點加入清單，後續用於選擇要挑出那些輪廓
        # 迴圈計算影像框選到的面積
        area = cv2.contourArea(contours[i])
        print(f"輪廓{i}面積 = {area}")
        # 可以最後提取出最大值(面積最大的)
        # 計算每個輪廓的質心
        M = cv2.moments(contours[i])
        cX = int(M["m10"] / M["m00"]) # 計算X方向質心
        cY = int(M["m01"] / M["m00"]) # 計算Y方向質心

        if area < 500: # 測試 若面積小於一定閾值，則加入清除清單
            # cv2.circle(img, (cX, cY), 5, (0, 255, 0), -1) # 在要清除的區塊做綠點標記
            cv2.drawContours(img, contours, i, (0, 255, 0), -1)  # 在要將清除的區塊以綠色塗滿
            clear_list.append(i)
        # 計算輪廓質心與左邊界的距離(理論上可以先加上篩選條件就不用全部點都計算，或是只計算垂直水平距離等)
        # 或是也可以直接規定四邊界內縮100pixel的質心加入要篩選掉的清單!(暴力簡單)[已完成]
        if cX < 100 or cX > (img.shape[1]-100) or cY < 100 or cY > (img.shape[0]-100):
            # 在img原圖上於座標(cX, cY)繪製小圓點
            # cv2.circle(img, (cX, cY), 10, (0, 0, 255), -1) # 在要清除的區塊做紅點標記
            cv2.drawContours(img, contours, i, (0, 0, 255), -1) # 在要將清除的區塊以紅色塗滿
            clear_list.append(i)

        """ # (封存)計算效率較低的方法，因為要取邊界所有的點和選取的面積計算距離        
        # 左邊界
        for j in range(img.shape[0]):
            c_distance = ((0 - cX)**2 + (j - cY)**2)**0.5
            # print(c_distance)
            if c_distance < 100:
                cv2.circle(img, (cX, cY), 5, (0, 255, 0), -1)
                # 將不要的輪廓加入clear.list清單中
                clear_list.append(i)
        # 右邊界
        for j in range(img.shape[0]):
            c_distance = ((img.shape[1] - cX)**2 + (j - cY)**2)**0.5
            # print(c_distance)
            if c_distance < 100:
                cv2.circle(img, (cX, cY), 5, (0, 255, 0), -1)
                clear_list.append(i)
        # 上邊界
        for j in range(img.shape[1]):
            c_distance = ((j - cX)**2 + (0 - cY)**2)**0.5
            # print(c_distance)
            if c_distance < 100:
                cv2.circle(img, (cX, cY), 5, (0, 255, 0), -1)
                clear_list.append(i)
        # 下邊界
        for j in range(img.shape[1]):
            c_distance = ((j - cX)**2 + (img.shape[0] - cY)**2)**0.5
            # print(c_distance)
            if c_distance < 100:
                cv2.circle(img, (cX, cY), 5, (0, 255, 0), -1)
                clear_list.append(i)
        """

    # contours後的-1是取全部，可以單獨選取第n個框選目標，最後面是框線粗度
    # dst是在img的基礎上根據contours的資料繪製框線(會畫在img上!!)
    # 特別注意!前面其實不需要用變數來承接資料，因為她是直接畫在原圖上...==，這樣操作也只是讓變數dst承接繪製完的資料，拿到後面使用這樣

    # 創建一個蒙版(mask)(也可以在後面 +255)，產生一張全白的蒙版
    mask = np.zeros(img.shape, np.uint8)
    # cv2.drawContours()，第一個參數是指明在哪幅影像上繪製輪廓(mask)，第二個參數是輪廓本身，在python中是list(contours)
    # 第三個參數是繪製輪廓list中的哪條輪廓，如果是-1則繪製其中所有輪廓。第四個參數是色彩，第五個參數是繪製線段的粗度，若為-1則為填充模式
    # 在mask(全黑圖像上)繪製填充色塊(白色色塊)
    # mask = cv2.drawContours(mask, contours, -1, (255, 255, 255), -1)

    # 以下測試項目

    # clear_list = set(clear_list) # 刪除重複元素
    # contours_list = set(contours_list) # 將清單轉成set(集合)，用於取差集
    # contours_list = contours_list - clear_list
    # 也可以縮成
    # contours_list = set(contours_list) - set(clear_list) # ver1
    contours_list = set(contours_list).difference(set(clear_list)) # ver2
    # contours_list = set(clear_list).difference(set(contours_list)) # 反著取就變成看那些點是被刪除的點
    for i in contours_list:
        mask = cv2.drawContours(mask,contours,i,(255,255,255),-1)

    # 0327 17:00；問題點，目前是一次處理完成，對於大面積的處理OK但對於文字部分可能會連同逗點都處理掉
    # 也許可以考慮分階段處理，膨脹迭代次數大有助於保留較細節的文字如逗點等(單相對的雜訊也會保留)
    # 膨脹迭代次數小的話，輪廓就會分割得更多，此時對於面積的篩選條件就要降低
    # 關鍵影響參數 1.膨脹迭代係數 2.面積的篩選閾值 3.邊界內縮處理閾值
    # 面積篩選閾值的思路可以從數學角度來思考，將檢測到的輪廓面積列出來，取後四分之一平均作為閾值或是直接排序篩掉後四分之一的點(可能會誤殺)，都可以試試看
    # 邊界內縮處理的思路可能要看處理的資料...不敢下定論，目前是抓內縮100 pixel效果還行，但最好要有個方法算or公式算or直接訂一個常數

    # 二階段處理思路，A. 一階段 先使用膨脹迭代*10+大面積篩選閾值(1000)，二階段在使用較低的迭代係數*2+小面積篩選閾值(進一步篩選雜點)
    # B. 或是二階段在較大膨脹迭代*10+數學取面積篩選閾值 (思路:因為一階段已經處理完大部分雜點，畫面已經較為乾淨，比較不會因為膨脹把想要的文字和雜點連接起來)
    # 新增，處理資料的大小也可以考慮，目前是resize成1/4大小(xy都除以2)，若resize成更小處理會更快，但取的range會更大?
    # 用原尺寸處理可能會更精細，但計算時間可能更長要考慮的東西也更多這樣
    # 以上測試項目


    # 註記:(0,0,0)是黑色；(255,255,255)是白色
    show_img(mask)
    # 將np全1的矩陣*255再減去蒙版等於取反
    mask_reverse = (np.ones(img.shape, dtype=np.uint8)*255) - mask
    show_img(mask_reverse)

    # resize 是要填(x寬,y高)，img.shape提供的是(高,寬,通道數)，img.shape在搞==
    # 此處是將蒙版縮放回原始圖像的大小，並與原始圖像合併
    mask_reverse = cv2.resize(mask_reverse,(origin_img.shape[1],origin_img.shape[0]))
    img_add = cv2.add(origin_img, mask_reverse)
    show_img(img_add)

    # 帶入原圖和先前計算的等高線
    img_line = draw_approx_hull_polygon(img, contours)
    img_rect = draw_min_rect_circle(img, contours)

    show_img(img_line)
    show_img(img_rect)
    # img_add = cv2.add(img, img_line) # 是將兩個影像暴力疊加起來
    # img_fusion = cv2.addWeighted(img, 0.5, img_line, 0.5, 0) # 將兩個影像按比例融合起來








import cv2
import os

class ImgTools:
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

    def save_img(self, book_name, img, img_number):
        dir_path =f"./OldBookRemake_{book_name[:-4]}"
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
        # Saving the image 儲存圖片
        # Using cv2.imwrite() method
        filename = f'{dir_path}/OldBookRemake_{book_name[:-4]}_page{img_number + 1}.tif'
        # img_remake[:,:,0] 0表示只取第一通道(單通道)
        cv2.imwrite(filename, img[:, :, 0], [int(cv2.IMWRITE_TIFF_RESUNIT), 2,  # 解析度單位
                                             int(cv2.IMWRITE_TIFF_COMPRESSION), 5,  # 壓縮方式..?參數不確定
                                             int(cv2.IMWRITE_TIFF_XDPI), 600,  # 設定水平dpi
                                             int(cv2.IMWRITE_TIFF_YDPI), 600,  # 設定垂直dpi
                                             ])


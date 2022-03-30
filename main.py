import logging
import cv2
import numpy as np
from logger import logger_config
from BLL.import_book import ImportBook
from BLL.img_tools import ImgTools
from model.img_preprocessing import ImgPreprocessing
from model.img_noise_remove import ImgNoiseRemove
from model.draw_frame_line import DrawFrameLine
from model.img_process import ImgProcess

class OldBookRemake:
    def __init__(self, file):
        # 要匯入的檔案名稱
        self.file = file
    def process_one_img(self, img_number, resize_ratio, filter_size, dilate_iter, min_area_size, indent):
        imgs = ImportBook().import_book_one_page(self.file, img_number)
        img_add = ImgProcess().img_process(imgs, resize_ratio, filter_size, dilate_iter, min_area_size, indent)
        # ImgTools().show_img(img_add)
        ImgTools().save_img(self.file, img_add, img_number)
        logger.info(f'圖像處理 第{img_number+1}頁 完成')

    def process_all_img(self, resize_ratio, filter_size, dilate_iter, min_area_size, indent):
        img_number = 0
        try:
            while True:
                # 一次讀取一張，若直接將整本書讀取到清單中的話，記憶體會爆炸
                imgs = ImportBook().import_book_one_page(self.file, img_number)
                if len(imgs) == 0: # 若len(imgs)==0 表示沒有讀取到圖片，則跳出迴圈
                    break
                img_add = ImgProcess().img_process(imgs, resize_ratio, filter_size, dilate_iter, min_area_size, indent)
                ImgTools().save_img(self.file, img_add, img_number)
                img_number += 1
                logger.info(f'圖像處理 第{img_number}頁 完成')
        except:
            logger.warning("發生錯誤")


if __name__ == '__main__':
    # class內填入要處理的檔案名稱
    book_name = "OldBook_CH.tif"
    OBR = OldBookRemake(book_name)

    logger_config = logger_config()
    logger = logger_config.create_logger(f"{book_name[:-4]}_圖像處理") # [:-4]為了清除掉後面附加的檔名(.tif)

    # 處理單張圖的測試
    img_add = OBR.process_one_img(0, 0.4, 3, 5, 200, 100)

    # import time
    # start = time.time()

    # OBR.process_all_img(0.4, 3, 5, 200, 100) # 處理整本書
    # "OldBook_CH.tif" 本地筆電耗時338.8秒

    # end = time.time()
    # print(format(end - start))
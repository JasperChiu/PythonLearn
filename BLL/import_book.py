import cv2

class ImportBook:
    def import_book_one_page(self, book_name, img_number):
        try:
            imgs = []
            loaded, imgs = cv2.imreadmulti(book_name, img_number, 1, imgs, cv2.IMREAD_COLOR)
            return imgs
        except:
            # 怪怪的不確定該怎麼樣紀錄
            logger_config = logger_config()
            logger = logger_config.create_logger("隨機測試")
            logger.info('匯入檔案名稱錯誤')





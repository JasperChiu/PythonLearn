# -*- coding: utf-8 -*-

"""這個檔案為測試外部python檔案調用這裡的class，能否輸出log到統一設定的log檔案"""

import logging
import sys
# 為了引用隔壁資料夾的logger檔案，要將上一層資料夾加入系統路徑，然後再引入
# from 資料夾.py檔名 import class_name
sys.path.append('..')
from logs.logger import MyLogger

class log_testcase:
    def __init__(self):
        self.logger = MyLogger.create_logger()
        self.logger.info('內層的python檔案被調用了')
        # self.logger = logging.getLogger('fileAndConsole')

    def py_log_test123(self):
        try:
            self.logger.info('執行py_log_test123函式')
            self.logger.info('控制台顯示層級為INFO')
        except:
            # exc_info=True 參數設為True就可以記錄例外(Exception)
            self.logger.error('error 訊息', exc_info=True)
            self.logger.critical('critical 訊息', exc_info=True)


if __name__ == '__main__':
    rt = log_testcase()
    run = rt.py_log_test123()



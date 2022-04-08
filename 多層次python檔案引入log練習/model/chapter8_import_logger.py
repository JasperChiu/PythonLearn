# -*- coding: utf-8 -*-

"""此練習為引入不同資料夾下的logger.py設定檔"""

import logging
import sys
# 為了引用隔壁資料夾的logger檔案，要將上一層資料夾加入系統路徑，然後再引入
# from 資料夾.py檔名 import class_name
sys.path.append('..')
from logs.logger import MyLogger

class run_testcase:
    def __init__(self):
        self.logger = MyLogger.create_logger()
        self.logger.info('開始記錄log')

    def py_log_test(self):
        try:
            self.logger.debug('debug 訊息')
            self.logger.info('info 訊息')
            self.logger.warning('warn 訊息', exc_info=True)
            x = 5 / 0
            # debug、info、warning這幾行通常會在一般的時候使用，紀錄資訊等
        except Exception as e:
            # exc_info=True 參數設為True就可以記錄例外(Exception)
            self.logger.error('error 訊息')
            self.logger.critical('critical 訊息', exc_info=True)
            # Exception as e 可以調出精簡的錯誤訊息，再結合exc_info=True，可以給出完整錯誤訊息
            self.logger.info(e, exc_info=True)


if __name__ == '__main__':
    run = run_testcase().py_log_test()



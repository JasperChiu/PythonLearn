# -*- coding: utf-8 -*-

import logging
# 調用logger
from logs.logger import MyLogger
# 調用測試用的檔案
from model.uselog import log_testcase

class run_testcase:
    def __init__(self):
        self.logger = MyLogger.create_logger()
        self.logger.info('開始記錄main.py log')
        # self.logger = logging.getLogger('fileAndConsole')

    def py_log_test(self):
        try:
            self.logger.info('main.py的py_log_test正確執行中')
        except Exception as e:
            # exc_info=True 參數設為True就可以記錄例外(Exception)
            self.logger.error('error 訊息')
            self.logger.critical('critical 訊息', exc_info=True)
            # Exception as e 可以調出精簡的錯誤訊息，再結合exc_info=True，可以給出完整錯誤訊息
            self.logger.error(e, exc_info=True)


if __name__ == '__main__':
    # 調用同一python檔案的class
    rrun = run_testcase().py_log_test()
    # 調用model資料夾底下的uselog.py，測試能否正確執行，並輸出log到同一檔案
    lrun = log_testcase().py_log_test123()




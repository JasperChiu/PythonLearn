import logging
from logging.handlers import TimedRotatingFileHandler
from datetime import datetime

class MyLogger:

    @staticmethod
    def create_logger():
        my_logger = logging.getLogger("my_logger")
        my_logger.setLevel("DEBUG")
        filename = "{:%Y-%m-%d}".format(datetime.now()) + '.log'
        # 控制檯處理器
        stream_handler = logging.StreamHandler()
        stream_handler.setLevel("INFO") # 可以設定多少層級的訊息才要輸出到控制台

        # 使用時間滾動的檔案處理器
        log_file_handler = TimedRotatingFileHandler(filename="log.log", when='D', interval=1, backupCount=10)
        log_file_handler.setLevel("DEBUG") # 可以設定多少層級的訊息才要輸出到log檔案


        formatter = logging.Formatter('%(asctime)s - [%(filename)s-->line:%(lineno)d] - %(levelname)s: %(message)s')
        stream_handler.setFormatter(formatter)
        log_file_handler.setFormatter(formatter)

        if not my_logger.handlers:
            my_logger.addHandler(stream_handler)
            my_logger.addHandler(log_file_handler)
        return my_logger

if __name__ == '__main__':
    # 呼叫類的靜態方法，建立一個日誌收集器
    log = MyLogger.create_logger()
    log.info("test-info")
    log.error("test-error")
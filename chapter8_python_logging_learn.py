import logging
import datetime

# 獨立建立一個dev_logger而不是使用稱為root的logger
dev_logger = logging.getLogger(name="Jasper")
# 設定 logger 輸出級別的函式，即輸出debug即比debug層級更高(>10)的錯誤訊息
dev_logger.setLevel(logging.DEBUG)
# 設定 log 訊息格式的特性 formatter
formatter = logging.Formatter("%(asctime)s-%(name)s-%(levelname)s-%(message)s",
                              datefmt="%Y%m%d")

# 1. 要輸出到console的設定
# handler 負責處理 log 訊息的輸出工作，StreamHandler() 在不加任何參數的情況下
# 會把訊息輸出到 stderr，在作業系統未做額外的配置下，stderr 可以簡單的理解為顯示到螢幕上。
ch = logging.StreamHandler()
# 指定在console中 設定要顯示的層級
ch.setLevel(logging.DEBUG)
# 設定格式(套用先前設定好的格式)
ch.setFormatter(formatter)
# 添加handler，而一個 logger 可以加上數個 handler，除了加入一個 StreamHandler 外，還可以再定義其他的 handler
# 例如一個 FileHandler，如此一則 log 訊息就會被顯示在螢幕上以及被存到某個 log 檔內。
dev_logger.addHandler(ch)

# 2. 要輸出到log日誌檔的設定
# 設定 log 檔名
log_filename = datetime.datetime.now().strftime("%Y%m%d_test_log.log")
# 將log日誌記錄輸出到文件中，是從 StreamHandler 繼承了輸出功能。
# 預設的 mode 是 a:續寫 w:覆寫
fh = logging.FileHandler(log_filename, mode="a")
# 指定在log日誌檔中 設定要顯示的層級
fh.setLevel(logging.DEBUG)
# 設定格式(套用先前設定好的格式)
fh.setFormatter(formatter)
# 添加handler，而一個 logger 可以加上數個 handler，了加入一個 StreamHandler 外，還可以再定義其他的 handler
# 例如一個 FileHandler，如此一則 log 訊息就會被顯示在螢幕上以及被存到某個 log 檔內。
dev_logger.addHandler(fh)


if __name__ == "__main__":
    # logging.basicConfig 基本的 log 輸出設定)，進階設置完就不需要再調用，這也能儲存基本的log資訊
    # LOGGING_FORMAT = "%(asctime)s-%(name)s-%(levelname)s-%(message)s"
    # logging.basicConfig(level=logging.DEBUG, filename=log_filename, filemode="w",
    #                     format=LOGGING_FORMAT,datefmt="%Y%m%d")

    dev_logger.debug('debug message')       # 10
    dev_logger.info('info message')         # 20
    dev_logger.warning('warning message')   # 30
    dev_logger.error('error message')       # 40
    dev_logger.critical('critical message') # 50
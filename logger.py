import logging
import os
from datetime import datetime

dir_path = './logs/' # 設定 logs 目錄
filename = "{:%Y-%m-%d}".format(datetime.now()) + '.log' # 設定檔名

# log_folder 是設定log檔案要存放的資料夾，引入定義時需命名
def create_logger(log_folder):
    # config
    logging.captureWarnings(True)  # 捕捉 py waring message
    logger = logging.getLogger('Jasper')  # 捕捉 py waring message
    logger.setLevel(logging.DEBUG) #設定層級
    detail_formatter = logging.Formatter("%(asctime)s-%(name)s-%(filename)s-%(funcName)s-"
                                         "%(module)s-%(lineno)d-%(levelname)s-%(message)s",
                                         datefmt="%Y%m%d")
    simple_formatter = logging.Formatter("%(asctime)s-%(name)s-%(levelname)s-%(message)s",
                                         datefmt="%Y%m%d")

    # 若不存在目錄則新建
    if not os.path.exists(dir_path+log_folder):
        os.makedirs(dir_path+log_folder)

    # 註記若要詳細資訊 logger.debug('debug message', exc_info=True)；後面要加註 exc_info=True
    # file handler
    fileHandler = logging.FileHandler(f"{dir_path}{log_folder}/{filename}", 'a', 'utf-8') # 續寫設定
    # fileHandler = logging.FileHandler(f"{dir_path}{log_folder}/{filename}", 'w', 'utf-8') # 覆寫設定
    fileHandler.setLevel(logging.DEBUG)
    fileHandler.setFormatter(detail_formatter)
    logger.addHandler(fileHandler)

    # console handler
    consoleHandler = logging.StreamHandler()
    consoleHandler.setLevel(logging.DEBUG)
    consoleHandler.setFormatter(simple_formatter)
    logger.addHandler(consoleHandler)

    return logger
# -*- coding: utf-8 -*-
import logging
import datetime

# 同時輸出到 console 與日誌檔
dev_logger = logging.getLogger(name="Jasper")
dev_logger.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s-%(name)s-%(levelname)s-%(message)s",
                              datefmt="%Y%m%d")
# 輸出到console
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
ch.setFormatter(formatter)

# 輸出成日誌檔
log_filename = datetime.datetime.now().strftime("%Y%m%d_test_log.log")
fh = logging.FileHandler(log_filename, mode="a")
fh.setLevel(logging.DEBUG)
fh.setFormatter(formatter)

dev_logger.addHandler(ch)
dev_logger.addHandler(fh)

if __name__ == "__main__":
    dev_logger.debug("debug")
    dev_logger.info("info")
    dev_logger.warning("warning")
    dev_logger.error("error")
    dev_logger.critical("critical")



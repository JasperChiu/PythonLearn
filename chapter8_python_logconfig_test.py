# -*- coding: utf-8 -*-

import logging
import logging.config

logging.config.fileConfig('logging.conf')

# create logger
logger = logging.getLogger('fileAndConsole')

# 'application' code
# logger.debug('debug message')
# logger.info('info message')
# logger.warning('warn message')
# logger.error('error message')
# logger.critical('critical message')

try:
    logger.debug('debug message', exc_info=True)
    logger.info('info message', exc_info=True)
    logger.warning('warn message', exc_info=True)
    x = 5 / 0
    # debug、info、warning這幾行通常會在一般的時候使用，紀錄資訊等
except:
    # exc_info=True 參數設為True就可以記錄例外(Exception)
    logger.error('error message', exc_info=True)
    logger.critical('critical message', exc_info=True)


def login(username=None, password=None):
    if username is None or password is None:
        logger.error("登錄失敗，用戶名或密碼為空")
        return {"code": 400, "msg": "用戶名或密碼為空"}
    if username == "Jasper" and password == "123456":
        logger.info("登錄成功，正常信息版")
        # logger.warning("登錄成功，警告版")
        return {"code": 200, "msg": "登錄成功"}
    logger.info("登錄失敗，用戶名或密碼錯誤")
    return {"code": 300, "msg": "用戶名或密碼錯誤"}

print(login("Jasper"))
print(login("Jasper","123444"))
print(login("Jasper","123456"))
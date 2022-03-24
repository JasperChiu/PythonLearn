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
    x = 5 / 0
except:
    # exc_info=True 參數設為True就可以記錄例外(Exception)
    logger.debug('debug message', exc_info=True)
    logger.info('info message', exc_info=True)
    logger.warning('warn message', exc_info=True)
    logger.error('error message', exc_info=True)
    logger.critical('critical message', exc_info=True)

try:
    x = 1
    y = "1"
    z = x + y
except:
    # exc_info=True 參數設為True就可以記錄例外(Exception)
    logger.debug('debug message', exc_info=True)
    logger.info('info message', exc_info=True)
    logger.warning('warn message', exc_info=True)
    logger.error('error message', exc_info=True)
    logger.critical('critical message', exc_info=True)
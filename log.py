import logging
import sys


APP_LOGGER_NAME="bili-sofa"

def setup_applevel_logger(logger_name = APP_LOGGER_NAME, file_name=None): 
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    sh = logging.StreamHandler(sys.stdout)
    sh.setFormatter(formatter)
    fh = logging.FileHandler("ob.log")
    fh.setFormatter(formatter)

    logger.handlers.clear()
    logger.addHandler(sh)
    logger.addHandler(fh)

    if file_name:
        fh = logging.FileHandler(file_name)
        fh.setFormatter(formatter)
        logger.addHandler(fh)
    return logger


def get_logger():    
   return logging.getLogger(APP_LOGGER_NAME)

logger = setup_applevel_logger()
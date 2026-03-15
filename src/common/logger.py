import logging
import os
from datetime import datetime

#创建日志目录
log_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "logs")
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

#日志配置
def setup_logger():
    logger = logging.getLogger("api_auto")
    logger.setLevel(logging.INFO)

    #避免重复添加处理器
    if logger.handlers:
        return logger
    
    #文件处理器
    log_file= os.path.join(log_dir, f"api_test_{datetime.now().strftime('%Y%m%d')}.log")
    file_handler = logging.FileHandler(log_file, encoding="utf-8")
    file_handler.setLevel(logging.INFO)

    #控制台处理器
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)

    #日志格式
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s"
    )
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    #添加处理器
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger

#全局日志实例
logger = setup_logger()
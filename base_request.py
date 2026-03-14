import requests
import logging
import os
import allure
from datetime import datetime

# ===================== 1. 配置日志 =====================
# 创建logs文件夹（不存在则自动创建）
if not os.path.exists("logs"):
    os.makedirs("logs")

# 日志配置
logging.basicConfig(
    level=logging.INFO,  # 日志级别：DEBUG < INFO < WARNING < ERROR
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",  # 日志格式
    handlers=[
        # 输出到文件（按时间命名，避免覆盖）
        logging.FileHandler(f"logs/api_auto_{datetime.now().strftime('%Y%m%d')}.log", encoding="utf-8"),
        # 同时输出到控制台
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("api_auto")  # 日志器名称

# ===================== 2. 封装请求（加日志+Allure） =====================


class BaseRequest:
    """封装requests请求，增加日志记录+Allure集成"""
    def get(self, url, params=None, headers=None):
        """封装GET请求"""
        try:
            log_msg = f"发送GET请求：URL={url}，参数={params}"
            logger.info(log_msg)
            allure.attach(log_msg, "请求日志", allure.attachment_type.TEXT)
            
            response = requests.get(url, params=params, headers=headers, timeout=10)
            
            log_msg = f"GET响应：状态码={response.status_code}，响应内容={response.text[:200]}"
            logger.info(log_msg)
            allure.attach(log_msg, "响应日志", allure.attachment_type.TEXT)
            return response
        except Exception as e:
            log_msg = f"GET请求失败：{str(e)}"
            logger.error(log_msg, exc_info=True)
            allure.attach(log_msg, "错误日志", allure.attachment_type.TEXT)
            raise

    def post(self, url, json=None, headers=None, timeout=10):
        """封装POST请求（优先json格式）"""
        try:
            log_msg = f"POST请求：URL={url}，JSON数据={json}, 超时={timeout}秒"
            logger.info(log_msg)
            allure.attach(log_msg, "请求日志", allure.attachment_type.TEXT)
            #适配多环境超时配置
            response = requests.post(
                url=url,
                json=json,
                headers=headers,
                timeout=timeout
            )
            
            log_msg = f"POST响应：状态码={response.status_code}，响应内容={response.text[:200]}"
            logger.info(log_msg)
            allure.attach(log_msg, "响应日志", allure.attachment_type.TEXT)
            return response
        except Exception as e:
            log_msg = f"POST请求失败：{str(e)}"
            logger.error(log_msg, exc_info=True)
            allure.attach(log_msg, "错误日志", allure.attachment_type.TEXT)
            raise

# 实例化
req = BaseRequest()
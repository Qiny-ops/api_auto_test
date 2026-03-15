import requests
import os
import sys
import allure

# ========== 同样添加项目根目录到sys.path ==========
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, BASE_DIR)

# 导入日志模块（现在能识别了）
from src.common.logger import logger

class BaseRequest:
    """HTTP请求封装"""
    
    def __request(self, method, url, **kwargs):
        """核心请求方法"""
        try:
            logger.info(f"📢 {method.upper()}请求：URL={url}，参数={kwargs}")
            allure.attach(f"{method.upper()} {url}\n参数：{kwargs}", "请求信息", allure.attachment_type.TEXT)
            
            response = requests.request(
                method=method,
                url=url,
                timeout=kwargs.pop("timeout", 10),
                **kwargs
            )
            
            logger.info(f"📩 响应：状态码={response.status_code}，响应体={response.text[:500]}")
            allure.attach(f"状态码：{response.status_code}\n响应体：{response.text}", "响应信息", allure.attachment_type.TEXT)
            
            return response
        except Exception as e:
            logger.error(f"❌ 请求失败：{str(e)}", exc_info=True)
            allure.attach(f"请求失败：{str(e)}", "错误信息", allure.attachment_type.TEXT)
            raise
    
    def get(self, url, params=None, headers=None, **kwargs):
        """GET请求"""
        return self.__request("get", url, params=params, headers=headers, **kwargs)
    
    def post(self, url, json=None, data=None, headers=None, **kwargs):
        """POST请求"""
        return self.__request("post", url, json=json, data=data, headers=headers, **kwargs)

# 全局请求实例
req = BaseRequest()
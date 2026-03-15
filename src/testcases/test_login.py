import os
import sys
import json
import allure
import pytest
from src.common.base_request import req

# 核心：添加项目根目录到系统路径
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, PROJECT_ROOT)

# ===================== 数据驱动（核心学习点） =====================
def load_login_test_data():
    """加载登录测试数据（新手易理解）"""
    # 拼接数据文件路径
    data_file = os.path.join(PROJECT_ROOT, "src/data/login_data.json")
    # 读取JSON数据
    with open(data_file, "r", encoding="utf-8") as f:
        data = json.load(f)
    # 转换为pytest参数化格式（匹配你的原始字段）
    return [
        (
            case["case_name"],
            case["username"],
            case["password"],
            case["expected_username"],
            case["expected_pwd_len"]
        )
        for case in data["login_cases"]
    ]

# 预加载数据（一次加载，所有用例复用）
LOGIN_TEST_DATA = load_login_test_data()
# 生成用例ID（Allure报告显示中文用例名，新手易读）
LOGIN_CASE_IDS = [case[0] for case in LOGIN_TEST_DATA]

# ===================== 测试用例（新手易理解） =====================
@allure.feature("登录模块")  # 大模块（Allure报告分类）
class TestLogin:
    @allure.story("登录接口数据驱动测试")  # 子功能
    @pytest.mark.parametrize(
        "case_name, username, password, expected_username, expected_pwd_len",
        LOGIN_TEST_DATA,
        ids=LOGIN_CASE_IDS
    )
    def test_login(self, env_config, case_name, username, password, expected_username, expected_pwd_len):
        """登录接口测试（数据驱动核心）"""
        # Allure报告标题（显示环境+用例名）
        allure.dynamic.title(f"【{env_config['env']}】{case_name}")
        
        # 1. 构造请求（新手易改）
        url = f"{env_config['base_url']}/post"  # 模拟登录接口
        request_data = {"username": username, "password": password}
        
        # 2. 发送请求（复用封装的req）
        response = req.post(url, json=request_data, headers=env_config["headers"])
        
        # 3. 断言（核心验证，新手易理解）
        assert response.status_code == 200, f"状态码错误，预期200，实际{response.status_code}"
        assert response.json()["json"]["username"] == expected_username, "返回用户名与预期不符"
        assert len(response.json()["json"]["password"]) == expected_pwd_len, "密码长度与预期不符"
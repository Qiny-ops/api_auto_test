import pytest
import allure
import json
from base_request import req
from conftest import read_json_data

# 预加载JSON数据，用于生成ids
with open("data/login_data.json", "r", encoding="utf-8") as f:
    json_data = json.load(f)
    case_ids = [case["case_name"] for case in json_data["login_cases"]]


# =============== 多环境+数据驱动用例(核心) =============================

@allure.feature("登录接口-多环境数据驱动")
class TestLoginWithMultiEnv:
    @allure.story("JSON数据+多环境执行")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.parametrize(
        "case_name, username, password, expected_username, expected_pwd_len",
        read_json_data("login_data.json"),
        ids=case_ids  # 核心：让报告显示中文用例名
    )
    def test_login_multi_json(self, env_config, case_name, username, password, expected_username, expected_pwd_len):
        """
        登录接口多环境数据驱动测试
        :param env_config: 多环境配置（包含base_url/headers/env等
        """
         # 动态设置用例标题（环境+用例名，报告核心优化）
        allure.dynamic.title(f"【{env_config['env']}环境】 {case_name}")
        
        #步骤1： 打印当前环境（日志/控制台可见）
        with allure.step(f"1. 确认执行环境：{env_config['env']}"):
            allure.attach(env_config["env"], "执行环境", allure.attachment_type.TEXT)

        #步骤2： 拼接环境专属URL
        with allure.step(f"2.拼接接口URL："):
            url = f"{env_config['base_url']}/post"
            allure.attach(url, "接口URL", allure.attachment_type.TEXT)

        #步骤3： 构造请求数据
        with allure.step(f"3.构造请求数据："):
            request_data = {"username": username, "password": password}
            allure.attach(
                json.dumps(request_data, ensure_ascii=False),
                "请求数据",
                allure.attachment_type.JSON
            )
            
        #步骤4：发送请求（带超时配置）
        with allure.step("发送POST请求"):
            response = req.post(
                url=url,
                json=request_data,
                headers=env_config["headers"],
                timeout=env_config["timeout"]
            )
        
        #步骤5：断言响应（失败重跑后仍失败标记为失败）
        with allure.step("5.断言响应结果"):
            # 核心断言（失败会触发pytest.ini的重跑机制）
            assert response.status_code == 200, f"【{env_config['env']}环境】状态码错误"
            assert response.json()["json"]["username"] == expected_username, f"【{env_config['env']}环境】用户名返回错误"
            assert len(response.json()["json"]["password"]) == expected_pwd_len, f"【{env_config['env']}环境】密码长度错误"
        
        #附加环境专属响应数据
        allure.attach(
            json.dumps(response.json(), ensure_ascii=False, indent=2),
            f"【{env_config['env']}环境】完整响应数据",
            allure.attachment_type.JSON
        )

# ===================== Excel用例暂时注释（先保证JSON跑通） =====================
# @allure.feature("登录模块")
# class TestLoginWithExcel:
#     @allure.story("数据驱动-Excel")
#     @allure.severity(allure.severity_level.NORMAL)
#     @pytest.mark.parametrize("case_name, username, password, expected_username, expected_pwd_len",
#                              read_excel_data("login_data.xlsx"))
#     def test_login_excel(self, env_config, case_name, username, password, expected_username, expected_pwd_len):
#         """Excel数据驱动登录测试"""
#         with allure.step(f"执行用例：{case_name}"):
#             url = f"{env_config['base_url']}/post"
#             data = {"username": username, "password": password}
#             
#             with allure.step("发送POST请求"):
#                 response = req.post(url, json=data, headers=env_config["headers"])
#             
#             with allure.step("断言响应结果"):
#                 assert response.status_code == 200
#                 assert response.json()["json"]["username"] == expected_username
#                 assert len(response.json()["json"]["password"]) == expected_pwd_len
#             
#             allure.attach(case_name, "用例名称", allure.attachment_type.TEXT)
#             allure.attach(response.text, "响应内容", allure.attachment_type.JSON)
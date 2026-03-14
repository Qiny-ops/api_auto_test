import allure
import pytest
import json  # 新增：确保json模块导入
from base_request import req

@allure.feature("用户信息模块（需登录Token）")
class TestUserInfo:
    @allure.story("获取用户基本信息")
    # 修复1：装饰器中只留简单标题，去掉复杂表达式
    @allure.title("获取用户信息接口")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_get_user_info(self, env_config, auth_headers):
        """
        核心验证点：
        1. 请求头自动携带Token
        2. 接口响应正常
        3. Token有效性验证（真实项目可断言Token相关字段）
        """
        # 修复2：先提取env变量，再动态设置标题
        env = env_config["env"]
        allure.dynamic.title(f"【{env}环境】获取用户信息接口")
        
        # 1. 构造业务接口URL（真实项目替换为实际接口）
        url = f"{env_config['base_url']}/get"
        
        # 2. 发送请求（自动携带Token）
        with allure.step("1. 发送带Token的请求"):
            # 打印请求头，验证Token是否携带（控制台可见）
            print(f"\n📤 请求头（含Token）：{auth_headers}")
            # 调用封装的请求方法
            resp = req.get(
                url=url,
                headers=auth_headers,  # 直接使用带Token的请求头
                timeout=env_config["timeout"]
            )
        
        # 3. 断言验证
        with allure.step("2. 验证响应结果"):
            # 基础断言：状态码200
            assert resp.status_code == 200, f"❌ 状态码错误，预期200，实际{resp.status_code}"
            # 验证请求头中是否包含Token（httpbin会返回请求头，真实项目可断言业务字段）
            resp_headers = resp.json()["headers"]
            assert "Authorization" in resp_headers, "❌ 请求头未携带Token"
            assert resp_headers["Authorization"].startswith("Bearer "), "❌ Token格式错误"
        
        # 4. 附加响应到报告
        with allure.step("3. 附加响应数据到报告"):
            allure.attach(
                json.dumps(resp.json(), ensure_ascii=False, indent=2),
                "完整响应数据",
                allure.attachment_type.JSON
            )
            # 附加Token到报告，便于追溯
            allure.attach(
                auth_headers["Authorization"],
                "使用的Token",
                allure.attachment_type.TEXT
            )

    @allure.story("修改用户昵称（需Token）")
    # 修复1：装饰器标题简化
    @allure.title("修改用户昵称接口")
    def test_update_user_nickname(self, env_config, auth_headers):
        """
        扩展场景：带Token+业务参数的POST请求
        """
        # 修复2：动态设置标题
        env = env_config["env"]
        allure.dynamic.title(f"【{env}环境】修改用户昵称接口")
        
        url = f"{env_config['base_url']}/post"
        # 构造业务参数
        update_data = {
            "nickname": "AI测试工程师",
            "user_id": 123456
        }
        
        with allure.step("1. 发送修改昵称请求"):
            resp = req.post(
                url=url,
                json=update_data,
                headers=auth_headers
            )
        
        with allure.step("2. 验证修改结果"):
            assert resp.status_code == 200
            # 验证请求参数是否正确传递
            assert resp.json()["json"]["nickname"] == "AI测试工程师"
            # 验证Token是否携带
            assert resp.json()["headers"]["Authorization"] is not None
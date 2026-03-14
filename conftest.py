import pytest
import yaml
import os
import json
import openpyxl
from base_request import req

# ===================== 读取配置文件 =====================
def read_env_config(env="test"):
    """
    读取指定环境的配置文件
    :param env: 环境标识（test=测试/ pre=预发/ prod=生产）
    :return: 环境配置字典
    """
    current_dir = os.path.dirname(os.path.abspath(__file__))
    #环境配置文件映射（一键切换核心）
    env_file_map = {
        "test": "test_config.yaml",
        "pre": "pre_config.yaml",
        "prod": "prod_config.yaml"
    }
    #拼接配置文件路径
    config_path = os.path.join(current_dir, "config", env_file_map.get(env, "test_config.yaml"))

    try:
        with open(config_path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)
    except Exception as e:
        raise Exception(f"读取{env}文件失败：{str(e)}")


# 可选：命令行指定环境（更灵活）
def pytest_addoption(parser):
    """新增命令行参数：--env 指定执行环境"""
    parser.addoption(
        "--env", 
        action="store", 
        default="test", 
        help="指定测试环境：test(默认)/pre/prod"
    )

@pytest.fixture(scope="session")
def env_config(request):
    """通过命令行参数获取环境配置（替代上面的params方式）"""
    env = request.config.getoption("--env")
    config = read_env_config(env)
    config["env"] = env
    return config


#==========================新增：Token 自动获取 Fixture =======================
@pytest.fixture(scope="session") #session级：整个测试只执行1次
def token(env_config):
    """
    自动登录获取Token, 核心逻辑：
    1. 调用登录接口
    2. 从响应中提取Token(真实项目替换提取逻辑)
    3. 返回Token供其他接口使用
    """
    #1. 获取当前环境的基础配置
    base_url = env_config["base_url"]
    headers = env_config["headers"].copy()   #避免修改原配置

    #2. 构造登录请求参数（真实项目替换为实际登录参数）
    login_url = f"{base_url}/post"  
    login_data = {
        "username": "test123",
        "password": "123456"
    }

    #3. 发送登录请求
    print(f"\n 正在【{env_config['env']}环境】执行自动登录....")
    resp = req.post(url=login_url, json=login_data, headers=headers)

    # 4. 提取Token（关键：真实项目需根据接口响应格式修改）
    # 示例1：若响应是 {"code":200,"data":{"token":"xxx"}} → 取 resp.json()["data"]["token"]
    # 示例2：httpbin无真实Token，模拟生成一个
    if resp.status_code == 200:
        # 真实项目替换这行：token_str = resp.json()["data"]["token"]
        token_str = f"mock-token-{env_config['env']}-123456789"
        print(f"✅ 【{env_config['env']}环境】登录成功，Token：{token_str}")
        return token_str
    else:
        raise Exception(f"❌ 【{env_config['env']}环境】登录失败，状态码：{resp.status_code}")


# ===================== 新增：带Token的请求头 Fixture =====================
@pytest.fixture(scope='session')
def auth_headers(env_config, token):
    """
    封装带Token的请求头，所有需要登录态的接口直接使用
    企业级格式：Authorization: Bearer {token}（也可根据接口要求改为 Token: {token}）
    """
    headers = env_config["headers"].copy()
    # 关键：添加Token到请求头（真实项目按接口要求调整格式）
    headers["Authorization"] = f"Bearer {token}"
    return headers

    
# ===================== 读取JSON测试数据（核心：返回列表套元组） =====================
def read_json_data(file_name):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(current_dir, "data", file_name)
    try:
        with open(data_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        case_list = []
        for case in data["login_cases"]:
            case_tuple = (
                case["case_name"],
                case["username"],
                case["password"],
                case["expected_username"],
                case["expected_pwd_len"]
            )
            case_list.append(case_tuple)
        return case_list
    except Exception as e:
        raise Exception(f"读取JSON数据失败：{str(e)}")
    

# # ===================== 全局fixture（多环境+基础配置） =====================
# @pytest.fixture(scope="session", params=["test", "pre"])   #批量执行多环境
# #@pytest.fixture(scope="session", params=["test", "pre"])   #生产环境单独执行 

# def api_config(request):
#     """
#     多环境配置Fixture：
#     1. 默认执行测试+预发环境
#     2. 如需指定单环境：修改params为["test"]/["pre"]/["prod"]
#     """

#     env = request.param  #获取当前执行环境
#     config = read_env_config(env)
#     config["env"] = env
#     return {
#         "base_url": config["base_url"],
#         "headers": config["headers"],
#         "timeout": config["timeout"],
#         "env": env    #传递环境名称用例
#     }


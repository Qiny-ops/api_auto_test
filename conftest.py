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

# ===================== 全局fixture（多环境+基础配置） =====================
@pytest.fixture(scope="session", params=["test", "pre"])   #批量执行多环境
#@pytest.fixture(scope="session", params=["test", "pre"])   #生产环境单独执行 

def api_config(request):
    """
    多环境配置Fixture：
    1. 默认执行测试+预发环境
    2. 如需指定单环境：修改params为["test"]/["pre"]/["prod"]
    """

    env = request.param  #获取当前执行环境
    config = read_env_config(env)
    config["env"] = env
    return {
        "base_url": config["base_url"],
        "headers": config["headers"],
        "timeout": config["timeout"],
        "env": env    #传递环境名称用例
    }

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
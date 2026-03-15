import pytest
import yaml
import os
import sys
import json

# ========== 关键：项目根目录 = configtest.py所在目录 ==========
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, PROJECT_ROOT)

# 导入src模块（现在路径正确）
from src.common.base_request import req

# ===================== 1. 定义命令行参数 =====================
def pytest_addoption(parser):
    parser.addoption(
        "--env",
        action="store",
        default="test",
        help="指定执行环境：test/pre/prod"
    )

# ===================== 2. 多环境配置Fixture =====================
@pytest.fixture(scope="session")
def env_config(request):
    env = request.config.getoption("--env")
    # 拼接配置文件路径（根目录 → src/config）
    config_dir = os.path.join(PROJECT_ROOT, "src/config")
    config_file = os.path.join(config_dir, f"{env}_config.yaml")
    
    if not os.path.exists(config_file):
        raise FileNotFoundError(f"❌ 环境配置文件不存在：{config_file}")
    
    with open(config_file, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)
    config["env"] = env
    return config

# ===================== 3. Token自动管理 =====================
@pytest.fixture(scope="session")
def token(env_config):
    login_url = f"{env_config['base_url']}/post"
    login_data = {"username": "test123", "password": "123456"}
    
    response = req.post(login_url, json=login_data, headers=env_config["headers"])
    assert response.status_code == 200, "❌ 登录接口请求失败"
    
    token_str = f"mock-token-{env_config['env']}-888888"
    print(f"\n✅ 【{env_config['env']}】登录成功，Token：{token_str}")
    return token_str

# ===================== 4. 带Token的请求头 =====================
@pytest.fixture(scope="session")
def auth_headers(env_config, token):
    headers = env_config["headers"].copy()
    headers["Authorization"] = f"Bearer {token}"
    return headers
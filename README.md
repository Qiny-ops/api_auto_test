<<<<<<< HEAD
以下是您提供的 README 内容（企业级标准版），已提取为可直接复制的 Markdown 格式：

```markdown
# 接口自动化测试框架（Login API Auto Test）
基于 Python + Pytest 实现的企业级接口自动化测试框架，支持多环境切换、数据驱动、失败重跑、Token 自动管理、Allure 精美报告，可直接用于登录类接口的自动化测试与回归验证。
=======
# 接口自动化测试框架（Login API Auto Test）
基于 Python + Pytest 实现的企业级接口自动化测试框架，支持多环境切换、数据驱动、失败重跑、Allure 精美报告，可直接用于登录类接口的自动化测试与回归验证。
>>>>>>> 2058c1dd6a36ba27a0d3c9a7584ac20b6821dfe6

## 📋 框架特点
- 🚀 **数据驱动**：支持 Excel/JSON 外部数据文件，用例与数据完全分离
- 🌍 **多环境切换**：一键切换测试/预发/生产环境，无需修改代码
- 🔄 **失败重跑**：用例失败自动重试，提升框架稳定性
<<<<<<< HEAD
- 🔑 **Token 自动管理**：全局 Token 提取与携带，适配登录态接口
=======
>>>>>>> 2058c1dd6a36ba27a0d3c9a7584ac20b6821dfe6
- 📊 **可视化报告**：集成 Allure 生成精美测试报告，支持步骤/附件/环境展示
- 📜 **完整日志**：请求/响应/错误日志自动记录，便于问题定位
- 🎯 **高扩展性**：新增接口/用例只需补充数据文件，核心代码无需改动

## 📂 框架目录结构
```
login_api_auto/
├── base_request.py        # HTTP请求封装（含日志/Allure集成）
<<<<<<< HEAD
├── conftest.py            # 全局Fixture（多环境/Token/数据读取）
├── test_login.py          # 登录接口测试用例（数据驱动）
├── test_user_info.py      # 业务接口测试用例（带Token校验）
=======
├── conftest.py            # 全局Fixture（多环境/数据读取）
├── test_login.py          # 登录接口测试用例（数据驱动）
>>>>>>> 2058c1dd6a36ba27a0d3c9a7584ac20b6821dfe6
├── pytest.ini             # Pytest全局配置（失败重跑/用例匹配）
├── config/                # 多环境配置文件夹
│   ├── test_config.yaml   # 测试环境配置（域名/Headers/超时）
│   ├── pre_config.yaml    # 预发环境配置
│   └── prod_config.yaml   # 生产环境配置
├── data/                  # 测试数据文件夹
│   ├── login_data.json    # JSON格式测试数据
│   └── login_data.xlsx    # Excel格式测试数据（可选）
├── logs/                  # 日志文件夹（自动生成）
├── allure-results/        # Allure报告数据（运行后自动生成）
└── README.md              # 框架说明文档
```

## 🛠 环境准备
### 1. 依赖安装
```bash
# 安装所有依赖包
pip install -r requirements.txt

# 若未创建requirements.txt，可执行以下命令手动安装
pip install pytest==7.4.3 openpyxl==3.1.2 pyyaml==6.0.1 allure-pytest==2.13.2 requests==2.31.0
```

### 2. 依赖包说明
<<<<<<< HEAD
| 包名          | 作用                 |
| ------------- | -------------------- |
| pytest        | 测试用例执行框架     |
| openpyxl      | 读取Excel测试数据    |
| pyyaml        | 读取YAML格式配置文件 |
| allure-pytest | 生成Allure测试报告   |
| requests      | 发送HTTP请求         |
=======
| 包名           | 作用                     |
|----------------|--------------------------|
| pytest         | 测试用例执行框架         |
| openpyxl       | 读取Excel测试数据        |
| pyyaml         | 读取YAML格式配置文件     |
| allure-pytest  | 生成Allure测试报告       |
| requests       | 发送HTTP请求             |
>>>>>>> 2058c1dd6a36ba27a0d3c9a7584ac20b6821dfe6

## 🚀 快速运行
### 1. 运行所有用例（默认测试环境）
```bash
# 执行用例并生成Allure报告数据
pytest -v -s --alluredir=allure-results

# 启动Allure报告（自动打开浏览器）
allure serve allure-results
```

### 2. 指定环境运行
```bash
# 运行生产环境用例
pytest --env prod -v -s --alluredir=allure-results

# 仅运行登录接口JSON数据用例
pytest test_login.py::TestLoginWithMultiEnv -v -s --env test
```

### 3. 禁用失败重跑（调试用）
```bash
pytest -v -s --no-rerun --alluredir=allure-results
```

## 📊 核心功能使用说明
### 1. 多环境切换
- 新增环境：在 `config/` 目录下新增 `xxx_config.yaml`，配置 `base_url`/`headers`/`timeout` 即可
- 运行指定环境：通过 `--env 环境名` 命令行参数指定（如 `--env pre` 运行预发环境）

### 2. 数据驱动扩展
#### JSON 数据扩展
修改 `data/login_data.json`，新增 `login_cases` 数组元素即可：
```json
{
  "login_cases": [
    {
      "case_name": "新增用例-密码含特殊字符",
      "username": "test123",
      "password": "123456@",
      "expected_username": "test123",
      "expected_pwd_len": 7
    }
  ]
}
```

#### Excel 数据扩展
在 `data/login_data.xlsx` 中新增一行数据，框架会自动读取并执行。

<<<<<<< HEAD
### 3. Token 自动管理
- 框架通过 `conftest.py` 中 `token` Fixture 自动登录获取 Token
- 所有需要登录态的接口，通过 `auth_headers` Fixture 自动携带 Token
- 替换真实项目时，只需修改 `token` Fixture 中的 Token 提取逻辑即可

=======
>>>>>>> 2058c1dd6a36ba27a0d3c9a7584ac20b6821dfe6
## 📈 报告查看
1. 运行用例后，执行 `allure serve allure-results` 启动报告
2. 报告包含：
   - 用例执行结果（通过率/失败原因）
   - 多环境执行区分
   - 每条用例的请求/响应数据
   - 失败重跑记录
   - 日志附件

## 🎯 扩展指南
### 新增业务接口用例
1. 在项目根目录新建 `test_xxx.py`
<<<<<<< HEAD
2. 参考 `test_user_info.py` 编写用例，复用 `api_config`/`auth_headers` Fixture
=======
2. 参考 `test_login.py` 编写用例，复用 `api_config` Fixture
>>>>>>> 2058c1dd6a36ba27a0d3c9a7584ac20b6821dfe6
3. 在 `data/` 目录新增对应数据文件（JSON/Excel）
4. 运行命令：`pytest test_xxx.py -v -s`

### 自定义断言
在 `base_request.py` 中封装通用断言函数，如：
```python
def assert_response(self, response, expected_code=200):
    """通用响应断言"""
    assert response.status_code == expected_code, f"状态码错误，预期{expected_code}，实际{response.status_code}"
    assert "error" not in response.json(), "响应包含错误信息"
```

## ❗ 常见问题
1. **Allure 报告启动失败**：确保已安装 Allure 客户端，且配置环境变量
2. **Excel 数据读取失败**：确保文件格式为 `.xlsx`，且表头与代码中字段一致
<<<<<<< HEAD
3. **Token 携带失败**：检查 `auth_headers` Fixture 中 Token 拼接格式是否符合接口要求
4. **多环境配置不生效**：检查 `conftest.py` 中 `env_file_map` 映射关系是否正确

## 📄 许可证
本项目仅供学习和面试使用，禁止商用。
```

您可以直接将以上内容粘贴到您的 `README.md` 文件中。如需进一步调整，请随时告知。
=======
3. **多环境配置不生效**：检查 `conftest.py` 中 `env_file_map` 映射关系是否正确

## 📄 许可证
本项目仅供学习和面试使用，禁止商用。

>>>>>>> 2058c1dd6a36ba27a0d3c9a7584ac20b6821dfe6

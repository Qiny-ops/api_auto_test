# 📝 接口自动化框架 README.md（移除 Token 管理版）
这份 README 已移除 Token 自动管理相关内容，完全适配仅包含「数据驱动+多环境+失败重跑+Allure 报告」的基础版接口自动化框架，可直接复制使用。

```markdown
# 接口自动化测试框架（Login API Auto Test）
基于 Python + Pytest 实现的企业级接口自动化测试框架，支持多环境切换、数据驱动、失败重跑、Allure 精美报告，可直接用于登录类接口的自动化测试与回归验证。

## 📋 框架特点
- 🚀 **数据驱动**：支持 Excel/JSON 外部数据文件，用例与数据完全分离
- 🌍 **多环境切换**：一键切换测试/预发/生产环境，无需修改代码
- 🔄 **失败重跑**：用例失败自动重试，提升框架稳定性
- 📊 **可视化报告**：集成 Allure 生成精美测试报告，支持步骤/附件/环境展示
- 📜 **完整日志**：请求/响应/错误日志自动记录，便于问题定位
- 🎯 **高扩展性**：新增接口/用例只需补充数据文件，核心代码无需改动

## 📂 框架目录结构
```
login_api_auto/
├── base_request.py        # HTTP请求封装（含日志/Allure集成）
├── conftest.py            # 全局Fixture（多环境/数据读取）
├── test_login.py          # 登录接口测试用例（数据驱动）
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
| 包名           | 作用                     |
|----------------|--------------------------|
| pytest         | 测试用例执行框架         |
| openpyxl       | 读取Excel测试数据        |
| pyyaml         | 读取YAML格式配置文件     |
| allure-pytest  | 生成Allure测试报告       |
| requests       | 发送HTTP请求             |

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
2. 参考 `test_login.py` 编写用例，复用 `api_config` Fixture
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
3. **多环境配置不生效**：检查 `conftest.py` 中 `env_file_map` 映射关系是否正确

## 📄 许可证
本项目仅供学习和面试使用，禁止商用。
```

## ✨ 调整说明
1. 移除了「Token 自动管理」相关的所有描述（框架特点、目录结构、扩展指南、常见问题等）；
2. 同步调整了「新增业务接口用例」的指引，仅保留 `api_config` Fixture 引用；
3. 保持文档整体结构和实用性不变，适配基础版框架的功能范围。

## 📌 使用步骤
1. 复制上述内容替换原有 `README.md`；
2. 确认本地框架代码已移除 Token 相关逻辑（如 `conftest.py` 中的 `token`/`auth_headers` Fixture）；
3. 提交到 GitHub：
   ```bash
   git add README.md
   git commit -m "更新README：移除Token自动管理相关内容"
   git push origin main
   ```

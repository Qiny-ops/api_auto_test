import os
import sys
import argparse
import subprocess

# 添加src目录到环境变量（解决导入问题）
sys.path.append(os.path.join(os.path.dirname(__file__), "src"))

def main():
    # 解析命令行参数
    parser = argparse.ArgumentParser(description="接口自动化测试执行入口")
    parser.add_argument("--env", default="test", help="执行环境：test/pre/prod")
    args = parser.parse_args()

    # 定义执行命令（核心修改：添加--rootdir指定项目根目录）
    test_command = [
        "pytest",
        "src/testcases/",
        "--rootdir", os.path.dirname(__file__),  # 新增：确保pytest找到conftest
        "-v",
        "-s",
        f"--env={args.env}",
        f"--alluredir=reports/allure-results",
        "--reruns=2",
        "--reruns-delay=1"
    ]

    # 创建报告目录
    if not os.path.exists("reports"):
        os.makedirs("reports")

    # 执行测试
    print(f"🚀 开始执行【{args.env}】环境接口自动化测试...")
    result = subprocess.run(test_command)

    # 执行结果判断
    if result.returncode == 0:
        print("✅ 测试执行完成，全部用例通过！")
    else:
        print("❌ 测试执行完成，部分用例失败！")
        sys.exit(1)

if __name__ == "__main__":
    main()
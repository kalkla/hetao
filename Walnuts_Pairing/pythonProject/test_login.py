# -*- coding: utf-8 -*-
"""
登录接口测试工具：用于测试登录功能并验证isFirstLogin字段的正确性
"""

import json
import requests
import sys
import time

def test_login(mock_code=None):
    """
    测试登录接口
    """
    # 服务器URL
    login_url = "http://localhost:5000/api/login"
    
    # 准备请求数据
    # 如果没有提供mock_code，使用一个固定的mock_code进行测试
    if not mock_code:
        mock_code = f"test_code_{int(time.time()) % 1000000}"
    
    # 请求体数据
    data = {
        "code": mock_code,
        "nickName": "测试用户",
        "avatarUrl": "http://example.com/avatar.jpg"
    }
    
    print(f"测试登录接口...")
    print(f"请求URL: {login_url}")
    print(f"请求数据: {json.dumps(data, ensure_ascii=False)}")
    
    try:
        # 发送登录请求
        response = requests.post(login_url, json=data)
        
        # 获取响应状态码
        status_code = response.status_code
        print(f"\n响应状态码: {status_code}")
        
        # 尝试解析JSON响应
        try:
            response_data = response.json()
            print(f"响应内容: {json.dumps(response_data, ensure_ascii=False, indent=2)}")
            
            # 检查是否包含isFirstLogin字段
            if "isFirstLogin" in response_data:
                print(f"\n✓ isFirstLogin字段存在，值为: {response_data['isFirstLogin']}")
            else:
                print("\n✗ 响应中没有isFirstLogin字段!")
            
            # 检查是否登录成功
            if response_data.get("success", False):
                print("✓ 登录成功")
                print(f"  - Token: {response_data.get('token', '')[:50]}..." if response_data.get('token') else "  - 无Token返回")
                print(f"  - 用户信息: {json.dumps(response_data.get('userInfo', {}), ensure_ascii=False)}")
            else:
                print(f"✗ 登录失败: {response_data.get('message', '未知错误')}")
                
        except json.JSONDecodeError:
            print(f"无法解析JSON响应，原始响应内容: {response.text}")
    
    except requests.exceptions.ConnectionError:
        print("错误: 无法连接到服务器，请确保服务器正在运行")
    except Exception as e:
        print(f"发生错误: {str(e)}")

def add_is_first_login_to_db_viewer():
    """
    增强数据库查看器，添加首次登录状态分析
    """
    print("\n数据库用户首次登录状态分析:")
    print("(注: 实际首次登录状态应在登录时由服务器动态判断)")
    print("  - 首次登录: 数据库中不存在该用户记录时")
    print("  - 非首次登录: 数据库中已存在该用户记录时")
    print("\n您可以多次使用相同的mock_code进行测试，观察isFirstLogin值的变化")
    print("示例：")
    print("  1. 使用mock_code='test123'第一次登录 -> isFirstLogin应该为true")
    print("  2. 使用相同mock_code再次登录 -> isFirstLogin应该为false")

def print_usage():
    """
    打印使用说明
    """
    print("核桃检测小程序登录测试工具")
    print("用法:")
    print("  python test_login.py               # 使用随机生成的mock_code测试")
    print("  python test_login.py <mock_code>   # 使用指定的mock_code测试")
    print("\n示例:")
    print("  python test_login.py test123       # 使用test123作为mock_code")
    print("\n说明:")
    print("  - 请确保服务器正在运行在 http://localhost:5000")
    print("  - 可以多次使用相同的mock_code测试首次/非首次登录行为")
    print("  - 脚本会显示完整的请求和响应信息，包括isFirstLogin字段")

def main():
    """
    主函数
    """
    # 检查命令行参数
    mock_code = None
    if len(sys.argv) > 1:
        mock_code = sys.argv[1]
    else:
        # 打印使用说明
        print_usage()
        print()
    
    # 测试登录
    test_login(mock_code)
    
    # 添加说明
    add_is_first_login_to_db_viewer()

if __name__ == "__main__":
    main()
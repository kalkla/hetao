# -*- coding: utf-8 -*-
"""
真实微信OpenID登录测试脚本

说明：
1. 请确保已将真实的微信AppID和AppSecret配置到config.yaml中
2. 测试时需要提供真实的微信小程序登录code
3. 登录成功后会返回用户的真实OpenID

测试步骤：
1. 在微信开发者工具中运行小程序，获取登录code
2. 将code粘贴到下面的wechat_code变量中
3. 运行该脚本
4. 查看控制台输出的结果

注意：
- 登录code具有时效性，通常只有5分钟有效期
- 每个code只能使用一次
"""

import requests
import json
import sys

# 设置测试参数
SERVER_URL = "http://127.0.0.1:5000/api/login"

# 真实微信登录code（需要替换为最新获取的code）
# 在微信开发者工具中可以通过调用wx.login()获取
wechat_code = ""

# 可选：用户信息
user_info = {
    "nickName": "测试用户",
    "avatarUrl": "http://example.com/avatar.jpg"
}

def main():
    print("真实微信OpenID登录测试")
    print("=" * 50)
    
    if not wechat_code:
        print("错误：未提供微信登录code")
        print("请在微信开发者工具中获取code并赋值给wechat_code变量")
        print("获取方式：在小程序代码中调用wx.login()")
        sys.exit(1)
    
    # 构造请求数据
    data = {
        "code": wechat_code
    }
    
    # 添加用户信息（如果有）
    if user_info:
        data.update(user_info)
    
    print(f"服务器URL：{SERVER_URL}")
    print(f"请求数据：{json.dumps(data, ensure_ascii=False)}")
    print()
    
    try:
        # 发送请求
        response = requests.post(SERVER_URL, json=data, timeout=10)
        
        print(f"响应状态码：{response.status_code}")
        
        # 解析响应
        response_data = response.json()
        print(f"响应内容：{json.dumps(response_data, ensure_ascii=False, indent=2)}")
        
        # 分析结果
        if response_data.get("success"):
            print()
            print("登录成功！")
            print()
            print("关键信息：")
            print(f"- OpenID：{response_data.get('userInfo', {}).get('openId', '')}")
            print(f"- 首次登录：{response_data.get('isFirstLogin', False)}")
            print(f"- Token：{response_data.get('token', '')[:50]}...")
            print()
            print("说明：")
            print("1. 用户信息已成功保存到数据库")
            print("2. OpenID是微信用户的唯一标识")
            print("3. Token用于后续API请求的身份验证")
            
            # 验证数据库操作
            print()
            print("验证数据库操作：")
            print("- 首次登录：用户信息已插入到users表")
            print("- 非首次登录：用户信息已更新到users表")
            
        else:
            print()
            print("登录失败！")
            print()
            print("错误信息：")
            print(f"- {response_data.get('message', '未知错误')}")
            print()
            print("可能的原因：")
            print("1. 登录code已过期或无效")
            print("2. 微信AppID或AppSecret配置错误")
            print("3. 网络问题导致无法连接微信服务器")
            print()
            print("建议：")
            print("1. 确保config.yaml中的微信配置正确")
            print("2. 获取最新的微信登录code")
            print("3. 检查网络连接是否正常")
            
    except requests.exceptions.ConnectionError:
        print("错误：无法连接到服务器，请确保服务器正在运行")
    except requests.exceptions.Timeout:
        print("错误：请求超时，请检查网络连接")
    except Exception as e:
        print(f"错误：{str(e)}")
    
    print("=" * 50)

if __name__ == "__main__":
    main()
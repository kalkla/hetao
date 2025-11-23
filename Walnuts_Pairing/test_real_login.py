import requests
import json

# 测试真实登录流程
# 使用一个有效的微信code（从微信开发者工具或真实小程序中获取）
# 这里需要替换为真实的code
wechat_code = ""  # 替换为真实的微信登录code

if not wechat_code:
    print("请在test_real_login.py文件中替换wechat_code为真实的微信登录code")
    print("你可以从微信开发者工具的Console中找到login方法返回的code")
    exit(1)

# 测试服务器URL
server_url = "http://127.0.0.1:5000/api/login"

# 发送登录请求
payload = {"code": wechat_code}

print("正在发送登录请求...")
print(f"URL: {server_url}")
print(f"Code: {wechat_code}")

try:
    response = requests.post(server_url, json=payload, timeout=10)
    print(f"\n响应状态码: {response.status_code}")
    print(f"响应内容: {response.text}")
    
    response_data = response.json()
    if response_data.get("success"):
        print("\n登录成功！")
        print(f"Token: {response_data.get("token")}")
        print(f"Is First Login: {response_data.get("isFirstLogin")}")
        print(f"User Info: {response_data.get("userInfo")}")
    else:
        print(f"\n登录失败: {response_data.get("message")}")

except Exception as e:
    print(f"\n请求失败: {str(e)}")
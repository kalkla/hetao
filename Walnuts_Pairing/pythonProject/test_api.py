import requests
import json

# 配置基本信息
BASE_URL = 'http://localhost:5000'
USERNAME = 'testuser'
PASSWORD = 'testpassword'

# 步骤1: 用户注册
print("1. 用户注册...")
register_url = f"{BASE_URL}/api/user/register"
register_data = {
    "username": USERNAME,
    "password": PASSWORD
}
register_response = requests.post(register_url, json=register_data)
print(f"   注册状态: {register_response.status_code}")
print(f"   注册响应: {register_response.text}")
print()

# 步骤2: 用户登录并获取令牌
print("2. 用户登录...")
login_url = f"{BASE_URL}/api/login"
login_auth = requests.auth.HTTPBasicAuth(USERNAME, PASSWORD)
login_response = requests.post(login_url, auth=login_auth)
print(f"   登录状态: {login_response.status_code}")
print(f"   登录响应: {login_response.text}")

# 获取令牌
if login_response.status_code == 200:
    token = login_response.json().get('token')
    print(f"   获取到令牌: {token[:20]}...")  # 只显示部分令牌
    print()

    # 步骤3: 测试 /compare 接口
    print("3. 测试 /compare 接口...")
    compare_url = f"{BASE_URL}/compare"
    compare_headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    # 使用简化的测试数据
    compare_data = {
        "images": ["dummy_base64_data"] * 6,
        "size": 35,
        "angles": ["angle1", "angle2", "angle3", "angle4", "angle5", "angle6"]
    }
    compare_response = requests.post(compare_url, headers=compare_headers, json=compare_data)
    print(f"   Compare接口状态: {compare_response.status_code}")
    print(f"   Compare接口响应: {compare_response.text}")
    print()

# 步骤4: 测试 /api/compare 接口
print("4. 测试 /api/compare 接口...")
api_compare_url = f"{BASE_URL}/api/compare"
api_compare_response = requests.post(api_compare_url, headers=compare_headers, json=compare_data)
print(f"   API Compare接口状态: {api_compare_response.status_code}")
print(f"   API Compare接口响应: {api_compare_response.text}")
print()

print("测试完成!")
import requests
import json

def test_login_flow():
    # 测试登录接口
    login_url = "http://127.0.0.1:5000/api/login"
    login_data = {
        "code": "test_code_123",
        "nickName": "Test User",
        "avatarUrl": "http://example.com/avatar.png"
    }
    
    response = requests.post(login_url, json=login_data)
    print("Login response status code:", response.status_code)
    
    if response.status_code != 200:
        print("Login failed!")
        return False
    
    login_result = response.json()
    print("Login result:", json.dumps(login_result, indent=2))
    
    if not login_result.get("success"):
        print("Login failed!")
        return False
    
    # 获取登录后返回的token
    token = login_result.get("token")
    if not token:
        print("Token not found in login response!")
        return False
    
    print("Login successful, token acquired.")
    
    # 测试获取用户信息接口
    user_info_url = "http://localhost:5000/api/user/info"
    headers = {
        "Authorization": f"Bearer {token}"
    }
    
    response = requests.get(user_info_url, headers=headers)
    print("User info response status code:", response.status_code)
    
    if response.status_code != 200:
        print("Get user info failed!")
        return False
    
    user_info_result = response.json()
    print("User info result:", json.dumps(user_info_result, indent=2))
    
    if not user_info_result.get("success"):
        print("Get user info failed!")
        return False
    
    # 验证用户信息是否完整
    user_info = user_info_result.get("userInfo", {})
    open_id = user_info.get("openId")  # 注意是大写的Id
    nick_name = user_info.get("nickName")
    avatar_url = user_info.get("avatarUrl")
    print(f"User info details: openId={open_id}, nickName={nick_name}, avatarUrl={avatar_url}")
    
    # 检查用户信息是否完整
    if not all([open_id, nick_name, avatar_url]):
        print("User info is incomplete!")
        return False
    
    print("All tests passed successfully!")
    return True

if __name__ == "__main__":
    test_login_flow()
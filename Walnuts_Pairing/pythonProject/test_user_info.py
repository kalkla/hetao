import requests
import jwt
import datetime

# 测试参数
SECRET_KEY = 'your-secret-key-here'
test_openid = 'test_openid_123'

# 生成JWT令牌
token = jwt.encode(
    {
        'sub': test_openid,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=7)
    },
    SECRET_KEY,
    algorithm='HS256'
)

# 调用获取用户信息接口
url = 'http://localhost:5000/api/user/info'
headers = {
    'Authorization': f'Bearer {token}'
}

response = requests.get(url, headers=headers)

print('Response status code:', response.status_code)
print('Response data:', response.json())
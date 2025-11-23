import requests
import base64
import os

# 读取测试图片
img_path = r'f:\xcx\hthd\Walnuts_Pairing\pythonProject\1-s-1.png'
with open(img_path, 'rb') as f:
    img_data = f.read()
    
# 编码为Base64
base64_data = base64.b64encode(img_data).decode('utf-8')

# 构造测试请求
url = 'http://localhost:5000/upload'
headers = {
    'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJtb2NrX2UxNDJhYjE3MjQwYjYwZDM3NDA5NGMwNTQyZGUxY2IwIiwiZXhwIjoxNzYzNzE0MjM5fQ.14554lGqNc4u-pPbOqtXbqxcTqBcIuXIUjticv_1cw8'
}

# 测试JSON上传
print('测试JSON上传...')
json_payload = {
    'image': f'data:image/png;base64,{base64_data}'
}
response = requests.post(url, json=json_payload, headers=headers)
print(f'JSON上传响应: {response.status_code}, {response.json()}')

# 测试表单上传
print('\n测试表单上传...')
files = {
    'file': open(img_path, 'rb')
}
response = requests.post(url, files=files, headers=headers)
print(f'表单上传响应: {response.status_code}, {response.json()}')
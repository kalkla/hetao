import requests
import json
import base64
import os

# 读取本地图片并转换为base64编码
def get_base64_image(image_path):
    if not os.path.exists(image_path):
        print(f"图片文件不存在: {image_path}")
        return None
    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")

# 登录获取令牌
def get_token():
    url = "http://localhost:5000/api/login"
    data = {"code": "test_code_123"}
    headers = {"Content-Type": "application/json"}
    response = requests.post(url, data=json.dumps(data), headers=headers)
    response_data = response.json()
    print(f"登录响应: {response_data}")
    return response_data.get('token')

# 使用令牌访问/compare接口
def test_compare(token):
    # 获取测试图片的base64编码
    image_path = "pic.png"  # 确保图片文件在项目根目录
    base64_image = get_base64_image(image_path)
    if not base64_image:
        print("获取图片base64编码失败")
        return
    # 构造包含真实base64编码的测试数据
    url = "http://localhost:5000/compare"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    data = {
        "images": [base64_image for _ in range(6)],
        "size": 35,
        "angles": ["angle1", "angle2", "angle3", "angle4", "angle5", "angle6"]
    }
    response = requests.post(url, data=json.dumps(data), headers=headers)
    print(f"/compare接口响应: {response.status_code}")
    print(f"响应内容: {response.json()}")

if __name__ == "__main__":
    token = get_token()
    if token:
        test_compare(token)
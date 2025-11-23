import requests
import json

# 测试服务器地址
BASE_URL = "http://localhost:5000"

def test_login():
    """测试登录接口"""
    url = f"{BASE_URL}/api/login"
    data = {"code": "testcode"}
    headers = {"Content-Type": "application/json"}
    response = requests.post(url, data=json.dumps(data), headers=headers)
    
    print("=== 登录接口测试结果 ===")
    print(f"状态码: {response.status_code}")
    print(f"响应内容: {response.text}")
    
    if response.status_code == 200:
        result = response.json()
        if result.get("success"):
            print("登录成功")
            return result.get("token")
    
    print("登录失败")
    return None

def test_upload(token):
    """测试图片上传接口"""
    if not token:
        return None
    
    url = f"{BASE_URL}/upload"
    headers = {
        "Authorization": f"Bearer {token}"
    }
    
    # 读取测试图片
    with open("pic.jpg", "rb") as f:
        files = [
            ("file", ("pic.jpg", f, "image/jpeg"))
        ]
        data = {
            "angle": "top",
            "purpose": "collection"
        }
        
        response = requests.post(url, headers=headers, files=files, data=data)
        
        print("\n=== 上传接口测试结果 ===")
        print(f"状态码: {response.status_code}")
        print(f"响应内容: {response.text}")
        
        if response.status_code == 200:
            result = response.json()
            if result.get("success"):
                print("上传成功")
                return result.get("file_id")
    
    print("上传失败")
    return None

def test_collection(token, file_ids):
    """测试核桃采集接口"""
    if not token or not file_ids or len(file_ids) < 6:
        return None
    
    url = f"{BASE_URL}/collection"
    data = {
        "images": file_ids[:6],  # 取前6个file_ids
        "size": 35,
        "angles": ["top", "bottom", "left", "right", "front", "back"]
    }
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    response = requests.post(url, data=json.dumps(data), headers=headers)
    
    print("\n=== 采集接口测试结果 ===")
    print(f"状态码: {response.status_code}")
    print(f"响应内容: {response.text}")
    
    if response.status_code == 200:
        result = response.json()
        if result.get("success"):
            print("采集成功")
            return result.get("collection_id")
    
    print("采集失败")
    return None

if __name__ == "__main__":
    # 步骤1: 登录获取token
    token = test_login()
    
    if not token:
        print("登录失败，无法继续测试")
        exit(1)
    
    # 步骤2: 上传6张图片（实际测试中可以重复使用同一张图片）
    file_ids = []
    for i in range(6):
        file_id = test_upload(token)
        if file_id:
            file_ids.append(file_id)
    
    if len(file_ids) < 6:
        print("上传图片不足6张，无法继续测试")
        exit(1)
    
    # 步骤3: 调用采集接口
    collection_id = test_collection(token, file_ids)
    
    if collection_id:
        print(f"\n=== 测试完成 ===")
        print(f"采集成功！Collection ID: {collection_id}")
    else:
        print(f"\n=== 测试完成 ===")
        print(f"采集失败！")
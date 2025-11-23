import requests
import json

# 虚拟的Base64图片数据（简化版，实际测试可用完整Base64字符串）
dummy_base64 = 'iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8/5+hHgAHggJ/PchI7wAAAABJRU5ErkJggg=='

# 首先获取测试用的token
login_url = 'http://127.0.0.1:5001/api/login'
login_payload = {
    'code': 'test_code_123'
}
login_headers = {
    'Content-Type': 'application/json'
}

print("正在获取测试用token...")
try:
    login_response = requests.post(login_url, data=json.dumps(login_payload), headers=login_headers)
    login_data = login_response.json()
    if login_data['success']:
        token = login_data['token']
        print(f"获取token成功: {token[:20]}...")
    else:
        print(f"获取token失败: {login_data['message']}")
        exit(1)
except Exception as e:
    print(f"获取token失败: {str(e)}")
    exit(1)

# 然后测试compare接口是否返回前三个相似结果
compare_url = 'http://127.0.0.1:5001/compare'

# 构造测试数据（使用Base64图片代替fileId）
compare_payload = {
    'images': [
        {'base64_data': dummy_base64, 'fileId': 'test1.png', 'name': 'test1.png'},  # 顶部
        {'base64_data': dummy_base64, 'fileId': 'test2.png', 'name': 'test2.png'},  # 底部
        {'base64_data': dummy_base64, 'fileId': 'test3.png', 'name': 'test3.png'},  # 左侧
        {'base64_data': dummy_base64, 'fileId': 'test4.png', 'name': 'test4.png'},  # 右侧
        {'base64_data': dummy_base64, 'fileId': 'test5.png', 'name': 'test5.png'},  # 前面
        {'base64_data': dummy_base64, 'fileId': 'test6.png', 'name': 'test6.png'}   # 后面
    ],
    'size': 40,
    'angles': ['top', 'bottom', 'left', 'right', 'front', 'back'],
    'walnut_id': 'test'
}

compare_headers = {
    'Content-Type': 'application/json',
    'Authorization': f'Bearer {token}'
}

print("\n正在测试compare接口...")
try:
    compare_response = requests.post(compare_url, data=json.dumps(compare_payload), headers=compare_headers)
    print(f"状态码: {compare_response.status_code}")
    print(f"响应内容: {json.dumps(compare_response.json(), ensure_ascii=False, indent=2)}")
    print("\n接口返回前三个相似结果测试完成")
except Exception as e:
    print(f"测试失败: {str(e)}")
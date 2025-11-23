import requests
import base64
import os
import shutil
import glob

# 清理临时文件夹
if os.path.exists('temp_images'):
    shutil.rmtree('temp_images')
os.makedirs('temp_images', exist_ok=True)

# 登录获取令牌
def get_token():
    url = 'http://localhost:5000/api/login'
    data = {
        'code': 'test_code_123'
    }
    response = requests.post(url, json=data)
    print('登录响应:', response.json())
    return response.json()['token']

try:
    token = get_token()
    headers = {
        'Authorization': f'Bearer {token}'
    }
except Exception as e:
    print('登录失败:', str(e))
    exit(1)

# 测试不同格式的图片上传
def test_image_format(format_name, file_ext, mime_type):
    print(f'\\n=== 测试{format_name}格式 ===')
    
    # 创建一个临时测试图片
    img_path = f'test_image.{file_ext}'
    
    # 对于PNG格式，我们使用现有的图片
    if file_ext == 'png':
        if os.path.exists('1-s-1.png'):
            shutil.copy('1-s-1.png', img_path)
        else:
            # 创建一个简单的PNG图片
            import cv2
            import numpy as np
            img = np.zeros((100, 100, 3), dtype=np.uint8)
            img[:, :] = (255, 255, 255)  # 白色图片
            cv2.imwrite(img_path, img)
    else:
        # 创建一个简单的图片
        import cv2
        import numpy as np
        img = np.zeros((100, 100, 3), dtype=np.uint8)
        img[:, :] = (0, 255, 0)  # 绿色图片
        cv2.imwrite(img_path, img)
    
    # 测试Base64上传
    print('1. Base64上传:')
    with open(img_path, 'rb') as f:
        img_data = f.read()
        base64_data = base64.b64encode(img_data).decode('utf-8')
        
    json_payload = {
        'image': f'data:{mime_type};base64,{base64_data}'
    }
    
    response = requests.post('http://localhost:5000/upload', json=json_payload, headers=headers)
    if response.status_code == 200:
        json_response = response.json()
        print(f'   状态: 成功')
        print(f'   URL: {json_response["url"]}')
        # 检查保存的文件是否为预期格式
        if file_ext in json_response["url"].lower():
            print(f'   ✓ 正确保存为{file_ext}格式')
        else:
            print(f'   ✗ 未保存为预期格式，实际URL包含: {json_response["url"]}')
    else:
        print(f'   状态: 失败 ({response.status_code})')
        print(f'   响应: {response.json()}')
    
    # 测试表单上传
    print('2. 表单上传:')
    with open(img_path, 'rb') as f:
        files = {
            'file': f
        }
        response = requests.post('http://localhost:5000/upload', files=files, headers=headers)
        if response.status_code == 200:
            form_response = response.json()
            print(f'   状态: 成功')
            print(f'   URL: {form_response["url"]}')
            # 检查保存的文件是否为预期格式
            if file_ext in form_response["url"].lower():
                print(f'   ✓ 正确保存为{file_ext}格式')
            else:
                print(f'   ✗ 未保存为预期格式，实际URL包含: {form_response["url"]}')
        else:
            print(f'   状态: 失败 ({response.status_code})')
            print(f'   响应: {response.json()}')
    
    # 清理临时图片
    os.remove(img_path)

# 测试PNG格式
test_image_format('PNG', 'png', 'image/png')

# 测试JPEG格式
test_image_format('JPEG', 'jpg', 'image/jpeg')

# 测试JPG格式
test_image_format('JPG', 'jpg', 'image/jpeg')

# 检查临时文件夹中的文件
print(f'\\n=== 临时文件夹内容 ===')
uploaded_files = glob.glob('temp_images/**/*.*', recursive=True)
for file in uploaded_files:
    ext = os.path.splitext(file)[1]
    print(f'{file} - 格式: {ext}')
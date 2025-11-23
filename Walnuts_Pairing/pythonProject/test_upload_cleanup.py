import os
import shutil
import requests
import time

# 测试上传文件清理功能
def test_upload_cleanup():
    # 启动服务器（假设已经在运行）
    base_url = "http://127.0.0.1:5000"
    
    # 首先获取令牌
    token = get_auth_token(base_url)
    if not token:
        print("无法获取令牌")
        return False
    print("令牌获取成功:", token)
    
    # 准备测试图片数据（使用简单的base64编码图片）
    # 这是一个1x1像素的红色PNG图片
    simple_image = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII="
    
    # 上传图片
    upload_url = base_url + "/upload"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }
    upload_data = {"image": f"data:image/png;base64,{simple_image}", "purpose": "comparison"}
    
    response = requests.post(upload_url, json=upload_data, headers=headers)
    print("Upload response:", response.json())
    
    if response.status_code != 200 or not response.json().get("success"):
        print("Upload failed")
        return False
    
    file_id = response.json().get("file_id")
    print("Uploaded file ID:", file_id)
    
    # 检查上传的文件是否存在
    uploaded_file_path = None
    search_pattern = os.path.join("temp_images", "**", f"{file_id}*")
    import glob
    image_files = glob.glob(search_pattern, recursive=True)
    if image_files:
        uploaded_file_path = image_files[0]
        print("Uploaded file found at:", uploaded_file_path)
    else:
        print("Uploaded file not found")
        return False
    
    # 使用上传的图片进行比较
    compare_url = base_url + "/compare"
    compare_data = {"images": [{"fileId": file_id}], "size": 35}
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }
    
    response = requests.post(compare_url, json=compare_data, headers=headers)
    print("Compare response status:", response.status_code)
    print("Compare response:", response.json())
    
    # 检查上传的文件是否已被清理
    time.sleep(1)  # 等待清理完成
    
    if os.path.exists(uploaded_file_path):
        print("ERROR: Uploaded file was not cleaned up")
        # 手动清理测试文件
        try:
            os.remove(uploaded_file_path)
        except:
            pass
        return False
    else:
        print("SUCCESS: Uploaded file was cleaned up")
    
    return True

def get_auth_token(base_url):
    """
    获取认证令牌
    """
    login_url = base_url + "/api/login"
    
    # 由于我们没有真实的微信code，我们可以尝试使用一个测试用的code
    # 在实际环境中，这个code应该来自微信小程序的wx.login() API
    test_code = "test_code_123"
    
    try:
        response = requests.post(login_url, json={"code": test_code})
        print("Login response:", response.json())
        
        if response.status_code == 200 and response.json().get("success"):
            return response.json().get("token")
        else:
            # 如果登录失败，我们可以尝试绕过认证
            print("登录失败，尝试绕过认证")
            return None
            
    except Exception as e:
        print("获取令牌失败:", e)
        return None

if __name__ == "__main__":
    test_upload_cleanup()
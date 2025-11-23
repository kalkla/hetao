import os
import shutil
import datetime
import sqlite3

# 模拟生成 walnut_id
current_time = datetime.datetime.now()
time_str = current_time.strftime("%Y%m%d%H%M%S")
size = 33
num = 1
walnut_id = f"{time_str}_{num}_{size}"

print(f"Generated walnut_id: {walnut_id}")

# 模拟创建临时文件夹和图片
TEMP_IMAGES_FOLDER = "temp_images"
temp_folder = os.path.join(TEMP_IMAGES_FOLDER, walnut_id)
os.makedirs(temp_folder, exist_ok=True)

# 创建6张测试图片
for i in range(6):
    filename = f"{time_str}_{i+1}.png"
    filepath = os.path.join(temp_folder, filename)
    with open(filepath, "wb") as f:
        f.write(b"test image data")

print(f"Created 6 test images in {temp_folder}")

# 模拟移动到新目录结构
ROOT_FOLDER = "data"
size_folder = os.path.join(ROOT_FOLDER, str(size))
os.makedirs(size_folder, exist_ok=True)
walnut_path = os.path.join(size_folder, walnut_id)

if os.path.exists(walnut_path):
    shutil.rmtree(walnut_path)
shutil.move(temp_folder, walnut_path)

print(f"Moved folder to {walnut_path}")

# 验证目录结构
if os.path.exists(walnut_path):
    print(f"✓ Collection folder exists: {walnut_path}")
    
    # 检查图片
    images = os.listdir(walnut_path)
    if len(images) == 6:
        print(f"✓ Found 6 PNG images in the collection folder")
        
        # 检查命名 convention
        for img_name in images:
            if img_name.endswith(".png") and img_name.startswith(time_str) and "_" in img_name:
                seq_num = img_name.split("_")[1].split(".")[0]
                if seq_num.isdigit() and 1 <= int(seq_num) <= 6:
                    print(f"  - Image name: {img_name} (valid)")
    else:
        print(f"✗ Only found {len(images)} images (expected 6)")
else:
    print(f"✗ Collection folder does not exist: {walnut_path}")

# 清理测试数据
if os.path.exists(walnut_path):
    shutil.rmtree(walnut_path)
if os.path.exists(size_folder) and not os.listdir(size_folder):
    os.rmdir(size_folder)

print("Test completed")
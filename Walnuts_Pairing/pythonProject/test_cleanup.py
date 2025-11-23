import datetime
import os
import sys
import time
import shutil

# 确保添加当前目录到Python路径
sys.path.append(os.path.abspath('.'))

# 创建临时目录（如果不存在）
TEMP_IMAGES_FOLDER = 'temp_images'
os.makedirs(TEMP_IMAGES_FOLDER, exist_ok=True)

# 定义清理函数（直接复制webserve中的实现）
def cleanup_temp_images():
    """清理超过30分钟的临时图片文件和目录"""
    now = datetime.datetime.now()
    cutoff = now - datetime.timedelta(minutes=30)
    
    if not os.path.exists(TEMP_IMAGES_FOLDER):
        return
    
    deleted_files = []
    errors = []
    
    for filename in os.listdir(TEMP_IMAGES_FOLDER):
        file_path = os.path.join(TEMP_IMAGES_FOLDER, filename)
        try:
            if os.path.isfile(file_path):
                mtime = datetime.datetime.fromtimestamp(os.path.getmtime(file_path))
                if mtime < cutoff:
                    os.remove(file_path)
                    deleted_files.append(file_path)
            elif os.path.isdir(file_path):
                mtime = datetime.datetime.fromtimestamp(os.path.getmtime(file_path))
                if mtime < cutoff:
                    shutil.rmtree(file_path)
                    deleted_files.append(file_path)
        except Exception as e:
            errors.append((file_path, str(e)))
    
    return deleted_files, errors

# 创建测试临时文件
print("创建测试临时文件...")

# 创建一个旧文件（31分钟前）
old_file_path = os.path.join(TEMP_IMAGES_FOLDER, "test_old_file.txt")
with open(old_file_path, 'w') as f:
    f.write("This is an old test file")
# 设置文件修改时间为31分钟前
old_mtime = time.time() - 31 * 60  # 31 minutes ago
os.utime(old_file_path, (old_mtime, old_mtime))

# 创建一个新文件（1分钟前）
new_file_path = os.path.join(TEMP_IMAGES_FOLDER, "test_new_file.txt")
with open(new_file_path, 'w') as f:
    f.write("This is a new test file")
new_mtime = time.time() - 60  # 1 minute ago
os.utime(new_file_path, (new_mtime, new_mtime))

# 创建一个旧目录和文件
old_dir_path = os.path.join(TEMP_IMAGES_FOLDER, "test_old_dir")
os.makedirs(old_dir_path, exist_ok=True)
old_dir_file_path = os.path.join(old_dir_path, "file.txt")
with open(old_dir_file_path, 'w') as f:
    f.write("This is a file in an old directory")
os.utime(old_dir_file_path, (old_mtime, old_mtime))
os.utime(old_dir_path, (old_mtime, old_mtime))

# 创建一个新目录和文件
new_dir_path = os.path.join(TEMP_IMAGES_FOLDER, "test_new_dir")
os.makedirs(new_dir_path, exist_ok=True)
new_dir_file_path = os.path.join(new_dir_path, "file.txt")
with open(new_dir_file_path, 'w') as f:
    f.write("This is a file in a new directory")
os.utime(new_dir_file_path, (new_mtime, new_mtime))
os.utime(new_dir_path, (new_mtime, new_mtime))

# 显示文件信息
print(f"旧文件: {old_file_path} (修改时间: {datetime.datetime.fromtimestamp(os.path.getmtime(old_file_path))})")
print(f"新文件: {new_file_path} (修改时间: {datetime.datetime.fromtimestamp(os.path.getmtime(new_file_path))})")
print(f"旧目录: {old_dir_path} (修改时间: {datetime.datetime.fromtimestamp(os.path.getmtime(old_dir_path))})")
print(f"新目录: {new_dir_path} (修改时间: {datetime.datetime.fromtimestamp(os.path.getmtime(new_dir_path))})")

# 执行清理函数
print("\n执行清理函数...")
deleted, errors = cleanup_temp_images()

# 打印清理结果
if deleted:
    print(f"✓ 删除了 {len(deleted)} 个旧文件/目录:")
    for file_path in deleted:
        print(f"   - {file_path}")
else:
    print("✗ 没有删除任何文件/目录")

if errors:
    print(f"✗ 清理过程中出现 {len(errors)} 个错误:")
    for file_path, error_msg in errors:
        print(f"   - {file_path}: {error_msg}")

# 验证结果
print("\n验证清理结果...")

# 验证旧文件是否被删除
if not os.path.exists(old_file_path):
    print(f"✓ 旧文件已被删除: {old_file_path}")
else:
    print(f"✗ 旧文件未被删除: {old_file_path}")

# 验证新文件是否保留
if os.path.exists(new_file_path):
    print(f"✓ 新文件保留: {new_file_path}")
else:
    print(f"✗ 新文件被错误删除: {new_file_path}")

# 验证旧目录是否被删除
if not os.path.exists(old_dir_path):
    print(f"✓ 旧目录已被删除: {old_dir_path}")
else:
    print(f"✗ 旧目录未被删除: {old_dir_path}")

# 验证新目录是否保留
if os.path.exists(new_dir_path):
    print(f"✓ 新目录保留: {new_dir_path}")
else:
    print(f"✗ 新目录被错误删除: {new_dir_path}")

# 清理测试文件
print("\n清理测试环境...")
if os.path.exists(new_file_path):
    os.remove(new_file_path)
    print(f"移除测试新文件: {new_file_path}")

if os.path.exists(new_dir_path):
    shutil.rmtree(new_dir_path)
    print(f"移除测试新目录: {new_dir_path}")

print("\n所有测试完成")
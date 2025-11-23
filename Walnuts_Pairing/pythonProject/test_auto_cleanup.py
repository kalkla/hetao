import os
import time
import datetime

# 创建临时目录
TEMP_IMAGES_FOLDER = 'temp_images'
os.makedirs(TEMP_IMAGES_FOLDER, exist_ok=True)

# 创建一个旧文件（59分钟前，会被清理）
old_file_path = os.path.join(TEMP_IMAGES_FOLDER, "test_old_file.txt")
with open(old_file_path, 'w') as f:
    f.write("This is an old test file that should be deleted")
old_mtime = time.time() - 59 * 60  # 59 minutes ago
os.utime(old_file_path, (old_mtime, old_mtime))

# 创建一个新文件（30秒前，不会被清理）
new_file_path = os.path.join(TEMP_IMAGES_FOLDER, "test_new_file.txt")
with open(new_file_path, 'w') as f:
    f.write("This is a new test file that should be kept")
new_mtime = time.time() - 30  # 30 seconds ago
os.utime(new_file_path, (new_mtime, new_mtime))

print("Created test files:")
print(f"- Old file: {old_file_path} (modified: {datetime.datetime.fromtimestamp(old_mtime)})")
print(f"- New file: {new_file_path} (modified: {datetime.datetime.fromtimestamp(new_mtime)})")

print("\nWaiting for 61 seconds for the cleanup job to run...")

# 等待61秒让定时任务执行
for i in range(61):
    time.sleep(1)
    print(f"\rWaiting {60 - i} seconds...", end="", flush=True)

print("\n" + "="*50)

# 检查文件是否被清理
print("Checking cleanup results:")

if not os.path.exists(old_file_path):
    print(f"✓ PASS: Old file has been deleted - {old_file_path}")
else:
    print(f"✗ FAIL: Old file still exists - {old_file_path}")
    mtime = datetime.datetime.fromtimestamp(os.path.getmtime(old_file_path))
    print(f"   Last modified: {mtime}")

if os.path.exists(new_file_path):
    print(f"✓ PASS: New file is still present - {new_file_path}")
else:
    print(f"✗ FAIL: New file has been deleted - {new_file_path}")

print("="*50)

# 清理测试环境
if os.path.exists(new_file_path):
    os.remove(new_file_path)
    print(f"Cleaned up test file: {new_file_path}")

print("Test completed")
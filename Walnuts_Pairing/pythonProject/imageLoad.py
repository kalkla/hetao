import cv2
import os
from glob import glob

# 本函数实现从folder_path根目录下读取全部的图片（6张）
# author：张
# qq：750123348
#变量：folder_path，文件路径
#返回值：列表  images，包含所有的6个图片

def load_images_from_folder(folder_path):
    # 使用glob获取指定文件夹下所有jpg和png格式的图片
    image_paths = glob(os.path.join(folder_path, "*.jpg")) + glob(os.path.join(folder_path, "*.png"))
    
    # 按角度编号排序图片路径（确保与上传顺序一致）
    def get_angle_number(filename):
        basename = os.path.basename(filename).split('.')[0]  # 去掉文件扩展名
        parts = basename.split('_')
        for part in parts:
            if part.isdigit():
                return int(part)
        return 0  # 默认值
    image_paths.sort(key=lambda x: get_angle_number(x))
    
    # 创建一个空列表来存储图片
    images = []
    # 遍历所有图片路径
    for img_path in image_paths:
        # 读取图片
        img = cv2.imread(img_path)
        # 检查图片是否正确读取
        if img is not None:
            # 将图片添加到列表中
            images.append(img)
        else:
            print(f"Failed to read: {img_path}")  # 添加打印语句
    return images

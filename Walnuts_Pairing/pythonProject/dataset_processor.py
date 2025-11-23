# dataset_processor.py
import os
import cv2
from vector_db import VectorDB
from similar import extract_texture_features, extract_edge_features, extract_color_features
from imageLoad import load_images_from_folder


def process_dataset_to_vector_db(dataset_root_path: str, vector_db_path: str = 'vector_features.db'):
    """
    遍历数据集目录，提取特征并存储到向量数据库

    Args:
        dataset_root_path: 数据集根目录路径，格式应为: root/尺寸/核桃ID_尺寸/
        vector_db_path: 向量数据库文件路径
    """
    # 初始化向量数据库
    vector_db = VectorDB(vector_db_path)

    # 遍历数据集根目录下的所有尺寸文件夹
    if not os.path.exists(dataset_root_path):
        raise FileNotFoundError(f"数据集路径不存在: {dataset_root_path}")

    # 获取所有尺寸文件夹
    size_dirs = [d for d in os.listdir(dataset_root_path)
                 if os.path.isdir(os.path.join(dataset_root_path, d))]

    print(f"发现 {len(size_dirs)} 个尺寸目录: {size_dirs}")

    total_processed = 0

    # 遍历每个尺寸目录
    for size_dir in size_dirs:
        size_path = os.path.join(dataset_root_path, size_dir)

        # 验证尺寸目录名是否为数字
        try:
            size = int(size_dir)
            if not (33 <= size <= 42):
                print(f"警告: 尺寸 {size} 不在有效范围内(33-42)，跳过")
                continue
        except ValueError:
            print(f"警告: 尺寸目录名 {size_dir} 不是有效数字，跳过")
            continue

        # 获取该尺寸下的所有核桃文件夹
        walnut_dirs = [d for d in os.listdir(size_path)
                       if os.path.isdir(os.path.join(size_path, d))]

        print(f"尺寸 {size} 下有 {len(walnut_dirs)} 个核桃目录")

        # 遍历每个核桃目录
        for walnut_dir in walnut_dirs:
            walnut_path = os.path.join(size_path, walnut_dir)

            # 解析核桃ID（假设格式为"核桃ID_尺寸"）
            if '_' in walnut_dir:
                walnut_id = walnut_dir.split('_')[0]
            else:
                walnut_id = walnut_dir

            print(f"处理核桃: {walnut_id}, 尺寸: {size}")

            try:
                # 加载核桃图片
                images = load_images_from_folder(walnut_path)

                if len(images) == 0:
                    print(f"  警告: {walnut_path} 中没有找到图片，跳过")
                    continue

                # 为每个角度提取并存储特征
                for i, image in enumerate(images):
                    # 提取三种特征
                    texture_features = extract_texture_features(image)
                    edge_features = extract_edge_features(image)
                    color_features = extract_color_features(image)

                    # 构造角度ID
                    angle_id = f"{walnut_id}_angle{i + 1}"

                    # 存储到向量数据库
                    vector_db.store_features(angle_id, str(size), 'texture', texture_features)
                    vector_db.store_features(angle_id, str(size), 'edge', edge_features)
                    vector_db.store_features(angle_id, str(size), 'color', color_features)

                    print(f"  已存储角度 {i + 1} 的特征")

                total_processed += 1
                print(f"  完成核桃 {walnut_id} 的特征提取和存储")

            except Exception as e:
                print(f"  处理核桃 {walnut_id} 时出错: {e}")
                continue

    print(f"处理完成！总共处理了 {total_processed} 个核桃的特征数据")
    return total_processed


def verify_vector_db_content(vector_db_path: str = 'vector_features.db'):
    """
    验证向量数据库中的内容

    Args:
        vector_db_path: 向量数据库文件路径
    """
    vector_db = VectorDB(vector_db_path)

    # 连接数据库查看内容
    import sqlite3
    conn = sqlite3.connect(vector_db_path)
    cursor = conn.cursor()

    # 查询统计信息
    cursor.execute("SELECT COUNT(*) FROM walnut_features")
    total_count = cursor.fetchone()[0]

    cursor.execute("SELECT DISTINCT size FROM walnut_features")
    sizes = [row[0] for row in cursor.fetchall()]

    print(f"向量数据库统计信息:")
    print(f"  总特征记录数: {total_count}")
    print(f"  尺寸种类: {sizes}")

    # 查询每个尺寸的记录数
    for size in sizes:
        cursor.execute("SELECT COUNT(*) FROM walnut_features WHERE size = ?", (size,))
        count = cursor.fetchone()[0]
        print(f"  尺寸 {size}: {count} 条记录")

    conn.close()


if __name__ == "__main__":
    # 使用示例
    dataset_path = "dataset"  # 假设数据集在data目录下
    process_dataset_to_vector_db(dataset_path)
    verify_vector_db_content()

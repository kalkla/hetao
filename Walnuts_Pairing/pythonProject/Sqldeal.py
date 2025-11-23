# Sqldeal.py
import math
import os
import sqlite3
from sqlite3 import Error
import numpy as np
import similar
from getData import filter_details_by_threshold
from imageLoad import load_images_from_folder
from Configdeal import get_config_value
from vector_db import VectorDB

# 初始化向量数据库
VECTOR_DB_PATH = 'vector_features.db'
vector_db = VectorDB(VECTOR_DB_PATH) if os.path.exists(VECTOR_DB_PATH) else None


def cosine_similarity(vec1: list, vec2: list) -> float:
    """计算两个向量的余弦相似度"""
    if len(vec1) == 0 or len(vec2) == 0:
        return 0.0

    vec1 = np.array(vec1)
    vec2 = np.array(vec2)

    dot_product = np.dot(vec1, vec2)
    norm_vec1 = np.linalg.norm(vec1)
    norm_vec2 = np.linalg.norm(vec2)

    if norm_vec1 == 0 or norm_vec2 == 0:
        return 0.0

    return float(dot_product / (norm_vec1 * norm_vec2))


def calculate_similarity_from_vectors(walnut_id1: str, size1: str, walnut_id2: str, size2: str) -> dict:
    """基于向量数据库计算两个核桃的相似度，只比较相同尺寸的核桃"""
    if not vector_db or size1 != size2:
        # 如果没有向量数据库或尺寸不同，返回None让调用者使用其他方法
        return None

    # 获取特征向量
    texture_vec1 = vector_db.get_features(walnut_id1, size1, 'texture')
    texture_vec2 = vector_db.get_features(walnut_id2, size2, 'texture')

    edge_vec1 = vector_db.get_features(walnut_id1, size1, 'edge')
    edge_vec2 = vector_db.get_features(walnut_id2, size2, 'edge')

    color_vec1 = vector_db.get_features(walnut_id1, size1, 'color')
    color_vec2 = vector_db.get_features(walnut_id2, size2, 'color')

    # 检查是否有空的特征向量
    if not all([texture_vec1, texture_vec2, edge_vec1, edge_vec2, color_vec1, color_vec2]):
        return None

    # 计算各部分相似度
    texture_similarity = cosine_similarity(texture_vec1, texture_vec2)
    edge_similarity = cosine_similarity(edge_vec1, edge_vec2)
    color_similarity = cosine_similarity(color_vec1, color_vec2)

    # 计算综合相似度（可以根据需要调整权重）
    overall_similarity = (texture_similarity + edge_similarity + color_similarity) / 3

    return {
        'similarity': overall_similarity,
        'texture_similarity': texture_similarity,
        'edge_similarity': edge_similarity,
        'color_similarity': color_similarity
    }


# 本函数负责实现在选择的数据库路径中选择创建三个表，如果有的话这个函数不会执行
# author：张
# qq：750123348
# 变量：db_path:数据库文件所在的路径
def create_similarity_table(db_path):
    """创建所需的数据库表"""
    # # 定义数据库路径
    # db_path = r"F:\python\核桃识别\ShiB
    # ie\example.db"
    print(db_path)
    # 创建数据库连接
    conn = None
    try:
        conn = sqlite3.connect(db_path)
        c = conn.cursor()

        # 创建核桃选中状态表
        c.execute('''
                  CREATE TABLE IF NOT EXISTS walnut_selection
                  (
                      id
                      INTEGER
                      PRIMARY
                      KEY
                      AUTOINCREMENT,
                      walnut_name
                      TEXT
                      NOT
                      NULL,
                      selected
                      BOOLEAN
                      NOT
                      NULL,
                      over
                      BOOLEAN
                      NOT
                      NULL
                  );
                  ''')

        # 创建时间戳和核桃ID表
        c.execute('''
                  CREATE TABLE IF NOT EXISTS time_stamped_similarities
                  (
                      id
                      INTEGER
                      PRIMARY
                      KEY
                      AUTOINCREMENT,
                      walnut_id1
                      TEXT
                      NOT
                      NULL,
                      walnut_id2
                      TEXT
                      NOT
                      NULL,
                      similarity
                      REAL
                      NOT
                      NULL,
                      timestamp
                      DATETIME
                      DEFAULT
                      CURRENT_TIMESTAMP
                  );
                  ''')

        # 创建核桃相似度详细信息表
        c.execute('''
                  CREATE TABLE IF NOT EXISTS similarities
                  (
                      id
                      INTEGER
                      PRIMARY
                      KEY
                      AUTOINCREMENT,
                      id1
                      TEXT
                      NOT
                      NULL,
                      id2
                      TEXT
                      NOT
                      NULL,
                      similarity
                      REAL
                      NOT
                      NULL,
                      texture_similarity
                      REAL
                      NOT
                      NULL,
                      edge_similarity
                      REAL
                      NOT
                      NULL,
                      color_similarity
                      REAL
                      NOT
                      NULL,
                      num
                      INTEGER
                      NOT
                      NULL
                  );
                  ''')

        # 提交更改并关闭连接
        conn.commit()
        print("表创建成功")
    except Error as e:
        print(f"发生错误: {e}")
    finally:
        if conn:
            conn.close()
            print("数据库连接已关闭")


# 本函数负责向数据库中插入核桃名称
# author：张
# qq：750123348
# 变量：db_path:数据库文件所在的路径，names_list:核桃名称列表
def insert_walnut_names(db_path, names_list):
    # 连接到SQLite数据库
    conn = None
    try:
        conn = sqlite3.connect(db_path)
        c = conn.cursor()

        # 插入核桃名称到 walnut_selection 表
        for name in names_list:
            # 检查是否已存在该名称
            c.execute("SELECT COUNT(*) FROM walnut_selection WHERE walnut_name=?", (name,))
            count = c.fetchone()[0]

            # 如果不存在，则插入新记录
            if count == 0:
                c.execute("INSERT INTO walnut_selection (walnut_name, selected, over) VALUES (?, ?, ?)",
                          (name, False, False))
                print(f"插入新记录: {name}")
            else:
                print(f"记录已存在: {name}")

        # 提交更改
        conn.commit()
        print("提交完成")
    except Error as e:
        print(f"发生错误: {e}")
    finally:
        if conn:
            conn.close()
            print("数据库连接已关闭")


# 本函数为上一个函数insert_walnut_names的辅助函数
def extract_number(s):
    """从字符串中提取第一个连续的数字序列，并转换为整数"""
    number_str = ''.join(filter(str.isdigit, s))
    return int(number_str) if number_str else 0


# ****本函数负责训练并将结果插入到数据库当中
# author：张
# qq：750123348
# 变量：db_path:数据库文件所在的路径，folder_path:图片文件所在的路径
def process_subfolders_and_store(db_path, root_folder, progress_callback=None):
    # 连接到SQLite数据库
    conn = sqlite3.connect(db_path)

    c = conn.cursor()

    subfolders = [f for f in os.listdir(root_folder) if os.path.isdir(os.path.join(root_folder, f))]
    total_iterations = int(math.comb(len(subfolders), 2))  # 计算组合数C(n, 2)

    iteration = 0  # 初始化迭代计数器

    # 确保所有子文件夹的over字段被初始化为False
    for subfolder in subfolders:
        c.execute("UPDATE walnut_selection SET over=? WHERE walnut_name=?", (False, subfolder))

    # 提交所有更改
    conn.commit()

    for index in range(len(subfolders) - 1):
        subfolder = subfolders[index]
        # 从文件夹名称中提取尺寸信息（假设格式为"核桃ID_尺寸"）
        parts = subfolder.split('_')
        walnut_id1 = parts[0] if len(parts) > 0 else subfolder
        size1 = parts[1] if len(parts) > 1 else "unknown"

        for index2 in range(index + 1, len(subfolders)):
            subfolder2 = subfolders[index2]
            # 从文件夹名称中提取尺寸信息
            parts2 = subfolder2.split('_')
            walnut_id2 = parts2[0] if len(parts2) > 0 else subfolder2
            size2 = parts2[1] if len(parts2) > 1 else "unknown"

            # 只比较相同尺寸的核桃
            if size1 != size2:
                iteration += 1
                continue

            iteration += 1
            if progress_callback:
                progress_callback(iteration, total_iterations)

            # 使用向量数据库计算相似度
            similarity_result = calculate_similarity_from_vectors(walnut_id1, size1, walnut_id2, size2)

            # 如果无法从向量数据库计算，则回退到原有方法
            if similarity_result is None:
                images_list1 = load_images_from_folder(os.path.join(root_folder, subfolder))
                images_list2 = load_images_from_folder(os.path.join(root_folder, subfolder2))

                similarity_result = similar.calulate_all_similarity(images_list1, images_list2)

            # 应用阈值过滤
            result = filter_details_by_threshold(similarity_result, get_config_value('G'))

            # 假设result是一个列表，前两项是subfolder和subfolder2，后面是数值
            # 将subfolder和subfolder2加入到result的开头，形成一个扁平的列表
            flat_result = [subfolder, subfolder2] + result

            # print(flat_result)
            flat_result_converted = [float(item) if isinstance(item, (np.float32, np.float64)) else item for item in
                                     flat_result]

            print(flat_result_converted)

            # 检查是否已经有相同记录
            c.execute('''
                      SELECT *
                      FROM similarities
                      WHERE id1 = ?
                        AND id2 = ?
                      ''', (subfolder, subfolder2))
            existing_row = c.fetchone()
            if not existing_row:
                # 如果没有相同记录，则插入新记录
                c.execute('''
                          INSERT INTO similarities (id1, id2, similarity, texture_similarity, edge_similarity,
                                                    color_similarity, num)
                          VALUES (?, ?, ?, ?, ?, ?, ?)
                          ''', tuple(flat_result_converted))
            else:
                # 如果已有记录，则更新
                c.execute('''
                          UPDATE similarities
                          SET similarity=?,
                              texture_similarity=?,
                              edge_similarity=?,
                              color_similarity=?,
                              num=?
                          WHERE id1 = ?
                            AND id2 = ?
                          ''', (flat_result_converted[2], flat_result_converted[3], flat_result_converted[4],
                                flat_result_converted[5], flat_result_converted[6], flat_result_converted[0],
                                flat_result_converted[1]))

    # 提交所有更改并关闭连接
    conn.commit()
    conn.close()

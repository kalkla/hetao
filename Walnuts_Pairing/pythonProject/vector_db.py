# vector_db.py
import sqlite3
import numpy as np
import json
from typing import List, Dict, Tuple


class VectorDB:
    def __init__(self, db_path: str):
        self.db_path = db_path
        self.init_db()

    def init_db(self):
        """初始化向量数据库表"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # 创建存储核桃特征的表，增加size字段
        cursor.execute('''
                       CREATE TABLE IF NOT EXISTS walnut_features
                       (
                           id
                           INTEGER
                           PRIMARY
                           KEY
                           AUTOINCREMENT,
                           walnut_id
                           TEXT
                           NOT
                           NULL,
                           size
                           TEXT
                           NOT
                           NULL, -- 核桃尺寸
                           feature_type
                           TEXT
                           NOT
                           NULL, -- 'texture', 'edge', 'color'等
                           feature_vector
                           TEXT
                           NOT
                           NULL, -- JSON格式存储向量
                           created_at
                           TIMESTAMP
                           DEFAULT
                           CURRENT_TIMESTAMP
                       )
                       ''')

        # 创建复合索引提高查询效率
        cursor.execute('''
                       CREATE INDEX IF NOT EXISTS idx_walnut_size ON walnut_features(walnut_id, size)
                       ''')

        conn.commit()
        conn.close()

    def store_features(self, walnut_id: str, size: str, feature_type: str, feature_vector: List[float]):
        """存储核桃特征向量"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # 将向量转换为JSON字符串存储
        feature_str = json.dumps(feature_vector)

        cursor.execute('''
                       INSERT INTO walnut_features (walnut_id, size, feature_type, feature_vector)
                       VALUES (?, ?, ?, ?)
                       ''', (walnut_id, size, feature_type, feature_str))

        conn.commit()
        conn.close()

    def get_features(self, walnut_id: str, size: str, feature_type: str) -> List[float]:
        """获取指定核桃的特征向量"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('''
                       SELECT feature_vector
                       FROM walnut_features
                       WHERE walnut_id = ? AND size = ? AND feature_type = ?
                       ''', (walnut_id, size, feature_type))

        result = cursor.fetchone()
        conn.close()

        if result:
            return json.loads(result[0])
        return []

    def get_walnut_ids_by_size(self, size: str) -> List[str]:
        """获取指定尺寸的所有核桃ID"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('''
                       SELECT DISTINCT walnut_id
                       FROM walnut_features
                       WHERE size = ?
                       ''', (size,))

        results = cursor.fetchall()
        conn.close()

        return [row[0] for row in results]

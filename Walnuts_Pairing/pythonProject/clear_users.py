#!/usr/bin/env python3
"""
清空用户表数据的脚本
"""

import sqlite3
import os

# 设置数据库路径
db_path = os.path.join(os.path.dirname(__file__), 'example.db')

def clear_users_table():
    try:
        # 连接数据库
        conn = sqlite3.connect(db_path)
        c = conn.cursor()
        
        # 执行删除语句
        c.execute('DELETE FROM users;')
        
        # 提交事务
        conn.commit()
        
        # 打印结果
        print(f"成功清空用户表，共删除 {c.rowcount} 条记录")
        
    except Exception as e:
        print(f"清空用户表失败: {str(e)}")
        import traceback
        traceback.print_exc()
    finally:
        if conn:
            conn.close()
            print("数据库连接已关闭")

if __name__ == "__main__":
    clear_users_table()
# -*- coding: utf-8 -*-
"""
数据库查询脚本：用于查看用户和核桃相关信息
"""

import sqlite3
import os

def query_users_table(db_path='example.db'):
    """
    查询users表中的所有用户信息
    """
    print(f"正在查询数据库: {db_path}")
    if not os.path.exists(db_path):
        print(f"错误：数据库文件 '{db_path}' 不存在")
        return
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # 检查表是否存在
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users'")
        if not cursor.fetchone():
            print("users表不存在")
            conn.close()
            return
        
        # 查询表的结构
        cursor.execute("PRAGMA table_info(users)")
        columns = cursor.fetchall()
        print("\nusers表结构:")
        print(f"{'列名':<15} {'类型':<10} {'允许空':<8} {'默认值':<15} {'主键'}")
        print("-" * 60)
        for col in columns:
            col_name = col[1]
            col_type = col[2]
            not_null = "否" if col[3] else "是"
            default_val = col[4] or "-"
            primary_key = "是" if col[5] else "否"
            print(f"{col_name:<15} {col_type:<10} {not_null:<8} {default_val:<15} {primary_key}")
        
        # 查询用户数据
        cursor.execute("SELECT * FROM users")
        users = cursor.fetchall()
        
        print(f"\n用户数量: {len(users)}")
        if users:
            print("\n用户数据:")
            # 获取列名
            cursor.execute("PRAGMA table_info(users)")
            column_names = [col[1] for col in cursor.fetchall()]
            print(" | ".join(column_names))
            print("-" * (sum(len(name) + 3 for name in column_names) - 1))
            
            # 打印每一行数据
            for user in users:
                print(" | ".join(str(item) for item in user))
        else:
            print("暂无用户数据")
            
    except sqlite3.Error as e:
        print(f"数据库查询错误: {e}")
    finally:
        if 'conn' in locals() and conn:
            conn.close()
            print("\n数据库连接已关闭")

def query_walnut_tables(db_path='example.db'):
    """
    查询核桃相关表的信息
    """
    print(f"\n正在查询核桃相关表: {db_path}")
    if not os.path.exists(db_path):
        print(f"错误：数据库文件 '{db_path}' 不存在")
        return
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # 查询数据库中所有表
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        
        print(f"\n数据库中存在的表: {[table[0] for table in tables]}")
        
        # 检查核桃相关表并查询基本信息
        walnut_tables = ['walnut_selection', 'similarities', 'time_stamped_similarities']
        
        for table in walnut_tables:
            cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table}'")
            if cursor.fetchone():
                cursor.execute(f"SELECT COUNT(*) FROM {table}")
                count = cursor.fetchone()[0]
                print(f"\n{table}表: {count} 条记录")
                
                # 查询表的前3条记录
                cursor.execute(f"SELECT * FROM {table} LIMIT 3")
                rows = cursor.fetchall()
                
                if rows:
                    # 获取列名
                    cursor.execute(f"PRAGMA table_info({table})")
                    column_names = [col[1] for col in cursor.fetchall()]
                    print(f"\n{table}表结构:")
                    print(" | ".join(column_names))
                    print("-" * (sum(len(name) + 3 for name in column_names) - 1))
                    
                    for row in rows[:3]:  # 最多显示3条
                        print(" | ".join(str(item) if len(str(item)) < 20 else str(item)[:17] + "..." for item in row))
                    
                    if count > 3:
                        print(f"... 还有 {count - 3} 条记录")
    
    except sqlite3.Error as e:
        print(f"数据库查询错误: {e}")
    finally:
        if 'conn' in locals() and conn:
            conn.close()
            print("\n数据库连接已关闭")

def main():
    """
    主函数
    """
    print("===== 核桃检测小程序数据库查询工具 =====")
    print("1. 查看用户信息")
    print("2. 查看核桃相关表信息")
    print("3. 查看所有信息")
    
    try:
        choice = input("\n请选择操作 (1-3): ")
        
        if choice == '1':
            query_users_table()
        elif choice == '2':
            query_walnut_tables()
        elif choice == '3':
            query_users_table()
            query_walnut_tables()
        else:
            print("无效的选择")
    except KeyboardInterrupt:
        print("\n程序已取消")
    except Exception as e:
        print(f"发生错误: {e}")

if __name__ == "__main__":
    main()
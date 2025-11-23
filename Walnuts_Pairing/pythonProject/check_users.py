import sqlite3
import os

# 获取数据库绝对路径
DATABASE_PATH = os.path.join(os.path.dirname(__file__), 'example.db')

try:
    conn = sqlite3.connect(DATABASE_PATH)
    c = conn.cursor()
    
    # 查询所有用户信息
    c.execute("SELECT * FROM users")
    users = c.fetchall()
    
    print(f"总用户数: {len(users)}")
    for user in users:
        print(f"OpenID: {user[0]}, 昵称: {user[1]}, 头像URL: {user[2]}, 创建时间: {user[3]}, 更新时间: {user[4]}")
    
    conn.close()
except sqlite3.Error as e:
    print(f"数据库查询错误: {e}")
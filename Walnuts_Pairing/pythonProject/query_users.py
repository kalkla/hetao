import sqlite3

# 连接到数据库
conn = sqlite3.connect('example.db')
cursor = conn.cursor()

# 列出所有表
print('数据库中的表:')
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()
for table in tables:
    print(table[0])

# 查看users表中的数据
print('\nusers表中的数据:')
cursor.execute('SELECT * FROM users;')
users = cursor.fetchall()
# 打印表头
cursor.execute('PRAGMA table_info(users);')
columns = cursor.fetchall()
column_names = [column[1] for column in columns]
print(' | '.join(column_names))
print('-' * 50)
# 打印数据
for user in users:
    print(' | '.join(str(field) for field in user))

# 关闭连接
conn.close()
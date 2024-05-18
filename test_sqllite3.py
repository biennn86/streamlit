import sqlite3

# Kết nối đến cơ sở dữ liệu SQLite
conn = sqlite3.connect('example.db')
c = conn.cursor()
# Tạo bảng
c.execute('''CREATE TABLE IF NOT EXISTS users
             (id INTEGER PRIMARY KEY, name TEXT, age INTEGER)''')

# Thêm dữ liệu
c.execute("INSERT INTO users (name, age) VALUES ('Alice', 30)")
c.execute("INSERT INTO users (name, age) VALUES ('Bob', 25)")

# Lưu thay đổi
conn.commit()

# Đóng kết nối
conn.close()

#=============
# Hàm thêm DataFrame vào cơ sở dữ liệu
def add_users_from_df(df):
    conn = sqlite3.connect('example.db')
    df.to_sql('users', conn, if_exists='append', index=False)
    conn.close()

def get_users_df():
    conn = sqlite3.connect('example.db')
    df = pd.read_sql_query('SELECT * FROM users', conn)
    conn.close()
    return df

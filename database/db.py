import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="taolao",
        database="LibraryDB",
        auth_plugin="mysql_native_password"
    )


def fetch_all(sql, params=None):
    """
    FIX: Thêm buffered=True để tránh lỗi 'Unread result found'
    """
    conn = get_connection()
    cur = conn.cursor(dictionary=True, buffered=True)  # THÊM buffered=True
    cur.execute(sql, params or ())
    data = cur.fetchall()
    cur.close()
    conn.close()
    return data

def fetch_one(sql, params=None):
    """
    FIX: Thêm buffered=True để tránh lỗi 'Unread result found'
    """
    conn = get_connection()
    cur = conn.cursor(dictionary=True, buffered=True)  # THÊM buffered=True
    cur.execute(sql, params or ())
    data = cur.fetchone()
    cur.close()
    conn.close()
    return data

def execute(sql, params=None):
    """
    Thực thi query không trả về kết quả (INSERT, UPDATE, DELETE)
    """
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(sql, params or ())
    conn.commit()
    cur.close()
    conn.close()

# Thêm alias để tương thích với code khác
def execute_query(sql, params=None):
    """Alias for execute function"""
    return execute(sql, params)
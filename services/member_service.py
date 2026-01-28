# đây là member_service.py , bạn xem qua nhé 
import mysql.connector
from database.db import get_connection, fetch_all, fetch_one, execute_query

def fetch_all_members():
    """Lấy tất cả thành viên"""
    sql = """
        SELECT
            user_id,
            fullname,
            email,
            phone,
            role_name,
            gender,
            address,
            user_status,
            totalFineDebt,
            created_at
        FROM USERS
        WHERE role_name = 'MEMBER'
        ORDER BY user_id DESC
    """
    return fetch_all(sql)

def insert_member(data):
    """
    Thêm thành viên mới
    data cần có: fullname, email, phone, gender, address, status
    """
    
    # Xử lý dữ liệu
    fullname = data.get("fullname") or data.get("full_name", "").strip()
    email = data.get("email", "").strip()
    phone = data.get("phone", "").strip() or "-"
    gender = data.get("gender", "").strip() or "-"
    address = data.get("address", "").strip() or "-"
    status = data.get("status", "ACTIVE").strip().upper()
    user_status = data.get("user_status", "ACTIVE").strip().upper()
    
    # Tạo password mặc định (nên hash trong thực tế)
    password = "hashed_password_default"
    
    sql = """
        INSERT INTO USERS 
        (fullname, email, phone, gender, address, status, user_status, 
         password, role_name, created_at, totalFineDebt)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, 'MEMBER', CURDATE(), 0)
    """
    
    execute_query(sql, (
        fullname,
        email,
        phone,
        gender,
        address,
        status,
        user_status,
        password
    ))
    
    # Lấy ID vừa insert
    result = fetch_one("SELECT LAST_INSERT_ID() as id")
    return result['id'] if result else None

def update_member(data):
    """
    Cập nhật thông tin thành viên
    data cần có: user_id, fullname, email, phone, gender, address, user_status
    """
    
    user_id = data.get("user_id", "").strip()
    if not user_id:
        return False
    
    fullname = data.get("fullname") or data.get("full_name", "").strip()
    email = data.get("email", "").strip()
    phone = data.get("phone", "").strip() or "-"
    gender = data.get("gender", "").strip() or "-"
    address = data.get("address", "").strip() or "-"
    user_status = data.get("user_status", "ACTIVE").strip().upper()
    
    sql = """
        UPDATE USERS SET
            fullname = %s,
            email = %s,
            phone = %s,
            gender = %s,
            address = %s,
            user_status = %s
        WHERE user_id = %s AND role_name = 'MEMBER'
    """
    
    execute_query(sql, (
        fullname,
        email,
        phone,
        gender,
        address,
        user_status,
        user_id
    ))
    
    return True
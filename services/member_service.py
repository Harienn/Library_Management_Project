# services/member_service.py
from database.db import execute_query, fetch_all, fetch_one, get_last_insert_id
from datetime import datetime

def fetch_all_members():
    """Lấy tất cả thành viên"""
    try:
        sql = """
            SELECT 
                user_id,
                fullname,
                email,
                COALESCE(phone, '-') as phone,
                COALESCE(gender, '-') as gender,
                COALESCE(address, '-') as address,
                COALESCE(user_status, 'ACTIVE') as user_status,
                status,
                created_at
            FROM users 
            WHERE role_name = 'MEMBER'
            ORDER BY user_id DESC
        """
        return fetch_all(sql)
    except Exception as e:
        print(f"Error fetching members: {e}")
        return []

def check_email_exists(email, exclude_user_id=None):
    """Kiểm tra email đã tồn tại chưa"""
    try:
        if exclude_user_id:
            sql = "SELECT user_id FROM users WHERE email = %s AND user_id != %s"
            result = fetch_one(sql, (email, exclude_user_id))
        else:
            sql = "SELECT user_id FROM users WHERE email = %s"
            result = fetch_one(sql, (email,))
        
        return result is not None
    except Exception as e:
        print(f"Error checking email: {e}")
        return False

def insert_member(data):
    """Thêm thành viên mới - SỬA LẠI ĐỂ TRẢ VỀ user_id"""
    try:
        # Tạo password mặc định (có thể thay đổi sau)
        default_password = "hashed_default_password_123"
        
        sql = """
            INSERT INTO users (
                fullname, password, created_at, status, 
                address, phone, email, role_name, gender, user_status
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        
        # Gọi execute_query và lấy last_insert_id
        result = execute_query(sql, (
            data["fullname"],
            default_password,
            datetime.now().date(),
            "ACTIVE",  # status field
            data.get("address"),
            data.get("phone"),
            data["email"],
            "MEMBER",
            data.get("gender"),
            data.get("user_status", "ACTIVE")
        ))
        
        # Lấy user_id vừa tạo
        user_id = get_last_insert_id()
        print(f"=== DEBUG: New member created with ID: {user_id} ===")
        
        return user_id if user_id else 0
        
    except Exception as e:
        print(f"Error inserting member: {e}")
        raise e  # Ném lỗi lên để xử lý ở caller

def update_member(data):
    """Cập nhật thành viên"""
    try:
        sql = """
            UPDATE users 
            SET 
                fullname = %s,
                email = %s,
                phone = %s,
                gender = %s,
                address = %s,
                user_status = %s,
                status = %s
            WHERE user_id = %s AND role_name = 'MEMBER'
        """
        
        # Map user_status sang status
        user_status = data.get("user_status", "ACTIVE")
        status = "ACTIVE" if user_status == "ACTIVE" else "BLOCKED"
        
        result = execute_query(sql, (
            data["fullname"],
            data["email"],
            data.get("phone"),
            data.get("gender"),
            data.get("address"),
            user_status,
            status,
            data["user_id"]
        ))
        
        return result > 0  # Trả về True nếu có row được update
        
    except Exception as e:
        print(f"Error updating member: {e}")
        return False

def delete_member(member_id):
    """Xóa thành viên"""
    try:
        sql = "DELETE FROM users WHERE user_id = %s AND role_name = 'MEMBER'"
        result = execute_query(sql, (member_id,))
        
        deleted = result > 0
        if deleted:
            print(f"=== DEBUG: Member {member_id} deleted successfully ===")
        else:
            print(f"=== DEBUG: No member found with ID {member_id} ===")
        
        return deleted
        
    except Exception as e:
        print(f"Error deleting member: {e}")
        return False
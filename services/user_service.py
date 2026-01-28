# services/user_service.py
"""
User Service - Handle user-related operations
✅ Profile management
✅ Password management
"""
from database.db import execute, fetch_one
import hashlib


def hash_password(password):
    """Hash password using SHA-256"""
    return hashlib.sha256(password.encode()).hexdigest()


def update_user_profile(user_id, fullname, phone, gender, address):
    """
    ✅ Cập nhật thông tin cá nhân của user
    
    Args:
        user_id: ID của user
        fullname: Họ tên đầy đủ
        phone: Số điện thoại
        gender: Giới tính (Male/Female/Other)
        address: Địa chỉ
    
    Returns:
        (success: bool, message: str)
    """
    try:
        # Validate inputs
        if not fullname or not fullname.strip():
            return False, "Full name is required"
        
        if not phone or not phone.strip():
            return False, "Phone number is required"
        
        if not gender:
            return False, "Gender is required"
        
        if not address or not address.strip():
            return False, "Address is required"
        
        # Update database
        query = """
        UPDATE USERS 
        SET fullname = %s, phone = %s, gender = %s, address = %s
        WHERE user_id = %s
        """
        
        execute(query, (fullname.strip(), phone.strip(), gender, address.strip(), user_id))
        
        print(f"✅ Profile updated for user {user_id}")
        return True, "Profile updated successfully!"
        
    except Exception as e:
        print(f"❌ Error updating profile: {e}")
        return False, f"Error: {str(e)}"


def change_password(user_id, current_password, new_password):
    """
    ✅ Thay đổi mật khẩu của user
    
    Args:
        user_id: ID của user
        current_password: Mật khẩu hiện tại
        new_password: Mật khẩu mới
    
    Returns:
        (success: bool, message: str)
    """
    try:
        # 1. Lấy thông tin user
        user = fetch_one(
            "SELECT password FROM USERS WHERE user_id = %s",
            (user_id,)
        )
        
        if not user:
            return False, "User not found"
        
        # 2. Kiểm tra mật khẩu hiện tại
        current_password_hash = hash_password(current_password)
        
        if user['password'] != current_password_hash:
            return False, "Current password is incorrect"
        
        # 3. Validate mật khẩu mới
        if len(new_password) < 8:
            return False, "New password must be at least 8 characters"
        
        # 4. Hash và update mật khẩu mới
        new_password_hash = hash_password(new_password)
        
        query = "UPDATE USERS SET password = %s WHERE user_id = %s"
        execute(query, (new_password_hash, user_id))
        
        print(f"✅ Password changed for user {user_id}")
        return True, "Password changed successfully!"
        
    except Exception as e:
        print(f"❌ Error changing password: {e}")
        return False, f"Error: {str(e)}"


def get_user_by_id(user_id):
    """
    Lấy thông tin user theo ID
    
    Args:
        user_id: ID của user
    
    Returns:
        User dict hoặc None
    """
    try:
        query = """
        SELECT 
            user_id, username, email, fullname, phone, gender, 
            address, role, status, totalFineDebt, created_at
        FROM USERS
        WHERE user_id = %s
        """
        
        return fetch_one(query, (user_id,))
        
    except Exception as e:
        print(f"❌ Error getting user: {e}")
        return None


def get_user_by_username(username):
    """
    Lấy thông tin user theo username
    
    Args:
        username: Username của user
    
    Returns:
        User dict hoặc None
    """
    try:
        query = """
        SELECT 
            user_id, username, email, password, fullname, phone, gender, 
            address, role, status, totalFineDebt, created_at
        FROM USERS
        WHERE username = %s
        """
        
        return fetch_one(query, (username,))
        
    except Exception as e:
        print(f"❌ Error getting user: {e}")
        return None


def check_profile_complete(user_id):
    """
    ✅ Kiểm tra xem profile đã đầy đủ chưa
    
    Args:
        user_id: ID của user
    
    Returns:
        (is_complete: bool, missing_fields: list)
    """
    try:
        user = fetch_one(
            "SELECT fullname, phone, gender, address FROM USERS WHERE user_id = %s",
            (user_id,)
        )
        
        if not user:
            return False, ["user_not_found"]
        
        missing_fields = []
        
        if not user.get('fullname') or not user['fullname'].strip():
            missing_fields.append("fullname")
        
        if not user.get('phone') or not user['phone'].strip():
            missing_fields.append("phone")
        
        if not user.get('gender'):
            missing_fields.append("gender")
        
        if not user.get('address') or not user['address'].strip():
            missing_fields.append("address")
        
        is_complete = len(missing_fields) == 0
        
        return is_complete, missing_fields
        
    except Exception as e:
        print(f"❌ Error checking profile: {e}")
        return False, ["error"]


def create_user(username, email, password, fullname=None, role='MEMBER'):
    """
    Tạo user mới
    
    Args:
        username: Username
        email: Email
        password: Password (sẽ được hash)
        fullname: Họ tên (optional)
        role: Role (MEMBER/ADMIN/GUEST)
    
    Returns:
        (success: bool, message: str, user_id: int)
    """
    try:
        # 1. Check username exists
        existing = fetch_one(
            "SELECT user_id FROM USERS WHERE username = %s",
            (username,)
        )
        
        if existing:
            return False, "Username already exists", None
        
        # 2. Check email exists
        existing = fetch_one(
            "SELECT user_id FROM USERS WHERE email = %s",
            (email,)
        )
        
        if existing:
            return False, "Email already exists", None
        
        # 3. Hash password
        password_hash = hash_password(password)
        
        # 4. Insert user
        query = """
        INSERT INTO USERS (username, email, password, fullname, role, status, totalFineDebt)
        VALUES (%s, %s, %s, %s, %s, 'ACTIVE', 0)
        """
        
        from database.db import get_connection
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute(query, (username, email, password_hash, fullname, role))
        user_id = cursor.lastrowid
        
        conn.commit()
        cursor.close()
        conn.close()
        
        print(f"✅ User created: {username} (ID: {user_id})")
        return True, "User created successfully!", user_id
        
    except Exception as e:
        print(f"❌ Error creating user: {e}")
        return False, f"Error: {str(e)}", None


def authenticate_user(username, password):
    """
    Xác thực user
    
    Args:
        username: Username
        password: Password
    
    Returns:
        User dict nếu thành công, None nếu thất bại
    """
    try:
        user = get_user_by_username(username)
        
        if not user:
            return None
        
        password_hash = hash_password(password)
        
        if user['password'] != password_hash:
            return None
        
        # Remove password from returned dict
        user.pop('password', None)
        
        return user
        
    except Exception as e:
        print(f"❌ Error authenticating user: {e}")
        return None


# Alias for backward compatibility
change_user_password = change_password
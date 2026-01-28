# services/user_service.py
"""
User Service - Handle user-related operations
✅ Profile management
✅ Password management
✅ Enhanced password validation (no duplicate password)
✅ SMART PASSWORD CHECK: Works with both plain text and hashed passwords
✅ Debug logging
"""
from database.db import execute, fetch_one
import hashlib


def hash_password(password):
    """
    Hash password using SHA-256
    CRITICAL: This MUST be identical across all files
    """
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
    ✅ Thay đổi mật khẩu của user với validation đầy đủ
    ✅ SMART: Tự động phát hiện nếu database lưu plain text hoặc hash
    
    Args:
        user_id: ID của user
        current_password: Mật khẩu hiện tại (plain text)
        new_password: Mật khẩu mới (plain text)
    
    Returns:
        (success: bool, message: str)
    
    Validations:
    1. Current password phải đúng (hỗ trợ cả plain text và hash)
    2. New password phải >= 8 ký tự
    3. ✅ NEW: New password KHÔNG được trùng current password
    """
    try:
        print(f"\n{'='*60}")
        print(f"🔐 CHANGE PASSWORD DEBUG - User ID: {user_id}")
        print(f"{'='*60}")
        
        # 1. Lấy thông tin user từ database
        user = fetch_one(
            "SELECT password FROM USERS WHERE user_id = %s",
            (user_id,)
        )
        
        if not user:
            print(f"❌ User not found: {user_id}")
            return False, "User not found"
        
        print(f"✅ User found: ID {user_id}")
        
        # 2. ✅ SMART CHECK: Kiểm tra mật khẩu hiện tại (hỗ trợ cả plain text và hash)
        stored_password_hash = user['password']
        current_password_hash = hash_password(current_password)
        
        print(f"\n📝 Current Password Verification:")
        print(f"   Input password: '{current_password[:3]}***'")
        print(f"   Input hash: {current_password_hash[:30]}...")
        print(f"   Stored in DB: {stored_password_hash[:30]}...")
        
        # ✅ Check both possibilities: plain text OR hashed
        is_plain_text_match = (stored_password_hash == current_password)
        is_hash_match = (stored_password_hash == current_password_hash)
        
        print(f"   Plain text match: {is_plain_text_match}")
        print(f"   Hash match: {is_hash_match}")
        
        if not (is_plain_text_match or is_hash_match):
            print(f"\n❌ FAILED: Current password does not match!")
            return False, "Current password is incorrect"
        
        # Determine if DB is storing plain text or hash
        db_uses_plain_text = is_plain_text_match and not is_hash_match
        
        if db_uses_plain_text:
            print(f"⚠️  WARNING: Database is storing PLAIN TEXT passwords!")
            print(f"   This is a security risk. Passwords should be hashed.")
        
        print(f"✅ Current password verified!")
        
        # 3. ✅ Kiểm tra mật khẩu mới không được trùng mật khẩu cũ
        new_password_hash = hash_password(new_password)
        
        print(f"\n🔍 Checking for duplicate password:")
        print(f"   Current password: '{current_password[:3]}***'")
        print(f"   New password: '{new_password[:3]}***'")
        
        # Check if passwords are the same (plain text comparison)
        if current_password == new_password:
            print(f"   ❌ Passwords are identical!")
            return False, "New password must be different from current password"
        
        print(f"   ✅ Passwords are different")
        
        # 4. Validate độ dài mật khẩu mới
        if len(new_password) < 8:
            print(f"❌ New password too short: {len(new_password)} chars")
            return False, "New password must be at least 8 characters"
        
        print(f"✅ New password length OK: {len(new_password)} chars")
        
        # 5. ✅ Update mật khẩu mới (ALWAYS USE HASH for security)
        print(f"\n🔄 Updating Password:")
        print(f"   New password: '{new_password[:3]}***'")
        print(f"   New hash: {new_password_hash[:30]}...")
        print(f"   ⚠️  Storing as HASH (for security)")
        
        query = "UPDATE USERS SET password = %s WHERE user_id = %s"
        execute(query, (new_password_hash, user_id))
        
        print(f"✅ Database UPDATE executed and committed")
        
        # 6. ✅ VERIFY update was successful
        updated_user = fetch_one(
            "SELECT password FROM USERS WHERE user_id = %s",
            (user_id,)
        )
        
        if not updated_user:
            print(f"❌ Cannot verify - user not found after update")
            return False, "Update verification failed"
        
        updated_hash = updated_user['password']
        
        print(f"\n🔍 Verification:")
        print(f"   Expected hash: {new_password_hash[:30]}...")
        print(f"   Actual hash:   {updated_hash[:30]}...")
        print(f"   Match: {updated_hash == new_password_hash}")
        
        if updated_hash == new_password_hash:
            print(f"\n✅ SUCCESS: Password changed and verified!")
            print(f"{'='*60}\n")
            
            # ⚠️ Important note for user
            if db_uses_plain_text:
                return True, "Password changed successfully! Note: Your password is now securely hashed."
            else:
                return True, "Password changed successfully!"
        else:
            print(f"\n❌ FAILED: Password hash mismatch after update!")
            print(f"{'='*60}\n")
            return False, "Password update verification failed"
        
    except Exception as e:
        print(f"\n❌ EXCEPTION: Error changing password: {e}")
        import traceback
        traceback.print_exc()
        print(f"{'='*60}\n")
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
            user_id, email, fullname, phone, gender, 
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
        
        print(f"🆕 Creating user: {username}")
        print(f"   Password hash: {password_hash[:30]}...")
        
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
    ✅ Xác thực user với debug logging
    ✅ SMART: Hỗ trợ cả plain text và hashed password trong database
    
    Args:
        username: Username
        password: Password (plain text)
    
    Returns:
        User dict nếu thành công, None nếu thất bại
    """
    try:
        print(f"\n{'='*60}")
        print(f"🔐 AUTHENTICATE USER DEBUG")
        print(f"{'='*60}")
        
        user = get_user_by_username(username)
        
        if not user:
            print(f"❌ User not found: {username}")
            print(f"{'='*60}\n")
            return None
        
        print(f"✅ User found: {username}")
        
        password_hash = hash_password(password)
        stored_hash = user['password']
        
        print(f"\n📝 Password Verification:")
        print(f"   Input password: '{password[:3]}***'")
        print(f"   Input hash: {password_hash[:30]}...")
        print(f"   Stored hash: {stored_hash[:30]}...")
        
        # ✅ Check both plain text and hash
        is_plain_match = (stored_hash == password)
        is_hash_match = (stored_hash == password_hash)
        
        print(f"   Plain text match: {is_plain_match}")
        print(f"   Hash match: {is_hash_match}")
        
        if not (is_plain_match or is_hash_match):
            print(f"\n❌ FAILED: Password mismatch!")
            print(f"{'='*60}\n")
            return None
        
        # Remove password from returned dict
        user.pop('password', None)
        
        print(f"\n✅ SUCCESS: Authentication successful!")
        print(f"{'='*60}\n")
        
        return user
        
    except Exception as e:
        print(f"\n❌ EXCEPTION: Error authenticating user: {e}")
        import traceback
        traceback.print_exc()
        print(f"{'='*60}\n")
        return None


# Alias for backward compatibility
change_user_password = change_password
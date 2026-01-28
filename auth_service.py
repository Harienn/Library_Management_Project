# services/auth_service.py
"""
Authentication Service - Xử lý đăng nhập với validation
"""
from database.db import fetch_one


def login_user(email, password):
    """
    Đăng nhập user
    
    Args:
        email: Email address
        password: Password (plain text)
        
    Returns:
        tuple: (success: bool, message: str, user_data: dict or None)
    """
    try:
        # Validate input
        if not email or not password:
            return False, "Please enter both email and password", None
        
        # Tìm user theo email
        query = """
        SELECT user_id, fullname, email, password, role_name, status, 
               phone, gender, address, totalFineDebt
        FROM USERS
        WHERE email = %s
        """
        user = fetch_one(query, (email,))
        
        if not user:
            return False, "Email not found", None
        
        # Kiểm tra password
        stored_password = user['password']
        
        # So sánh password (plain text)
        if stored_password != password:
            print(f"❌ Login failed: Incorrect password for {email}")
            return False, "Incorrect password", None
        
        # Kiểm tra account status
        if user['status'] == 'BLOCKED':
            return False, "Account is blocked. Please contact the library.", None
        
        # Login thành công
        print(f"✅ Login successful: {user['fullname']} ({email})")
        
        # Return user data (không bao gồm password)
        user_data = {
            'user_id': user['user_id'],
            'fullname': user['fullname'],
            'email': user['email'],
            'role_name': user['role_name'],
            'status': user['status'],
            'phone': user['phone'],
            'gender': user['gender'],
            'address': user['address'],
            'totalFineDebt': user['totalFineDebt']
        }
        
        return True, "Login successful!", user_data
        
    except Exception as e:
        print(f"❌ Login error: {e}")
        import traceback
        traceback.print_exc()
        return False, "System error occurred", None


def register_user(fullname, email, password, phone="", gender="", address=""):
    """
    Đăng ký user mới
    
    Returns:
        tuple: (success: bool, message: str)
    """
    try:
        from database.db import execute
        from datetime import date
        
        # Validate input
        if not fullname or not email or not password:
            return False, "Please fill in all required fields"
        
        if len(password) < 8:
            return False, "Password must be at least 8 characters"
        
        # Kiểm tra email đã tồn tại chưa
        check_query = "SELECT user_id FROM USERS WHERE email = %s"
        existing = fetch_one(check_query, (email,))
        
        if existing:
            return False, "Email already exists"
        
        # Tạo user mới
        insert_query = """
        INSERT INTO USERS 
        (fullname, email, password, created_at, status, role_name, 
         phone, gender, address, totalFineDebt)
        VALUES (%s, %s, %s, %s, 'ACTIVE', 'MEMBER', %s, %s, %s, 0)
        """
        
        execute(insert_query, (
            fullname,
            email,
            password,  # Plain text (không an toàn nhưng theo yêu cầu)
            date.today(),
            phone,
            gender,
            address
        ))
        
        print(f"✅ User registered: {fullname} ({email})")
        return True, "Registration successful!"
        
    except Exception as e:
        print(f"❌ Registration error: {e}")
        import traceback
        traceback.print_exc()
        return False, f"System error: {str(e)}"
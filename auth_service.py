# auth_service.py
from database.db import fetch_one, execute_query

def login(email, password):
    """Đăng nhập - Trả về thông tin user nếu thành công"""
    return fetch_one(
        """
        SELECT * FROM USERS
        WHERE email=%s AND password=%s
        AND user_status='ACTIVE'
        """,
        (email, password)
    )

def register(fullname, email, password):
    """
    Đăng ký tài khoản mới
    Returns: 
        - user dict nếu thành công
        - None nếu thất bại
    """
    try:
        # 1. Kiểm tra email đã tồn tại chưa
        existing_user = fetch_one(
            "SELECT email FROM USERS WHERE email=%s",
            (email,)
        )
        
        if existing_user:
            return {"error": "Email already exists"}
        
        # 2. Thêm user mới vào database
        execute_query(
            """
            INSERT INTO USERS 
            (fullname, email, password, role_name, user_status, status, created_at, totalFineDebt)
            VALUES (%s, %s, %s, 'MEMBER', 'ACTIVE', 'ACTIVE', NOW(), 0)
            """,
            (fullname, email, password)
        )
        
        # 3. Lấy thông tin user vừa tạo để trả về (tự động đăng nhập)
        new_user = fetch_one(
            """
            SELECT * FROM USERS 
            WHERE email=%s AND password=%s
            """,
            (email, password)
        )
        
        return new_user
        
    except Exception as e:
        print(f"Register error: {e}")
        return {"error": str(e)}
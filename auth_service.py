# auth_service.py
<<<<<<< HEAD
from database.db import fetch_one, execute_query
=======
"""
Authentication Service - Handle login/logout/register operations
✅ User login with password hashing
✅ User registration
✅ Password verification
✅ Compatible with your db.py module
"""
from database.db import fetch_one, execute, get_connection
import hashlib
import re
>>>>>>> version-2

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

<<<<<<< HEAD
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
=======
def hash_password(password):
    """
    Hash password using SHA-256
    IMPORTANT: This MUST match the hash_password in user_service.py
    """
    return hashlib.sha256(password.encode()).hexdigest()


def validate_email(email):
    """
    Validate email format
    
    Args:
        email: Email address to validate
    
    Returns:
        bool: True if valid, False otherwise
    """
    # Basic email regex pattern
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


def register_user(fullname, email, password):
    """
    Register a new user account
    
    Args:
        fullname: Full name of the user
        email: Email address (will be used as username)
        password: Plain text password (will be hashed)
    
    Returns:
        (success: bool, message: str)
    
    Validations:
    1. Fullname is required
    2. Email must be valid format and not exist
    3. Password must be at least 8 characters
    """
    try:
        print(f"\n{'='*60}")
        print(f"📝 REGISTER USER - Email: {email}")
        print(f"{'='*60}")
        
        # 1. Validate inputs
        if not fullname or not fullname.strip():
            print("❌ Fullname is empty")
            return False, "Full name is required"
        
        if not email or not email.strip():
            print("❌ Email is empty")
            return False, "Email is required"
        
        # 2. Validate email format
        if "@" not in email:
            print("❌ Email format invalid (no @)")
            return False, "Email must contain @ symbol"
        
        if not validate_email(email):
            print("❌ Email format invalid")
            return False, "Invalid email format"
        
        # 3. Validate password length
        if not password or len(password) < 8:
            print(f"❌ Password too short: {len(password) if password else 0} chars")
            return False, "Password must be at least 8 characters"
        
        # 4. Check if email already exists
        existing_user = fetch_one(
            "SELECT user_id FROM USERS WHERE email = %s",
            (email.strip(),)
        )
        
        if existing_user:
            print(f"❌ Email already exists: {email}")
            return False, "Email already registered"
        
        print(f"✅ Email available: {email}")
        
        # 5. Hash password
        password_hash = hash_password(password)
        print(f"✅ Password hashed: {password_hash[:30]}...")
        
        # 6. Insert new user into database (✅ KHÔNG DÙNG TABLE ROLES)
        query = """
        INSERT INTO USERS (email, password, fullname, role_name, status, totalFineDebt, created_at)
        VALUES (%s, %s, %s, 'MEMBER', 'ACTIVE', 0, CURDATE())
        """
        
        execute(query, (
            email.strip(),
            password_hash,
            fullname.strip()
        ))
        
        print(f"✅ User created successfully!")
        print(f"   Email: {email}")
        print(f"{'='*60}\n")
        
        return True, "Registration successful! Please login."
        
    except Exception as e:
        print(f"\n❌ EXCEPTION: Error during registration: {e}")
        import traceback
        traceback.print_exc()
        print(f"{'='*60}\n")
        return False, f"Registration failed: {str(e)}"


def login_user(username, password):
    """
    Authenticate user with username and password
    
    Args:
        username: Username (email)
        password: Plain text password (will be hashed)
    
    Returns:
        tuple: (success: bool, message: str, user_data: dict or None)
    """
    try:
        print(f"\n{'='*60}")
        print(f"🔐 LOGIN ATTEMPT - Username: {username}")
        print(f"{'='*60}")
        
        # 1. Get user from database (✅ KHÔNG DÙNG TABLE ROLES)
        query = """
        SELECT 
            user_id, email, password, 
            fullname, phone, gender, address, 
            role_name, status, totalFineDebt, created_at
        FROM USERS
        WHERE email = %s
        """
        
        user = fetch_one(query, (username,))
        
        if not user:
            print(f"❌ User not found: {username}")
            print(f"{'='*60}\n")
            return False, "Email not found", None
        
        print(f"✅ User found: {username}")
        
        # 2. Check user status
        if user.get('status') != 'ACTIVE':
            print(f"❌ User is not active: {username} (Status: {user.get('status')})")
            print(f"{'='*60}\n")
            return False, "Your account has been temporarily locked. Please contact the administrator.", None
        
        print(f"✅ User is active")
        
        # 3. Hash the input password
        password_hash = hash_password(password)
        
        # 4. Compare with stored password
        stored_password = user.get('password')
        
        # Debug logging
        print(f"\n📝 Password Verification:")
        print(f"   Input password: '{password[:3]}***'")
        print(f"   Input hash: {password_hash[:30]}...")
        print(f"   Stored: {stored_password[:30]}...")
        
        # ✅ HỖ TRỢ CẢ PLAIN TEXT VÀ HASHED
        # Kiểm tra plain text trước (cho data mẫu)
        if stored_password == password:
            print(f"   ✅ Match: Plain text")
            print(f"\n✅ SUCCESS: Login successful!")
            print(f"   User ID: {user.get('user_id')}")
            print(f"{'='*60}\n")
        # Kiểm tra hash
        elif stored_password == password_hash:
            print(f"   ✅ Match: Hashed")
            print(f"\n✅ SUCCESS: Login successful!")
            print(f"   User ID: {user.get('user_id')}")
            print(f"{'='*60}\n")
        else:
            print(f"   ❌ Match: False (tried both plain and hash)")
            print(f"\n❌ FAILED: Password mismatch!")
            print(f"{'='*60}\n")
            return False, "Incorrect password", None
        
        # 5. Prepare user data (remove password)
        user_data = {
            'user_id': user.get('user_id'),
            'fullname': user.get('fullname'),
            'email': user.get('email'),
            'role_name': user.get('role_name', 'MEMBER'),
            'status': user.get('status'),
            'phone': user.get('phone'),
            'gender': user.get('gender'),
            'address': user.get('address'),
            'totalFineDebt': user.get('totalFineDebt', 0)
        }
        
        return True, "Login successful!", user_data
        
    except Exception as e:
        print(f"\n❌ EXCEPTION: Error during login: {e}")
        import traceback
        traceback.print_exc()
        print(f"{'='*60}\n")
        return False, "System error occurred", None


def logout_user():
    """
    Logout user (clear session)
    """
    print("👋 User logged out")
    return True


def verify_password(user_id, password):
    """
    Verify if password matches for a user
    Used for password change verification
    
    Args:
        user_id: User ID
        password: Plain text password
    
    Returns:
        True if password matches, False otherwise
    """
    try:
        user = fetch_one(
            "SELECT password FROM USERS WHERE user_id = %s",
            (user_id,)
        )
        
        if not user:
            return False
        
        password_hash = hash_password(password)
        return user['password'] == password_hash
        
    except Exception as e:
        print(f"❌ Error verifying password: {e}")
        return False


def check_email_exists(email):
    """
    Check if email already exists in database
    
    Args:
        email: Email address to check
    
    Returns:
        bool: True if exists, False otherwise
    """
    try:
        user = fetch_one(
            "SELECT user_id FROM USERS WHERE email = %s",
            (email,)
        )
        return user is not None
    except Exception as e:
        print(f"❌ Error checking email: {e}")
        return False


def check_username_exists(username):
    """
    Check if username already exists in database
    
    Args:
        username: Username to check
    
    Returns:
        bool: True if exists, False otherwise
    """
    try:
        user = fetch_one(
            "SELECT user_id FROM USERS WHERE username = %s",
            (username,)
        )
        return user is not None
    except Exception as e:
        print(f"❌ Error checking username: {e}")
        return False
>>>>>>> version-2

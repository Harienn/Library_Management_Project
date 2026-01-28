# utils/auth_helpers.py
"""
Authentication Helper Functions
✅ Check fines sau khi login/register
✅ Hiển thị fine notification nếu cần
"""


def check_and_show_fines_after_login(page, user_id):
    """
    Kiểm tra và hiển thị thông báo phạt sau khi login thành công
    
    Args:
        page: Flet page object
        user_id: ID của user vừa login
    
    Returns:
        bool: True nếu có phạt cần hiển thị, False nếu không
    """
    try:
        from services.borrow_service import get_member_fines
        from components.fine_notification_overlay import show_fine_notification
        
        print(f"🔍 Checking fines for user {user_id}...")
        
        # Lấy thông tin phạt
        fine_info = get_member_fines(user_id)
        total_unpaid = fine_info.get('total_unpaid_fines', 0)
        
        print(f"💰 Total unpaid fines: {total_unpaid:,.0f} VND")
        
        # Nếu có phạt chưa trả, hiển thị notification
        if total_unpaid > 0:
            print(f"⚠️ User has unpaid fines - showing notification")
            show_fine_notification(page, fine_info)
            return True
        else:
            print("✅ No unpaid fines")
            return False
            
    except Exception as e:
        print(f"❌ Error checking fines: {e}")
        import traceback
        traceback.print_exc()
        return False


def on_login_success(page, user):
    """
    Xử lý sau khi login thành công
    
    Args:
        page: Flet page object
        user: User dict
    
    Usage trong login view:
        from utils.auth_helpers import on_login_success
        
        # Sau khi authenticate thành công
        user = authenticate_user(username, password)
        if user:
            self.current_user = user
            on_login_success(self.page, user)
            self.navigate("/")
    """
    try:
        user_id = user.get('user_id')
        user_name = user.get('fullname', user.get('username', 'User'))
        
        print(f"✅ Login successful for user: {user_name} (ID: {user_id})")
        
        # Check và hiển thị fines nếu có
        check_and_show_fines_after_login(page, user_id)
        
    except Exception as e:
        print(f"❌ Error in on_login_success: {e}")


def on_register_success(page, user):
    """
    Xử lý sau khi register thành công
    
    Args:
        page: Flet page object  
        user: User dict
    
    Usage trong register view:
        from utils.auth_helpers import on_register_success
        
        # Sau khi create user thành công
        user = get_user_by_id(user_id)
        if user:
            self.current_user = user
            on_register_success(self.page, user)
            self.navigate("/")
    """
    try:
        user_id = user.get('user_id')
        user_name = user.get('fullname', user.get('username', 'User'))
        
        print(f"✅ Registration successful for user: {user_name} (ID: {user_id})")
        
        # Thông thường user mới sẽ không có fines
        # Nhưng vẫn check để chắc chắn
        check_and_show_fines_after_login(page, user_id)
        
    except Exception as e:
        print(f"❌ Error in on_register_success: {e}")
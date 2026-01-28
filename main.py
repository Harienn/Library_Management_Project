# main.py
import flet as ft

# Import views
from views.home_view import HomeView
from views.books_view import BooksView
from views.book_detail_view import BookDetailView
from views.login_view import LoginView
from views.register_view import RegisterView
from views.my_borrowing_view import MyBorrowingView
from views.my_profile_view import MyProfileView
from views.instruction_view import InstructionView
from views.fine_notification_view import FineNotificationView

# Import admin app
from views.admin.admin_app import AdminApp

# Auth & Authorization
from auth_service import login
from authz import can


class LibraryApp:
    def __init__(self, page: ft.Page):
        self.page = page
        self.page.title = "Library System"
        self.page.theme_mode = ft.ThemeMode.LIGHT
        self.page.padding = 0

        self.page.theme = ft.Theme(
            color_scheme=ft.ColorScheme(
                primary="#4BC1D2",
                on_surface_variant=ft.Colors.TRANSPARENT,
            ),
        )

        self.current_user = None
        self.selected_book = None

        self.page.on_route_change = self.route_change
        self.page.on_view_pop = self.view_pop

        self.navigate("/")

    # ================= ROUTING =================

    def route_change(self, e):
        route = self.page.route
        print(f"🚀 Navigating to: {route}")
        self.page.views.clear()

        # CHECK ADMIN ROUTES
        if route.startswith("/admin"):
            if not can(self.current_user, "dashboard"):
                self.show_access_denied()
                self.navigate("/login")
                return
            
            user_role = self.current_user.get("role_name", "GUEST")
            admin_app = AdminApp(self.page, user_role=user_role)
            admin_app.current_user = self.current_user
            admin_app.navigate(route)
            return

        # BOOK DETAIL
        if route == "/book_detail":
            selected_book = None
            if self.page.data and isinstance(self.page.data, dict):
                selected_book = self.page.data.get('selected_book')
            
            print(f"📚 Loading book detail for: {selected_book}")
            view_instance = BookDetailView(self.page, self.current_user, self.navigate, self.on_logout, selected_book)
            built_view = view_instance.build()
            self.page.views.append(built_view)
            self.page.update()
            print(f"✅ Book detail page rendered")
            return

        # USER ROUTES
        if route == "/":
            view = HomeView(self.page, self.current_user, self.navigate, self.on_logout)

        elif route == "/books":
            view = BooksView(self.page, self.current_user, self.navigate, self.on_logout)

        elif route == "/login":
            view = LoginView(self.page, self.on_login, self.navigate)

        elif route == "/register":
            # ✅ FIX: Thêm on_register_success callback
            view = RegisterView(self.page, self.navigate, self.on_register_success)

        elif route == "/my_borrowing":
            view = MyBorrowingView(self.page, self.current_user, self.navigate, self.on_logout)

        elif route == "/my_profile":
            view = MyProfileView(self.page, self.current_user, self.navigate, self.on_logout)

        elif route == "/instruction":
            view = InstructionView(self.page, self.current_user, self.navigate, self.on_logout)

        elif route == "/fine_notification":
            view = FineNotificationView(self.page, self.current_user, self.navigate, self.on_logout)

        else:
            view = HomeView(self.page, self.current_user, self.navigate, self.on_logout)

        self.page.views.append(view.build())
        self.page.update()

    def view_pop(self, e):
        self.page.views.pop()
        top_view = self.page.views[-1]
        self.navigate(top_view.route)

    def navigate(self, route):
        self.page.route = route
        self.route_change(None)

    # ================= LOGIN =================

    def on_login(self, email, password):
        user = login(email, password)
        if user:
            self.current_user = user
            
            # REDIRECT DỰA VÀO ROLE
            role = user.get("role_name", "MEMBER")
            if role in ["LIBRARIAN", "ADMIN"]:
                self.navigate("/admin")
            else:
                self.navigate("/")
        else:
            pass

    # ✅ THÊM: on_register_success callback
    def on_register_success(self, user):
        """Callback sau khi đăng ký thành công"""
        self.current_user = user
        print(f"✅ Registration successful for: {user.get('fullname')}")
<<<<<<< HEAD
=======
        
        # ✅ Check fines trong background (popup overlay)
        if user and user.get('user_id'):
            import threading
            threading.Thread(
                target=lambda: self.check_and_show_fines(user['user_id']),
                daemon=True
            ).start()
        
        # ✅ NAVIGATE VỀ HOME
        self.navigate("/")
>>>>>>> version-2

    # ================= LOGOUT =================
    
    def on_logout(self):
        """Xử lý đăng xuất"""
        self.current_user = None
        self.navigate("/")

    # ================= ACCESS DENIED =================
    
    def show_access_denied(self):
        """Hiển thị thông báo không đủ quyền"""
        def close_dialog(e):
            dialog.open = False
            self.page.update()
        
        dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Access Denied", color=ft.Colors.RED_600, weight=ft.FontWeight.BOLD),
            content=ft.Text(
                "You don't have permission to access this area. Please login with appropriate credentials.",
                size=14
            ),
            actions=[
                ft.TextButton("OK", on_click=close_dialog),
            ],
        )
        
        self.page.dialog = dialog
        dialog.open = True
        self.page.update()


def main(page: ft.Page):
    LibraryApp(page)


if __name__ == "__main__":
    ft.app(main)
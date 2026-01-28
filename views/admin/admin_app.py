# admin_app.py
import flet as ft
from views.admin.components.sidebar import Sidebar
from views.admin.components.topbar import Topbar
from views.admin.pages.dashboard import DashboardPage
from views.admin.pages.manage_books import ManageBooksPage
from views.admin.pages.manage_members import ManageMembersPage
from views.admin.pages.manage_librarians import ManageLibrariansPage
from views.admin.pages.borrow_return import BorrowReturnPage
from views.admin.pages.view_fines import ViewFinesPage
from views.admin.pages.reports import ReportsPage

# ✅ THÊM IMPORT
from authz import can


class AdminApp:
    def __init__(self, page, user_role="Librarian"):
        self.page = page
        self.page.title = "LibrarySystem - Admin"
        
        self.user_role = user_role
        self.current_user = {
            "email": f"{user_role.lower()}@rary.local",
            "role_name": user_role.upper(),
            "name": user_role
        }
        
        self.current_route = "/admin"
        self.on_logout = None  # ✅ SẼ ĐƯỢC GÁN TỪ MAIN.PY
    
    def handle_logout(self, e=None):
        """✅ Xử lý logout cho admin/librarian"""
        print(f"🚪 Logging out {self.user_role}...")
        
        # Gọi callback logout từ main app TRƯỚC (quan trọng!)
        if self.on_logout:
            self.on_logout()
        
        # Clear admin user
        self.current_user = None
        
        # Approach 1: Gọi route_change từ page
        # Clear views và navigate về home
        self.page.views.clear()
        self.page.route = "/"
        
        # Force trigger route change event
        if hasattr(self.page, 'on_route_change') and self.page.on_route_change:
            # Manually trigger route change
            class FakeEvent:
                pass
            self.page.on_route_change(FakeEvent())
        else:
            # Fallback: just update
            self.page.update()
        
    def navigate(self, route):
        # ✅ CHECK QUYỀN TRƯỚC KHI NAVIGATE
        if route == "/admin/librarians":
            if not can(self.current_user, "manage_librarians"):
                self.show_admin_required_dialog()
                return
        
        # Nếu yêu cầu admin (từ sidebar)
        if route == "__require_admin__":
            self.show_admin_required_dialog()
            return
        
        self.current_route = route
        self.page.views.clear()
        self.page.views.append(self.build_page())
        self.page.update()
    
    def show_admin_required_dialog(self):
        """Hiển thị popup yêu cầu đăng nhập admin"""
        def close_dialog(e):
            dialog.open = False
            self.page.update()
        
        dialog = ft.AlertDialog(
            modal=True,
            title=ft.Row([
                ft.Icon(ft.icons.LOCK_OUTLINED, color=ft.Colors.ORANGE_600, size=24),
                ft.Text("Admin Access Required", size=18, weight=ft.FontWeight.BOLD),
            ], spacing=12),
            content=ft.Column([
                ft.Text(
                    "This feature is only available for Admin users.",
                    size=14,
                    color="#6B7280",
                ),
                ft.Text(
                    f"You are currently logged in as: {self.user_role}",
                    size=13,
                    color="#9CA3AF",
                ),
                ft.Container(height=10),
                ft.Text(
                    "Please contact your administrator to upgrade your account.",
                    size=12,
                    color="#EF4444",
                    italic=True,
                ),
            ], tight=True, spacing=12),
            actions=[
                ft.TextButton("Close", on_click=close_dialog),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        
        self.page.dialog = dialog
        dialog.open = True
        self.page.update()
    
    def build_page(self):
        # ✅ TRUYỀN LOGOUT CALLBACK CHO SIDEBAR
        sidebar_obj = Sidebar(self.current_route, self.navigate, self.user_role)
        sidebar_obj.on_logout = self.handle_logout  # ✅ Gán logout handler
        sidebar_widget = sidebar_obj.build()
        
        topbar = Topbar(self.get_page_title(), self.current_user).build()
        content = self.get_page_content()
        
        return ft.View(
            route=self.current_route,
            controls=[
                ft.Row([
                    sidebar_widget,
                    ft.Container(
                        content=ft.Column([
                            topbar,
                            ft.Container(
                                content=ft.Column([content], scroll=ft.ScrollMode.AUTO),
                                padding=32,
                                expand=True,
                            ),
                        ], spacing=0),
                        expand=True,
                    ),
                ], spacing=0, expand=True)
            ],
            padding=0,
            spacing=0,
            bgcolor="#F5F7FB",
        )
    
    def get_page_content(self):
        if self.current_route == "/admin":
            return DashboardPage(self.navigate).build()
        elif self.current_route == "/admin/books":
            return ManageBooksPage().build()
        elif self.current_route == "/admin/members":
            return ManageMembersPage().build()
        elif self.current_route == "/admin/librarians":
            # ✅ DOUBLE CHECK (phòng trường hợp bypass)
            if not can(self.current_user, "manage_librarians"):
                return ft.Text("Access Denied", size=20, color=ft.Colors.RED_600)
            return ManageLibrariansPage().build()
        elif self.current_route == "/admin/borrow":
            return BorrowReturnPage().build()
        elif self.current_route == "/admin/fines":
            return ViewFinesPage().build()
        elif self.current_route == "/admin/reports":
            return ReportsPage().build()
        else:
            return ft.Text("Page not found", size=20)
    
    def get_page_title(self):
        titles = {
            "/admin": "Dashboard",
            "/admin/books": "Manage books",
            "/admin/members": "Manage members",
            "/admin/librarians": "Manage librarians",
            "/admin/borrow": "Borrow / Return",
            "/admin/fines": "Manage penalties",
            "/admin/reports": "View statistical report",
        }
        return titles.get(self.current_route, "Admin")
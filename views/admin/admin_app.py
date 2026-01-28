# views/admin/admin_app.py
import flet as ft
from components.sidebar import Sidebar
from components.topbar import Topbar
from pages.dashboard import DashboardPage
from pages.manage_books import ManageBooksPage
from pages.manage_members import ManageMembersPage
from pages.manage_librarians import ManageLibrariansPage
from pages.borrow_return import BorrowReturnPage
from pages.view_fines import ViewFinesPage
from pages.reports import ReportsPage

class AdminApp:
    def __init__(self, page, user_role="Librarian"):
        self.page = page
        self.page.title = "LibrarySystem - Admin"
        self.page.padding = 0
        self.page.spacing = 0
        self.page.bgcolor = "#F5F7FB"
        
        self.user_role = user_role
        self.current_user = {
            "email": f"{user_role.lower()}@rary.local",
            "role": user_role,
            "name": user_role
        }
        
        self.current_route = "/admin"
        
    def navigate(self, route):
        # Kiểm tra nếu yêu cầu admin
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
                ft.Icon(ft.icons.LOCK, color=ft.Colors.ORANGE_600, size=24),
                ft.Text("Admin Access Required", size=18, weight=ft.FontWeight.BOLD),
            ], spacing=12),
            content=ft.Column([
                ft.Text(
                    "This feature is only available for Admin users.",
                    size=14,
                    color="#6B7280",
                ),
                ft.Text(
                    "Please login with an Admin account to access Manage Librarians.",
                    size=13,
                    color="#9CA3AF",
                ),
                ft.Container(height=10),
                ft.TextField(
                    label="Admin email",
                    hint_text="admin@rary.local",
                    border_color=ft.Colors.GREY_400,
                ),
                ft.TextField(
                    label="Admin password",
                    password=True,
                    can_reveal_password=True,
                    border_color=ft.Colors.GREY_400,
                ),
            ], tight=True, spacing=12),
            actions=[
                ft.TextButton("Cancel", on_click=close_dialog),
                ft.ElevatedButton(
                    "Login as Admin",
                    bgcolor=ft.Colors.CYAN_400,
                    color=ft.Colors.WHITE,
                    on_click=lambda e: print("Login admin clicked"),
                ),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        
        self.page.dialog = dialog
        dialog.open = True
        self.page.update()
    
    def build_page(self):
        sidebar = Sidebar(self.current_route, self.navigate, self.user_role).build()
        topbar = Topbar(self.get_page_title(), self.current_user).build()
        content = self.get_page_content()
        
        return ft.View(
            route=self.current_route,
            controls=[
                ft.Row([
                    sidebar,
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

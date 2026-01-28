# views/my_borrowing_view.py
import flet as ft
from components.header import Header
from components.navbar import NavBar


class MyBorrowingView:
    def __init__(self, page, current_user, navigate):
        self.page = page
        self.current_user = current_user
        self.navigate = navigate
    
    def build(self):
        header = Header(self.page, self.current_user, self.navigate)
        navbar = NavBar(self.page, self.current_user, self.navigate, "/my_borrowing")
        
        if not self.current_user:
            content = self.build_guest_view()
        else:
            content = self.build_member_view()
        
        # GIỐNG BOOKS_VIEW - HEADER + NAVBAR CỐ ĐỊNH
        main_content = ft.Column([
            header.build(),
            navbar.build(),
            content,  # Chỉ content scroll
        ], spacing=0, expand=True)
        
        return ft.View(
            route="/my_borrowing",
            controls=[
                ft.Container(
                    content=main_content,
                    padding=0,
                    bgcolor=ft.Colors.GREY_50,
                    expand=True,
                )
            ],
        )
    
    def build_guest_view(self):
        """Guest view - card tự động co lại"""
        guest_card = ft.Container(
            content=ft.Column([
                ft.Text(
                    "This feature is for members only",
                    size=18,
                    weight=ft.FontWeight.BOLD,
                ),
                ft.Container(height=8),
                ft.Text(
                    "As a guest, you can search and view book information, but you cannot:",
                    size=13,
                    color=ft.Colors.GREY_700,
                ),
                ft.Container(height=12),
                ft.Text("• Borrow books or see your borrowing information.", size=13),
                ft.Text("• Request extension of borrowing period.", size=13),
                ft.Text("• View history and penalties (overdue, damaged, lost).", size=13),
                
                ft.Container(height=16),
                
                ft.Text(
                    "Please register or login to use My Borrowing.",
                    size=13,
                    color=ft.Colors.GREY_700,
                ),
                
                ft.Container(height=20),
                
                ft.Row([
                    ft.FilledButton(
                        "Create member account",
                        bgcolor=ft.Colors.CYAN_400,
                        color=ft.Colors.WHITE,
                        on_click=lambda _: self.navigate("/register"),
                        style=ft.ButtonStyle(
                            shape=ft.RoundedRectangleBorder(radius=8),
                            padding=ft.Padding(left=20, right=20, top=12, bottom=12),
                        ),
                    ),
                    ft.OutlinedButton(
                        "Login",
                        on_click=lambda _: self.navigate("/login"),
                        style=ft.ButtonStyle(
                            shape=ft.RoundedRectangleBorder(radius=8),
                            side=ft.BorderSide(1, ft.Colors.GREY_400),
                            padding=ft.Padding(left=20, right=20, top=12, bottom=12),
                        ),
                    ),
                ], spacing=12),
            ], spacing=0),
            padding=24,
            bgcolor=ft.Colors.WHITE,
            border_radius=10,
            border=ft.Border.all(1, ft.Colors.GREY_200),
            # BỎ width=550 - để tự động co lại theo nội dung
        )
        
        # SCROLLABLE CONTENT - GIỐNG BOOKS_VIEW
        scrollable_content = ft.Container(
            content=ft.Column([
                ft.Container(height=24),
                ft.Text(
                    "My borrowing",
                    size=26,
                    weight=ft.FontWeight.BOLD,
                ),
                ft.Container(height=4),
                ft.Text(
                    "You need a member account to view borrowing information and penalties.",
                    size=13,
                    color=ft.Colors.GREY_600,
                ),
                ft.Container(height=24),
                guest_card,  # Card sẽ tự co lại
                ft.Container(height=40),
            ], horizontal_alignment="start", scroll="auto"),
            padding=ft.Padding(left=40, right=40, top=0, bottom=0),
            expand=True,
        )
        
        return scrollable_content
    
    def build_member_view(self):
        """Member view cho user đã đăng nhập"""
        # TODO: Implement member view
        scrollable_content = ft.Container(
            content=ft.Column([
                ft.Container(height=24),
                ft.Text("My borrowing", size=26, weight=ft.FontWeight.BOLD),
                ft.Container(height=20),
                ft.Text("Welcome, " + self.current_user.get("name", "Member") + "!"),
                ft.Text("Your borrowing records will appear here."),
            ], scroll="auto"),
            padding=ft.Padding(left=40, right=40, top=0, bottom=40),
            expand=True,
        )
        return scrollable_content

# views/my_profile_view.py
import flet as ft
from components.header import Header
from components.navbar import NavBar


class MyProfileView:
    def __init__(self, page, current_user, navigate):
        self.page = page
        self.current_user = current_user
        self.navigate = navigate
    
    def build(self):
        header = Header(self.page, self.current_user, self.navigate)
        navbar = NavBar(self.page, self.current_user, self.navigate, "/my_profile")
        
        if not self.current_user:
            content = self.build_guest_view()
        else:
            content = self.build_member_view()
        
        # HEADER + NAVBAR CỐ ĐỊNH, CHỈ CONTENT SCROLL
        main_content = ft.Column([
            header.build(),
            navbar.build(),
            content,
        ], spacing=0, expand=True)
        
        return ft.View(
            route="/my_profile",
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
                    "Guest capabilities",
                    size=18,
                    weight=ft.FontWeight.BOLD,
                ),
                ft.Container(height=4),
                ft.Text(
                    "As a guest, you can:",
                    size=13,
                    color=ft.Colors.GREY_700,
                ),
                ft.Container(height=12),
                ft.Text("• Search and filter books in the library catalog.", size=13),
                ft.Text("• View detailed book information (cover, title, author, category, summary).", size=13),
                ft.Text("• Browse featured and latest books on the homepage.", size=13),
                
                ft.Container(height=20),
                
                ft.Text(
                    "Why create a member profile?",
                    size=18,
                    weight=ft.FontWeight.BOLD,
                ),
                ft.Container(height=4),
                ft.Text(
                    "After registering and completing your profile, you will be able to:",
                    size=13,
                    color=ft.Colors.GREY_700,
                ),
                ft.Container(height=12),
                ft.Text("• Borrow books and view your borrowing information online.", size=13),
                ft.Text("• Request borrowing extensions (extension of due date) when allowed.", size=13),
                ft.Text("• View history and all penalties (overdue, damaged, lost).", size=13),
                ft.Text("• Receive notifications and reminders from the library.", size=13),
                
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
                        "Login instead",
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
            # BỎ width=550 - để card tự co lại
        )
        
        # SCROLLABLE CONTENT
        scrollable_content = ft.Container(
            content=ft.Column([
                ft.Container(height=24),
                ft.Text(
                    "My profile",
                    size=26,
                    weight=ft.FontWeight.BOLD,
                ),
                ft.Container(height=4),
                ft.Text(
                    "You are currently using the system as a guest. To borrow books and manage your account, please register as a member.",
                    size=13,
                    color=ft.Colors.GREY_600,
                ),
                ft.Container(height=24),
                guest_card,
                ft.Container(height=40),
            ], horizontal_alignment="start", scroll="auto"),
            padding=ft.Padding(left=40, right=40, top=0, bottom=0),
            expand=True,
        )
        
        return scrollable_content
    
    def build_member_view(self):
        """Member view cho user đã đăng nhập"""
        # TODO: Implement member profile view
        scrollable_content = ft.Container(
            content=ft.Column([
                ft.Container(height=24),
                ft.Text("My profile", size=26, weight=ft.FontWeight.BOLD),
                ft.Container(height=20),
                ft.Text("Welcome, " + self.current_user.get("name", "Member") + "!"),
                ft.Text("Your profile information will appear here."),
            ], scroll="auto"),
            padding=ft.Padding(left=40, right=40, top=0, bottom=40),
            expand=True,
        )
        return scrollable_content

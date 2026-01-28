# views/my_profile_view.py
import flet as ft
from components.header import Header
from components.navbar import NavBar


class MyProfileView:
    def __init__(self, page, current_user, navigate, on_logout=None):
        self.page = page
        self.current_user = current_user
        self.navigate = navigate
        self.on_logout = on_logout

    def build(self):
        header = Header(self.page, self.current_user, self.navigate, self.on_logout)
        navbar = NavBar(self.page, self.current_user, self.navigate, "/my_profile")

        if not self.current_user:
            content = self.build_guest_view()
        else:
            content = self.build_member_view()

        main_content = ft.Column(
            [
                header.build(),
                navbar.build(),
                content,
            ],
            spacing=0,
            expand=True,
        )

        return ft.View(
            route="/my_profile",
            controls=[
                ft.Container(
                    content=main_content,
                    bgcolor=ft.Colors.GREY_50,
                    expand=True,
                )
            ],
        )

    # ================= GUEST VIEW =================

    def build_guest_view(self):
        guest_card = ft.Container(
            content=ft.Column(
                [
                    ft.Text("Guest capabilities", size=18, weight=ft.FontWeight.BOLD),
                    ft.Container(height=4),
                    ft.Text(
                        "As a guest, you can:",
                        size=13,
                        color=ft.Colors.GREY_700,
                    ),
                    ft.Container(height=12),
                    ft.Text("• Search and filter books in the library catalog.", size=13),
                    ft.Text(
                        "• View detailed book information (cover, title, author, category, summary).",
                        size=13,
                    ),
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
                    ft.Text(
                        "• Borrow books and view your borrowing information online.", size=13
                    ),
                    ft.Text(
                        "• Request borrowing extensions (extension of due date) when allowed.",
                        size=13,
                    ),
                    ft.Text(
                        "• View history and all penalties (overdue, damaged, lost).",
                        size=13,
                    ),
                    ft.Text(
                        "• Receive notifications and reminders from the library.", size=13
                    ),
                    ft.Container(height=20),
                    ft.Row(
                        [
                            ft.FilledButton(
                                "Create member account",
                                bgcolor=ft.Colors.CYAN_400,
                                color=ft.Colors.WHITE,
                                on_click=lambda _: self.navigate("/register"),
                                style=ft.ButtonStyle(
                                    shape=ft.RoundedRectangleBorder(radius=8),
                                    padding=ft.Padding(20, 12, 20, 12),
                                ),
                            ),
                            ft.OutlinedButton(
                                "Login instead",
                                on_click=lambda _: self.navigate("/login"),
                                style=ft.ButtonStyle(
                                    shape=ft.RoundedRectangleBorder(radius=8),
                                    side=ft.BorderSide(1, ft.Colors.GREY_400),
                                    padding=ft.Padding(20, 12, 20, 12),
                                ),
                            ),
                        ],
                        spacing=12,
                    ),
                ],
                spacing=0,
            ),
            padding=24,
            bgcolor=ft.Colors.WHITE,
            border_radius=10,
            border=ft.Border.all(1, ft.Colors.GREY_200),
        )

        return ft.Container(
            content=ft.Column(
                [
                    ft.Container(height=24),
                    ft.Text("My profile", size=26, weight=ft.FontWeight.BOLD),
                    ft.Container(height=4),
                    ft.Text(
                        "You are currently using the system as a guest. To borrow books and manage your account, please register as a member.",
                        size=13,
                        color=ft.Colors.GREY_600,
                    ),
                    ft.Container(height=24),
                    guest_card,
                    ft.Container(height=40),
                ],
                scroll="auto",
            ),
            padding=ft.Padding(left=40, right=40, top=0, bottom=0),
            expand=True,
        )

    # ================= MEMBER VIEW =================

    def build_member_view(self):
        user = self.current_user or {}

        member_id = user.get("user_id", "123")
        fullname = user.get("fullname", "Nguyen Van A")
        email = user.get("email", "member@example.com")
        phone = user.get("phone", "")
        gender = user.get("gender", "")
        address = user.get("address", "")

        personal_info = ft.Container(
            content=ft.Column(
                [
                    ft.Text("Personal information", size=18, weight=ft.FontWeight.BOLD),
                    ft.Container(height=12),
                    ft.Row(
                        [
                            ft.TextField(
                                label="Member ID",
                                value=str(member_id),
                                disabled=True,
                                expand=1,
                            ),
                            ft.TextField(
                                label="Card status",
                                value="Active",
                                disabled=True,
                                expand=1,
                            ),
                        ],
                        spacing=16,
                    ),
                    ft.TextField(label="Full name", value=fullname),
                    ft.TextField(label="Email address", value=email),
                    ft.Row(
                        [
                            ft.TextField(
                                label="Phone number", value=phone, expand=1
                            ),
                            ft.Dropdown(
                                label="Gender",
                                value=gender if gender else None,
                                options=[
                                    ft.dropdown.Option("Male"),
                                    ft.dropdown.Option("Female"),
                                    ft.dropdown.Option("Other"),
                                ],
                                expand=1,
                            ),
                        ],
                        spacing=16,
                    ),
                    ft.TextField(
                        label="Address", value=address, multiline=True
                    ),
                    ft.Container(height=16),
                    ft.FilledButton(
                        "Save changes",
                        bgcolor=ft.Colors.CYAN_400,
                        color=ft.Colors.WHITE,
                        style=ft.ButtonStyle(
                            shape=ft.RoundedRectangleBorder(radius=8),
                            padding=ft.Padding(20, 14, 20, 14),
                        ),
                        on_click=lambda e: None,  # TODO DB
                    ),
                    ft.Container(height=8),
                    ft.Text(
                        "New members must complete personal information before borrowing books.",
                        size=12,
                        color=ft.Colors.CYAN_700,
                    ),
                ],
                spacing=10,
            ),
            padding=24,
            bgcolor=ft.Colors.WHITE,
            border_radius=10,
            border=ft.Border.all(1, ft.Colors.GREY_200),
            expand=2,
        )

        change_password = ft.Container(
            content=ft.Column(
                [
                    ft.Text("Change password", size=18, weight=ft.FontWeight.BOLD),
                    ft.Container(height=12),
                    ft.TextField(
                        label="Current password",
                        password=True,
                        can_reveal_password=True,
                    ),
                    ft.TextField(
                        label="New password",
                        password=True,
                        can_reveal_password=True,
                    ),
                    ft.TextField(
                        label="Confirm new password",
                        password=True,
                        can_reveal_password=True,
                    ),
                    ft.Container(height=12),
                    ft.FilledButton(
                        "Update password",
                        bgcolor=ft.Colors.CYAN_400,
                        color=ft.Colors.WHITE,
                        style=ft.ButtonStyle(
                            shape=ft.RoundedRectangleBorder(radius=8),
                            padding=ft.Padding(20, 14, 20, 14),
                        ),
                        on_click=lambda e: None,  # TODO DB
                    ),
                    ft.Container(height=16),
                    ft.Text("Maximum books allowed: 10", size=13),
                    ft.Text("Standard borrowing period: 15 days", size=13),
                    ft.Text("Current outstanding fines: 410,000 VND", size=13),
                    ft.Text(
                        "Borrowing status: Blocked when fines exceed limit or books are overdue.",
                        size=13,
                        color=ft.Colors.RED_400,
                    ),
                ],
                spacing=10,
            ),
            padding=24,
            bgcolor=ft.Colors.WHITE,
            border_radius=10,
            border=ft.Border.all(1, ft.Colors.GREY_200),
            expand=1,
        )

        return ft.Container(
            content=ft.Column(
                [
                    ft.Container(height=24),
                    ft.Text("My profile", size=26, weight=ft.FontWeight.BOLD),
                    ft.Container(height=24),
                    ft.Row(
                        [
                            personal_info,
                            change_password,
                        ],
                        spacing=24,
                    ),
                    ft.Container(height=40),
                ],
                scroll="auto",
            ),
            padding=ft.Padding(left=40, right=40, top=0, bottom=0),
            expand=True,
        )
# components/header.py
import flet as ft


class Header:
    def __init__(self, page, current_user, navigate, on_logout=None):
        self.page = page
        self.current_user = current_user
        self.navigate = navigate
        self.on_logout = on_logout

    def build(self):
        # ================= SEARCH =================
        search_container = ft.Container(
            content=ft.Row(
                [
                    ft.TextField(
                        hint_text="Search in the library...",
                        border="none",
                        expand=True,
                        height=50,
                        text_size=15,
                        content_padding=ft.Padding(left=25, right=10, top=0, bottom=0),
                    ),
                    ft.FilledButton(
                        "Search",
                        bgcolor=ft.Colors.CYAN_400,
                        color=ft.Colors.WHITE,
                        height=50,
                        style=ft.ButtonStyle(
                            shape=ft.RoundedRectangleBorder(
                                radius=ft.BorderRadius(
                                    top_left=0,
                                    top_right=25,
                                    bottom_left=0,
                                    bottom_right=25,
                                )
                            ),
                            padding=ft.Padding(left=30, right=30, top=0, bottom=0),
                        ),
                    ),
                ],
                spacing=0,
            ),
            border_radius=25,
            bgcolor=ft.Colors.WHITE,
            border=ft.Border.all(1, ft.Colors.GREY_300),
            height=50,
            expand=True,
        )

        # ================= AUTH =================
        if self.current_user:
            name = self.current_user.get("fullname", "Member")
            avatar_char = name[0].upper()

            # ✅ FIX: Tạo hàm riêng thay vì lambda
            def handle_logout(e):
                if self.on_logout:
                    self.on_logout()
            
            def go_to_profile(e):
                self.navigate("/my_profile")
            
            def go_to_borrowing(e):
                self.navigate("/my_borrowing")

            auth_section = ft.PopupMenuButton(
                content=ft.Row(
                    [
                        ft.Text(name, size=14),
                        ft.CircleAvatar(
                            content=ft.Text(avatar_char),
                            bgcolor=ft.Colors.BLUE_400,
                            radius=18,
                        ),
                    ],
                    spacing=10,
                ),
                items=[
                    ft.PopupMenuItem(
                        content=ft.Text("My Profile"),
                        on_click=go_to_profile,
                    ),
                    ft.PopupMenuItem(
                        content=ft.Text("My Borrowing"),
                        on_click=go_to_borrowing,
                    ),
                    ft.PopupMenuItem(
                        content=ft.Text("Logout"),
                        on_click=handle_logout,
                    ),
                ],
            )
        else:
            def go_to_login(e):
                self.navigate("/login")
            
            def go_to_register(e):
                self.navigate("/register")
            
            auth_section = ft.Row(
                [
                    ft.TextButton(
                        "Login",
                        on_click=go_to_login,
                    ),
                    ft.OutlinedButton(
                        "Register",
                        on_click=go_to_register,
                        style=ft.ButtonStyle(
                            shape=ft.RoundedRectangleBorder(radius=20),
                            side=ft.BorderSide(1.5, ft.Colors.CYAN_400),
                        ),
                    ),
                ],
                spacing=10,
            )

        # ================= HEADER =================
        return ft.Container(
            content=ft.Row(
                [
                    ft.Row(
                        [
                            ft.Text("Library", size=24, weight=ft.FontWeight.BOLD),
                            ft.Text(
                                "System",
                                size=24,
                                weight=ft.FontWeight.BOLD,
                                color=ft.Colors.CYAN_400,
                            ),
                        ],
                        spacing=0,
                    ),
                    search_container,
                    auth_section,
                ],
                alignment="spaceBetween",
                vertical_alignment="center",
            ),
            padding=ft.Padding(left=40, right=40, top=15, bottom=15),
            bgcolor=ft.Colors.WHITE,
            border=ft.Border(bottom=ft.BorderSide(1, ft.Colors.GREY_300)),
        )
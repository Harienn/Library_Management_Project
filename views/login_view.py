import flet as ft
from auth_service import login_user


class LoginView:
    def __init__(self, page, on_login, navigate):
        self.page = page
        self.on_login = on_login
        self.navigate = navigate
    
    def build(self):
        # ✅ ERROR MESSAGE
        error_message = ft.Text(
            "",
            size=13,
            color=ft.Colors.RED_600,
            visible=False,
            text_align=ft.TextAlign.CENTER,
            width=400,
        )
        
        def show_error(message):
            """Hiển thị lỗi"""
            error_message.value = message
            error_message.visible = True
            self.page.update()
        
        def hide_error():
            """Ẩn lỗi"""
            error_message.visible = False
            self.page.update()
        
        # INPUT FIELDS
        email_field = ft.TextField(
            hint_text="Enter email",
            hint_style=ft.TextStyle(color="#c0c0c0"),
            border_radius=8,
            border_color=ft.Colors.GREY_300,
            height=50,
            text_size=14,
            content_padding=ft.Padding(left=16, right=16, top=14, bottom=14),
            width=400,
        )
        
        # ✅ PASSWORD FIELD với TEXT TOGGLE
        password_field = ft.TextField(
            hint_text="Enter password",
            hint_style=ft.TextStyle(color="#c0c0c0"),
            password=True,
            border_radius=8,
            border_color=ft.Colors.GREY_300,
            height=50,
            text_size=14,
            content_padding=ft.Padding(left=16, right=70, top=14, bottom=14),
            width=400,
        )
        
        # Text button thay cho icon
        password_toggle_btn = ft.TextButton(
            content=ft.Text("Show", size=13, weight=ft.FontWeight.W_500),
            style=ft.ButtonStyle(
                color={"": ft.Colors.CYAN_400},
                padding=ft.padding.all(0),
            ),
            on_click=None,
        )
        
        def toggle_password_visibility(e):
            """Toggle hiển thị/ẩn password"""
            if password_field.password:
                password_field.password = False
                password_toggle_btn.content = ft.Text("Hide", size=13, weight=ft.FontWeight.W_500)
            else:
                password_field.password = True
                password_toggle_btn.content = ft.Text("Show", size=13, weight=ft.FontWeight.W_500)
            self.page.update()
        
        password_toggle_btn.on_click = toggle_password_visibility
        
        # Stack password field với toggle button
        password_container = ft.Stack(
            [
                password_field,
                ft.Container(
                    content=password_toggle_btn,
                    right=10,
                    top=10,
                ),
            ],
            height=50,
            width=400,
        )
        
        # ✅ HANDLE LOGIN với AUTH SERVICE
        def handle_login(e):
            hide_error()
            
            email = email_field.value
            password = password_field.value
            
            # Validate input
            if not email or not password:
                show_error("Please enter both email and password")
                return
            
            # ✅ GỌI AUTH SERVICE
            success, message, user_data = login_user(email, password)
            
            if success:
                # ✅ Login thành công
                self.on_login(user_data)
            else:
                # ❌ Hiển thị lỗi
                show_error(message)  # "Incorrect password" hoặc "Email not found"
        
        # LABELS
        email_label = ft.Text(
            "Email address",
            size=13,
            weight=ft.FontWeight.W_500,
            color=ft.Colors.GREY_800,
        )
        
        password_label = ft.Text(
            "Password",
            size=13,
            weight=ft.FontWeight.W_500,
            color=ft.Colors.GREY_800,
        )
        
        # LOGIN BUTTON
        login_btn = ft.Button(
            content=ft.Text("Login", color=ft.Colors.WHITE),
            width=400,
            height=48,
            style=ft.ButtonStyle(
                bgcolor={"": "#4BC1D2"},
                shape=ft.RoundedRectangleBorder(radius=24),
            ),
            on_click=handle_login,  # ✅ Dùng handle_login mới
        )
        
        # LOGO
        logo = ft.Row(
            spacing=0,
            alignment=ft.MainAxisAlignment.CENTER,
            controls=[
                ft.Text("Library", size=22, weight=ft.FontWeight.BOLD, color=ft.Colors.BLACK),
                ft.Text("System", size=22, weight=ft.FontWeight.BOLD, color="#4BC1D2"),
            ],
        )
        
        # TITLE
        title = ft.Text(
            "Sign in",
            size=20,
            weight=ft.FontWeight.BOLD,
            color=ft.Colors.BLACK,
        )
        
        # REGISTER LINK
        register_row = ft.Row(
            spacing=4,
            alignment=ft.MainAxisAlignment.CENTER,
            controls=[
                ft.Text("New to this library?", size=13, color=ft.Colors.GREY_700),
                ft.TextButton(
                    content=ft.Text("Create a new member account", color="#4BC1D2"),
                    style=ft.ButtonStyle(padding=0),
                    on_click=lambda e: self.navigate("/register"),
                ),
            ],
        )
        
        # BACK TO HOMEPAGE
        back_btn = ft.TextButton(
            content=ft.Text("Back to homepage", color="#4BC1D2"),
            style=ft.ButtonStyle(padding=0),
            on_click=lambda e: self.navigate("/"),
        )
        
        # LOGIN CARD
        login_card = ft.Container(
            width=450,
            bgcolor=ft.Colors.WHITE,
            border_radius=12,
            padding=40,
            shadow=ft.BoxShadow(
                spread_radius=1,
                blur_radius=15,
                color=ft.Colors.with_opacity(0.1, ft.Colors.BLACK),
            ),
            content=ft.Column(
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=12,
                tight=True,
                controls=[
                    logo,
                    ft.Container(height=2),
                    title,
                    ft.Container(height=6),
                    
                    # ✅ ERROR MESSAGE
                    error_message,
                    
                    # EMAIL
                    ft.Column(
                        spacing=6,
                        horizontal_alignment=ft.CrossAxisAlignment.START,
                        controls=[
                            email_label,
                            email_field,
                        ],
                    ),
                    
                    # PASSWORD với TEXT BUTTON
                    ft.Column(
                        spacing=6,
                        horizontal_alignment=ft.CrossAxisAlignment.START,
                        controls=[
                            password_label,
                            password_container,
                        ],
                    ),
                    
                    ft.Container(height=2),
                    login_btn,
                    ft.Container(height=6),
                    
                    register_row,
                    back_btn,
                ],
            ),
        )
        
        # RETURN FULL VIEW
        return ft.Stack(
            controls=[
                ft.Container(
                    content=login_card,
                    alignment=ft.alignment.Alignment(0, 0),
                    bgcolor="#E8E8E8",
                    expand=True,
                )
            ],
        )
import flet as ft


class LoginView:
    def __init__(self, page, on_login, navigate):
        self.page = page
        self.on_login = on_login
        self.navigate = navigate
    
    def build(self):
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
        
        password_field = ft.TextField(
            hint_text="Enter password",
            hint_style=ft.TextStyle(color="#c0c0c0"),
            password=True,
            can_reveal_password=True,
            border_radius=8,
            border_color=ft.Colors.GREY_300,
            height=50,
            text_size=14,
            content_padding=ft.Padding(left=16, right=16, top=14, bottom=14),
            width=400,
        )
        
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
            on_click=lambda e: self.on_login(
                email_field.value, 
                password_field.value
            ),
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
        
        # FORGOT PASSWORD
        forgot_link = ft.TextButton(
            content=ft.Text("Forgot password?", color="#4BC1D2"),
            style=ft.ButtonStyle(padding=0),
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
        
        # LOGIN CARD - KHÔNG CHO SELECT TEXT
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
            # TẮT USER SELECT
            data={"user-select": "none"},
            content=ft.Column(
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=12,
                tight=True,
                controls=[
                    logo,
                    ft.Container(height=2),
                    title,
                    ft.Container(height=6),
                    
                    # EMAIL
                    ft.Column(
                        spacing=6,
                        horizontal_alignment=ft.CrossAxisAlignment.START,
                        controls=[
                            email_label,
                            email_field,
                        ],
                    ),
                    
                    # PASSWORD
                    ft.Column(
                        spacing=6,
                        horizontal_alignment=ft.CrossAxisAlignment.START,
                        controls=[
                            password_label,
                            password_field,
                        ],
                    ),
                    
                    # FORGOT PASSWORD
                    ft.Container(
                        content=forgot_link,
                        alignment=ft.alignment.Alignment(1, 0),
                        width=400,
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

# views/register_view.py
import flet as ft
from auth_service import register  # ✅ IMPORT HÀM REGISTER


class RegisterView:
    def __init__(self, page, navigate, on_register_success):
        self.page = page
        self.navigate = navigate
        self.on_register_success = on_register_success  # ✅ CALLBACK ĐỂ SET current_user
    
    def build(self):
        # ✅ THÊM ERROR MESSAGE
        error_text = ft.Text(
            "",
            size=13,
            color=ft.Colors.RED_600,
            visible=False,
            text_align=ft.TextAlign.CENTER,
        )
        
        # Form fields
        full_name_field = ft.TextField(
            hint_text="Enter full name",
            border_radius=8,
            border_color=ft.Colors.GREY_300,
            height=50,
            text_size=14,
            content_padding=ft.Padding(left=16, right=16, top=0, bottom=0),
            expand=True,
        )
        
        email_field = ft.TextField(
            hint_text="Enter email",
            border_radius=8,
            border_color=ft.Colors.GREY_300,
            height=50,
            text_size=14,
            content_padding=ft.Padding(left=16, right=16, top=0, bottom=0),
            expand=True,
        )
        
        password_field = ft.TextField(
            hint_text="Enter password",
            password=True,
            can_reveal_password=True,
            border_radius=8,
            border_color=ft.Colors.GREY_300,
            height=50,
            text_size=14,
            content_padding=ft.Padding(left=16, right=16, top=0, bottom=0),
        )
        
        confirm_password_field = ft.TextField(
            hint_text="Re-enter password",
            password=True,
            can_reveal_password=True,
            border_radius=8,
            border_color=ft.Colors.GREY_300,
            height=50,
            text_size=14,
            content_padding=ft.Padding(left=16, right=16, top=0, bottom=0),
        )
        
        def show_error(message):
            """Hiển thị thông báo lỗi"""
            error_text.value = message
            error_text.visible = True
            self.page.update()
        
        def hide_error():
            """Ẩn thông báo lỗi"""
            error_text.visible = False
            self.page.update()
        
        def handle_register(e):
            hide_error()
            
            # ✅ VALIDATE FORM
            if not full_name_field.value:
                show_error("Please enter your full name")
                return
            
            if not email_field.value:
                show_error("Please enter your email")
                return
            
            if not password_field.value:
                show_error("Please enter password")
                return
            
            if not confirm_password_field.value:
                show_error("Please confirm your password")
                return
            
            if password_field.value != confirm_password_field.value:
                show_error("Passwords do not match")
                return
            
            if len(password_field.value) < 6:
                show_error("Password must be at least 6 characters")
                return
            
            # ✅ GỌI HÀM REGISTER
            result = register(
                full_name_field.value,
                email_field.value,
                password_field.value
            )
            
            # ✅ XỬ LÝ KẾT QUẢ
            if result and "error" not in result:
                # Đăng ký thành công -> tự động đăng nhập
                self.on_register_success(result)  # Set current_user
                self.navigate("/")  # Chuyển về trang chủ
            elif result and "error" in result:
                # Có lỗi
                show_error(result["error"])
            else:
                show_error("Registration failed. Please try again.")
        
        # === CARD REGISTER ===
        register_card = ft.Container(
            content=ft.Column([
                # Logo
                ft.Row([
                    ft.Text("Library", size=24, weight=ft.FontWeight.BOLD, color=ft.Colors.BLACK_87),
                    ft.Text("System", size=24, weight=ft.FontWeight.BOLD, color=ft.Colors.CYAN_400),
                ], alignment="center", spacing=0),
                
                ft.Container(height=8),
                
                # Title
                ft.Text("Create member account", size=22, weight=ft.FontWeight.BOLD, text_align="center"),
                
                ft.Container(height=16),
                
                # ✅ ERROR MESSAGE
                error_text,
                ft.Container(height=8),
                
                # Full Name
                ft.Row([
                    ft.Column([
                        ft.Text("Full name", size=14, color=ft.Colors.BLACK_87),
                        ft.Container(height=4),
                        full_name_field,
                    ], spacing=0, alignment="start", expand=True),
                ]),
                
                ft.Container(height=10),
                
                # Email
                ft.Row([
                    ft.Column([
                        ft.Text("Email address", size=14, color=ft.Colors.BLACK_87),
                        ft.Container(height=4),
                        email_field,
                    ], spacing=0, alignment="start", expand=True),
                ]),
                
                ft.Container(height=10),
                
                # Password + Confirm Password
                ft.Row([
                    # Password
                    ft.Container(
                        content=ft.Column([
                            ft.Text("Password", size=14, color=ft.Colors.BLACK_87),
                            ft.Container(height=4),
                            password_field,
                        ], spacing=0, alignment="start"),
                        expand=1,
                    ),
                    
                    ft.Container(width=12),
                    
                    # Confirm Password
                    ft.Container(
                        content=ft.Column([
                            ft.Text("Confirm password", size=14, color=ft.Colors.BLACK_87),
                            ft.Container(height=4),
                            confirm_password_field,
                        ], spacing=0, alignment="start"),
                        expand=1,
                    ),
                ]),
                
                ft.Container(height=16),
                
                # Register button
                ft.FilledButton(
                    "Register",
                    width=float('inf'),
                    height=48,
                    bgcolor=ft.Colors.CYAN_400,
                    color=ft.Colors.WHITE,
                    on_click=handle_register,
                    style=ft.ButtonStyle(
                        shape=ft.RoundedRectangleBorder(radius=24),
                    ),
                ),
                
                ft.Container(height=16),
                
                # DIVIDER
                ft.Divider(height=1, color=ft.Colors.GREY_300),
                
                ft.Container(height=12),
                
                # Already have account
                ft.Row([
                    ft.Text("Already have an account? ", size=14, color=ft.Colors.BLACK_87),
                    ft.TextButton(
                        "Sign in",
                        on_click=lambda _: self.navigate("/login"),
                        style=ft.ButtonStyle(
                            color=ft.Colors.CYAN_400,
                            padding=0,
                        ),
                    ),
                ], alignment="center", spacing=0),
                
                ft.Container(height=4),
                
                # Back to homepage
                ft.TextButton(
                    "Back to homepage",
                    on_click=lambda _: self.navigate("/"),
                    style=ft.ButtonStyle(
                        color=ft.Colors.CYAN_400,
                        padding=0,
                    ),
                ),
                
            ], horizontal_alignment="center", spacing=0, tight=True),
            width=550,
            padding=32,
            bgcolor=ft.Colors.WHITE,
            border_radius=16,
            shadow=ft.BoxShadow(
                blur_radius=20,
                color=ft.Colors.with_opacity(0.2, ft.Colors.BLACK),
            ),
        )
        
        # === NỀN XÁM ===
        return ft.View(
            route="/register",
            controls=[
                ft.Container(
                    content=ft.Container(
                        content=register_card,
                        padding=20,
                    ),
                    alignment=ft.alignment.Alignment(0, 0),
                    bgcolor="#E8E8E8",
                    expand=True,
                )
            ],
            padding=0,
            bgcolor="#E8E8E8",
        )
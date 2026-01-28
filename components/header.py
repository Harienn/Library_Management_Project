# components/header.py
import flet as ft


class Header:
    def __init__(self, page, current_user, navigate, on_logout=None):
        self.page = page
        self.current_user = current_user
        self.navigate = navigate
        self.on_logout = on_logout
    
    def build(self):
        # Search section - PILL SHAPE HOÀN HẢO
        search_container = ft.Container(
            content=ft.Row([
                # TextField - KHÔNG BO GÓC PHẢI
                ft.TextField(
                    hint_text="Search in the library...",
                    border="none",  # Bỏ border riêng
                    filled=False,
                    expand=True,
                    height=50,
                    text_size=15,
                    content_padding=ft.Padding(left=25, right=10, top=0, bottom=0),
                ),
                
                # Button - CHỈ BO GÓC PHẢI (nửa viên thuốc)
                ft.FilledButton(
                    content=ft.Text("Search", size=17, weight=ft.FontWeight.W_500),
                    bgcolor=ft.Colors.CYAN_400,
                    color=ft.Colors.WHITE,
                    height=50,
                    style=ft.ButtonStyle(
                        shape=ft.RoundedRectangleBorder(
                            radius=ft.BorderRadius(
                                top_left=0,      # Góc trên trái: VUÔNG
                                top_right=25,    # Góc trên phải: TRÒN
                                bottom_left=0,   # Góc dưới trái: VUÔNG
                                bottom_right=25, # Góc dưới phải: TRÒN
                            )
                        ),
                        padding=ft.Padding(left=30, right=30, top=0, bottom=0),
                    ),
                ),
            ], spacing=0, vertical_alignment="center"),  # spacing=0 để SÁT NHAU
            
            # Container ngoài - BO TRÒN HOÀN TOÀN
            border_radius=25,
            bgcolor=ft.Colors.WHITE,
            border=ft.Border.all(1, ft.Colors.GREY_300),
            height=50,
            expand=True,
        )
        
        # Auth section
        if self.current_user:
            auth_section = ft.PopupMenuButton(
                content=ft.Row([
                    ft.Text(self.current_user.get("name", "Member"), size=14),
                    ft.CircleAvatar(
                        content=ft.Text(
                            self.current_user.get("name", "M")[0].upper(),
                            color=ft.Colors.WHITE,
                        ),
                        bgcolor=ft.Colors.BLUE_400,
                        radius=18,
                    ),
                ], spacing=10),
                items=[
                    ft.PopupMenuItem(text="My Profile", on_click=lambda _: self.navigate("/my_profile")),
                    ft.PopupMenuItem(text="Logout", on_click=self.handle_logout),
                ],
            )
        else:
            auth_section = ft.Row([
                ft.TextButton(
                    content=ft.Text("Login", size=15, color=ft.Colors.BLACK_87),
                    on_click=lambda _: self.navigate("/login"),
                    style=ft.ButtonStyle(overlay_color=ft.Colors.GREY_100),
                ),
                
                ft.OutlinedButton(
                    content=ft.Text("Register", size=15, color=ft.Colors.CYAN_400),
                    on_click=lambda _: self.navigate("/register"),
                    style=ft.ButtonStyle(
                        shape=ft.RoundedRectangleBorder(radius=20),
                        side=ft.BorderSide(1.5, ft.Colors.CYAN_400),
                        bgcolor=ft.Colors.WHITE,
                        overlay_color=ft.Colors.CYAN_50,
                    ),
                ),
            ], spacing=10)
        
        return ft.Container(
            content=ft.Row([
                # Logo
                ft.Row([
                    ft.Text("Library", size=24, weight=ft.FontWeight.BOLD, color=ft.Colors.BLACK_87),
                    ft.Text("System", size=24, weight=ft.FontWeight.BOLD, color=ft.Colors.CYAN_400),
                ], spacing=0),
                
                ft.Container(width=40),
                
                # Search section
                search_container,
                
                ft.Container(width=40),
                
                # Auth section
                auth_section,
            ], alignment="spaceBetween", vertical_alignment="center"),
            padding=ft.Padding(left=40, right=40, top=15, bottom=15),
            bgcolor=ft.Colors.WHITE,
            border=ft.Border( 
                bottom=ft.BorderSide(1, ft.Colors.GREY_300)),
        )
    
    def handle_logout(self, e):
        if self.on_logout:
            self.on_logout()
        self.navigate("/")

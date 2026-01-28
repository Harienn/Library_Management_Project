# components/navbar.py
import flet as ft


class NavBar:
    def __init__(self, page, current_user, navigate, current_route):
        self.page = page
        self.current_user = current_user
        self.navigate = navigate
        self.current_route = current_route  # Route hiện tại
    
    def build(self):
        # Danh sách menu items
        menu_items = [
            {"route": "/", "label": "Home"},
            {"route": "/books", "label": "Books"},
            {"route": "/my_borrowing", "label": "My Borrowing"},
            {"route": "/my_profile", "label": "My Profile"},
            {"route": "/instruction", "label": "Instruction"},
        ]
        
        # Tạo các nút menu
        nav_buttons = []
        for item in menu_items:
            is_active = self.current_route == item["route"]  # Kiểm tra active
            
            nav_buttons.append(
                ft.TextButton(
                    content=ft.Text(
                        item["label"],
                        size=15,
                        weight=ft.FontWeight.BOLD if is_active else ft.FontWeight.NORMAL,  # Bold nếu active
                        color=ft.Colors.CYAN_400 if is_active else ft.Colors.BLACK_87,  # Cyan nếu active
                    ),
                    on_click=lambda _, r=item["route"]: self.navigate(r),
                    style=ft.ButtonStyle(
                        overlay_color=ft.Colors.CYAN_50,  # Hover effect
                    ),
                )
            )
        
        return ft.Container(
            content=ft.Row(
                nav_buttons,
                spacing=5,
            ),
            padding=ft.Padding(left=40, right=40, top=10, bottom=10),
            bgcolor=ft.Colors.WHITE,
        )

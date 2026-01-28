# components/navbar.py
import flet as ft


class NavBar:
    def __init__(self, page, current_user, navigate, current_route):
        self.page = page
        self.current_user = current_user
        self.navigate = navigate
        self.current_route = current_route
    
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
            is_active = self.current_route == item["route"]
            
            # ✅ FIX: Tạo closure đúng cách
            def make_handler(route):
                def handler(e):
                    self.navigate(route)
                return handler
            
            nav_buttons.append(
                ft.TextButton(
                    content=ft.Text(
                        item["label"],
                        size=15,
                        weight=ft.FontWeight.BOLD if is_active else ft.FontWeight.NORMAL,
                        color=ft.Colors.CYAN_400 if is_active else ft.Colors.BLACK_87,
                    ),
                    on_click=make_handler(item["route"]),
                    style=ft.ButtonStyle(
                        overlay_color=ft.Colors.CYAN_50,
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
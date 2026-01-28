# views/admin/components/topbar.py
import flet as ft

class Topbar:
    def __init__(self, title, user_info):
        self.title = title
        self.user_info = user_info
    
    def build(self):
        return ft.Container(
            content=ft.Row([
                ft.Column([
                    ft.Text(self.title, size=22, weight=ft.FontWeight.BOLD, color="#1F2937"),
                    ft.Text("Today's borrowing, returns and fines handled at the circulation desk.", size=13, color="#6B7280"),
                ], spacing=4),
                ft.Container(expand=True),
                ft.Row([
                    ft.Text("Librarian", size=12, color="#6B7280"),
                    ft.Container(
                        content=ft.Text("L", size=16, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
                        width=36,
                        height=36,
                        bgcolor=ft.Colors.CYAN_400,
                        border_radius=18,
                        alignment=ft.Alignment(0, 0),
                    ),
                ], spacing=12),
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            padding=ft.Padding(32, 20, 32, 20),
            bgcolor=ft.Colors.WHITE,
            border=ft.Border(bottom=ft.BorderSide(1, "#E5E7EB")),
        )

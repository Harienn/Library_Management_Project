# views/admin/components/topbar.py
import flet as ft

class Topbar:
    def __init__(self, title, user_info):
        self.title = title
        self.user_info = user_info
    
    def build(self):
        # LẤY THÔNG TIN USER
        user_name = self.user_info.get("name", "User")
        user_role = self.user_info.get("role_name", "GUEST")
        
        # LẤY CHỮ CÁI ĐẦU CỦA TÊN
        initial = user_name[0].upper() if user_name else "U"
        
        # MÀU AVATAR DỰA VÀO ROLE
        avatar_color = ft.Colors.CYAN_400 if user_role == "ADMIN" else ft.Colors.BLUE_400
        
        return ft.Container(
            content=ft.Row([
                ft.Column([
                    ft.Text(self.title, size=22, weight=ft.FontWeight.BOLD, color="#1F2937"),
                    ft.Text("Today's borrowing, returns and fines handled at the circulation desk.", size=13, color="#6B7280"),
                ], spacing=4),
                ft.Container(expand=True),
                ft.Row([
                    # HIỂN THỊ TÊN USER VÀ ROLE
                    ft.Column([
                        ft.Text(user_name, size=13, weight=ft.FontWeight.W_500, color="#1F2937", text_align=ft.TextAlign.RIGHT),
                        ft.Text(user_role.capitalize(), size=11, color="#6B7280", text_align=ft.TextAlign.RIGHT),
                    ], spacing=2, horizontal_alignment=ft.CrossAxisAlignment.END),
                    ft.Container(
                        content=ft.Text(initial, size=16, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
                        width=40,
                        height=40,
                        bgcolor=avatar_color,
                        border_radius=20,
                        alignment=ft.Alignment(0, 0),
                    ),
                ], spacing=12),
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            padding=ft.Padding(32, 20, 32, 20),
            bgcolor=ft.Colors.WHITE,
            border=ft.Border(bottom=ft.BorderSide(1, "#E5E7EB")),
        )
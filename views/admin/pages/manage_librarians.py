# views/admin/pages/manage_librarians.py
import flet as ft

class ManageLibrariansPage:
    def build(self):
        return ft.Column([
            ft.Text("View, add, update and delete librarians in the system.", size=13, color="#6B7280"),
            ft.ElevatedButton("+ Add new librarian", bgcolor=ft.Colors.CYAN_400, color=ft.Colors.WHITE),
            ft.Container(
                content=ft.Text("👨‍💼 Librarian list will be here...", size=14, color="#9CA3AF"),
                padding=40,
                bgcolor=ft.Colors.WHITE,
                border_radius=8,
                border=ft.Border.all(1, "#E5E7EB"),
            ),
        ], spacing=16)

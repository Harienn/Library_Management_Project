# views/admin/main.py
import flet as ft
from views.admin.admin_app import AdminApp

def main(page: ft.Page):
    # Mặc định Librarian - front-end only
    app = AdminApp(page, user_role="Librarian")
    app.navigate("/admin")

if __name__ == "__main__":
    ft.run(main)

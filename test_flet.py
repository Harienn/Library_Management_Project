import flet as ft

def main(page: ft.Page):
    page.add(ft.Text("Hello Flet!", size=50, color=ft.Colors.BLUE))

ft.app(target=main)
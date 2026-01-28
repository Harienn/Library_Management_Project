# views/book_detail_view.py
import flet as ft
from components.header import Header
from components.navbar import NavBar


class BookDetailView:
    def __init__(self, page, current_user, navigate):
        self.page = page
        self.current_user = current_user
        self.navigate = navigate
    
    def build(self):
        header = Header(self.page, self.current_user, self.navigate)
        navbar = NavBar(self.page, self.current_user, self.navigate, "/books")
        
        breadcrumb = ft.Row([
            ft.TextButton(
                content=ft.Text("Home"),
                on_click=lambda _: self.navigate("/")
            ),
            ft.Text("›"),
            ft.TextButton(
                content=ft.Text("Books"),
                on_click=lambda _: self.navigate("/books")
            ),
            ft.Text("›"),
            ft.Text("Chain of Gold"),
        ])
        
        book_info = ft.Row([
            ft.Image(src="https://via.placeholder.com/250x350", width=250, height=350, fit="cover"),
            ft.Container(width=30),
            ft.Column([
                ft.Container(
                    content=ft.Text("Available", color=ft.Colors.WHITE),
                    bgcolor=ft.Colors.GREEN,
                    padding=10,  # Sửa: dùng số thay vì Padding()
                    border_radius=5,
                ),
                ft.Text("Chain of Gold", size=28, weight=ft.FontWeight.BOLD),
                ft.Text("The Last Hours", size=16, color=ft.Colors.GREY_700),
                ft.Text("Author: Cassandra Clare", size=14),
                ft.Text("Category: Fantasy, Young Adult", size=14),
                ft.Text("ISBN: 978-1-9821-8582-4", size=14),
                ft.Text("Publication year: 2020", size=14),
                ft.Text("Publisher: Margaret K. McElderry Books", size=14),
                ft.Container(height=10),
                ft.Row([
                    ft.Container(
                        content=ft.Text("Shadowhunters"),
                        bgcolor=ft.Colors.BLUE_100,
                        padding=10,  # Sửa
                        border_radius=5,
                    ),
                    ft.Container(
                        content=ft.Text("Magic"),
                        bgcolor=ft.Colors.PURPLE_100,
                        padding=10,  # Sửa
                        border_radius=5,
                    ),
                    ft.Container(
                        content=ft.Text("Teen"),
                        bgcolor=ft.Colors.PINK_100,
                        padding=10,  # Sửa
                        border_radius=5,
                    ),
                ]),
                ft.Container(height=10),
                ft.FilledButton(
                    content=ft.Text("Login to borrow"),
                    bgcolor=ft.Colors.BLUE_700,
                    color=ft.Colors.WHITE,
                    on_click=lambda _: self.navigate("/login"),
                ),
            ], spacing=8),
        ], alignment="start")
        
        summary = ft.Column([
            ft.Text("Summary", size=20, weight=ft.FontWeight.BOLD),
            ft.Text(
                "From a bestselling author comes the first novel in a new trilogy where evil hides in plain sight and love cuts deeper than any blade. In Edwardian London, the children of the Shadowhunters must face deadly new powers, forbidden romances, and dangerous secrets that could change the fate of their world.",
                size=14,
            ),
        ])
        
        copies_info = ft.Column([
            ft.Text("Copies in the library", size=18, weight=ft.FontWeight.BOLD),
            ft.Text("• 3 books available on shelf."),
            ft.Text("• 1 book currently borrowed (due date: 18/01/2026)."),
        ])
        
        content = ft.Column([
            header.build(),
            navbar.build(),
            ft.Container(height=10),
            breadcrumb,
            ft.Container(height=20),
            book_info,
            ft.Container(height=30),
            summary,
            ft.Container(height=20),
            copies_info,
        ], spacing=10, scroll="auto")
        
        return ft.View(
            route="/book_detail",
            controls=[
                ft.Container(
                    content=content,
                    padding=20,
                    bgcolor=ft.Colors.GREY_50,
                    expand=True,
                )
            ],
        )

# components/book_card.py - PHIÊN BẢN CUỐI CÙNG (không có print debug)
import flet as ft


class BookCard:
    def __init__(self, book_data, on_book_click=None, on_borrow_click=None):
        self.book_data = book_data
        self.on_book_click = on_book_click
        self.on_borrow_click = on_borrow_click
    
    def build(self):
        return ft.Container(
            content=ft.Column(
                controls=[
                    # 1. Ảnh sách
                    ft.Image(
                        src=self.book_data.get("cover_url", "https://via.placeholder.com/200x280/4DD0E1/FFFFFF?text=" + self.book_data.get("title", "Book")[:8]),
                        width=200,
                        height=280,
                        fit="cover",
                        border_radius=8,
                    ),
                    
                    # 2. Tên sách
                    ft.Text(
                        self.book_data.get("title", "Unknown Title"),
                        size=15,
                        weight=ft.FontWeight.BOLD,
                        color=ft.Colors.BLACK_87,
                        max_lines=2,
                        overflow="ellipsis",
                        width=200,
                    ),
                    
                    # 3. Tác giả
                    ft.Text(
                        self.book_data.get("author", "Unknown Author"),
                        size=13,
                        color=ft.Colors.GREY_700,
                        width=200,
                    ),
                    
                    # 4. Nút borrow
                    ft.FilledButton(
                        content=ft.Text("Login to borrow", size=13),
                        on_click=self.on_borrow_click,
                        bgcolor=ft.Colors.CYAN_400,
                        color=ft.Colors.WHITE,
                        width=200,
                        height=40,
                    ),
                ],
                spacing=8,
                horizontal_alignment="center",
                tight=True,
            ),
            width=220,
            height=450,
            padding=10,
            border_radius=10,
            bgcolor=ft.Colors.WHITE,
            shadow=ft.BoxShadow(
                blur_radius=10,
                spread_radius=0,
                color=ft.Colors.with_opacity(0.1, ft.Colors.BLACK),
                offset=ft.Offset(0, 2),
            ),
        )

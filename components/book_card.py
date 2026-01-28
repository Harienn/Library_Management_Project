# components/book_card.py
"""
Book Card Component - Clickable to view book detail
✅ Click vào ảnh hoặc title → xem chi tiết sách
"""
import flet as ft

class BookCard:
    def __init__(self, book_data, current_user=None, on_book_click=None, on_borrow_click=None):
        self.book_data = book_data
        self.current_user = current_user
        self.on_book_click = on_book_click  # ✅ Callback để xem chi tiết
        self.on_borrow_click = on_borrow_click
    
    def build(self):
        is_logged_in = self.current_user is not None
        
        # ===== TEXT + ACTION THEO ROLE =====
        if is_logged_in:
            button_text = "Borrow"
            button_action = lambda e: self.on_borrow_click(e) if self.on_borrow_click else None
        else:
            button_text = "Login to borrow"
            button_action = lambda e: self.on_borrow_click(e) if self.on_borrow_click else None
        
        return ft.Container(
            content=ft.Column(
                [
                    # 1. Cover - ✅ CLICKABLE
                    ft.Container(
                        content=ft.Image(
                            src=self.book_data.get(
                                "cover_url",
                                "https://via.placeholder.com/200x280/4DD0E1/FFFFFF?text=Book"
                            ),
                            width=200,
                            height=280,
                            fit="cover",
                            border_radius=8,
                        ),
                        on_click=lambda e: self.on_book_click(e) if self.on_book_click else None,  # ✅ CLICK VÀO ẢNH
                        ink=True,  # Hiệu ứng ripple khi click
                        border_radius=8,
                    ),
                    
                    # 2. Title - ✅ CLICKABLE
                    ft.Container(
                        content=ft.Text(
                            self.book_data.get("title", "Unknown Title"),
                            size=15,
                            weight=ft.FontWeight.BOLD,
                            max_lines=2,
                            overflow="ellipsis",
                            width=200,
                            text_align=ft.TextAlign.CENTER,
                        ),
                        on_click=lambda e: self.on_book_click(e) if self.on_book_click else None,  # ✅ CLICK VÀO TITLE
                        ink=True,
                        padding=ft.padding.symmetric(vertical=5),
                    ),
                    
                    # 3. Author
                    ft.Text(
                        self.book_data.get("author", "Unknown Author"),
                        size=13,
                        color=ft.Colors.GREY_700,
                        width=200,
                        text_align=ft.TextAlign.CENTER,
                    ),
                    
                    # 4. BUTTON – LUÔN MÀU XANH
                    ft.ElevatedButton(
                        content=ft.Text(button_text, color=ft.Colors.WHITE),
                        on_click=button_action,
                        bgcolor=ft.Colors.CYAN_400,
                        width=200,
                        height=40,
                    ),
                ],
                spacing=8,
                horizontal_alignment="center",
            ),
            width=220,
            padding=10,
            border_radius=10,
            bgcolor=ft.Colors.WHITE,
            shadow=ft.BoxShadow(
                blur_radius=10,
                color=ft.Colors.with_opacity(0.1, ft.Colors.BLACK),
                offset=ft.Offset(0, 2),
            ),
        )
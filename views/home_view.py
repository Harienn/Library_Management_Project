# views/home_view.py
import flet as ft
from components.header import Header
from components.navbar import NavBar
from components.book_card import BookCard
from database.db import fetch_all

class HomeView:
    def __init__(self, page, current_user, navigate, on_logout=None):
        self.page = page
        self.current_user = current_user
        self.navigate = navigate
        self.on_logout = on_logout

    def build(self):
        header = Header(self.page, self.current_user, self.navigate, self.on_logout)
        navbar = NavBar(self.page, self.current_user, self.navigate, "/")

        # HERO SECTION - CHỈ THAY ĐỔI PHẦN NÀY: Thêm ảnh vào container xám
        hero_left = ft.Container(
            content=ft.Stack([
                # Ảnh thư viện
                ft.Container(
                    content=ft.Image(
                        src="https://images.unsplash.com/photo-1521587760476-6c12a4b040da?w=1200&q=80",
                        fit="cover",
                    ),
                    width=9999,
                    height=340,
                ),
                # Overlay tối để text dễ đọc
                ft.Container(
                    width=9999,
                    height=340,
                    gradient=ft.LinearGradient(
                        begin=ft.alignment.Alignment(0, -1),
                        end=ft.alignment.Alignment(0, 1),
                        colors=["#00000040", "#00000070"],
                    ),
                ),
                # Text
                ft.Container(
                    content=ft.Column([
                        ft.Text(
                            "Welcome to Our Library",
                            size=32,
                            weight=ft.FontWeight.BOLD,
                            color=ft.Colors.WHITE,
                            text_align=ft.TextAlign.CENTER,
                        ),
                        ft.Container(height=8),
                        ft.Text(
                            "Discover thousands of books and resources",
                            size=16,
                            color=ft.Colors.WHITE,
                            text_align=ft.TextAlign.CENTER,
                            opacity=0.95,
                        ),
                    ], 
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                    width=9999,
                    height=340,
                ),
            ]),
            border_radius=18,
            expand=2,
            height=340,
            clip_behavior=ft.ClipBehavior.ANTI_ALIAS,
        )

        # GIỮ NGUYÊN PHẦN NÀY - KHÔNG THAY ĐỔI
        hero_right = ft.Container(
            content=ft.Column([
                ft.Text("Featured statistics", size=22, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
                ft.Container(height=24),
                self.create_stat_item("📚", "16,702+", "publications"),
                ft.Container(height=28),
                self.create_stat_item("📖", "15+", "books & magazines"),
                ft.Container(height=28),
                self.create_stat_item("🎓", "55+", "learning materials"),
            ], spacing=0),
            bgcolor=ft.Colors.CYAN_400,
            gradient=ft.LinearGradient(
                begin=ft.alignment.Alignment(-1, -1),
                end=ft.alignment.Alignment(1, 1),
                colors=["#35a6b8", "#4BC1D2", "#2f8c9a"],
            ),
            padding=ft.Padding(left=28, right=28, top=32, bottom=32),
            border_radius=18,
            expand=1,
            height=340,
        )

        hero_section = ft.Container(
            content=ft.Row([hero_left, hero_right], spacing=24),
            padding=ft.Padding(left=40, right=40, top=28, bottom=0),
        )

        # TOP BORROWING BOOKS
        top_books = self.get_top_borrowing_books()
        top_books_section = ft.Column([
            ft.Text("Top Borrowing Books", size=28, weight=ft.FontWeight.BOLD),
            ft.Container(height=20),
            ft.Row([
                BookCard(
                    book_data=book,
                    current_user=self.current_user,
                    on_book_click=lambda e, b=book: self.handle_book_click(b),
                    on_borrow_click=lambda e, b=book: self.handle_borrow_click(b),
                ).build()
                for book in top_books
            ], spacing=22, scroll="auto"),
        ])

        # MUST READ
        must_read_books = self.get_must_read_books()
        must_read_section = ft.Column([
            ft.Text("You must read it now", size=28, weight=ft.FontWeight.BOLD),
            ft.Container(height=20),
            ft.Row([
                BookCard(
                    book_data=book,
                    current_user=self.current_user,
                    on_book_click=lambda e, b=book: self.handle_book_click(b),
                    on_borrow_click=lambda e, b=book: self.handle_borrow_click(b),
                ).build()
                for book in must_read_books
            ], spacing=22, scroll="auto"),
        ])

        # SCROLLABLE CONTENT
        scrollable_content = ft.Column([
            hero_section,
            ft.Container(height=28),
            ft.Container(
                content=ft.Column([
                    top_books_section,
                    ft.Container(height=28),
                    must_read_section,
                ]),
                padding=ft.Padding(left=40, right=40, top=0, bottom=34),
            ),
        ], scroll="auto", expand=True)

        # MAIN VIEW
        return ft.View(
            route="/",
            controls=[
                ft.Container(
                    content=ft.Column([
                        header.build(),
                        navbar.build(),
                        scrollable_content,
                    ], expand=True),
                    bgcolor=ft.Colors.GREY_50,
                    expand=True,
                )
            ],
        )

    def create_stat_item(self, icon, value, label):
        return ft.Row([
            ft.Container(
                content=ft.Text(icon, size=24),
                width=52,
                height=52,
                border_radius=26,
                bgcolor=ft.Colors.with_opacity(0.1, ft.Colors.WHITE),
                alignment=ft.alignment.Alignment(0, 0),
            ),
            ft.Column([
                ft.Text(value, size=24, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
                ft.Text(label, size=16, color=ft.Colors.with_opacity(0.9, ft.Colors.WHITE)),
            ], spacing=0, tight=True),
        ], spacing=16, vertical_alignment="center")

    def handle_book_click(self, book):
        """Handle click on book card to view detail"""
        print(f"📖 Book clicked: {book.get('title')}")
        print(f"📖 Book ID: {book.get('book_id')}")
        
        if self.page.data is None:
            self.page.data = {}
        elif not isinstance(self.page.data, dict):
            self.page.data = {}
            
        self.page.data['selected_book'] = book
        self.navigate("/book_detail")

    def handle_borrow_click(self, book):
        """Handle borrow"""
        if not self.current_user:
            self.navigate("/login")
            return
        
        from services.borrow_service import borrow_book
        
        book_id = book.get("book_id")
        member_id = self.current_user.get("user_id")
        
        # ✅ FIX: Handle both 2-value and 3-value returns
        result = borrow_book(member_id, book_id)
        success, message = result[0], result[1] if len(result) >= 2 else (False, "Error")
        
        self.page.snack_bar = ft.SnackBar(
            content=ft.Text(message, color=ft.Colors.WHITE),
            bgcolor=ft.Colors.GREEN_700 if success else ft.Colors.RED_700,
        )
        self.page.snack_bar.open = True
        self.page.update()
        
        if success:
            import time
            time.sleep(1)
            self.navigate("/my_borrowing")

    def get_top_borrowing_books(self):
        try:
            query = """
                SELECT 
                    b.book_id, b.title,
                    a.author_name as author,
                    b.image_url as cover_url,
                    b.available_copies,
                    COUNT(bt.transaction_id) as borrow_count
                FROM BOOKS b
                LEFT JOIN AUTHORS a ON b.author_id = a.author_id
                LEFT JOIN BORROWING_TRANSACTION_DETAILS btd ON b.book_id = btd.book_id
                LEFT JOIN BORROWING_TRANSACTION bt ON btd.transaction_id = bt.transaction_id
                WHERE b.available_copies > 0
                GROUP BY b.book_id, b.title, a.author_name, b.image_url, b.available_copies
                ORDER BY borrow_count DESC
                LIMIT 5
            """
            books = fetch_all(query)
            
            result = []
            for book in books:
                result.append({
                    'book_id': book['book_id'],
                    'title': book['title'],
                    'author': book['author'] or 'Unknown Author',
                    'cover_url': book['cover_url'] or self.generate_placeholder(book['title']),
                    'available_copies': book.get('available_copies', 0)
                })
            
            return result if result else self.get_fallback_books()
        except Exception as e:
            print(f"Error loading top books: {e}")
            return self.get_fallback_books()

    def get_must_read_books(self):
        try:
            query = """
                SELECT 
                    b.book_id, b.title,
                    a.author_name as author,
                    b.image_url as cover_url,
                    b.available_copies,
                    b.publish_date
                FROM BOOKS b
                LEFT JOIN AUTHORS a ON b.author_id = a.author_id
                WHERE b.available_copies > 0
                ORDER BY b.publish_date DESC, b.book_id DESC
                LIMIT 5
            """
            books = fetch_all(query)
            
            result = []
            for book in books:
                result.append({
                    'book_id': book['book_id'],
                    'title': book['title'],
                    'author': book['author'] or 'Unknown Author',
                    'cover_url': book['cover_url'] or self.generate_placeholder(book['title']),
                    'available_copies': book.get('available_copies', 0)
                })
            
            return result if result else self.get_fallback_books()
        except Exception as e:
            print(f"Error loading must read books: {e}")
            return self.get_fallback_books()

    def generate_placeholder(self, title):
        import hashlib
        color = hashlib.md5(title.encode()).hexdigest()[:6]
        safe_title = title.replace(' ', '+')[:20]
        return f"https://via.placeholder.com/200x280/{color}/FFFFFF?text={safe_title}"

    def get_fallback_books(self):
        return [
            {
                "book_id": 1,
                "title": "Tôi thấy hoa vàng trên cỏ xanh",
                "author": "Nguyễn Nhật Ánh",
                "cover_url": "https://via.placeholder.com/200x280/FF6B6B/FFFFFF?text=Hoa+Vang",
                "available_copies": 5
            },
            {
                "book_id": 2,
                "title": "Cho tôi xin một vé đi tuổi thơ",
                "author": "Nguyễn Nhật Ánh",
                "cover_url": "https://via.placeholder.com/200x280/4ECDC4/FFFFFF?text=Ve+Di+Tuoi+Tho",
                "available_copies": 3
            },
            {
                "book_id": 3,
                "title": "Chí Phèo",
                "author": "Nam Cao",
                "cover_url": "https://via.placeholder.com/200x280/45B7D1/FFFFFF?text=Chi+Pheo",
                "available_copies": 4
            },
        ]
# views/home_view.py
import flet as ft
from components.header import Header
from components.navbar import NavBar
from components.book_card import BookCard


class HomeView:
    def __init__(self, page, current_user, navigate):
        self.page = page
        self.current_user = current_user
        self.navigate = navigate
    
    def build(self):
        header = Header(self.page, self.current_user, self.navigate)
        navbar = NavBar(self.page, self.current_user, self.navigate, "/")
        
        # === HERO SECTION ===
        hero_left = ft.Container(
            bgcolor=ft.Colors.GREY_300,
            border_radius=18,
            expand=2,
            height=340,
        )
        
        hero_right = ft.Container(
            content=ft.Column([
                ft.Text(
                    "Featured statistics",
                    size=22,
                    weight=ft.FontWeight.BOLD,
                    color=ft.Colors.WHITE,
                ),
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
        
        # === TOP BORROWING BOOKS ===
        top_books = self.get_top_borrowing_books()
        top_books_section = ft.Column([
            ft.Text("Top Borrowing Books", size=28, weight=ft.FontWeight.BOLD),
            ft.Container(height=20),
            ft.Row([
                BookCard(
                    book,
                    on_book_click=lambda e, b=book: self.navigate("/book_detail"),
                    on_borrow_click=lambda e, b=book: self.handle_borrow_click()
                ).build() 
                for book in top_books
            ], spacing=22, scroll="auto"),
        ], spacing=0)
        
        # === YOU MUST READ IT NOW ===
        must_read_books = self.get_must_read_books()
        must_read_section = ft.Column([
            ft.Text("You must read it now", size=28, weight=ft.FontWeight.BOLD),
            ft.Container(height=20),
            ft.Row([
                BookCard(
                    book,
                    on_book_click=lambda e, b=book: self.navigate("/book_detail"),
                    on_borrow_click=lambda e, b=book: self.handle_borrow_click()
                ).build() 
                for book in must_read_books
            ], spacing=22, scroll="auto"),
        ], spacing=0)
        
        # === SCROLLABLE CONTENT (CHỈ PHẦN NÀY SCROLL) ===
        scrollable_content = ft.Column([
            hero_section,
            ft.Container(height=28),
            ft.Container(
                content=ft.Column([
                    top_books_section,
                    ft.Container(height=28),
                    must_read_section,
                ], spacing=0),
                padding=ft.Padding(left=40, right=40, top=0, bottom=34),
            ),
        ], spacing=0, scroll="auto", expand=True)  # CHỈ PHẦN NÀY SCROLL
        
        # === MAIN LAYOUT (HEADER + NAVBAR CỐ ĐỊNH) ===
        content = ft.Column([
            header.build(),      # CỐ ĐỊNH
            navbar.build(),      # CỐ ĐỊNH
            scrollable_content,  # SCROLL
        ], spacing=0, expand=True)
        
        return ft.View(
            route="/",
            controls=[
                ft.Container(
                    content=content,
                    padding=0,
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
    
    def handle_borrow_click(self):
        if self.current_user:
            pass
        else:
            self.navigate("/login")
    
    def get_top_borrowing_books(self):
        return [
            {
                "title": "Financial Feminist",
                "author": "Tori Dunlap",
                "cover_url": "https://via.placeholder.com/200x280/FF6B6B/FFFFFF?text=Financial+Feminist"
            },
            {
                "title": "No More Police",
                "author": "Andrea Ritchie",
                "cover_url": "https://via.placeholder.com/200x280/4ECDC4/FFFFFF?text=No+More+Police"
            },
            {
                "title": "I'm Glad My Mom Died",
                "author": "Jennette McCurdy",
                "cover_url": "https://via.placeholder.com/200x280/45B7D1/FFFFFF?text=My+Mom+Died"
            },
            {
                "title": "Nona the Ninth",
                "author": "Tamsyn Muir",
                "cover_url": "https://via.placeholder.com/200x280/FFA07A/FFFFFF?text=Nona+Ninth"
            },
            {
                "title": "Chain of Gold",
                "author": "Cassandra Clare",
                "cover_url": "https://via.placeholder.com/200x280/98D8C8/FFFFFF?text=Chain+Gold"
            },
        ]
    
    def get_must_read_books(self):
        return [
            {
                "title": "Monthly Top Book 1",
                "author": "Author name",
                "cover_url": "https://via.placeholder.com/200x280/F7DC6F/FFFFFF?text=Monthly+1"
            },
            {
                "title": "Monthly Top Book 2",
                "author": "Author name",
                "cover_url": "https://via.placeholder.com/200x280/BB8FCE/FFFFFF?text=Monthly+2"
            },
            {
                "title": "Monthly Top Book 3",
                "author": "Author name",
                "cover_url": "https://via.placeholder.com/200x280/85C1E2/FFFFFF?text=Monthly+3"
            },
            {
                "title": "Monthly Top Book 4",
                "author": "Author name",
                "cover_url": "https://via.placeholder.com/200x280/F8B195/FFFFFF?text=Monthly+4"
            },
            {
                "title": "Monthly Top Book 5",
                "author": "Author name",
                "cover_url": "https://via.placeholder.com/200x280/C06C84/FFFFFF?text=Monthly+5"
            },
        ]

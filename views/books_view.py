# views/books_view.py
import flet as ft
from components.header import Header
from components.navbar import NavBar
from components.book_card import BookCard


class BooksView:
    def __init__(self, page, current_user, navigate):
        self.page = page
        self.current_user = current_user
        self.navigate = navigate
        self.current_page_num = 1  # Trang hiện tại
        self.books_per_page = 15   # 15 sách mỗi trang
    
    def build(self):
        header = Header(self.page, self.current_user, self.navigate)
        navbar = NavBar(self.page, self.current_user, self.navigate, "/books")
        
        # === SEARCH & FILTER ===
        search_filter_section = ft.Container(
            content=ft.Column([
                ft.Text("Search & filter books", size=16, weight=ft.FontWeight.BOLD),
                ft.Container(height=12),
                
                ft.Row([
                    ft.Column([
                        ft.Text("Keyword", size=13),
                        ft.Container(height=4),
                        ft.TextField(
                            hint_text="Title, author, ISBN...",
                            border_color=ft.Colors.GREY_300,
                            height=40,
                            text_size=13,
                            width=220,
                            content_padding=ft.Padding(left=12, right=12, top=0, bottom=0),
                        ),
                    ], spacing=0),
                    
                    ft.Container(width=12),
                    
                    ft.Column([
                        ft.Container(height=17),
                        ft.FilledButton(
                            content=ft.Text("Search", size=13),
                            bgcolor=ft.Colors.CYAN_400,
                            color=ft.Colors.WHITE,
                            height=40,
                            style=ft.ButtonStyle(
                                shape=ft.RoundedRectangleBorder(radius=6),
                                padding=ft.Padding(left=20, right=20, top=0, bottom=0),
                            ),
                        ),
                    ], spacing=0),
                    
                    ft.Container(width=20),
                    ft.Text("Pagination will be applied when results exceed 15 items.", size=11, color=ft.Colors.GREY_600),
                ], spacing=0, alignment="start"),
                
                ft.Container(height=16),
                
                ft.Row([
                    ft.Column([
                        ft.Text("Category", size=13),
                        ft.Container(height=4),
                        ft.Dropdown(
                            width=200,
                            height=40,
                            options=[ft.dropdown.Option("All")],
                            value="All",
                            border_color=ft.Colors.GREY_300,
                            text_size=13,
                        ),
                    ], spacing=0),
                    
                    ft.Container(width=12),
                    
                    ft.Column([
                        ft.Text("Publication year", size=13),
                        ft.Container(height=4),
                        ft.Dropdown(
                            width=200,
                            height=40,
                            options=[ft.dropdown.Option("All")],
                            value="All",
                            border_color=ft.Colors.GREY_300,
                            text_size=13,
                        ),
                    ], spacing=0),
                    
                    ft.Container(width=12),
                    
                    ft.Column([
                        ft.Text("Status", size=13),
                        ft.Container(height=4),
                        ft.Dropdown(
                            width=200,
                            height=40,
                            options=[ft.dropdown.Option("All")],
                            value="All",
                            border_color=ft.Colors.GREY_300,
                            text_size=13,
                        ),
                    ], spacing=0),
                    
                    ft.Container(width=20),
                    
                    ft.Column([
                        ft.Container(height=17),
                        ft.FilledButton(
                            content=ft.Text("Apply filters", size=13),
                            bgcolor=ft.Colors.CYAN_400,
                            color=ft.Colors.WHITE,
                            height=40,
                            style=ft.ButtonStyle(
                                shape=ft.RoundedRectangleBorder(radius=6),
                                padding=ft.Padding(left=20, right=20, top=0, bottom=0),
                            ),
                        ),
                    ], spacing=0),
                    
                    ft.Container(width=8),
                    
                    ft.Column([
                        ft.Container(height=17),
                        ft.TextButton(
                            content=ft.Text("Clear", size=13),
                            height=40,
                        ),
                    ], spacing=0),
                ], spacing=0, alignment="start"),
                
            ], spacing=0),
            bgcolor=ft.Colors.WHITE,
            padding=18,
            border_radius=10,
            border=ft.Border.all(1, ft.Colors.GREY_200),
        )
        
        # === BOOKS GRID - DYNAMIC ===
        all_books = self.get_sample_books()
        total_books = len(all_books)
        total_pages = (total_books + self.books_per_page - 1) // self.books_per_page  # Tính tổng số trang
        
        # Lấy sách của trang hiện tại
        start_idx = (self.current_page_num - 1) * self.books_per_page
        end_idx = start_idx + self.books_per_page
        current_books = all_books[start_idx:end_idx]
        
        books_grid = ft.GridView(
            controls=[
                BookCard(
                    book,
                    on_book_click=lambda e, b=book: self.navigate("/book_detail"),
                    on_borrow_click=lambda e, b=book: self.handle_borrow_click()
                ).build() 
                for book in current_books
            ],
            runs_count=5,
            spacing=18,
            run_spacing=18,
            max_extent=230,
            child_aspect_ratio=0.5,
            padding=0,
        )
        
        # === PAGINATION - DYNAMIC ===
        pagination_buttons = []
        
        # Tạo nút cho mỗi trang
        for page_num in range(1, total_pages + 1):
            is_active = page_num == self.current_page_num
            
            pagination_buttons.append(
                ft.Container(
                    content=ft.Text(
                        str(page_num),
                        size=14,
                        weight=ft.FontWeight.BOLD if is_active else ft.FontWeight.NORMAL,
                        color=ft.Colors.WHITE if is_active else ft.Colors.BLACK_87
                    ),
                    width=40,
                    height=40,
                    border_radius=20,
                    bgcolor=ft.Colors.CYAN_400 if is_active else ft.Colors.GREY_100,
                    alignment=ft.alignment.Alignment(0, 0),
                    ink=not is_active,
                    on_click=None if is_active else lambda _, p=page_num: self.change_page(p),
                )
            )
            pagination_buttons.append(ft.Container(width=8))
        
        # Nút Next
        pagination_buttons.append(
            ft.Container(
                content=ft.Text("Next ›", size=14, color=ft.Colors.BLACK_87),
                padding=ft.Padding(left=16, right=16, top=10, bottom=10),
                border_radius=20,
                bgcolor=ft.Colors.GREY_100,
                ink=True,
                on_click=lambda _: self.change_page(self.current_page_num + 1) if self.current_page_num < total_pages else None,
            )
        )
        
        pagination = ft.Row(pagination_buttons, alignment="center", spacing=0)
        
        # === MAIN CONTENT ===
        content = ft.Column([
            header.build(),
            navbar.build(),
            
            ft.Container(
                content=ft.Column([
                    ft.Container(height=20),
                    
                    ft.Text("Books catalog", size=26, weight=ft.FontWeight.BOLD),
                    ft.Text(
                        f" ",
                        size=13,
                        color=ft.Colors.GREY_600,
                    ),
                    
                    ft.Container(height=20),
                    search_filter_section,
                    ft.Container(height=24),
                    books_grid,
                    ft.Container(height=24),
                    pagination,
                    ft.Container(height=30),
                    
                ], spacing=0, scroll="auto"),
                padding=ft.Padding(left=40, right=40, top=0, bottom=0),
                expand=True,
            ),
        ], spacing=0, expand=True)
        
        return ft.View(
            route="/books",
            controls=[
                ft.Container(
                    content=content,
                    padding=0,
                    bgcolor=ft.Colors.GREY_50,
                    expand=True,
                )
            ],
        )
    
    def change_page(self, page_num):
        """Chuyển trang"""
        all_books = self.get_sample_books()
        total_pages = (len(all_books) + self.books_per_page - 1) // self.books_per_page
        
        if 1 <= page_num <= total_pages:
            self.current_page_num = page_num
            self.navigate("/books")  # Reload view
    
    def handle_borrow_click(self):
        if self.current_user:
            pass
        else:
            self.navigate("/login")
    
    def get_sample_books(self):
        """20 sách mẫu"""
        colors = ["FF6B6B", "4ECDC4", "45B7D1", "FFA07A", "98D8C8", "F7DC6F", "BB8FCE", "85C1E2", "F8B195", "C06C84", 
                  "FF9AA2", "FFB7B2", "FFDAC1", "E2F0CB", "B5EAD7", "C7CEEA", "FFDFD3", "A8E6CF", "FFD3B6", "FFAAA5"]
        books_data = [
            ("Financial Feminist", "Tori Dunlap"),
            ("No More Police", "Andrea Ritchie"),
            ("I'm Glad My Mom Died", "Jennette McCurdy"),
            ("Nona the Ninth", "Tamsyn Muir"),
            ("Chain of Gold", "Cassandra Clare"),
            ("Harlem Shuffle", "Colson Whitehead"),
            ("Book Lovers", "Emily Henry"),
            ("Carrie Soto Is Back", "Taylor Jenkins Reid"),
            ("The Librarian Spy", "Madeline Martin"),
            ("Other Birds", "Sarah Addison Allen"),
            ("The Atlas Six", "Olivie Blake"),
            ("Brave and Bound", "L.P. Dover"),
            ("Two Old Women", "Velma Wallis"),
            ("City of Fallen Angels", "Cassandra Clare"),
            ("Clockwork Princess", "Cassandra Clare"),
            # 5 CUỐN THÊM CHO TRANG 2
            ("The Seven Husbands", "Taylor Jenkins Reid"),
            ("Project Hail Mary", "Andy Weir"),
            ("The Midnight Library", "Matt Haig"),
            ("Atomic Habits", "James Clear"),
            ("Where the Crawdads Sing", "Delia Owens"),
        ]
        
        return [
            {
                "title": title,
                "author": author,
                "cover_url": f"https://via.placeholder.com/200x280/{colors[i]}/FFFFFF?text={title.replace(' ', '+')[:15]}"
            }
            for i, (title, author) in enumerate(books_data)
        ]

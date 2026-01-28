# views/books_view.py
# ✅ ĐÃ SỬA: Tích hợp tìm kiếm/lọc thực tế từ database + Click to view detail
import flet as ft
from components.header import Header
from components.navbar import NavBar
from components.book_card import BookCard
from services.book_service import search_books, get_all_categories, get_all_publish_years


class BooksView:
    def __init__(self, page, current_user, navigate, on_logout=None):
        self.page = page
        self.current_user = current_user
        self.navigate = navigate
        self.on_logout = on_logout
        
        # Search & Filter state
        self.current_page_num = 1
        self.books_per_page = 15
        self.search_keyword = ""
        self.filter_category = "All"
        self.filter_year = "All"
        self.filter_status = "All"
        
        # Controls references
        self.keyword_field = None
        self.category_dropdown = None
        self.year_dropdown = None
        self.status_dropdown = None
        self.books_grid_container = None
        self.pagination_container = None
        self.result_text = None
    
    def build(self):
        header = Header(self.page, self.current_user, self.navigate, self.on_logout)
        navbar = NavBar(self.page, self.current_user, self.navigate, "/books")
        
        # === SEARCH & FILTER ===
        self.keyword_field = ft.TextField(
            hint_text="Title, author, ISBN...",
            border_color=ft.Colors.GREY_300,
            height=40,
            text_size=13,
            width=220,
            content_padding=ft.Padding(left=12, right=12, top=0, bottom=0),
            on_submit=lambda e: self.handle_search(),
        )
        
        # ✅ Load categories and years từ database
        try:
            categories = get_all_categories()
            years = get_all_publish_years()
        except Exception as e:
            print(f"Error loading filters: {e}")
            categories = []
            years = []
        
        self.category_dropdown = ft.Dropdown(
            width=200,
            height=40,
            options=[ft.dropdown.Option("All")] + 
                    [ft.dropdown.Option(str(cat['category_id']), cat['category_name']) 
                     for cat in categories],
            value="All",
            border_color=ft.Colors.GREY_300,
            text_size=13,
        )
        
        self.year_dropdown = ft.Dropdown(
            width=200,
            height=40,
            options=[ft.dropdown.Option("All")] + 
                    [ft.dropdown.Option(year) for year in years],
            value="All",
            border_color=ft.Colors.GREY_300,
            text_size=13,
        )
        
        self.status_dropdown = ft.Dropdown(
            width=200,
            height=40,
            options=[
                ft.dropdown.Option("All"),
                ft.dropdown.Option("AVAILABLE"),
                ft.dropdown.Option("BORROWED"),
            ],
            value="All",
            border_color=ft.Colors.GREY_300,
            text_size=13,
        )
        
        search_filter_section = ft.Container(
            content=ft.Column([
                ft.Text("Search & filter books", size=16, weight=ft.FontWeight.BOLD),
                ft.Container(height=12),
                
                ft.Row([
                    ft.Column([
                        ft.Text("Keyword", size=13),
                        ft.Container(height=4),
                        self.keyword_field,
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
                            on_click=lambda e: self.handle_search(),
                        ),
                    ], spacing=0),
                    
                    ft.Container(width=20),
                    ft.Text("Pagination will be applied when results exceed 15 items.", 
                           size=11, color=ft.Colors.GREY_600),
                ], spacing=0, alignment="start"),
                
                ft.Container(height=16),
                
                ft.Row([
                    ft.Column([
                        ft.Text("Category", size=13),
                        ft.Container(height=4),
                        self.category_dropdown,
                    ], spacing=0),
                    
                    ft.Container(width=12),
                    
                    ft.Column([
                        ft.Text("Publication year", size=13),
                        ft.Container(height=4),
                        self.year_dropdown,
                    ], spacing=0),
                    
                    ft.Container(width=12),
                    
                    ft.Column([
                        ft.Text("Status", size=13),
                        ft.Container(height=4),
                        self.status_dropdown,
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
                            on_click=lambda e: self.handle_apply_filters(),
                        ),
                    ], spacing=0),
                    
                    ft.Container(width=8),
                    
                    ft.Column([
                        ft.Container(height=17),
                        ft.TextButton(
                            content=ft.Text("Clear", size=13),
                            height=40,
                            on_click=lambda e: self.handle_clear_filters(),
                        ),
                    ], spacing=0),
                ], spacing=0, alignment="start"),
                
            ], spacing=0),
            bgcolor=ft.Colors.WHITE,
            padding=18,
            border_radius=10,
            border=ft.Border.all(1, ft.Colors.GREY_200),
        )
        
        # Result text
        self.result_text = ft.Text("", size=13, color=ft.Colors.GREY_600)
        
        # Books grid container (will be populated)
        self.books_grid_container = ft.Container(
            content=ft.Text("Loading...", size=14),
            padding=20,
        )
        
        # Pagination container
        self.pagination_container = ft.Container()
        
        # ✅ Load initial data
        self.load_books()
        
        # === MAIN CONTENT ===
        content = ft.Column([
            header.build(),
            navbar.build(),
            
            ft.Container(
                content=ft.Column([
                    ft.Container(height=20),
                    
                    ft.Text("Books catalog", size=26, weight=ft.FontWeight.BOLD),
                    self.result_text,
                    
                    ft.Container(height=20),
                    search_filter_section,
                    ft.Container(height=24),
                    self.books_grid_container,
                    ft.Container(height=24),
                    self.pagination_container,
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
    
    def load_books(self):
        """✅ Load books từ database với filters hiện tại"""
        try:
            # Get search results từ database
            result = search_books(
                keyword=self.search_keyword if self.search_keyword else None,
                category_id=self.filter_category if self.filter_category != "All" else None,
                publish_year=self.filter_year if self.filter_year != "All" else None,
                status=self.filter_status if self.filter_status != "All" else None,
                page=self.current_page_num,
                per_page=self.books_per_page
            )
            
            books = result['books']
            total = result['total']
            total_pages = result['total_pages']
            
            # Update result text
            if self.search_keyword or self.filter_category != "All" or self.filter_year != "All" or self.filter_status != "All":
                self.result_text.value = f"Found {total} books matching your criteria"
            else:
                self.result_text.value = f"Showing {len(books)} of {total} books"
            
            # Update books grid
            if books:
                books_grid = ft.GridView(
                    controls=[
                        BookCard(
                            book_data=self.convert_book_data(book),
                            current_user=self.current_user,
                            on_book_click=lambda e, b=book: self.handle_book_click(b),
                            on_borrow_click=lambda e, b=book: self.handle_borrow_click(b),
                        ).build() 
                        for book in books
                    ],
                    runs_count=5,
                    spacing=18,
                    run_spacing=18,
                    max_extent=230,
                    child_aspect_ratio=0.5,
                    padding=0,
                )
                self.books_grid_container.content = books_grid
            else:
                self.books_grid_container.content = ft.Container(
                    content=ft.Column([
                        ft.Icon(ft.Icons.SEARCH_OFF, size=64, color=ft.Colors.GREY_400),
                        ft.Container(height=16),
                        ft.Text("No books found", size=18, weight=ft.FontWeight.BOLD),
                        ft.Text("Try adjusting your search or filters", size=13, color=ft.Colors.GREY_600),
                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                    padding=60,
                    alignment=ft.alignment.center,
                )
            
            # Update pagination
            self.build_pagination(total_pages)
            
            # Update page
            self.page.update()
            
        except Exception as e:
            print(f"Error loading books: {e}")
            self.books_grid_container.content = ft.Text(
                f"Error loading books: {str(e)}", 
                size=14, 
                color=ft.Colors.RED
            )
            self.page.update()
    
    def convert_book_data(self, book):
        """Convert database book to BookCard format"""
        return {
            'book_id': book['book_id'],
            'title': book['title'],
            'author': book['author_name'] or 'Unknown Author',
            'cover_url': book['image_url'] or self.generate_placeholder_url(book['title']),
            'available_copies': book['available_copies'],
        }
    
    def generate_placeholder_url(self, title):
        """Generate placeholder image URL"""
        import hashlib
        color = hashlib.md5(title.encode()).hexdigest()[:6]
        safe_title = title.replace(' ', '+')[:20]
        return f"https://via.placeholder.com/200x280/{color}/FFFFFF?text={safe_title}"
    
    def build_pagination(self, total_pages):
        """Build pagination controls"""
        if total_pages <= 1:
            self.pagination_container.content = None
            return
        
        pagination_buttons = []
        
        # Page numbers
        for page_num in range(1, min(total_pages + 1, 11)):
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
        
        # Next button
        if self.current_page_num < total_pages:
            pagination_buttons.append(
                ft.Container(
                    content=ft.Text("Next ›", size=14, color=ft.Colors.BLACK_87),
                    padding=ft.Padding(left=16, right=16, top=10, bottom=10),
                    border_radius=20,
                    bgcolor=ft.Colors.GREY_100,
                    ink=True,
                    on_click=lambda _: self.change_page(self.current_page_num + 1),
                )
            )
        
        self.pagination_container.content = ft.Row(
            pagination_buttons, 
            alignment="center", 
            spacing=0
        )
    
    def change_page(self, page_num):
        """Chuyển trang"""
        self.current_page_num = page_num
        self.load_books()
    
    def handle_search(self):
        """Handle search button click"""
        self.search_keyword = self.keyword_field.value or ""
        self.current_page_num = 1
        self.load_books()
    
    def handle_apply_filters(self):
        """Handle apply filters button click"""
        self.filter_category = self.category_dropdown.value
        self.filter_year = self.year_dropdown.value
        self.filter_status = self.status_dropdown.value
        self.current_page_num = 1
        self.load_books()
    
    def handle_clear_filters(self):
        """Handle clear filters button click"""
        self.search_keyword = ""
        self.filter_category = "All"
        self.filter_year = "All"
        self.filter_status = "All"
        self.current_page_num = 1
        
        # Reset UI
        self.keyword_field.value = ""
        self.category_dropdown.value = "All"
        self.year_dropdown.value = "All"
        self.status_dropdown.value = "All"
        
        self.load_books()
    
    def handle_book_click(self, book):
        """✅ Handle click on book to view detail"""
        print(f"📖 Book clicked from Books page: {book.get('title')}")
        
        # ✅ LƯU VÀO page.data
        if self.page.data is None:
            self.page.data = {}
        elif not isinstance(self.page.data, dict):
            self.page.data = {}
        
        self.page.data['selected_book'] = book
        
        # Navigate to book detail
        self.navigate("/book_detail")
    
    def handle_borrow_click(self, book=None):
        """✅ Handle borrow button click"""
        if not self.current_user:
            self.navigate("/login")
            return
        
        if not book:
            return
        
        # Import borrow_book service
        from services.borrow_service import borrow_book
        
        book_id = book.get("book_id")
        member_id = self.current_user.get("user_id")
        
        success, message, transaction_id = borrow_book(member_id, book_id)
        
        # Show snackbar
        self.page.snack_bar = ft.SnackBar(
            content=ft.Text(message, color=ft.Colors.WHITE),
            bgcolor=ft.Colors.GREEN_700 if success else ft.Colors.RED_700,
        )
        self.page.snack_bar.open = True
        self.page.update()
        
        if success:
            # Reload books to update available_copies
            self.load_books()
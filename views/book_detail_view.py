# views/book_detail_view.py
"""
Book Detail View - Complete with all sections
"""
import flet as ft
from database.db import fetch_one, fetch_all


class BookDetailView:
    def __init__(self, page, current_user, navigate, on_logout, book_data=None):
        self.page = page
        self.current_user = current_user
        self.navigate = navigate
        self.on_logout = on_logout
        self.book_data = book_data or {}
        
        print(f"🔍 BookDetailView init with book_data: {self.book_data}")
        
        # Load full data from DB
        if self.book_data and self.book_data.get("book_id"):
            book_id = self.book_data.get("book_id")
            full_data = self.get_book_detail(book_id)
            if full_data:
                self.book_data = full_data
                print(f"✅ Loaded book: {self.book_data.get('title')}")

    def get_book_detail(self, book_id):
        """Get full book details"""
        try:
            sql = """
                SELECT 
                    b.book_id, b.title, b.isbn, b.publish_date,
                    b.total_copies, b.available_copies, b.is_reference_only,
                    b.publisher, b.summary, b.image_url, b.price, b.book_status,
                    a.author_name, a.author_id, c.category_name, c.category_id
                FROM BOOKS b
                LEFT JOIN AUTHORS a ON b.author_id = a.author_id
                LEFT JOIN CATEGORIES c ON b.category_id = c.category_id
                WHERE b.book_id = %s
            """
            return fetch_one(sql, (book_id,)) or {}
        except Exception as e:
            print(f"❌ Error loading book: {e}")
            return {}

    def get_books_by_author(self, author_id, book_id):
        """Get other books by author"""
        if not author_id:
            return []
        try:
            sql = """
                SELECT b.book_id, b.title, b.image_url, b.available_copies, a.author_name
                FROM BOOKS b
                LEFT JOIN AUTHORS a ON b.author_id = a.author_id
                WHERE b.author_id = %s AND b.book_id != %s
                LIMIT 5
            """
            return fetch_all(sql, (author_id, book_id)) or []
        except Exception as e:
            print(f"Error loading books by author: {e}")
            return []

    def get_books_by_category(self, category_id, book_id):
        """Get books in same category"""
        if not category_id:
            return []
        try:
            sql = """
                SELECT b.book_id, b.title, b.image_url, b.available_copies, a.author_name
                FROM BOOKS b
                LEFT JOIN AUTHORS a ON b.author_id = a.author_id
                WHERE b.category_id = %s AND b.book_id != %s
                LIMIT 5
            """
            return fetch_all(sql, (category_id, book_id)) or []
        except Exception as e:
            print(f"Error loading books by category: {e}")
            return []

    def build(self):
        """Build complete book detail"""
        print(f"🔨 Building BookDetailView...")
        
        if not self.book_data or not self.book_data.get("book_id"):
            print("⚠️ No book data")
            return self.build_error_view()
        
        try:
            print("📦 Building breadcrumb...")
            breadcrumb = self.build_breadcrumb()
            
            print("📦 Building main info...")
            main_info = self.build_main_info()
            
            print("📦 Building copies notes...")
            copies_notes = self.build_copies_notes()
            
            print("📦 Building more by author...")
            more_by_author = self.build_more_by_author()
            
            print("📦 Building same genre...")
            same_genre = self.build_same_genre()
            
            print("📦 Building header...")
            # Simple header (NO ICONS)
            user_name = "Guest"
            if self.current_user:
                user_name = self.current_user.get('fullname', 'User')
            
            simple_header = ft.Container(
                content=ft.Row([
                    ft.TextButton(
                        "← Back",
                        style=ft.ButtonStyle(color=ft.Colors.WHITE),
                        on_click=lambda _: self.navigate("/books"),
                    ),
                    ft.Text("Library System", size=18, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
                    ft.Container(expand=True),
                    ft.Text(f"Hello, {user_name}", size=14, color=ft.Colors.WHITE),
                    ft.Container(width=10),
                    ft.TextButton(
                        "🏠 Home",
                        style=ft.ButtonStyle(color=ft.Colors.WHITE),
                        on_click=lambda _: self.navigate("/"),
                    ),
                ], alignment=ft.MainAxisAlignment.START),
                padding=ft.padding.symmetric(horizontal=20, vertical=10),
                bgcolor=ft.Colors.CYAN_400,
            )
            
            print("📦 Assembling content...")
            content = ft.Column([
                simple_header,
                ft.Container(
                    content=ft.Column([
                        breadcrumb,
                        main_info,
                        copies_notes,
                        more_by_author,
                        same_genre,
                        ft.Container(height=40),
                    ], scroll=ft.ScrollMode.AUTO),
                    expand=True,
                ),
            ], spacing=0, expand=True)
            
            print(f"✅ BookDetailView built successfully")
            return ft.View("/book_detail", [content], padding=0, bgcolor=ft.Colors.GREY_50)
        
        except Exception as e:
            print(f"❌ ERROR BUILDING VIEW: {e}")
            import traceback
            traceback.print_exc()
            return self.build_error_view(str(e))

    def build_error_view(self, error_msg=None):
        """Build error view (NO ICONS)"""
        return ft.View(
            "/book_detail",
            [ft.Container(
                content=ft.Column([
                    ft.Text("❌", size=80),
                    ft.Container(height=20),
                    ft.Text("Book not found", size=24, weight=ft.FontWeight.BOLD),
                    ft.Container(height=10),
                    ft.Text(
                        error_msg if error_msg else "The book you're looking for doesn't exist.",
                        size=14,
                        color=ft.Colors.GREY_600
                    ),
                    ft.Container(height=30),
                    ft.ElevatedButton(
                        "Back to Books",
                        bgcolor=ft.Colors.CYAN_400,
                        color=ft.Colors.WHITE,
                        on_click=lambda _: self.navigate("/books")
                    ),
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                padding=100,
                expand=True,
            )],
            bgcolor=ft.Colors.GREY_50,
        )

    def build_breadcrumb(self):
        """Breadcrumb"""
        return ft.Container(
            content=ft.Row([
                ft.TextButton("Home", on_click=lambda _: self.navigate("/")),
                ft.Text("›", color="#999", size=16),
                ft.TextButton("Books", on_click=lambda _: self.navigate("/books")),
                ft.Text("›", color="#999", size=16),
                ft.Text(self.book_data.get("title", "")[:40], color="#333", size=14),
            ], spacing=5),
            padding=ft.padding.only(left=40, right=40, top=20, bottom=10),
        )

    def build_main_info(self):
        """Main book info"""
        available = self.book_data.get("available_copies", 0) > 0
        is_reference = self.book_data.get("is_reference_only", 0) == 1
        
        # Cover
        cover_url = self.book_data.get("image_url")
        if cover_url:
            try:
                cover_content = ft.Image(
                    src=cover_url,
                    width=200,
                    height=300,
                    fit=ft.ImageFit.COVER,
                )
            except:
                cover_content = ft.Container(
                    content=ft.Text("📚", size=80),
                    width=200,
                    height=300,
                    bgcolor="#B2EBF2",
                    alignment=ft.Alignment(0, 0),
                )
        else:
            cover_content = ft.Container(
                content=ft.Text("📚", size=80),
                width=200,
                height=300,
                bgcolor="#B2EBF2",
                alignment=ft.Alignment(0, 0),
            )
        
        cover = ft.Container(
            content=cover_content,
            border_radius=8,
            border=ft.border.all(1, "#E5E7EB"),
        )
        
        # Badge
        if is_reference:
            badge_text, badge_color = "Reference Only", "#F59E0B"
        elif available:
            badge_text, badge_color = "Available", "#10B981"
        else:
            badge_text, badge_color = "Not Available", "#EF4444"
        
        badge = ft.Container(
            content=ft.Text(badge_text, size=12, color=ft.Colors.WHITE, weight=ft.FontWeight.BOLD),
            bgcolor=badge_color,
            padding=ft.padding.symmetric(horizontal=20, vertical=8),
            border_radius=20,
            margin=ft.margin.only(top=15),
        )
        
        # Details
        details = ft.Column([
            ft.Text(self.book_data.get("title", "Unknown Title"), size=32, weight=ft.FontWeight.BOLD, color="#111827"),
            ft.Container(height=15),
            self.info_row("Author:", self.book_data.get("author_name") or "Unknown Author"),
            self.info_row("Category:", self.book_data.get("category_name") or "Unknown"),
            self.info_row("ISBN:", self.book_data.get("isbn") or "N/A"),
            self.info_row("Published:", str(self.book_data.get("publish_date") or "N/A")),
            self.info_row("Publisher:", self.book_data.get("publisher") or "Unknown"),
            ft.Container(height=15),
            self.build_tags(),
            ft.Container(height=25),
            self.build_borrow_section(available, is_reference),
            ft.Container(height=25),
            ft.Text("Summary", size=18, weight=ft.FontWeight.BOLD, color="#111827"),
            ft.Container(height=10),
            ft.Text(
                self.book_data.get("summary") or "No summary available for this book.",
                size=13,
                color="#444"
            ),
        ], spacing=3)
        
        return ft.Container(
            content=ft.Row([
                ft.Column([cover, badge], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                ft.Container(width=40),
                details,
            ], vertical_alignment=ft.CrossAxisAlignment.START),
            padding=ft.padding.symmetric(horizontal=40, vertical=20),
        )

    def info_row(self, label, value):
        """Info row helper"""
        return ft.Row([
            ft.Text(label, size=13, color="#666", weight=ft.FontWeight.BOLD, width=100),
            ft.Text(str(value), size=13, color="#333"),
        ], spacing=5)

    def build_tags(self):
        """Build category tags"""
        category = self.book_data.get("category_name", "")
        tags = []
        
        if "Văn học" in category or "Fiction" in category:
            tags = ["Fiction", "Literature"]
        elif "Khoa học" in category or "Science" in category:
            tags = ["Science", "Educational"]
        elif "Kỹ năng" in category:
            tags = ["Self-help", "Skills"]
        elif "Kinh tế" in category:
            tags = ["Business", "Economics"]
        elif category:
            tags = [category]
        
        if not tags:
            return ft.Container()
        
        return ft.Row([
            ft.Container(
                content=ft.Text(tag, size=11, color="#1E88E5"),
                bgcolor="#E3F2FD",
                padding=ft.padding.symmetric(horizontal=12, vertical=6),
                border_radius=15,
            ) for tag in tags[:3]
        ], spacing=10)

    def build_borrow_section(self, available, is_reference):
        """Borrow button or message"""
        if is_reference:
            return ft.Container(
                content=ft.Text(
                    "📖 This is a reference-only book. Cannot be borrowed.",
                    size=12,
                    color="#92400E",
                ),
                padding=15,
                bgcolor="#FEF3C7",
                border_radius=8,
            )
        
        if not self.current_user:
            return ft.Container(
                content=ft.Column([
                    ft.Text(
                        "🔒 Guests can view book information. To borrow, please log in.",
                        size=12,
                        color="#666",
                    ),
                    ft.Container(height=10),
                    ft.ElevatedButton(
                        "Login to borrow",
                        bgcolor=ft.Colors.CYAN_400,
                        color=ft.Colors.WHITE,
                        on_click=lambda _: self.navigate("/login")
                    ),
                ]),
                padding=15,
                bgcolor="#E8F5E9",
                border_radius=8,
            )
        
        return ft.ElevatedButton(
            "Borrow This Book" if available else "Not Available",
            disabled=not available,
            bgcolor=ft.Colors.CYAN_400 if available else ft.Colors.GREY_400,
            color=ft.Colors.WHITE,
            on_click=self.handle_borrow if available else None,
        )

    def build_copies_notes(self):
        """Copies info and notes"""
        total = self.book_data.get("total_copies", 0)
        available = self.book_data.get("available_copies", 0)
        borrowed = total - available
        
        copies = ft.Container(
            content=ft.Column([
                ft.Text("📚 Copies in the library", size=16, weight=ft.FontWeight.BOLD, color="#111827"),
                ft.Container(height=10),
                ft.Text(f"• {total} books on shelf", size=13, color="#374151"),
                ft.Text(
                    f"• {borrowed} currently borrowed" if borrowed > 0 else "• All available",
                    size=13,
                    color="#374151"
                ),
            ], spacing=5),
            padding=20,
            bgcolor=ft.Colors.WHITE,
            border_radius=8,
            expand=1,
        )
        
        price = self.book_data.get("price", 0)
        status = self.book_data.get("book_status", "AVAILABLE")
        
        notes = ft.Container(
            content=ft.Column([
                ft.Text("ℹ️ Quick notes", size=16, weight=ft.FontWeight.BOLD, color="#111827"),
                ft.Container(height=10),
                ft.Text(
                    f"• Price: {price:,.0f} VND" if price else "• Price: N/A",
                    size=13,
                    color="#374151"
                ),
                ft.Text(f"• Status: {status}", size=13, color="#374151"),
            ], spacing=5),
            padding=20,
            bgcolor=ft.Colors.WHITE,
            border_radius=8,
            expand=1,
        )
        
        return ft.Container(
            content=ft.Row([copies, ft.Container(width=20), notes]),
            padding=ft.padding.symmetric(horizontal=40, vertical=20),
        )

    def build_more_by_author(self):
        """More books by this author"""
        author_id = self.book_data.get("author_id")
        book_id = self.book_data.get("book_id")
        
        if not author_id:
            return ft.Container()
        
        books = self.get_books_by_author(author_id, book_id)
        if not books:
            return ft.Container()
        
        return ft.Container(
            content=ft.Column([
                ft.Text("More books by this author", size=18, weight=ft.FontWeight.BOLD, color="#111827"),
                ft.Container(height=20),
                ft.Row(
                    [self.create_book_card(book) for book in books],
                    spacing=15,
                    scroll=ft.ScrollMode.AUTO
                ),
            ]),
            padding=ft.padding.symmetric(horizontal=40, vertical=20),
        )

    def build_same_genre(self):
        """You may also like"""
        category_id = self.book_data.get("category_id")
        book_id = self.book_data.get("book_id")
        
        if not category_id:
            return ft.Container()
        
        books = self.get_books_by_category(category_id, book_id)
        if not books:
            return ft.Container()
        
        return ft.Container(
            content=ft.Column([
                ft.Text("You may also like", size=18, weight=ft.FontWeight.BOLD, color="#111827"),
                ft.Container(height=20),
                ft.Row(
                    [self.create_book_card(book) for book in books],
                    spacing=15,
                    scroll=ft.ScrollMode.AUTO
                ),
            ]),
            padding=ft.padding.symmetric(horizontal=40, vertical=20),
        )

    def create_book_card(self, book):
        """Create small book card"""
        title = book.get("title", "")
        available = book.get("available_copies", 0) > 0
        book_id = book.get("book_id")
        
        def on_click(e):
            if self.page.data is None:
                self.page.data = {}
            self.page.data['selected_book'] = {"book_id": book_id}
            self.navigate("/book_detail")
        
        return ft.Container(
            content=ft.Column([
                ft.Container(
                    content=ft.Text("📚", size=60),
                    width=140,
                    height=200,
                    bgcolor="#B2EBF2",
                    alignment=ft.Alignment(0, 0),
                    border_radius=8,
                    on_click=on_click,
                    ink=True,
                ),
                ft.Container(height=10),
                ft.Text(title[:30], size=13, weight=ft.FontWeight.BOLD, max_lines=2, color="#111827"),
                ft.Container(height=10),
                ft.ElevatedButton(
                    "Borrow" if available else "Not available",
                    disabled=not available,
                    width=140,
                    bgcolor=ft.Colors.CYAN_400 if available else ft.Colors.GREY_400,
                    color=ft.Colors.WHITE,
                ),
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            padding=10,
        )

    def handle_borrow(self, e):
        """Handle borrow book"""
        try:
            from services.borrow_service import borrow_book
            
            book_id = self.book_data.get("book_id")
            member_id = self.current_user.get("user_id")
            
            success, message = borrow_book(member_id, book_id)
            
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
        
        except Exception as error:
            print(f"Error borrowing book: {error}")
            self.page.snack_bar = ft.SnackBar(
                content=ft.Text(f"Error: {str(error)}", color=ft.Colors.WHITE),
                bgcolor=ft.Colors.RED_700,
            )
            self.page.snack_bar.open = True
            self.page.update()
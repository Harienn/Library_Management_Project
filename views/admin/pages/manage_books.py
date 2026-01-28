# views/admin/pages/manage_books.py
import flet as ft


class ManageBooksPage:
    def __init__(self):
        self.current_isbn = None
        self.page_ref = None  # Thêm reference đến page
        
    def build(self):
        content = ft.Column([
            # Header
            ft.Row([
                ft.Text("Book list", size=16, weight=ft.FontWeight.BOLD, color="#1F2937"),
                ft.Container(expand=True),
                ft.ElevatedButton(
                    "+ Add book",
                    bgcolor="#E5E7EB",
                    color="#111827",
                    on_click=self.reset_form,
                ),
            ]),
            
            ft.Text(
                "Search by ISBN, title or author. Use the form above to add or edit book details, including public cover image URL and a short summary.",
                size=12,
                color="#6B7280",
            ),
            
            ft.Container(height=8),
            
            # Form
            self._build_form(),
            
            # Toolbar
            self._build_toolbar(),
            
            # Table
            self._build_table(),
            
            # Note
            ft.Text(
                "Status is simplified to Available and Not available so staff can quickly see if the title can be borrowed or is out of stock/checked out.",
                size=11,
                color="#6B7280",
                italic=True,
            ),
        ], spacing=10)
        
        # Wrap trong Container với key để scroll
        self.main_container = ft.Container(
            content=content,
            padding=ft.Padding(14, 14, 16, 16),
            bgcolor="#FFFFFF",
            border_radius=14,
            border=ft.Border.all(1, "#E5E7EB"),
        )
        
        return self.main_container
    
    def reset_form(self, e=None):
        """Reset form"""
        self.current_isbn = None
        self.isbn_field.value = ""
        self.title_field.value = ""
        self.author_field.value = ""
        self.category_field.value = ""
        self.summary_field.value = ""
        self.publisher_field.value = ""
        self.year_field.value = ""
        self.pages_field.value = ""
        self.price_field.value = ""
        self.total_field.value = ""
        self.available_field.value = ""
        self.cover_url_field.value = ""
        self.status_field.value = "Available"
        if e:
            e.page.update()
    
    def edit_book(self, book_data, e):
        """Load dữ liệu sách vào form và scroll lên"""
        self.current_isbn = book_data["isbn"]
        self.isbn_field.value = book_data["isbn"]
        self.title_field.value = book_data["title"]
        self.author_field.value = book_data["author"]
        self.category_field.value = book_data["category"]
        self.summary_field.value = ""  # Không có trong data mẫu
        self.publisher_field.value = book_data["publisher"]
        self.year_field.value = book_data["year"]
        self.pages_field.value = book_data["pages"]
        self.price_field.value = book_data["price"]
        self.total_field.value = book_data["total"]
        self.available_field.value = book_data["available"]
        self.cover_url_field.value = ""  # Không có trong data mẫu
        self.status_field.value = book_data["status"]
        
        # Update UI
        e.page.update()
        
        # Scroll to top - Tìm ScrollableControl và scroll lên
        # Vì page được wrap trong scroll, ta cần scroll về đầu
        try:
            # Nếu page có scroll_to method
            if hasattr(e.page, 'scroll_to'):
                e.page.scroll_to(offset=0, duration=300)
            # Hoặc scroll bằng cách update window
            e.page.window_scroll_to(0, 0)
        except:
            pass
    
    def _build_form(self):
        """Form theo thiết kế mới - full width"""
        
        # Fields
        self.isbn_field = ft.TextField(
            border_color="#D1D5DB",
            text_size=13,
            border_radius=6,
            height=40,
            expand=True,
        )
        
        self.title_field = ft.TextField(
            border_color="#D1D5DB",
            text_size=13,
            border_radius=6,
            height=40,
            expand=True,
        )
        
        self.author_field = ft.TextField(
            border_color="#D1D5DB",
            text_size=13,
            border_radius=6,
            height=40,
            expand=True,
        )
        
        self.category_field = ft.TextField(
            border_color="#D1D5DB",
            text_size=13,
            border_radius=6,
            height=40,
            expand=True,
        )
        
        self.summary_field = ft.TextField(
            border_color="#D1D5DB",
            text_size=13,
            border_radius=6,
            multiline=True,
            min_lines=3,
            max_lines=3,
            expand=True,
        )
        
        self.publisher_field = ft.TextField(
            border_color="#D1D5DB",
            text_size=13,
            border_radius=6,
            height=40,
            expand=True,
        )
        
        self.year_field = ft.TextField(
            border_color="#D1D5DB",
            text_size=13,
            border_radius=6,
            height=40,
            keyboard_type=ft.KeyboardType.NUMBER,
            expand=True,
        )
        
        self.pages_field = ft.TextField(
            border_color="#D1D5DB",
            text_size=13,
            border_radius=6,
            height=40,
            keyboard_type=ft.KeyboardType.NUMBER,
            expand=True,
        )
        
        self.price_field = ft.TextField(
            border_color="#D1D5DB",
            text_size=13,
            border_radius=6,
            height=40,
            keyboard_type=ft.KeyboardType.NUMBER,
            expand=True,
        )
        
        self.total_field = ft.TextField(
            border_color="#D1D5DB",
            text_size=13,
            border_radius=6,
            height=40,
            keyboard_type=ft.KeyboardType.NUMBER,
            expand=True,
        )
        
        self.available_field = ft.TextField(
            border_color="#D1D5DB",
            text_size=13,
            border_radius=6,
            height=40,
            keyboard_type=ft.KeyboardType.NUMBER,
            expand=True,
        )
        
        self.cover_url_field = ft.TextField(
            border_color="#D1D5DB",
            text_size=13,
            border_radius=6,
            height=40,
            expand=True,
        )
        
        self.status_field = ft.Dropdown(
            options=[
                ft.dropdown.Option("Available"),
                ft.dropdown.Option("Not available"),
            ],
            value="Available",
            border_color="#D1D5DB",
            text_size=13,
            border_radius=6,
            height=40,
            width=600,
        )
        
        # Layout
        return ft.Column([
            # Row 1: ISBN + Title
            ft.Row([
                ft.Column([
                    ft.Text("ISBN", size=12, color="#374151"),
                    self.isbn_field,
                ], spacing=4, expand=1),
                ft.Container(width=16),
                ft.Column([
                    ft.Text("Title", size=12, color="#374151"),
                    self.title_field,
                ], spacing=4, expand=1),
            ]),
            
            # Row 2: Author + Category
            ft.Row([
                ft.Column([
                    ft.Text("Author", size=12, color="#374151"),
                    self.author_field,
                ], spacing=4, expand=1),
                ft.Container(width=16),
                ft.Column([
                    ft.Text("Category / Genre", size=12, color="#374151"),
                    self.category_field,
                ], spacing=4, expand=1),
            ]),
            
            # Row 3: Summary - FULL WIDTH
            ft.Column([
                ft.Text("Summary / Description", size=12, color="#374151"),
                self.summary_field,
            ], spacing=4),
            
            # Row 4: Publisher + Publication year
            ft.Row([
                ft.Column([
                    ft.Text("Publisher", size=12, color="#374151"),
                    self.publisher_field,
                ], spacing=4, expand=1),
                ft.Container(width=16),
                ft.Column([
                    ft.Text("Publication year", size=12, color="#374151"),
                    self.year_field,
                ], spacing=4, expand=1),
            ]),
            
            # Row 5: Pages + Price
            ft.Row([
                ft.Column([
                    ft.Text("Pages", size=12, color="#374151"),
                    self.pages_field,
                ], spacing=4, expand=1),
                ft.Container(width=16),
                ft.Column([
                    ft.Text("Price (VND)", size=12, color="#374151"),
                    self.price_field,
                ], spacing=4, expand=1),
            ]),
            
            # Row 6: Total copies + Available copies
            ft.Row([
                ft.Column([
                    ft.Text("Total copies", size=12, color="#374151"),
                    self.total_field,
                ], spacing=4, expand=1),
                ft.Container(width=16),
                ft.Column([
                    ft.Text("Available copies", size=12, color="#374151"),
                    self.available_field,
                ], spacing=4, expand=1),
            ]),
            
            # Row 7: Cover URL - FULL WIDTH
            ft.Column([
                ft.Text("Cover image URL (public)", size=12, color="#374151"),
                self.cover_url_field,
            ], spacing=4),
            
            # Row 8: Status + Save button
            ft.Row([
                ft.Column([
                    ft.Text("Status", size=12, color="#374151"),
                    self.status_field,
                ], spacing=4, expand=1),
                ft.Container(width=16),
                ft.Container(
                    content=ft.ElevatedButton(
                        "Save book",
                        bgcolor="#2563EB",
                        color="#FFFFFF",
                        height=40,
                        expand=True,
                        on_click=self.save_book,
                    ),
                    expand=1,
                    padding=ft.Padding(0, 18, 0, 0),
                ),
            ]),
        ], spacing=12)
    
    def _build_toolbar(self):
        """Search toolbar"""
        return ft.Container(
            content=ft.Row([
                ft.TextField(
                    hint_text="",
                    border_radius=999,
                    border_color="#D1D5DB",
                    text_size=14,
                    height=40,
                    expand=True,
                ),
                ft.Dropdown(
                    options=[
                        ft.dropdown.Option("all", "All fields"),
                        ft.dropdown.Option("isbn", "ISBN"),
                        ft.dropdown.Option("title", "Title"),
                        ft.dropdown.Option("author", "Author"),
                    ],
                    value="all",
                    border_radius=999,
                    border_color="#D1D5DB",
                    text_size=13,
                    width=140,
                    height=40,
                ),
                ft.ElevatedButton(
                    "Search",
                    bgcolor="#2563EB",
                    color="#FFFFFF",
                    height=40,
                ),
            ], spacing=8),
            margin=ft.Margin(0, 10, 0, 10),
        )
    
    def _build_table(self):
        """Table với scroll ngang"""
        books = [
            {
                "isbn": "978-1-9821-8582-4",
                "title": "Chain of Gold",
                "author": "Cassandra Clare",
                "category": "Fantasy, Young Adult",
                "publisher": "Margaret K. McElderry Books",
                "year": "2020",
                "pages": "592",
                "price": "250000",
                "total": "5",
                "available": "3",
                "status": "Available",
            },
            {
                "isbn": "978-0-385-54792-5",
                "title": "Harlem Shuffle",
                "author": "Colson Whitehead",
                "category": "Historical fiction",
                "publisher": "Doubleday",
                "year": "2021",
                "pages": "336",
                "price": "300000",
                "total": "3",
                "available": "0",
                "status": "Not available",
            },
        ]
        
        rows = []
        for book in books:
            is_available = book["status"] == "Available"
            price_val = int(book["price"])
            price_formatted = f"{price_val:,}".replace(",", ".") + " đ"
            
            rows.append(
                ft.DataRow(cells=[
                    # Image
                    ft.DataCell(ft.Container(width=40, height=50, bgcolor="#E5E7EB", border_radius=4)),
                    # ISBN
                    ft.DataCell(ft.Text(book["isbn"], size=12, color="#374151", no_wrap=False)),
                    # Title
                    ft.DataCell(ft.Text(book["title"], size=12, color="#374151")),
                    # Author
                    ft.DataCell(ft.Text(book["author"], size=12, color="#374151")),
                    # Category
                    ft.DataCell(ft.Text(book["category"], size=12, color="#374151", no_wrap=False)),
                    # Publisher
                    ft.DataCell(ft.Text(book["publisher"], size=12, color="#374151", no_wrap=False)),
                    # Year
                    ft.DataCell(ft.Text(book["year"], size=12, color="#374151")),
                    # Pages
                    ft.DataCell(ft.Text(book["pages"], size=12, color="#374151")),
                    # Price
                    ft.DataCell(ft.Text(price_formatted, size=12, color="#374151")),
                    # Total
                    ft.DataCell(ft.Text(book["total"], size=12, color="#374151")),
                    # Available
                    ft.DataCell(ft.Text(book["available"], size=12, color="#374151")),
                    # Status
                    ft.DataCell(
                        ft.Container(
                            content=ft.Text(
                                book["status"], 
                                size=11, 
                                color="#15803D" if is_available else "#B91C1C",
                                weight=ft.FontWeight.W_500
                            ),
                            bgcolor="#DCFCE7" if is_available else "#FEE2E2",
                            padding=ft.Padding(10, 4, 10, 4),
                            border_radius=4,
                        )
                    ),
                    # Actions
                    ft.DataCell(
                        ft.Row([
                            ft.ElevatedButton(
                                "Edit", 
                                bgcolor="#3B82F6", 
                                color="#FFFFFF", 
                                height=36,
                                on_click=lambda e, b=book: self.edit_book(b, e),
                                style=ft.ButtonStyle(
                                    shape=ft.RoundedRectangleBorder(radius=20),
                                    padding=ft.Padding(24, 0, 24, 0),
                                ),
                            ),
                            ft.ElevatedButton(
                                "Delete", 
                                bgcolor="#EF4444", 
                                color="#FFFFFF", 
                                height=36,
                                style=ft.ButtonStyle(
                                    shape=ft.RoundedRectangleBorder(radius=20),
                                    padding=ft.Padding(24, 0, 24, 0),
                                ),
                            ),
                        ], spacing=8)
                    ),
                ])
            )
        
        table = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("IMAGE", size=11, color="#9CA3AF", weight=ft.FontWeight.W_600)),
                ft.DataColumn(ft.Text("ISBN", size=11, color="#9CA3AF", weight=ft.FontWeight.W_600)),
                ft.DataColumn(ft.Text("TITLE", size=11, color="#9CA3AF", weight=ft.FontWeight.W_600)),
                ft.DataColumn(ft.Text("AUTHOR", size=11, color="#9CA3AF", weight=ft.FontWeight.W_600)),
                ft.DataColumn(ft.Text("CATEGORY", size=11, color="#9CA3AF", weight=ft.FontWeight.W_600)),
                ft.DataColumn(ft.Text("PUBLISHER", size=11, color="#9CA3AF", weight=ft.FontWeight.W_600)),
                ft.DataColumn(ft.Text("PUBLICATION YEAR", size=11, color="#9CA3AF", weight=ft.FontWeight.W_600)),
                ft.DataColumn(ft.Text("PAGES", size=11, color="#9CA3AF", weight=ft.FontWeight.W_600)),
                ft.DataColumn(ft.Text("PRICE (VND)", size=11, color="#9CA3AF", weight=ft.FontWeight.W_600)),
                ft.DataColumn(ft.Text("TOTAL COPIES", size=11, color="#9CA3AF", weight=ft.FontWeight.W_600)),
                ft.DataColumn(ft.Text("AVAILABLE COPIES", size=11, color="#9CA3AF", weight=ft.FontWeight.W_600)),
                ft.DataColumn(ft.Text("STATUS", size=11, color="#9CA3AF", weight=ft.FontWeight.W_600)),
                ft.DataColumn(ft.Text("ACTIONS", size=11, color="#9CA3AF", weight=ft.FontWeight.W_600)),
            ],
            rows=rows,
            horizontal_lines=ft.BorderSide(1, "#E5E7EB"),
            heading_row_height=36,
            data_row_min_height=56,
            column_spacing=20,
        )
        
        # Wrap table trong Row để scroll ngang
        return ft.Row(
            [table],
            scroll=ft.ScrollMode.AUTO,
        )
    
    def save_book(self, e):
        """Save book"""
        print(f"Save: {self.isbn_field.value} - {self.title_field.value}")
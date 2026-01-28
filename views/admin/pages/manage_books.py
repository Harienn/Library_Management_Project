# views/admin/pages/manage_books.py
import flet as ft
from database.db import execute_query, fetch_one, get_last_insert_id
from services.book_service import search_books
from services.book_service import delete_book_by_isbn
from services.book_service import (
    insert_book,
    update_book,
    get_book_by_isbn
)

class ManageBooksPage:
    def __init__(self):
        self.current_isbn = None
        self.page_ref = None  # Thêm reference đến page
        

    def build(self, page: ft.Page = None):
        if page:
            self.page_ref = page

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
        """Reset form về trạng thái ban đầu"""
        print("=== DEBUG: Resetting form ===")
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
        
        # Cập nhật UI
        if hasattr(self, 'isbn_field'):
            self.isbn_field.update()
            self.title_field.update()
            self.author_field.update()
            self.category_field.update()
            self.summary_field.update()
            self.publisher_field.update()
            self.year_field.update()
            self.pages_field.update()
            self.price_field.update()
            self.total_field.update()
            self.available_field.update()
            self.cover_url_field.update()
            self.status_field.update()
        
        if e and hasattr(e, 'page'):
            e.page.update()
        elif self.page_ref:
            self.page_ref.update()
    
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
        self.search_input = ft.TextField(
            hint_text="Search...",
            border_radius=999,
            border_color="#D1D5DB",
            text_size=14,
            height=40,
            expand=True,
        )

        self.search_type = ft.Dropdown(
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
        )

        return ft.Container(
            content=ft.Row([
                self.search_input,
                self.search_type,
                ft.ElevatedButton(
                    "Search",
                    bgcolor="#2563EB",
                    color="#FFFFFF",
                    height=40,
                    on_click=self.search_books_action,
                ),
            ], spacing=8),
            margin=ft.Margin(0, 10, 0, 10),
        )
    
    def _build_table(self):
        """Table với scroll ngang"""
        # === LẤY DỮ LIỆU TỪ DATABASE ===
        result = search_books(
            keyword=None,
            category_id=None,
            publish_year=None,
            status=None,
            page=1,
            per_page=15
        )

        # Map dữ liệu DB -> format UI (KHÔNG SỬA UI)
        books = []
        for b in result["books"]:
            books.append({
                "isbn": b["isbn"],
                "title": b["title"],
                "author": b["author_name"],
                "category": b["category_name"],
                "publisher": b["publisher"],
                "year": str(b["publish_date"]) if b["publish_date"] else "",
                "pages": str(b.get("pages", "")) if "pages" in b else "",
                "price": str(b["price"]) if b["price"] else "0",
                "total": str(b["total_copies"]),
                "available": str(b["available_copies"]),
                "status": "Available" if b["availability_status"] == "AVAILABLE" else "Not available",
            })
        
        rows = []
        for book in books:
            is_available = book["status"] == "Available"
            price_val = int(float(book["price"]))
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
                                on_click=lambda e, b=book: self.confirm_delete(b["isbn"]),
                                style=ft.ButtonStyle(
                                    shape=ft.RoundedRectangleBorder(radius=20),
                                    padding=ft.Padding(24, 0, 24, 0),
                                ),
                            ),
                        ], spacing=8)
                    ),
                ])
            )
        
        self.table = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("IMAGE")),
                ft.DataColumn(ft.Text("ISBN")),
                ft.DataColumn(ft.Text("TITLE")),
                ft.DataColumn(ft.Text("AUTHOR")),
                ft.DataColumn(ft.Text("CATEGORY")),
                ft.DataColumn(ft.Text("PUBLISHER")),
                ft.DataColumn(ft.Text("PUBLICATION YEAR")),
                ft.DataColumn(ft.Text("PAGES")),
                ft.DataColumn(ft.Text("PRICE (VND)")),
                ft.DataColumn(ft.Text("TOTAL COPIES")),
                ft.DataColumn(ft.Text("AVAILABLE COPIES")),
                ft.DataColumn(ft.Text("STATUS")),
                ft.DataColumn(ft.Text("ACTIONS")),
            ],
            rows=rows,
            horizontal_lines=ft.BorderSide(1, "#E5E7EB"),
            heading_row_height=36,
            data_row_min_height=56,
            column_spacing=20,
        )

        return ft.Row([self.table], scroll=ft.ScrollMode.AUTO)
        
    def search_books_action(self, e):
        keyword = self.search_input.value.strip()
        search_type = self.search_type.value

        if not keyword:
            self.keyword = None
        else:
            # search_books chỉ cần keyword, service đã search all
            self.keyword = keyword

        self.refresh_table()
    
    def load_books(self):
        result = search_books(
            keyword=None,
            page=1,
            per_page=50
        )
        return result["books"]
    
    def save_book(self, e):
        try:
            print("=== DEBUG: Starting save_book ===")
            
            data = {
                "isbn": self.isbn_field.value.strip(),
                "title": self.title_field.value.strip(),
                "author": self.author_field.value.strip(),
                "category": self.category_field.value.strip(),
                "publisher": self.publisher_field.value.strip(),
                "publish_year": self.year_field.value.strip(),
                "pages": self.pages_field.value.strip(),
                "price": self.price_field.value.strip(),
                "total": self.total_field.value.strip(),
                "available": self.available_field.value.strip(),
                "summary": self.summary_field.value.strip(),
                "cover_url": self.cover_url_field.value.strip(),
                "status": self.status_field.value.strip(),
            }
            
            print(f"=== DEBUG: Data to save: {data} ===")
            print(f"=== DEBUG: Current ISBN: {self.current_isbn} ===")
            
            # Validate required fields
            if not data["isbn"]:
                print("=== DEBUG: ISBN is empty ===")
                self.show_error("ISBN is required")
                return
                
            if not data["title"]:
                print("=== DEBUG: Title is empty ===")
                self.show_error("Title is required")
                return
            
            if self.current_isbn:
                # Update existing book
                print("=== DEBUG: Calling update_book ===")
                success = update_book(data)
                print(f"=== DEBUG: Update result: {success} ===")
                if success:
                    self.show_success("Book updated successfully")
                    self.reset_form()
                else:
                    self.show_error("Failed to update book")
            else:
                # Insert new book
                print("=== DEBUG: Calling insert_book ===")
                book_id = insert_book(data)
                print(f"=== DEBUG: Insert result - Book ID: {book_id} ===")
                if book_id:
                    self.show_success(f"Book added successfully (ID: {book_id})")
                    self.reset_form()
                else:
                    self.show_error("Failed to add book")
            
            # Refresh table
            print("=== DEBUG: Refreshing table ===")
            self.refresh_table()
            
        except Exception as ex:
            print(f"=== DEBUG: Exception in save_book: {ex} ===")
            import traceback
            traceback.print_exc()
            self.show_error(f"Error saving book: {str(ex)}")
            
        except Exception as ex:
            print(f"Error saving book: {ex}")
            self.show_error(f"Error saving book: {str(ex)}")
    
    def delete_book(self, isbn, e):
        delete_book_by_isbn(isbn)
        self.page_ref.update()
    
    def confirm_delete(self, isbn):
        def yes(e):
            delete_book_by_isbn(isbn)
            self.refresh_table()
            self.page_ref.dialog.open = False

        self.page_ref.dialog = ft.AlertDialog(
            title=ft.Text("Confirm delete"),
            content=ft.Text("Are you sure you want to delete this book?"),
            actions=[
                ft.TextButton("Cancel"),
                ft.TextButton("Delete", on_click=yes),
            ],
        )
        self.page_ref.dialog.open = True

    def refresh_table(self):
        result = search_books(
            keyword=self.keyword if hasattr(self, "keyword") else None,
            page=1,
            per_page=15
        )

        # reload page
        self.page_ref.views.clear()
        self.page_ref.views.append(self.build(self.page_ref))
        self.page_ref.update()
        
    def show_success(self, message):
        """Hiển thị thông báo thành công"""
        print(f"=== DEBUG show_success: {message} ===")
        if self.page_ref:
            self.page_ref.snack_bar = ft.SnackBar(
                content=ft.Text(message, color="#FFFFFF"),
                bgcolor="#10B981",
            )
            self.page_ref.snack_bar.open = True
            self.page_ref.update()
        else:
            print("=== DEBUG: No page_ref available ===")

    def show_error(self, message):
        """Hiển thị thông báo lỗi"""
        print(f"=== DEBUG show_error: {message} ===")
        if self.page_ref:
            self.page_ref.snack_bar = ft.SnackBar(
                content=ft.Text(message, color="#FFFFFF"),
                bgcolor="#EF4444",
            )
            self.page_ref.snack_bar.open = True
            self.page_ref.update()
        else:
            print("=== DEBUG: No page_ref available ===")
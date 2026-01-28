# views/admin/pages/manage_books.py
import flet as ft
from services.book_service import search_books, insert_book, update_book, delete_book_by_isbn

class ManageBooksPage:
    def __init__(self):
        self.current_isbn = None
        self.page_ref = None
        self.keyword = None
        self.table_holder = ft.Container()
        
        # Khởi tạo các field MỘT LẦN DUY NHẤT
        self._create_fields()
    
    def _create_fields(self):
        """Khởi tạo các field control một lần duy nhất"""
        # Text fields
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
        
        # Dropdown field
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
        
        # Search fields
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
    
    def build(self, page: ft.Page = None):
        if page:
            self.page_ref = page
        
        # Tạo table holder với dữ liệu ban đầu
        self.table_holder.content = self._build_table()
        
        # Xây dựng form layout với các field đã tạo
        form_content = self._build_form()
        
        # Xây dựng giao diện hoàn chỉnh
        content = ft.Column([
            # Header
            ft.Row([
                ft.Text("Book list", size=16, weight=ft.FontWeight.BOLD, color="#1F2937"),
                ft.Container(expand=True),
                ft.TextButton(
                    "Refresh",
                    style=ft.ButtonStyle(color="#4B5563"),
                    on_click=lambda _: self.refresh_table()
                ),
                ft.ElevatedButton(
                    "+ Add book",
                    bgcolor="#E5E7EB",
                    color="#111827",
                    on_click=self.reset_form,
                ),
            ]),
            
            ft.Text(
                "Search by ISBN, title or author. Use the form above to add or edit book details.",
                size=12, color="#6B7280",
            ),
            
            ft.Container(height=8),
            
            # Form
            form_content,
            
            # Search toolbar
            self._build_toolbar(),
            
            # Table holder
            self.table_holder,
            
            # Footer note
            ft.Text(
                "Status is simplified to Available and Not available.",
                size=11, color="#6B7280", italic=True,
            ),
        ], spacing=10)
        
        self.main_container = ft.Container(
            content=content,
            padding=ft.Padding(14, 14, 16, 16),
            bgcolor="#FFFFFF",
            border_radius=14,
            border=ft.Border.all(1, "#E5E7EB"),
        )
        
        return self.main_container
    
    def _build_form(self):
        """Xây dựng form layout với các field đã tạo sẵn"""
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
        """Xây dựng thanh công cụ tìm kiếm"""
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
    
    def reset_form(self, e=None):
        """Reset form về trạng thái ban đầu"""
        print("=== DEBUG: Resetting form ===")
        
        self.current_isbn = None
        
        # Clear tất cả các field
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
        
        # Update UI
        if self.page_ref:
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
            
            self.page_ref.update()
    
    def edit_book(self, book_data, e):
        """Load dữ liệu sách vào form để chỉnh sửa"""
        print(f"=== DEBUG edit_book: Editing book with ISBN {book_data['isbn']} ===")
        
        try:
            # Lưu ISBN hiện tại
            self.current_isbn = book_data["isbn"]
            
            # Điền dữ liệu vào các field
            self.isbn_field.value = book_data["isbn"]
            self.title_field.value = book_data["title"]
            self.author_field.value = book_data["author"]
            self.category_field.value = book_data["category"]
            self.summary_field.value = book_data.get("summary", "")
            self.publisher_field.value = book_data["publisher"]
            self.year_field.value = str(book_data["year"]) if book_data["year"] else ""
            self.pages_field.value = str(book_data["pages"]) if book_data["pages"] else ""
            
            # Xử lý giá tiền
            try:
                price_str = book_data["price"]
                if isinstance(price_str, str):
                    # Loại bỏ " đ" và dấu phân cách
                    price_str = price_str.replace("đ", "").replace(".", "").strip()
                    price_val = int(price_str) if price_str else 0
                else:
                    price_val = int(price_str) if price_str else 0
                self.price_field.value = str(price_val)
            except:
                self.price_field.value = "0"
            
            self.total_field.value = str(book_data["total"])
            self.available_field.value = str(book_data["available"])
            self.cover_url_field.value = book_data.get("cover_url", "")
            
            # Xử lý status
            status_value = book_data["status"]
            if status_value in ["Available", "AVAILABLE"]:
                self.status_field.value = "Available"
            else:
                self.status_field.value = "Not available"
            
            # Update UI
            if e and hasattr(e, 'page'):
                e.page.update()
            elif self.page_ref:
                self.page_ref.update()
            
            print(f"=== DEBUG: Form loaded successfully ===")
            print(f"  - ISBN: {self.isbn_field.value}")
            print(f"  - Title: {self.title_field.value}")
            
        except Exception as ex:
            print(f"=== DEBUG edit_book error: {ex}")
            self.show_error(f"Error loading book data: {str(ex)}")
    
    def save_book(self, e):
        """Lưu sách vào database"""
        print("=== DEBUG save_book: Starting save process ===")
        
        try:
            # Lấy và validate dữ liệu
            isbn = self.isbn_field.value.strip()
            title = self.title_field.value.strip()
            
            if not isbn:
                self.show_error("ISBN is required!")
                return
                
            if not title:
                self.show_error("Title is required!")
                return
            
            # Chuẩn bị dữ liệu
            data = {
                "isbn": isbn,
                "title": title,
                "author": self.author_field.value.strip(),
                "category": self.category_field.value.strip(),
                "publisher": self.publisher_field.value.strip(),
                "publish_year": self._safe_int(self.year_field.value),
                "pages": self._safe_int(self.pages_field.value),
                "price": self._safe_int(self.price_field.value),
                "total": self._safe_int(self.total_field.value),
                "available": self._safe_int(self.available_field.value),
                "summary": self.summary_field.value.strip(),
                "cover_url": self.cover_url_field.value.strip(),
                "status": "AVAILABLE" if self.status_field.value == "Available" else "NOT_AVAILABLE",
            }
            
            print(f"=== DEBUG: Data to save: {data}")
            
            # Xác định là thêm mới hay cập nhật
            if self.current_isbn and self.current_isbn == isbn:
                # Đang edit cùng một ISBN
                print("=== DEBUG: Updating existing book ===")
                success = update_book(data)
                message = "Book updated successfully!"
            else:
                # Thêm mới hoặc ISBN bị thay đổi
                print("=== DEBUG: Adding new book ===")
                success = insert_book(data)
                message = "New book added successfully!"
            
            # Xử lý kết quả
            if success:
                self.show_success(message)
                self.current_isbn = None
                self.refresh_table()
            else:
                self.show_error("Failed to save book. Please check the ISBN (might be duplicate).")
                
        except Exception as ex:
            print(f"=== DEBUG save_book error: {ex}")
            self.show_error(f"System error: {str(ex)}")
    
    def _safe_int(self, value):
        """Chuyển đổi an toàn sang integer"""
        try:
            if not value:
                return 0
            if isinstance(value, str):
                # Loại bỏ tất cả ký tự không phải số
                clean_value = ''.join(filter(str.isdigit, value))
                return int(clean_value) if clean_value else 0
            return int(value)
        except:
            return 0
    
    def search_books_action(self, e):
        """Xử lý tìm kiếm sách"""
        keyword = self.search_input.value.strip()
        search_type = self.search_type.value
        
        print(f"=== DEBUG search_books_action: Searching '{keyword}' (type: {search_type}) ===")
        
        if not keyword:
            self.keyword = None
        else:
            self.keyword = keyword
        
        self.refresh_table()
    
    def _build_table(self):
        """Xây dựng bảng dữ liệu sách"""
        print("=== DEBUG _build_table: Building table ===")
        
        try:
            # Lấy dữ liệu từ database
            result = search_books(
                keyword=self.keyword,
                category_id=None,
                publish_year=None,
                status=None,
                page=1,
                per_page=15
            )
            
            books = result.get("books", [])
            print(f"=== DEBUG: Found {len(books)} books ===")
            
            # Tạo rows cho DataTable
            rows = []
            for book in books:
                try:
                    # Map dữ liệu
                    isbn = book.get("isbn", "")
                    title = book.get("title", "")
                    author = book.get("author_name", book.get("author", ""))
                    category = book.get("category_name", book.get("category", ""))
                    publisher = book.get("publisher", "")
                    year = str(book.get("publish_date", ""))
                    
                    # Price formatting
                    price = book.get("price", 0)
                    try:
                        price_val = int(float(price)) if price else 0
                        price_formatted = f"{price_val:,}".replace(",", ".") + " đ"
                    except:
                        price_formatted = "0 đ"
                    
                    total = str(book.get("total_copies", 0))
                    available = str(book.get("available_copies", 0))
                    
                    # Status
                    status = book.get("status", "")
                    availability = book.get("availability_status", "")
                    
                    if availability == "AVAILABLE" or status == "Available":
                        status_text = "Available"
                        status_color = "#15803D"
                        status_bg = "#DCFCE7"
                    else:
                        status_text = "Not available"
                        status_color = "#B91C1C"
                        status_bg = "#FEE2E2"
                    
                    # Tạo row
                    row = ft.DataRow(cells=[
                        # Image
                        ft.DataCell(ft.Container(width=40, height=50, bgcolor="#E5E7EB", border_radius=4)),
                        # ISBN
                        ft.DataCell(ft.Text(isbn, size=12, color="#374151")),
                        # Title
                        ft.DataCell(ft.Text(title, size=12, color="#374151")),
                        # Author
                        ft.DataCell(ft.Text(author, size=12, color="#374151")),
                        # Category
                        ft.DataCell(ft.Text(category, size=12, color="#374151")),
                        # Publisher
                        ft.DataCell(ft.Text(publisher, size=12, color="#374151")),
                        # Year
                        ft.DataCell(ft.Text(year, size=12, color="#374151")),
                        # Pages (not in data, leave empty)
                        ft.DataCell(ft.Text("", size=12, color="#374151")),
                        # Price
                        ft.DataCell(ft.Text(price_formatted, size=12, color="#374151")),
                        # Total
                        ft.DataCell(ft.Text(total, size=12, color="#374151")),
                        # Available
                        ft.DataCell(ft.Text(available, size=12, color="#374151")),
                        # Status
                        ft.DataCell(
                            ft.Container(
                                content=ft.Text(
                                    status_text, 
                                    size=11, 
                                    color=status_color,
                                    weight=ft.FontWeight.W_500
                                ),
                                bgcolor=status_bg,
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
                                    on_click=lambda e, b=book: self._prepare_edit_book(b, e),
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
                                    on_click=lambda e, b=book: self.confirm_delete(b.get("isbn", ""), e),
                                    style=ft.ButtonStyle(
                                        shape=ft.RoundedRectangleBorder(radius=20),
                                        padding=ft.Padding(24, 0, 24, 0),
                                    ),
                                ),
                            ], spacing=8)
                        ),
                    ])
                    rows.append(row)
                    
                except Exception as ex:
                    print(f"=== DEBUG: Error processing book row: {ex}")
                    continue
            
            # Tạo DataTable
            table = ft.DataTable(
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
            
            return ft.Row([table], scroll=ft.ScrollMode.AUTO)
            
        except Exception as ex:
            print(f"=== DEBUG _build_table error: {ex}")
            return ft.Text(f"Error loading table: {str(ex)}", color="red")
    
    def _prepare_edit_book(self, book_data, e):
        """Chuẩn bị dữ liệu trước khi edit"""
        print(f"=== DEBUG _prepare_edit_book: Preparing to edit ===")
        
        # Chuẩn bị dữ liệu theo định dạng mong đợi
        formatted_data = {
            "isbn": book_data.get("isbn", ""),
            "title": book_data.get("title", ""),
            "author": book_data.get("author_name", book_data.get("author", "")),
            "category": book_data.get("category_name", book_data.get("category", "")),
            "publisher": book_data.get("publisher", ""),
            "year": book_data.get("publish_date", ""),
            "pages": book_data.get("pages", ""),
            "price": str(book_data.get("price", "0")),
            "total": str(book_data.get("total_copies", "0")),
            "available": str(book_data.get("available_copies", "0")),
            "summary": book_data.get("summary", ""),
            "cover_url": book_data.get("image_url", book_data.get("cover_url", "")),
            "status": book_data.get("availability_status", book_data.get("status", "Available")),
        }
        
        # Gọi hàm edit chính
        self.edit_book(formatted_data, e)
    
    def confirm_delete(self, isbn, e=None):
        """Hiển thị dialog xác nhận xóa"""
        if not isbn:
            self.show_error("No ISBN provided for deletion")
            return
        
        def yes_action(e):
            try:
                print(f"=== DEBUG: Deleting book with ISBN {isbn} ===")
                
                # Đóng dialog
                if self.page_ref and hasattr(self.page_ref, 'dialog'):
                    self.page_ref.dialog.open = False
                    self.page_ref.update()
                
                # Thực hiện xóa
                success = delete_book_by_isbn(isbn)
                
                if success:
                    self.show_success(f"Book {isbn} deleted successfully!")
                    # Refresh table
                    self.refresh_table()
                else:
                    self.show_error(f"Failed to delete book {isbn}")
                    
            except Exception as ex:
                self.show_error(f"Error deleting book: {str(ex)}")
        
        def cancel_action(e):
            if self.page_ref and hasattr(self.page_ref, 'dialog'):
                self.page_ref.dialog.open = False
                self.page_ref.update()
        
        # Tạo dialog
        if self.page_ref:
            self.page_ref.dialog = ft.AlertDialog(
                modal=True,
                title=ft.Text("Confirm Delete"),
                content=ft.Text(f"Are you sure you want to delete the book with ISBN: {isbn}?\nThis action cannot be undone."),
                actions=[
                    ft.TextButton("Cancel", on_click=cancel_action),
                    ft.TextButton("Delete", on_click=yes_action, style=ft.ButtonStyle(color="#EF4444")),
                ],
            )
            self.page_ref.dialog.open = True
            self.page_ref.update()
    
    def refresh_table(self):
        """Làm mới bảng dữ liệu"""
        print("=== DEBUG refresh_table: Refreshing table ===")
        
        try:
            # Vẽ lại bảng
            new_table_content = self._build_table()
            
            # Cập nhật holder
            self.table_holder.content = new_table_content
            
            # Update UI
            if self.page_ref:
                self.table_holder.update()
                self.page_ref.update()
                
            print("=== DEBUG: Table refreshed successfully ===")
            
        except Exception as ex:
            print(f"=== DEBUG refresh_table error: {ex}")
    
    def show_success(self, message):
        """Hiển thị thông báo thành công"""
        print(f"=== SUCCESS: {message} ===")
        
        if self.page_ref:
            self.page_ref.snack_bar = ft.SnackBar(
                content=ft.Text(message, color="#FFFFFF"),
                bgcolor="#10B981",
                duration=3000,
            )
            self.page_ref.snack_bar.open = True
            self.page_ref.update()
    
    def show_error(self, message):
        """Hiển thị thông báo lỗi"""
        print(f"=== ERROR: {message} ===")
        
        if self.page_ref:
            self.page_ref.snack_bar = ft.SnackBar(
                content=ft.Text(message, color="#FFFFFF"),
                bgcolor="#EF4444",
                duration=3000,
            )
            self.page_ref.snack_bar.open = True
            self.page_ref.update()
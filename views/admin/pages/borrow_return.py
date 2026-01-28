import flet as ft
from datetime import datetime, timedelta
from database.db import fetch_one, fetch_all, execute
from services.borrow_service import (
    create_borrow_transaction, 
    return_book, 
    get_all_active_transactions,
    get_overdue_transactions
)
from services.book_service import get_book_detail


class BorrowReturnPage:
    def __init__(self, page: ft.Page, current_user):
        self.page = page
        self.current_user = current_user
        self.current_tab = "borrow"
        self.selected_books = []
        self.member_info = None
        self.active_transactions = []
        
    def build(self):
        # Custom tab buttons
        self.borrow_tab_btn = ft.Container(
            content=ft.Text(
                "Manage Borrowing Books", 
                size=14, 
                color="#111827",
                weight=ft.FontWeight.W_400
            ),
            padding=ft.padding.symmetric(horizontal=20, vertical=12),
            bgcolor="#FFFFFF",
            border=ft.border.all(1, "#E5E7EB"),
            border_radius=25,
            on_click=lambda e: self.switch_tab("borrow", e),
        )
        
        self.return_tab_btn = ft.Container(
            content=ft.Text(
                "Manage Return Books", 
                size=14, 
                color="#6B7280",
                weight=ft.FontWeight.W_400
            ),
            padding=ft.padding.symmetric(horizontal=20, vertical=12),
            bgcolor="#F3F4F6",
            border_radius=25,
            on_click=lambda e: self.switch_tab("return", e),
        )
        
        tabs_row = ft.Container(
            content=ft.Row([
                self.borrow_tab_btn,
                self.return_tab_btn,
            ], spacing=8, tight=True),
            padding=4,
            bgcolor="#F3F4F6",
            border_radius=25,
        )
        
        # Content area
        self.content_area = ft.Container(
            content=self._build_borrow_content(),
            padding=20,
            bgcolor="#F9FAFB",
        )
        
        return ft.Container(
            content=ft.Column([
                # Header
                ft.Row([
                    ft.Text(
                        "Borrowing & Return", 
                        size=18, 
                        weight=ft.FontWeight.BOLD, 
                        color="#1F2937"
                    ),
                    ft.Container(expand=True),
                ]),
                ft.Container(height=16),
                
                # Tabs
                tabs_row,
                
                # Content
                self.content_area,
            ], spacing=0),
            padding=20,
            bgcolor="#FFFFFF",
        )
    
    def switch_tab(self, tab_name, e):
        """Switch between tabs"""
        if tab_name == "borrow":
            self.current_tab = "borrow"
            self.borrow_tab_btn.bgcolor = "#FFFFFF"
            self.borrow_tab_btn.border = ft.border.all(1, "#E5E7EB")
            self.borrow_tab_btn.content.color = "#111827"
            self.return_tab_btn.bgcolor = "#F3F4F6"
            self.return_tab_btn.border = None
            self.return_tab_btn.content.color = "#6B7280"
            self.content_area.content = self._build_borrow_content()
        else:
            self.current_tab = "return"
            self.return_tab_btn.bgcolor = "#FFFFFF"
            self.return_tab_btn.border = ft.border.all(1, "#E5E7EB")
            self.return_tab_btn.content.color = "#111827"
            self.borrow_tab_btn.bgcolor = "#F3F4F6"
            self.borrow_tab_btn.border = None
            self.borrow_tab_btn.content.color = "#6B7280"
            self.content_area.content = self._build_return_content()
        
        self.page.update()
    
    # ============ MANAGE BORROWING BOOKS ============
    
    def _build_borrow_content(self):
        """Content for Manage Borrowing Books tab"""
        return ft.Column([
            self._build_create_borrowing(),
            ft.Container(height=24),
            self._build_current_borrowing_table(),
        ], spacing=0, scroll=ft.ScrollMode.AUTO)
    
    def _build_create_borrowing(self):
        """Form to create borrowing transaction"""
        
        self.member_email_field = ft.TextField(
            hint_text="member@example.com",
            border_color="#D1D5DB",
            text_size=13,
            border_radius=20,
            height=40,
            content_padding=10,
            expand=True,
        )
        
        self.member_id_field = ft.TextField(
            hint_text="123",
            border_color="#D1D5DB",
            text_size=13,
            border_radius=20,
            height=40,
            width=120,
            content_padding=10,
        )
        
        check_member_btn = ft.ElevatedButton(
            "Check member",
            bgcolor="#3B82F6",
            color="#FFFFFF",
            height=40,
            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=20)),
            on_click=self.check_member,
        )
        
        # Member details container (initially hidden)
        self.member_details = ft.Container(
            content=ft.Column([
                ft.Text("Member details", size=12, color="#374151", weight=ft.FontWeight.W_600),
                ft.Container(height=8),
                self._build_member_info_placeholder(),
            ], spacing=0),
            padding=16,
            bgcolor="#F0F9FF",
            border_radius=8,
            border=ft.border.all(1, "#BFDBFE"),
            visible=False,
        )
        
        self.book_isbn_field = ft.TextField(
            hint_text="978-... or Book ID",
            border_color="#D1D5DB",
            text_size=13,
            border_radius=20,
            height=40,
            content_padding=10,
            expand=True,
        )
        
        self.created_date_field = ft.TextField(
            value=datetime.now().strftime("%m/%d/%Y"),
            border_color="#D1D5DB",
            text_size=13,
            border_radius=20,
            height=40,
            width=150,
            content_padding=10,
            read_only=True,
        )
        
        add_book_btn = ft.ElevatedButton(
            "Add book",
            bgcolor="#E5E7EB",
            color="#374151",
            height=40,
            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=20)),
            on_click=self.add_book_to_slip,
        )
        
        # Books in slip table
        self.books_table_container = ft.Container(
            content=ft.Column([
                ft.Text("No books added yet", size=12, color="#9CA3AF", text_align=ft.TextAlign.CENTER),
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            padding=20,
            border=ft.border.all(1, "#E5E7EB"),
            border_radius=6,
        )
        
        confirm_borrowing_btn = ft.ElevatedButton(
            "Confirm borrowing",
            bgcolor="#3B82F6",
            color="#FFFFFF",
            height=40,
            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=20)),
            on_click=self.confirm_borrowing,
        )
        
        return ft.Container(
            content=ft.Column([
                ft.Text("Create borrowing transaction", size=14, weight=ft.FontWeight.BOLD, color="#111827"),
                ft.Text("Start a new borrowing slip using member email or member ID, then add books and created date.", size=12, color="#6B7280"),
                ft.Container(height=12),
                
                # Member search
                ft.Row([
                    ft.Column([
                        ft.Text("Member email", size=12, color="#374151"),
                        ft.Container(height=4),
                        self.member_email_field,
                    ], spacing=0, expand=True),
                    ft.Container(content=ft.Text("or", size=12, color="#9CA3AF"), padding=ft.padding.only(top=24)),
                    ft.Column([
                        ft.Text("Member ID", size=12, color="#374151"),
                        ft.Container(height=4),
                        self.member_id_field,
                    ], spacing=0),
                    ft.Container(padding=ft.padding.only(top=18), content=check_member_btn),
                ], spacing=8),
                
                ft.Container(height=12),
                self.member_details,
                ft.Container(height=16),
                
                # Book input
                ft.Row([
                    ft.Column([
                        ft.Text("Book ISBN", size=12, color="#374151"),
                        ft.Container(height=4),
                        self.book_isbn_field,
                    ], spacing=0, expand=True),
                    ft.Column([
                        ft.Text("Created date", size=12, color="#374151"),
                        ft.Container(height=4),
                        self.created_date_field,
                    ], spacing=0),
                    ft.Container(padding=ft.padding.only(top=18), content=add_book_btn),
                ], spacing=8),
                
                ft.Container(height=16),
                
                # Books table
                self.books_table_container,
                
                ft.Container(height=16),
                confirm_borrowing_btn,
                
            ], spacing=0),
            padding=20,
            bgcolor="#FFFFFF",
            border_radius=12,
            border=ft.border.all(1, "#E5E7EB"),
        )
    
    def _build_member_info_placeholder(self):
        """Placeholder for member info"""
        return ft.Text("Select a member to view details", size=12, color="#9CA3AF")
    
    def check_member(self, e):
        """Check and load member information"""
        email = self.member_email_field.value
        member_id = self.member_id_field.value
        
        if not email and not member_id:
            self.show_error("Please enter member email or ID")
            return
        
        try:
            # Search member by email or ID
            if email:
                member = fetch_one(
                    "SELECT * FROM USERS WHERE email = %s AND role_name = 'MEMBER'",
                    (email,)
                )
            else:
                member = fetch_one(
                    "SELECT * FROM USERS WHERE user_id = %s AND role_name = 'MEMBER'",
                    (member_id,)
                )
            
            if not member:
                self.show_error("Member not found")
                return
            
            # Get current borrowing count - SỬA: dùng BORROWING_TRANSACTION thay vì TRANSACTIONS
            borrow_count = fetch_one("""
                SELECT COUNT(*) as count 
                FROM BORROWING_TRANSACTION bt
                JOIN BORROWING_TRANSACTION_DETAILS btd ON bt.transaction_id = btd.transaction_id
                WHERE bt.member_id = %s 
                AND bt.borrower_status IN ('BORROWED', 'OVERDUE')
            """, (member['user_id'],))
            
            self.member_info = member
            self.member_details.content = ft.Column([
                ft.Text("Member details", size=12, color="#374151", weight=ft.FontWeight.W_600),
                ft.Container(height=8),
                
                # Row 1: ID và Name
                ft.Row([
                    ft.Row([
                        ft.Text("ID:", size=12, color="#6B7280", weight=ft.FontWeight.W_600),
                        ft.Text(str(member['user_id']), size=12, color="#374151"),
                    ], spacing=4),
                    ft.Container(width=24),
                    ft.Row([
                        ft.Text("Name:", size=12, color="#6B7280", weight=ft.FontWeight.W_600),
                        ft.Text(member['fullname'], size=12, color="#374151"),
                    ], spacing=4),
                ], spacing=0),
                
                ft.Container(height=6),
                
                # Row 2: Email và Phone
                ft.Row([
                    ft.Row([
                        ft.Text("Email:", size=12, color="#6B7280", weight=ft.FontWeight.W_600),
                        ft.Text(member['email'], size=12, color="#374151"),
                    ], spacing=4),
                    ft.Container(width=24),
                    ft.Row([
                        ft.Text("Phone:", size=12, color="#6B7280", weight=ft.FontWeight.W_600),
                        ft.Text(member.get('phone', 'N/A'), size=12, color="#374151"),
                    ], spacing=4),
                ], spacing=0),
                
                ft.Container(height=6),
                
                # Row 3: Account status và Address
                ft.Row([
                    ft.Row([
                        ft.Text("Account status:", size=12, color="#6B7280, weight=ft.FontWeight.W_600"),
                        ft.Container(
                            content=ft.Text(
                                member['user_status'] if 'user_status' in member else member.get('status', 'ACTIVE'), 
                                size=11, 
                                color="#059669" if (member.get('user_status') or member.get('status')) == 'ACTIVE' else "#DC2626",
                                weight=ft.FontWeight.W_500
                            ),
                            padding=ft.padding.symmetric(horizontal=8, vertical=2),
                            bgcolor="#D1FAE5" if (member.get('user_status') or member.get('status')) == 'ACTIVE' else "#FEE2E2",
                            border_radius=4,
                        ),
                    ], spacing=4),
                    ft.Container(width=24),
                    ft.Row([
                        ft.Text("Address:", size=12, color="#6B7280", weight=ft.FontWeight.W_600),
                        ft.Text(member.get('address', 'N/A'), size=12, color="#374151"),
                    ], spacing=4),
                ], spacing=0),
                
                ft.Container(height=6),
                
                # Row 4: Currently borrowing và Outstanding fines
                ft.Row([
                    ft.Row([
                        ft.Text("Currently borrowing:", size=12, color="#6B7280", weight=ft.FontWeight.W_600),
                        ft.Text(f"{borrow_count['count']} / 5 items", size=12, color="#374151"),
                    ], spacing=4),
                    ft.Container(width=24),
                    ft.Row([
                        ft.Text("Outstanding fines:", size=12, color="#6B7280", weight=ft.FontWeight.W_600),
                        ft.Text(f"{member.get('totalFineDebt', 0):,.0f} VND", size=12, color="#DC2626" if member.get('totalFineDebt', 0) > 0 else "#374151"),
                    ], spacing=4),
                ], spacing=0),
            ], spacing=0)
            
            self.member_details.visible = True
            
            # Check if member can borrow
            member_status = member.get('user_status') or member.get('status', 'ACTIVE')
            if member_status != 'ACTIVE':
                self.show_error("Member account is not active")
            elif member.get('totalFineDebt', 0) > 0:
                self.show_error(f"Member has outstanding fines: {member.get('totalFineDebt', 0):,.0f} VND")
            elif borrow_count['count'] >= 5:
                self.show_error("Member has reached maximum borrowing limit (5 books)")
            else:
                self.show_success("Member verified successfully")
            
            self.page.update()
            
        except Exception as ex:
            print(f"Error checking member: {ex}")
            self.show_error(f"Error: {str(ex)}")
    
    def add_book_to_slip(self, e):
        """Add book to borrowing slip"""
        if not self.member_info:
            self.show_error("Please check member first")
            return
        
        isbn_or_id = self.book_isbn_field.value
        if not isbn_or_id:
            self.show_error("Please enter Book ISBN or ID")
            return
        
        try:
            # Search book by ISBN or ID
            book = None
            if isbn_or_id.isdigit():
                book = get_book_detail(int(isbn_or_id))
            else:
                book = fetch_one("SELECT * FROM BOOKS WHERE isbn = %s", (isbn_or_id,))
            
            if not book:
                self.show_error("Book not found")
                return
            
            if book['available_copies'] <= 0:
                self.show_error("No copies available")
                return
            
            # Check if book already in slip
            if any(b['book_id'] == book['book_id'] for b in self.selected_books):
                self.show_error("Book already in slip")
                return
            
            # Add to selected books
            self.selected_books.append(book)
            self.update_books_table()
            self.book_isbn_field.value = ""
            self.show_success(f"Added: {book['title']}")
            self.page.update()
            
        except Exception as ex:
            print(f"Error adding book: {ex}")
            self.show_error(f"Error: {str(ex)}")
    
    def remove_book_from_slip(self, book_id):
        """Remove book from slip"""
        self.selected_books = [b for b in self.selected_books if b['book_id'] != book_id]
        self.update_books_table()
        self.page.update()
    
    def update_books_table(self):
        """Update books table display"""
        if not self.selected_books:
            self.books_table_container.content = ft.Column([
                ft.Text("No books added yet", size=12, color="#9CA3AF", text_align=ft.TextAlign.CENTER),
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER)
            return
        
        rows = []
        for idx, book in enumerate(self.selected_books, 1):
            rows.append(
                ft.DataRow(cells=[
                    ft.DataCell(ft.Text(str(idx), size=12, color="#374151")),
                    ft.DataCell(ft.Text(book.get('isbn', 'N/A'), size=12, color="#374151")),
                    ft.DataCell(ft.Text(book['title'][:50], size=12, color="#374151")),
                    ft.DataCell(ft.Text(self.created_date_field.value, size=12, color="#374151")),
                    ft.DataCell(
                        ft.TextButton(
                            "Remove", 
                            style=ft.ButtonStyle(color="#EF4444"),
                            on_click=lambda e, bid=book['book_id']: self.remove_book_from_slip(bid)
                        )
                    ),
                ])
            )
        
        self.books_table_container.content = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("#", size=11, color="#6B7280", weight=ft.FontWeight.W_600)),
                ft.DataColumn(ft.Text("ISBN", size=11, color="#6B7280", weight=ft.FontWeight.W_600)),
                ft.DataColumn(ft.Text("TITLE", size=11, color="#6B7280", weight=ft.FontWeight.W_600)),
                ft.DataColumn(ft.Text("CREATED DATE", size=11, color="#6B7280", weight=ft.FontWeight.W_600)),
                ft.DataColumn(ft.Text("", size=11)),
            ],
            rows=rows,
            border=ft.border.all(1, "#E5E7EB"),
            border_radius=6,
            heading_row_height=36,
            data_row_min_height=44,
        )
    
    def confirm_borrowing(self, e):
        """Confirm and create borrowing transactions"""
        if not self.member_info:
            self.show_error("Please check member first")
            return
        
        if not self.selected_books:
            self.show_error("Please add at least one book")
            return
        
        try:
            librarian_id = self.current_user.get('user_id')
            success_count = 0
            
            for book in self.selected_books:
                result = create_borrow_transaction(
                    self.member_info['user_id'],
                    book['book_id'],
                    librarian_id
                )
                
                if result['success']:
                    success_count += 1
                else:
                    print(f"Failed to borrow {book['title']}: {result['message']}")
            
            if success_count > 0:
                self.show_success(f"Successfully borrowed {success_count} book(s)")
                # Reset form
                self.selected_books = []
                self.member_info = None
                self.member_details.visible = False
                self.member_email_field.value = ""
                self.member_id_field.value = ""
                self.update_books_table()
                self.load_current_borrowing()
                self.page.update()
            else:
                self.show_error("Failed to create borrowing transactions")
                
        except Exception as ex:
            print(f"Error confirming borrowing: {ex}")
            self.show_error(f"Error: {str(ex)}")
    
    def _build_current_borrowing_table(self):
        """Table showing current borrowing transactions"""
        self.current_borrowing_container = ft.Container(
            content=ft.Column([
                ft.Text("Loading...", size=12, color="#9CA3AF"),
            ]),
            padding=20,
        )
        
        # Load data
        self.load_current_borrowing()
        
        return ft.Container(
            content=ft.Column([
                ft.Row([
                    ft.Text("Current borrowing", size=14, weight=ft.FontWeight.BOLD, color="#111827"),
                    ft.Container(expand=True),
                    ft.TextButton("Go to \"Borrow / Return\"", on_click=lambda e: None),
                ]),
                ft.Container(height=12),
                self.current_borrowing_container,
            ], spacing=0),
            padding=20,
            bgcolor="#FFFFFF",
            border_radius=12,
            border=ft.border.all(1, "#E5E7EB"),
        )
    
    def load_current_borrowing(self):
        """Load current borrowing transactions from database"""
        try:
            # SỬA: Sử dụng view vw_borrowing_details hoặc truy vấn đúng bảng
            transactions = fetch_all("""
                SELECT 
                    bt.transaction_id,
                    u.user_id as member_id,
                    u.fullname as member_name,
                    b.title,
                    bt.borrow_date,
                    bt.due_date,
                    bt.borrower_status as display_status,
                    btd.item_status
                FROM BORROWING_TRANSACTION bt
                JOIN USERS u ON bt.member_id = u.user_id
                JOIN BORROWING_TRANSACTION_DETAILS btd ON bt.transaction_id = btd.transaction_id
                JOIN BOOKS b ON btd.book_id = b.book_id
                WHERE bt.borrower_status IN ('BORROWED', 'OVERDUE')
                ORDER BY bt.borrow_date DESC
                LIMIT 10
            """)
            
            if not transactions:
                self.current_borrowing_container.content = ft.Column([
                    ft.Text("No active borrowing transactions", size=12, color="#9CA3AF"),
                ])
                if hasattr(self, 'page'):
                    self.page.update()
                return
            
            rows = []
            for t in transactions:
                status_color = "#059669" if t['display_status'] == 'BORROWED' else "#DC2626"
                status_bg = "#D1FAE5" if t['display_status'] == 'BORROWED' else "#FEE2E2"
                
                rows.append(
                    ft.DataRow(cells=[
                        ft.DataCell(ft.Text(str(t['transaction_id']), size=12, color="#374151")),
                        ft.DataCell(ft.Text(str(t['member_id']), size=12, color="#374151")),
                        ft.DataCell(ft.Text(t['member_name'], size=12, color="#374151")),
                        ft.DataCell(ft.Text(t['title'][:30], size=12, color="#374151")),
                        ft.DataCell(ft.Text(str(t['borrow_date']), size=12, color="#374151")),
                        ft.DataCell(ft.Text(str(t['due_date']), size=12, color="#374151")),
                        ft.DataCell(
                            ft.Container(
                                content=ft.Text(
                                    t['display_status'], 
                                    size=11, 
                                    color=status_color,
                                    weight=ft.FontWeight.W_500
                                ),
                                padding=ft.padding.symmetric(horizontal=8, vertical=2),
                                bgcolor=status_bg,
                                border_radius=4,
                            )
                        ),
                    ])
                )
            
            self.current_borrowing_container.content = ft.DataTable(
                columns=[
                    ft.DataColumn(ft.Text("TRANSACTION ID", size=11, color="#6B7280", weight=ft.FontWeight.W_600)),
                    ft.DataColumn(ft.Text("MEMBER ID", size=11, color="#6B7280", weight=ft.FontWeight.W_600)),
                    ft.DataColumn(ft.Text("MEMBER NAME", size=11, color="#6B7280", weight=ft.FontWeight.W_600)),
                    ft.DataColumn(ft.Text("BOOK", size=11, color="#6B7280", weight=ft.FontWeight.W_600)),
                    ft.DataColumn(ft.Text("BORROWED", size=11, color="#6B7280", weight=ft.FontWeight.W_600)),
                    ft.DataColumn(ft.Text("DUE DATE", size=11, color="#6B7280", weight=ft.FontWeight.W_600)),
                    ft.DataColumn(ft.Text("STATUS", size=11, color="#6B7280", weight=ft.FontWeight.W_600)),
                ],
                rows=rows,
                border=ft.border.all(1, "#E5E7EB"),
                border_radius=6,
                heading_row_height=36,
                data_row_min_height=44,
            )
            
            if hasattr(self, 'page'):
                self.page.update()
                
        except Exception as ex:
            print(f"Error loading current borrowing: {ex}")
            self.current_borrowing_container.content = ft.Text(f"Error: {str(ex)}", size=12, color="#DC2626")
    
    # ============ MANAGE RETURN BOOKS ============
    
    def _build_return_content(self):
        """Content for Manage Return Books tab"""
        self.return_transaction_field = ft.TextField(
            hint_text="Enter Transaction ID",
            border_color="#D1D5DB",
            text_size=13,
            border_radius=20,
            height=40,
            content_padding=10,
            expand=True,
        )
        
        search_transaction_btn = ft.ElevatedButton(
            "Search transaction",
            bgcolor="#3B82F6",
            color="#FFFFFF",
            height=40,
            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=20)),
            on_click=self.search_transaction,
        )
        
        self.transaction_details = ft.Container(
            content=ft.Text("Enter transaction ID to view details", size=12, color="#9CA3AF"),
            padding=16,
            bgcolor="#F9FAFB",
            border_radius=8,
            border=ft.border.all(1, "#E5E7EB"),
        )
        
        self.return_book_btn = ft.ElevatedButton(
            "Return book",
            bgcolor="#10B981",
            color="#FFFFFF",
            height=40,
            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=20)),
            on_click=self.process_return,
            visible=False,
        )
        
        return ft.Column([
            ft.Container(
                content=ft.Column([
                    ft.Text("Return book", size=14, weight=ft.FontWeight.BOLD, color="#111827"),
                    ft.Text("Enter transaction ID to process book return.", size=12, color="#6B7280"),
                    ft.Container(height=12),
                    
                    ft.Row([
                        self.return_transaction_field,
                        search_transaction_btn,
                    ], spacing=8),
                    
                    ft.Container(height=16),
                    self.transaction_details,
                    ft.Container(height=16),
                    self.return_book_btn,
                ], spacing=0),
                padding=20,
                bgcolor="#FFFFFF",
                border_radius=12,
                border=ft.border.all(1, "#E5E7EB"),
            ),
        ], spacing=0, scroll=ft.ScrollMode.AUTO)
    
    def search_transaction(self, e):
        """Search transaction by ID"""
        transaction_id = self.return_transaction_field.value
        
        if not transaction_id or not transaction_id.isdigit():
            self.show_error("Please enter a valid transaction ID")
            return
        
        try:
            # SỬA: Sử dụng BORROWING_TRANSACTION thay vì TRANSACTIONS
            transaction = fetch_one("""
                SELECT 
                    bt.transaction_id,
                    bt.borrow_date,
                    bt.due_date,
                    bt.return_date,
                    bt.borrower_status,
                    bt.renew_week_count,
                    u.user_id,
                    u.fullname as member_name,
                    u.email,
                    b.book_id,
                    b.title,
                    a.author_name as author,
                    btd.item_status,
                    btd.damage_percentage,
                    btd.days_late,
                    CASE 
                        WHEN bt.borrower_status = 'BORROWED' AND bt.due_date < CURDATE() THEN 'OVERDUE'
                        ELSE bt.borrower_status
                    END as display_status,
                    CASE
                        WHEN bt.borrower_status = 'BORROWED' AND bt.due_date < CURDATE() 
                        THEN DATEDIFF(CURDATE(), bt.due_date)
                        ELSE 0
                    END as days_overdue,
                    CASE
                        WHEN bt.borrower_status = 'BORROWED' AND bt.due_date < CURDATE() 
                        THEN DATEDIFF(CURDATE(), bt.due_date) * 20000
                        ELSE 0
                    END as estimated_fine
                FROM BORROWING_TRANSACTION bt
                JOIN USERS u ON bt.member_id = u.user_id
                JOIN BORROWING_TRANSACTION_DETAILS btd ON bt.transaction_id = btd.transaction_id
                JOIN BOOKS b ON btd.book_id = b.book_id
                LEFT JOIN AUTHORS a ON b.author_id = a.author_id
                WHERE bt.transaction_id = %s
                AND bt.borrower_status = 'BORROWED'
                LIMIT 1
            """, (transaction_id,))
            
            if not transaction:
                self.show_error("Transaction not found or book already returned")
                return
            
            # Display transaction details
            status_color = "#059669" if transaction['display_status'] == 'BORROWED' else "#DC2626"
            status_bg = "#D1FAE5" if transaction['display_status'] == 'BORROWED' else "#FEE2E2"
            
            details_content = ft.Column([
                ft.Text("Transaction details", size=12, color="#374151", weight=ft.FontWeight.W_600),
                ft.Container(height=8),
                
                ft.Row([
                    ft.Column([
                        ft.Text("Transaction ID:", size=12, color="#6B7280", weight=ft.FontWeight.W_600),
                        ft.Text(str(transaction['transaction_id']), size=12, color="#374151"),
                    ], spacing=2),
                    ft.Container(width=20),
                    ft.Column([
                        ft.Text("Member:", size=12, color="#6B7280", weight=ft.FontWeight.W_600),
                        ft.Text(transaction['member_name'], size=12, color="#374151"),
                    ], spacing=2),
                ]),
                
                ft.Container(height=8),
                
                ft.Column([
                    ft.Text("Book:", size=12, color="#6B7280", weight=ft.FontWeight.W_600),
                    ft.Text(transaction['title'], size=12, color="#374151"),
                    ft.Text(f"by {transaction.get('author', 'Unknown')}", size=11, color="#6B7280"),
                ], spacing=2),
                
                ft.Container(height=8),
                
                ft.Row([
                    ft.Column([
                        ft.Text("Borrowed:", size=12, color="#6B7280", weight=ft.FontWeight.W_600),
                        ft.Text(str(transaction['borrow_date']), size=12, color="#374151"),
                    ], spacing=2),
                    ft.Container(width=20),
                    ft.Column([
                        ft.Text("Due date:", size=12, color="#6B7280", weight=ft.FontWeight.W_600),
                        ft.Text(str(transaction['due_date']), size=12, color="#374151"),
                    ], spacing=2),
                ]),
                
                ft.Container(height=8),
                
                ft.Row([
                    ft.Column([
                        ft.Text("Status:", size=12, color="#6B7280", weight=ft.FontWeight.W_600),
                        ft.Container(
                            content=ft.Text(
                                transaction['display_status'], 
                                size=11, 
                                color=status_color,
                                weight=ft.FontWeight.W_500
                            ),
                            padding=ft.padding.symmetric(horizontal=8, vertical=2),
                            bgcolor=status_bg,
                            border_radius=4,
                        ),
                    ], spacing=2),
                ]),
            ], spacing=0)
            
            if transaction['days_overdue'] > 0:
                details_content.controls.append(ft.Container(height=8))
                details_content.controls.append(
                    ft.Container(
                        content=ft.Column([
                            ft.Text("⚠️ OVERDUE", size=12, color="#DC2626", weight=ft.FontWeight.W_600),
                            ft.Text(f"Days overdue: {transaction['days_overdue']}", size=12, color="#DC2626"),
                            ft.Text(f"Estimated fine: {transaction['estimated_fine']:,.0f} VND", size=12, color="#DC2626", weight=ft.FontWeight.W_600),
                        ], spacing=4),
                        padding=12,
                        bgcolor="#FEE2E2",
                        border_radius=6,
                    )
                )
            
            self.transaction_details.content = details_content
            self.return_book_btn.visible = True
            self.current_transaction = transaction
            self.page.update()
            
        except Exception as ex:
            print(f"Error searching transaction: {ex}")
            self.show_error(f"Error: {str(ex)}")
    
    def process_return(self, e):
        """Process book return"""
        if not hasattr(self, 'current_transaction'):
            self.show_error("No transaction selected")
            return
        
        try:
            result = return_book(self.current_transaction['transaction_id'])
            
            if result['success']:
                fine_msg = f" Fine charged: {result['fine_amount']:,.0f} VND" if result['fine_amount'] > 0 else ""
                self.show_success(f"Book returned successfully!{fine_msg}")
                
                # Reset form
                self.return_transaction_field.value = ""
                self.transaction_details.content = ft.Text("Enter transaction ID to view details", size=12, color="#9CA3AF")
                self.return_book_btn.visible = False
                self.current_transaction = None
                self.load_current_borrowing()
                self.page.update()
            else:
                self.show_error(result['message'])
                
        except Exception as ex:
            print(f"Error processing return: {ex}")
            self.show_error(f"Error: {str(ex)}")
    
    # ============ HELPER METHODS ============
    
    def show_success(self, message):
        """Show success snackbar"""
        self.page.snack_bar = ft.SnackBar(
            content=ft.Text(message, color="#FFFFFF"),
            bgcolor="#10B981",
        )
        self.page.snack_bar.open = True
        self.page.update()
    
    def show_error(self, message):
        """Show error snackbar"""
        self.page.snack_bar = ft.SnackBar(
            content=ft.Text(message, color="#FFFFFF"),
            bgcolor="#EF4444",
        )
        self.page.snack_bar.open = True
        self.page.update()
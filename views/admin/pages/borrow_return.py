import flet as ft
from datetime import datetime, timedelta


class BorrowReturnPage:
    def __init__(self):
        self.current_tab = "borrow"
        self.selected_books = []
        self.member_info = None
        
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
                # Header with title and user info
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
            # Active tab style - white bg with border
            self.borrow_tab_btn.bgcolor = "#FFFFFF"
            self.borrow_tab_btn.border = ft.border.all(1, "#E5E7EB")
            self.borrow_tab_btn.content.color = "#111827"
            # Inactive tab style - gray bg no border
            self.return_tab_btn.bgcolor = "#F3F4F6"
            self.return_tab_btn.border = None
            self.return_tab_btn.content.color = "#6B7280"
            # Switch content
            self.content_area.content = self._build_borrow_content()
        else:
            self.current_tab = "return"
            # Active tab style - white bg with border
            self.return_tab_btn.bgcolor = "#FFFFFF"
            self.return_tab_btn.border = ft.border.all(1, "#E5E7EB")
            self.return_tab_btn.content.color = "#111827"
            # Inactive tab style - gray bg no border
            self.borrow_tab_btn.bgcolor = "#F3F4F6"
            self.borrow_tab_btn.border = None
            self.borrow_tab_btn.content.color = "#6B7280"
            # Switch content
            self.content_area.content = self._build_return_content()
        
        e.page.update()
    
    # ============ MANAGE BORROWING BOOKS ============
    
    def _build_borrow_content(self):
        """Content for Manage Borrowing Books tab"""
        return ft.Column([
            self._build_create_borrowing(),
            ft.Container(height=24),
            self._build_extend_due_date(),
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
        )
        
        self.member_details = ft.Container(
            content=ft.Column([
                ft.Text("Member details", size=12, color="#374151", weight=ft.FontWeight.W_600),
                ft.Container(height=8),
                
                # Row 1: ID và Name
                ft.Row([
                    ft.Row([
                        ft.Text("ID:", size=12, color="#6B7280", weight=ft.FontWeight.W_600),
                        ft.Text("123", size=12, color="#374151"),
                    ], spacing=4),
                    ft.Container(width=24),
                    ft.Row([
                        ft.Text("Name:", size=12, color="#6B7280", weight=ft.FontWeight.W_600),
                        ft.Text("Nguyen Van A", size=12, color="#374151"),
                    ], spacing=4),
                ], spacing=0),
                
                ft.Container(height=6),
                
                # Row 2: Email và Phone
                ft.Row([
                    ft.Row([
                        ft.Text("Email:", size=12, color="#6B7280", weight=ft.FontWeight.W_600),
                        ft.Text("member@example.com", size=12, color="#374151"),
                    ], spacing=4),
                    ft.Container(width=24),
                    ft.Row([
                        ft.Text("Phone:", size=12, color="#6B7280", weight=ft.FontWeight.W_600),
                        ft.Text("0901 234 567", size=12, color="#374151"),
                    ], spacing=4),
                ], spacing=0),
                
                ft.Container(height=6),
                
                # Row 3: Account status và Address
                ft.Row([
                    ft.Row([
                        ft.Text("Account status:", size=12, color="#6B7280", weight=ft.FontWeight.W_600),
                        ft.Container(
                            content=ft.Text("Active", size=11, color="#059669", weight=ft.FontWeight.W_500),
                            padding=ft.padding.symmetric(horizontal=8, vertical=2),
                            bgcolor="#D1FAE5",
                            border_radius=4,
                        ),
                    ], spacing=4),
                    ft.Container(width=24),
                    ft.Row([
                        ft.Text("Address:", size=12, color="#6B7280", weight=ft.FontWeight.W_600),
                        ft.Text("12 Nguyen Trai, District 5, Ho Chi Minh City", size=12, color="#374151"),
                    ], spacing=4),
                ], spacing=0),
                
                ft.Container(height=6),
                
                # Row 4: Currently borrowing và Outstanding fines
                ft.Row([
                    ft.Row([
                        ft.Text("Currently borrowing:", size=12, color="#6B7280", weight=ft.FontWeight.W_600),
                        ft.Text("1 / 5 items", size=12, color="#374151"),
                    ], spacing=4),
                    ft.Container(width=24),
                    ft.Row([
                        ft.Text("Outstanding fines:", size=12, color="#6B7280", weight=ft.FontWeight.W_600),
                        ft.Text("0 VND", size=12, color="#374151"),
                    ], spacing=4),
                ], spacing=0),
                
            ], spacing=0),
            padding=16,
            bgcolor="#F0F9FF",
            border_radius=8,
            border=ft.border.all(1, "#BFDBFE"),
            visible=True,
        )
        
        self.book_isbn_field = ft.TextField(
            hint_text="978-...",
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
        )
        
        add_book_btn = ft.ElevatedButton(
            "Add book",
            bgcolor="#E5E7EB",
            color="#374151",
            height=40,
            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=20)),
        )
        
        books_in_slip = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("#", size=11, color="#6B7280", weight=ft.FontWeight.W_600)),
                ft.DataColumn(ft.Text("ISBN", size=11, color="#6B7280", weight=ft.FontWeight.W_600)),
                ft.DataColumn(ft.Text("TITLE", size=11, color="#6B7280", weight=ft.FontWeight.W_600)),
                ft.DataColumn(ft.Text("CREATED DATE", size=11, color="#6B7280", weight=ft.FontWeight.W_600)),
                ft.DataColumn(ft.Text("", size=11)),
            ],
            rows=[
                ft.DataRow(cells=[
                    ft.DataCell(ft.Text("1", size=12, color="#374151")),
                    ft.DataCell(ft.Text("978-1-9821-8582-4", size=12, color="#374151")),
                    ft.DataCell(ft.Text("Chain of Gold", size=12, color="#374151")),
                    ft.DataCell(ft.Text("07/01/2026", size=12, color="#374151")),
                    ft.DataCell(ft.TextButton("Remove", style=ft.ButtonStyle(color="#EF4444"))),
                ]),
            ],
            border=ft.border.all(1, "#E5E7EB"),
            border_radius=6,
            heading_row_height=36,
            data_row_min_height=44,
        )
        
        confirm_borrowing_btn = ft.ElevatedButton(
            "Confirm borrowing",
            bgcolor="#3B82F6",
            color="#FFFFFF",
            height=40,
            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=20)),
        )
        
        return ft.Container(
            content=ft.Column([
                ft.Text("Create borrowing transaction", size=14, weight=ft.FontWeight.BOLD, color="#111827"),
                ft.Text("Start a new borrowing slip using member email or member ID, then add books and created date.", size=12, color="#6B7280"),
                ft.Container(height=12),
                
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
                    ft.Container(content=check_member_btn, padding=ft.padding.only(top=24)),
                ], spacing=12),
                
                ft.Container(height=12),
                self.member_details,
                ft.Container(height=16),
                
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
                    ft.Container(content=add_book_btn, padding=ft.padding.only(top=24)),
                ], spacing=12),
                
                ft.Container(height=12),
                ft.Text("Items in slip: 1", size=12, color="#374151", weight=ft.FontWeight.W_600),
                ft.Container(height=8),
                books_in_slip,
                
                ft.Container(height=16),
                ft.Row([ft.Container(expand=True), confirm_borrowing_btn]),
            ], spacing=0),
            padding=16,
            bgcolor="#FFFFFF",
            border_radius=8,
            border=ft.border.all(1, "#E5E7EB"),
        )
    
    def _build_extend_due_date(self):
        """Form to extend due date"""
        
        self.extend_search_field = ft.TextField(
            hint_text="e.g. 23 or 123 or member@example.com",
            border_color="#D1D5DB",
            text_size=13,
            border_radius=20,
            height=40,
            content_padding=10,
            expand=True,
        )
        
        search_loans_btn = ft.ElevatedButton(
            "Search loans",
            bgcolor="#3B82F6",
            color="#FFFFFF",
            height=40,
            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=20)),
        )
        
        # Radio group for selection
        self.loan_radio_group = ft.RadioGroup(
            content=ft.Column([
                ft.DataTable(
                    columns=[
                        ft.DataColumn(ft.Text("SELECT", size=11, color="#6B7280", weight=ft.FontWeight.W_600)),
                        ft.DataColumn(ft.Text("TRANSACTION ID", size=11, color="#6B7280", weight=ft.FontWeight.W_600)),
                        ft.DataColumn(ft.Text("ISBN", size=11, color="#6B7280", weight=ft.FontWeight.W_600)),
                        ft.DataColumn(ft.Text("TITLE", size=11, color="#6B7280", weight=ft.FontWeight.W_600)),
                        ft.DataColumn(ft.Text("BORROWED", size=11, color="#6B7280", weight=ft.FontWeight.W_600)),
                        ft.DataColumn(ft.Text("CURRENT DUE", size=11, color="#6B7280", weight=ft.FontWeight.W_600)),
                        ft.DataColumn(ft.Text("EXTENSIONS USED", size=11, color="#6B7280", weight=ft.FontWeight.W_600)),
                        ft.DataColumn(ft.Text("STATUS", size=11, color="#6B7280", weight=ft.FontWeight.W_600)),
                    ],
                    rows=[
                        ft.DataRow(cells=[
                            ft.DataCell(ft.Radio(value="23", label="")),
                            ft.DataCell(ft.Text("23", size=12, color="#374151")),
                            ft.DataCell(ft.Text("978-1-9821-8582-4", size=12, color="#374151")),
                            ft.DataCell(ft.Text("Chain of Gold", size=12, color="#374151")),
                            ft.DataCell(ft.Text("01/01/2026", size=12, color="#374151")),
                            ft.DataCell(ft.Text("16/01/2026", size=12, color="#374151")),
                            ft.DataCell(ft.Text("0 / 2", size=12, color="#374151")),
                            ft.DataCell(ft.Container(
                                content=ft.Text("On loan", size=11, color="#1D4ED8"),
                                padding=ft.padding.symmetric(horizontal=8, vertical=2),
                                bgcolor="#DBEAFE",
                                border_radius=4,
                            )),
                        ]),
                    ],
                    border=ft.border.all(1, "#E5E7EB"),
                    border_radius=6,
                    heading_row_height=36,
                    data_row_min_height=44,
                )
            ])
        )
        
        self.new_due_date_field = ft.TextField(
            value=(datetime.now() + timedelta(days=15)).strftime("%m/%d/%Y"),
            border_color="#D1D5DB",
            text_size=13,
            border_radius=20,
            height=40,
            width=150,
            content_padding=10,
            read_only=True,
        )
        
        extend_loan_btn = ft.ElevatedButton(
            "Extend selected loan",
            bgcolor="#3B82F6",
            color="#FFFFFF",
            height=40,
            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=20)),
        )
        
        return ft.Container(
            content=ft.Column([
                ft.Text("Extend due date", size=14, weight=ft.FontWeight.BOLD, color="#111827"),
                ft.Text("Enter a transaction ID or member ID / email to locate the loan, then extend its due date by 15 days.", size=12, color="#6B7280"),
                ft.Container(height=12),
                
                ft.Row([
                    ft.Column([
                        ft.Text("Transaction ID or Member ID / email", size=12, color="#374151"),
                        ft.Container(height=4),
                        self.extend_search_field,
                    ], spacing=0, expand=True),
                    ft.Container(content=search_loans_btn, padding=ft.padding.only(top=24)),
                ], spacing=12),
                
                ft.Container(height=12),
                ft.Container(content=self.loan_radio_group, border=ft.border.all(1, "#E5E7EB"), border_radius=6),
                
                ft.Container(height=12),
                ft.Row([
                    ft.Text("New due date (+15 days)", size=12, color="#374151"),
                    self.new_due_date_field,
                    ft.Container(expand=True),
                    extend_loan_btn,
                ], spacing=12, alignment=ft.MainAxisAlignment.START),
            ], spacing=0),
            padding=16,
            bgcolor="#FFFFFF",
            border_radius=8,
            border=ft.border.all(1, "#E5E7EB"),
        )
    
    def _build_current_borrowing_table(self):
        """Current borrowing table"""
        
        self.current_search_field = ft.TextField(
            hint_text="Search transaction ID, member ID, name or book...",
            border_color="#D1D5DB",
            text_size=13,
            border_radius=20,
            height=40,
            content_padding=10,
            expand=True,
        )
        
        def status_badge(text, color_scheme):
            colors = {
                "borrowing": ("#1D4ED8", "#DBEAFE"),
                "overdue": ("#DC2626", "#FEE2E2"),
                "not_returned": ("#1D4ED8", "#DBEAFE"),
            }
            text_color, bg_color = colors.get(color_scheme, ("#6B7280", "#F3F4F6"))
            return ft.Container(
                content=ft.Text(text, size=11, color=text_color, weight=ft.FontWeight.W_500),
                padding=ft.padding.symmetric(horizontal=8, vertical=4),
                bgcolor=bg_color,
                border_radius=4,
            )
        
        current_table = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("TRANSACTION ID", size=11, color="#6B7280", weight=ft.FontWeight.W_600)),
                ft.DataColumn(ft.Text("MEMBER ID", size=11, color="#6B7280", weight=ft.FontWeight.W_600)),
                ft.DataColumn(ft.Text("MEMBER NAME", size=11, color="#6B7280", weight=ft.FontWeight.W_600)),
                ft.DataColumn(ft.Text("BOOK", size=11, color="#6B7280", weight=ft.FontWeight.W_600)),
                ft.DataColumn(ft.Text("BORROWED", size=11, color="#6B7280", weight=ft.FontWeight.W_600)),
                ft.DataColumn(ft.Text("DUE DATE", size=11, color="#6B7280", weight=ft.FontWeight.W_600)),
                ft.DataColumn(ft.Text("STATUS", size=11, color="#6B7280", weight=ft.FontWeight.W_600)),
            ],
            rows=[
                ft.DataRow(cells=[
                    ft.DataCell(ft.Text("23", size=12, color="#374151")),
                    ft.DataCell(ft.Text("123", size=12, color="#374151")),
                    ft.DataCell(ft.Text("Nguyen Van A", size=12, color="#374151")),
                    ft.DataCell(ft.Text("Chain of Gold", size=12, color="#374151")),
                    ft.DataCell(ft.Text("01/01/2026", size=12, color="#374151")),
                    ft.DataCell(ft.Text("16/01/2026", size=12, color="#374151")),
                    ft.DataCell(status_badge("Borrowing", "borrowing")),
                ]),
                ft.DataRow(cells=[
                    ft.DataCell(ft.Text("15", size=12, color="#374151")),
                    ft.DataCell(ft.Text("123", size=12, color="#374151")),
                    ft.DataCell(ft.Text("Nguyen Van A", size=12, color="#374151")),
                    ft.DataCell(ft.Text("Nona the Ninth", size=12, color="#374151")),
                    ft.DataCell(ft.Text("30/12/2025", size=12, color="#374151")),
                    ft.DataCell(ft.Text("14/01/2026", size=12, color="#374151")),
                    ft.DataCell(status_badge("Overdue", "overdue")),
                ]),
                ft.DataRow(cells=[
                    ft.DataCell(ft.Text("10", size=12, color="#374151")),
                    ft.DataCell(ft.Text("123", size=12, color="#374151")),
                    ft.DataCell(ft.Text("Nguyen Van A", size=12, color="#374151")),
                    ft.DataCell(ft.Text("Financial Feminist", size=12, color="#374151")),
                    ft.DataCell(ft.Text("27/12/2025", size=12, color="#374151")),
                    ft.DataCell(ft.Text("11/01/2026", size=12, color="#374151")),
                    ft.DataCell(status_badge("Borrowing", "borrowing")),
                ]),
                ft.DataRow(cells=[
                    ft.DataCell(ft.Text("24", size=12, color="#374151")),
                    ft.DataCell(ft.Text("124", size=12, color="#374151")),
                    ft.DataCell(ft.Text("Tran Thi B", size=12, color="#374151")),
                    ft.DataCell(ft.Text("Database System Concepts", size=12, color="#374151")),
                    ft.DataCell(ft.Text("02/01/2026", size=12, color="#374151")),
                    ft.DataCell(ft.Text("17/01/2026", size=12, color="#374151")),
                    ft.DataCell(status_badge("Borrowing", "borrowing")),
                ]),
                ft.DataRow(cells=[
                    ft.DataCell(ft.Text("19", size=12, color="#374151")),
                    ft.DataCell(ft.Text("125", size=12, color="#374151")),
                    ft.DataCell(ft.Text("Le Van C", size=12, color="#374151")),
                    ft.DataCell(ft.Text("Data Structures & Algorithms", size=12, color="#374151")),
                    ft.DataCell(ft.Text("26/12/2025", size=12, color="#374151")),
                    ft.DataCell(ft.Text("10/01/2026", size=12, color="#374151")),
                    ft.DataCell(status_badge("Overdue", "overdue")),
                ]),
            ],
            border=ft.border.all(1, "#E5E7EB"),
            border_radius=6,
            heading_row_height=36,
            data_row_min_height=44,
            column_spacing=20,
        )
        
        return ft.Container(
            content=ft.Column([
                ft.Text("Current borrowing", size=14, weight=ft.FontWeight.BOLD, color="#111827"),
                ft.Text("Use this list to look up the correct transaction ID if the patron does not remember it.", size=12, color="#6B7280"),
                ft.Container(height=12),
                
                ft.Column([
                    ft.Text("Search", size=12, color="#374151"),
                    ft.Container(height=4),
                    self.current_search_field,
                ], spacing=0),
                
                ft.Container(height=12),
                ft.Container(content=current_table, border=ft.border.all(1, "#E5E7EB"), border_radius=6),
            ], spacing=0),
            padding=16,
            bgcolor="#FFFFFF",
            border_radius=8,
            border=ft.border.all(1, "#E5E7EB"),
        )
    
    # ============ MANAGE RETURN BOOKS ============
    
    def _build_return_content(self):
        """Content for Manage Return Books tab"""
        
        self.return_transaction_field = ft.TextField(
            hint_text="23",
            border_color="#D1D5DB",
            text_size=13,
            border_radius=20,
            height=40,
            width=200,
            content_padding=10,
        )
        
        load_loan_btn = ft.ElevatedButton(
            "Load loan record",
            bgcolor="#3B82F6",
            color="#FFFFFF",
            height=40,
            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=20)),
        )
        
        return_details = ft.Container(
            content=ft.Column([
                # Row 1: Member và Book
                ft.Row([
                    ft.Column([
                        ft.Text("Member", size=11, color="#6B7280", weight=ft.FontWeight.W_600),
                        ft.Container(height=4),
                        ft.Text("Nguyen Van A (ID 123)", size=13, color="#111827", weight=ft.FontWeight.W_500),
                    ], spacing=0, expand=1),
                    
                    ft.Column([
                        ft.Text("Book", size=11, color="#6B7280", weight=ft.FontWeight.W_600),
                        ft.Container(height=4),
                        ft.Text("Harlem Shuffle", size=13, color="#111827", weight=ft.FontWeight.W_500),
                        ft.Text("ISBN: 978-0-385-54792-5", size=12, color="#6B7280"),
                    ], spacing=2, expand=1),
                    
                    # Cột trống để cân bằng với Row 2
                    ft.Column([], spacing=0, expand=1),
                ], spacing=20),
                
                ft.Container(height=16),
                ft.Divider(height=1, color="#E5E7EB"),
                ft.Container(height=16),
                
                # Row 2: Borrowed date, Due date, Status (3 cột)
                ft.Row([
                    ft.Column([
                        ft.Text("Borrowed date", size=11, color="#6B7280", weight=ft.FontWeight.W_600),
                        ft.Container(height=4),
                        ft.Text("20/12/2025", size=13, color="#111827", weight=ft.FontWeight.W_500),
                    ], spacing=0, expand=1),
                    
                    ft.Column([
                        ft.Text("Due date", size=11, color="#6B7280", weight=ft.FontWeight.W_600),
                        ft.Container(height=4),
                        ft.Text("05/01/2026", size=13, color="#111827", weight=ft.FontWeight.W_500),
                    ], spacing=0, expand=1),
                    
                    ft.Column([
                        ft.Text("Status", size=11, color="#6B7280", weight=ft.FontWeight.W_600),
                        ft.Container(height=4),
                        ft.Container(
                            content=ft.Text("Not returned", size=11, color="#1D4ED8", weight=ft.FontWeight.W_500),
                            padding=ft.padding.symmetric(horizontal=10, vertical=4),
                            bgcolor="#DBEAFE",
                            border_radius=6,
                        ),
                    ], spacing=0, expand=1),
                ], spacing=20),
                
                ft.Container(height=16),
                ft.Divider(height=1, color="#E5E7EB"),
                ft.Container(height=16),
                
                # Row 3: Book replacement cost, Late return fine
                ft.Row([
                    ft.Column([
                        ft.Text("Book replacement cost", size=11, color="#6B7280", weight=ft.FontWeight.W_600),
                        ft.Container(height=4),
                        ft.Text("200,000 VND", size=13, color="#111827", weight=ft.FontWeight.W_500),
                    ], spacing=0, expand=1),
                    
                    ft.Column([
                        ft.Text("Late return fine", size=11, color="#6B7280", weight=ft.FontWeight.W_600),
                        ft.Container(height=4),
                        ft.Text("10,000 VND", size=13, color="#DC2626", weight=ft.FontWeight.W_500),
                    ], spacing=0, expand=1),
                    
                    # Cột trống để cân bằng với Row 2
                    ft.Column([], spacing=0, expand=1),
                ], spacing=20),
                
            ], spacing=0),
            padding=20,
            bgcolor="#F9FAFB",
            border_radius=8,
            border=ft.border.all(1, "#E5E7EB"),
        )
        
        self.physical_condition_dropdown = ft.Dropdown(
            options=[
                ft.dropdown.Option("Normal"),
                ft.dropdown.Option("Damage percentage (%)"),
            ],
            value="Normal",
            border_color="#D1D5DB",
            text_size=13,
            border_radius=20,
            height=40,
            content_padding=10,
        )
        
        self.damage_percentage_field = ft.TextField(
            hint_text="0",
            value="0",
            border_color="#D1D5DB",
            text_size=13,
            border_radius=20,
            height=40,
            width=120,
            content_padding=10,
        )
        
        self.damage_amount_field = ft.TextField(
            value="0 VND",
            border_color="#D1D5DB",
            text_size=13,
            border_radius=20,
            height=40,
            width=150,
            content_padding=10,
            read_only=True,
            bgcolor="#F9FAFB",
        )
        
        self.staff_notes_field = ft.TextField(
            hint_text="Notes for damage/loss, assessment, payment confirmation, etc.",
            border_color="#D1D5DB",
            text_size=13,
            border_radius=20,
            multiline=True,
            min_lines=3,
            max_lines=3,
            content_padding=10,
            expand=True,
        )
        
        self.payment_status_dropdown = ft.Dropdown(
            options=[
                ft.dropdown.Option("Unpaid"),
                ft.dropdown.Option("Paid"),
            ],
            value="Unpaid",
            border_color="#D1D5DB",
            text_size=13,
            border_radius=20,
            height=40,
            width=150,
            content_padding=10,
        )
        
        confirm_return_btn = ft.ElevatedButton(
            "Confirm return",
            bgcolor="#3B82F6",
            color="#FFFFFF",
            height=40,
            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=20)),
        )
        
        return ft.Column([
            ft.Container(
                content=ft.Column([
                    ft.Text("Return book", size=14, weight=ft.FontWeight.BOLD, color="#111827"),
                    ft.Text("Enter the transaction ID to load loan details, assess damage as a percentage of replacement cost, and confirm return.", size=12, color="#6B7280"),
                    ft.Container(height=12),
                    
                    ft.Row([
                        ft.Column([
                            ft.Text("Transaction ID", size=12, color="#374151"),
                            ft.Container(height=4),
                            self.return_transaction_field,
                        ], spacing=0),
                        ft.Container(content=load_loan_btn, padding=ft.padding.only(top=24)),
                    ], spacing=12),
                    
                    ft.Container(height=12),
                    return_details,
                    ft.Container(height=16),
                    
                    ft.Row([
                        ft.Column([
                            ft.Text("Physical condition", size=12, color="#374151"),
                            ft.Container(height=4),
                            self.physical_condition_dropdown,
                        ], spacing=0),
                        ft.Column([
                            ft.Text("Damage percentage (%)", size=12, color="#374151"),
                            ft.Container(height=4),
                            self.damage_percentage_field,
                        ], spacing=0),
                        ft.Column([
                            ft.Text("Damage amount (auto)", size=12, color="#374151"),
                            ft.Container(height=4),
                            self.damage_amount_field,
                        ], spacing=0),
                    ], spacing=12),
                    
                    ft.Container(height=12),
                    
                    ft.Column([
                        ft.Text("Staff notes", size=12, color="#374151"),
                        ft.Container(height=4),
                        self.staff_notes_field,
                    ], spacing=0),
                    
                    ft.Container(height=16),
                    ft.Divider(height=1, color="#E5E7EB"),
                    ft.Container(height=16),
                    
                    ft.Row([
                        ft.Text("Late return fine", size=12, color="#374151"),
                        ft.Container(expand=True),
                        ft.Text("10,000 VND", size=12, color="#374151"),
                    ]),
                    ft.Container(height=8),
                    ft.Row([
                        ft.Text("Damage / lost fine", size=12, color="#374151"),
                        ft.Container(expand=True),
                        ft.Text("0 VND", size=12, color="#374151"),
                    ]),
                    ft.Container(height=12),
                    ft.Divider(height=1, color="#E5E7EB"),
                    ft.Container(height=12),
                    ft.Row([
                        ft.Text("Total to collect", size=13, color="#111827", weight=ft.FontWeight.BOLD),
                        ft.Container(expand=True),
                        ft.Text("10,000 VND", size=13, color="#111827", weight=ft.FontWeight.BOLD),
                    ]),
                    
                    ft.Container(height=16),
                    
                    ft.Row([
                        ft.Column([
                            ft.Text("Payment status", size=12, color="#374151"),
                            ft.Container(height=4),
                            self.payment_status_dropdown,
                        ], spacing=0),
                        ft.Container(expand=True),
                        ft.Container(content=confirm_return_btn, padding=ft.padding.only(top=24)),
                    ], spacing=12),
                    
                    ft.Container(height=12),
                    ft.Text("Damage fines are calculated as a percentage of the book's replacement price, added on top of the late return fine when applicable.", size=11, color="#6B7280", italic=True),
                ], spacing=0),
                padding=16,
                bgcolor="#FFFFFF",
                border_radius=8,
                border=ft.border.all(1, "#E5E7EB"),
            ),
            
            ft.Container(height=24),
            self._build_current_borrowing_table(),
        ], spacing=0, scroll=ft.ScrollMode.AUTO)

# views/admin/pages/reports.py
import flet as ft
from datetime import datetime, timedelta
from database.db import execute_query, fetch_all, fetch_one


class ReportsPage:
    """Trang báo cáo thống kê"""
    
    def __init__(self, page: ft.Page = None):
        self.page_ref = page
        self.report_type = None
        self.from_date = None
        self.to_date = None
        self.report_content = None
        
    def build(self, page: ft.Page = None):
        """Xây dựng giao diện chính"""
        if page:
            self.page_ref = page
            
        # Report content section - ẨN BAN ĐẦU
        self.report_content = ft.Container(
            visible=False,  # ẨN BAN ĐẦU, CHỈ HIỆN KHI CLICK VIEW REPORT
        )
        
        main_content = ft.Column([
            self._build_header(),
            ft.Container(height=16),
            self._build_report_selector(),
            ft.Container(height=20),
            self.report_content,
        ], spacing=0, scroll=ft.ScrollMode.AUTO)
        
        return ft.Container(
            content=main_content,
            padding=ft.padding.all(20),
            bgcolor="#FFFFFF",
            border_radius=12,
            border=ft.border.all(1, "#E5E7EB"),
        )
    
    def _build_header(self):
        """Header"""
        return ft.Column([
            ft.Text(
                "View statistical reports",
                size=20,
                weight=ft.FontWeight.BOLD,
                color="#1F2937",
            ),
            ft.Container(height=4),
            ft.Text(
                "Select report type and, if needed, entering a timeframe.",
                size=12,
                color="#6B7280",
            ),
        ], spacing=0)
    
    def _build_report_selector(self):
        """Phần chọn loại báo cáo và khoảng thời gian"""
        self.report_type_dropdown = ft.Dropdown(
            options=[
                ft.dropdown.Option("Total Book Statistics"),
                ft.dropdown.Option("Borrowing Statistics"),
                ft.dropdown.Option("Most Borrowed Books"),
                ft.dropdown.Option("Overdue List"),
                ft.dropdown.Option("New Members"),
            ],
            value="Total Book Statistics",
            border_color="#D1D5DB",
            focused_border_color="#2563EB",
            text_size=13,
            border_radius=6,
            height=44,
            width=300,
        )
        
        self.from_date_field = ft.TextField(
            hint_text="mm/dd/yyyy",
            border_color="#D1D5DB",
            focused_border_color="#2563EB",
            text_size=13,
            border_radius=6,
            height=44,
            width=150,
        )
        
        self.to_date_field = ft.TextField(
            hint_text="mm/dd/yyyy",
            border_color="#D1D5DB",
            focused_border_color="#2563EB",
            text_size=13,
            border_radius=6,
            height=44,
            width=150,
        )
        
        view_report_btn = ft.ElevatedButton(
            "View report",
            bgcolor="#06B6D4",
            color="#FFFFFF",
            height=44,
            on_click=self._on_view_report,
        )
        
        return ft.Row([
            ft.Column([
                ft.Text("Report type", size=12, color="#374151"),
                ft.Container(height=4),
                self.report_type_dropdown,
            ], spacing=0),
            ft.Container(width=16),
            ft.Column([
                ft.Text("From date (optional)", size=12, color="#374151"),
                ft.Container(height=4),
                self.from_date_field,
            ], spacing=0),
            ft.Container(width=16),
            ft.Column([
                ft.Text("To date (optional)", size=12, color="#374151"),
                ft.Container(height=4),
                self.to_date_field,
            ], spacing=0),
            ft.Container(width=16),
            ft.Column([
                ft.Text("", size=12),  # Spacer để align button
                ft.Container(height=4),
                view_report_btn,
            ], spacing=0),
        ])
    
    def _on_view_report(self, e):
        """Xử lý khi click View report"""
        try:
            report_type = self.report_type_dropdown.value
            from_date = self.from_date_field.value.strip() if self.from_date_field.value else None
            to_date = self.to_date_field.value.strip() if self.to_date_field.value else None
            
            # Xác thực ngày nếu có
            if from_date and to_date:
                try:
                    datetime.strptime(from_date, "%m/%d/%Y")
                    datetime.strptime(to_date, "%m/%d/%Y")
                except ValueError:
                    self._show_error("Invalid date format. Please use mm/dd/yyyy")
                    return
            
            # Hiển thị báo cáo dựa trên loại được chọn
            if report_type == "Total Book Statistics":
                report_content = self._build_book_statistics_report()
            elif report_type == "Borrowing Statistics":
                report_content = self._build_borrowing_statistics_report(from_date, to_date)
            elif report_type == "Most Borrowed Books":
                report_content = self._build_most_borrowed_report(from_date, to_date)
            elif report_type == "Overdue List":
                report_content = self._build_overdue_list_report()
            elif report_type == "New Members":
                report_content = self._build_new_members_report(from_date, to_date)
            else:
                report_content = ft.Text("Report type not implemented", size=16)
            
            self.report_content.content = report_content
            self.report_content.visible = True
            self.report_content.update()
            
        except Exception as ex:
            print(f"Error generating report: {ex}")
            self._show_error(f"Error generating report: {str(ex)}")
    
    def _build_book_statistics_report(self):
        """Báo cáo thống kê sách từ database"""
        try:
            # 1. Tổng số sách và bản sao
            total_stats_query = """
                SELECT 
                    COUNT(DISTINCT b.book_id) as total_books,
                    SUM(b.total_copies) as total_copies,
                    SUM(b.available_copies) as available_copies
                FROM books b
            """
            total_stats_result = fetch_one(total_stats_query)
            total_stats = total_stats_result if total_stats_result else {"total_books": 0, "total_copies": 0, "available_copies": 0}
            
            # 2. Sách đang mượn
            borrowed_query = """
                SELECT COUNT(*) as currently_borrowed
                FROM borrowing_transaction_details btd
                JOIN borrowing_transaction bt ON btd.transaction_id = bt.transaction_id
                WHERE bt.borrower_status = 'BORROWED'
                    AND btd.item_status = 'BORROWED'
            """
            borrowed_result = fetch_one(borrowed_query)
            currently_borrowed = borrowed_result["currently_borrowed"] if borrowed_result else 0
            
            # 3. Sách quá hạn
            overdue_query = """
                SELECT COUNT(*) as overdue_count
                FROM borrowing_transaction_details btd
                JOIN borrowing_transaction bt ON btd.transaction_id = bt.transaction_id
                WHERE bt.borrower_status = 'OVERDUE'
                    OR (bt.due_date < CURDATE() AND bt.return_date IS NULL)
            """
            overdue_result = fetch_one(overdue_query)
            overdue_count = overdue_result["overdue_count"] if overdue_result else 0
            
            # 4. Sách tham khảo chỉ
            reference_query = """
                SELECT COUNT(*) as reference_books
                FROM books b
                WHERE b.is_reference_only = TRUE
            """
            reference_result = fetch_one(reference_query)
            reference_books = reference_result["reference_books"] if reference_result else 0
            
            # 5. Thống kê theo thể loại
            category_query = """
                SELECT 
                    c.category_name as category,
                    COUNT(DISTINCT b.book_id) as total_books,
                    SUM(b.total_copies) as total_copies,
                    SUM(b.available_copies) as available_copies
                FROM books b
                JOIN categories c ON b.category_id = c.category_id
                GROUP BY c.category_id, c.category_name
                ORDER BY total_books DESC
            """
            category_stats = fetch_all(category_query) or []
            
            # 6. Thống kê tổng giá trị sách
            value_query = """
                SELECT 
                    COUNT(*) as book_count,
                    SUM(b.price * b.total_copies) as total_value
                FROM books b
            """
            value_result = fetch_one(value_query)
            total_value = value_result["total_value"] if value_result else 0
            
            # Tạo giao diện report
            return ft.Column([
                # Overall summary
                ft.Text("Overall Book Statistics", size=16, weight=ft.FontWeight.BOLD, color="#1F2937"),
                ft.Container(height=16),
                ft.Row([
                    self._build_stat_card("Total Books", 
                                         str(total_stats.get('total_books', 0)), 
                                         "Unique titles"),
                    ft.Container(width=16),
                    self._build_stat_card("Total Copies", 
                                         str(total_stats.get('total_copies', 0)), 
                                         "All physical copies"),
                    ft.Container(width=16),
                    self._build_stat_card("Available", 
                                         str(total_stats.get('available_copies', 0)), 
                                         "Ready to borrow"),
                    ft.Container(width=16),
                    self._build_stat_card("On Loan", 
                                         str(currently_borrowed), 
                                         "Currently borrowed"),
                ]),
                
                ft.Container(height=16),
                
                ft.Row([
                    self._build_stat_card("Overdue", 
                                         str(overdue_count), 
                                         "Past due date"),
                    ft.Container(width=16),
                    self._build_stat_card("Reference Only", 
                                         str(reference_books), 
                                         "For reference only"),
                    ft.Container(width=16),
                    self._build_stat_card("Total Value", 
                                         f"{total_value:,.0f} VND" if total_value else "0 VND", 
                                         "Inventory value"),
                ]),
                
                ft.Container(height=32),
                
                # Category statistics
                ft.Text("Statistics by Category", size=16, weight=ft.FontWeight.BOLD, color="#1F2937"),
                ft.Container(height=12),
                ft.Text("Number of unique titles in each category", size=12, color="#6B7280"),
                ft.Container(height=12),
                self._build_category_statistics_table(category_stats),
                
            ], spacing=0)
            
        except Exception as ex:
            print(f"Error in book statistics: {ex}")
            return ft.Text(f"Error loading book statistics: {str(ex)}", color="#EF4444")
    
    def _build_borrowing_statistics_report(self, from_date=None, to_date=None):
        """Báo cáo thống kê mượn trả"""
        try:
            # Xây dựng điều kiện WHERE cho khoảng thời gian
            date_condition = ""
            if from_date:
                from_date_obj = datetime.strptime(from_date, "%m/%d/%Y")
                date_condition += f" AND DATE(bt.borrow_date) >= '{from_date_obj.strftime('%Y-%m-%d')}'"
            if to_date:
                to_date_obj = datetime.strptime(to_date, "%m/%d/%Y")
                date_condition += f" AND DATE(bt.borrow_date) <= '{to_date_obj.strftime('%Y-%m-%d')}'"
            
            # Query thống kê mượn trả theo ngày
            query = f"""
                SELECT 
                    DATE(bt.borrow_date) as borrow_date,
                    COUNT(DISTINCT bt.transaction_id) as transactions_count,
                    COUNT(btd.transaction_detail_id) as books_borrowed,
                    SUM(CASE WHEN bt.return_date IS NOT NULL THEN 1 ELSE 0 END) as transactions_returned,
                    SUM(CASE WHEN bt.borrower_status = 'OVERDUE' THEN 1 ELSE 0 END) as overdue_count
                FROM borrowing_transaction bt
                JOIN borrowing_transaction_details btd ON bt.transaction_id = btd.transaction_id
                WHERE 1=1
                    {date_condition}
                GROUP BY DATE(bt.borrow_date)
                ORDER BY borrow_date DESC
                LIMIT 30
            """
            
            borrowing_stats = fetch_all(query) or []
            
            # Tổng thống kê
            summary_query = f"""
                SELECT 
                    COUNT(DISTINCT bt.transaction_id) as total_transactions,
                    COUNT(btd.transaction_detail_id) as total_books_borrowed,
                    COUNT(DISTINCT bt.member_id) as unique_members
                FROM borrowing_transaction bt
                JOIN borrowing_transaction_details btd ON bt.transaction_id = btd.transaction_id
                WHERE 1=1
                    {date_condition}
            """
            summary_stats = fetch_one(summary_query) or {}
            
            return ft.Column([
                ft.Text("Borrowing Statistics", size=16, weight=ft.FontWeight.BOLD, color="#1F2937"),
                ft.Container(height=12),
                ft.Text(f"Period: {from_date or 'All time'} - {to_date or 'Now'}", size=12, color="#6B7280"),
                
                ft.Container(height=16),
                
                # Summary stats
                ft.Row([
                    self._build_stat_card("Total Transactions", 
                                         str(summary_stats.get('total_transactions', 0)), 
                                         "Borrowing records"),
                    ft.Container(width=16),
                    self._build_stat_card("Books Borrowed", 
                                         str(summary_stats.get('total_books_borrowed', 0)), 
                                         "Total books"),
                    ft.Container(width=16),
                    self._build_stat_card("Unique Members", 
                                         str(summary_stats.get('unique_members', 0)), 
                                         "Active borrowers"),
                ]),
                
                ft.Container(height=24),
                
                # Daily statistics table
                ft.Text("Daily Statistics", size=14, weight=ft.FontWeight.BOLD, color="#1F2937"),
                ft.Container(height=12),
                self._build_borrowing_table(borrowing_stats),
            ], spacing=0)
            
        except Exception as ex:
            print(f"Error in borrowing statistics: {ex}")
            return ft.Text(f"Error loading borrowing statistics: {str(ex)}", color="#EF4444")
    
    def _build_most_borrowed_report(self, from_date=None, to_date=None):
        """Báo cáo sách được mượn nhiều nhất"""
        try:
            # Xây dựng điều kiện WHERE cho khoảng thời gian
            date_condition = ""
            if from_date:
                from_date_obj = datetime.strptime(from_date, "%m/%d/%Y")
                date_condition += f" AND DATE(bt.borrow_date) >= '{from_date_obj.strftime('%Y-%m-%d')}'"
            if to_date:
                to_date_obj = datetime.strptime(to_date, "%m/%d/%Y")
                date_condition += f" AND DATE(bt.borrow_date) <= '{to_date_obj.strftime('%Y-%m-%d')}'"
            
            # Query sách được mượn nhiều nhất
            query = f"""
                SELECT 
                    b.book_id,
                    b.title,
                    a.author_name,
                    c.category_name,
                    COUNT(btd.transaction_detail_id) as borrow_count,
                    b.total_copies,
                    b.available_copies,
                    b.price
                FROM borrowing_transaction_details btd
                JOIN borrowing_transaction bt ON btd.transaction_id = bt.transaction_id
                JOIN books b ON btd.book_id = b.book_id
                LEFT JOIN authors a ON b.author_id = a.author_id
                LEFT JOIN categories c ON b.category_id = c.category_id
                WHERE 1=1
                    {date_condition}
                GROUP BY b.book_id, b.title, a.author_name, c.category_name, b.total_copies, b.available_copies, b.price
                ORDER BY borrow_count DESC
                LIMIT 15
            """
            
            most_borrowed = fetch_all(query) or []
            
            # Tổng số lần mượn
            total_query = f"""
                SELECT COUNT(*) as total_borrows
                FROM borrowing_transaction_details btd
                JOIN borrowing_transaction bt ON btd.transaction_id = bt.transaction_id
                WHERE 1=1
                    {date_condition}
            """
            total_result = fetch_one(total_query)
            total_borrows = total_result["total_borrows"] if total_result else 0
            
            return ft.Column([
                ft.Text("Most Borrowed Books", size=16, weight=ft.FontWeight.BOLD, color="#1F2937"),
                ft.Container(height=12),
                ft.Text(f"Period: {from_date or 'All time'} - {to_date or 'Now'}", size=12, color="#6B7280"),
                ft.Container(height=8),
                ft.Text(f"Total borrows in period: {total_borrows}", size=12, color="#6B7280"),
                
                ft.Container(height=16),
                
                self._build_most_borrowed_table(most_borrowed),
            ], spacing=0)
            
        except Exception as ex:
            print(f"Error in most borrowed report: {ex}")
            return ft.Text(f"Error loading most borrowed books: {str(ex)}", color="#EF4444")
    
    def _build_overdue_list_report(self):
        """Báo cáo danh sách quá hạn"""
        try:
            # Query sách quá hạn
            query = """
                SELECT 
                    bt.transaction_id,
                    u.user_id,
                    u.fullname as member_name,
                    u.email,
                    u.phone,
                    b.book_id,
                    b.title,
                    a.author_name,
                    bt.borrow_date,
                    bt.due_date,
                    DATEDIFF(CURDATE(), bt.due_date) as days_overdue,
                    b.price,
                    btd.item_status
                FROM borrowing_transaction bt
                JOIN users u ON bt.member_id = u.user_id
                JOIN borrowing_transaction_details btd ON bt.transaction_id = btd.transaction_id
                JOIN books b ON btd.book_id = b.book_id
                LEFT JOIN authors a ON b.author_id = a.author_id
                WHERE bt.borrower_status = 'BORROWED'
                    AND bt.due_date < CURDATE()
                    AND bt.return_date IS NULL
                ORDER BY days_overdue DESC, bt.due_date
                LIMIT 50
            """
            
            overdue_list = fetch_all(query) or []
            
            # Thống kê tổng quá hạn
            summary_query = """
                SELECT 
                    COUNT(DISTINCT bt.transaction_id) as overdue_transactions,
                    COUNT(btd.transaction_detail_id) as overdue_books,
                    COUNT(DISTINCT bt.member_id) as affected_members,
                    SUM(b.price) as total_value
                FROM borrowing_transaction bt
                JOIN borrowing_transaction_details btd ON bt.transaction_id = btd.transaction_id
                JOIN books b ON btd.book_id = b.book_id
                WHERE bt.borrower_status = 'BORROWED'
                    AND bt.due_date < CURDATE()
                    AND bt.return_date IS NULL
            """
            summary_result = fetch_one(summary_query) or {}
            
            return ft.Column([
                ft.Text("Overdue Items", size=16, weight=ft.FontWeight.BOLD, color="#1F2937"),
                ft.Container(height=12),
                ft.Text(f"As of {datetime.now().strftime('%m/%d/%Y %H:%M')}", size=12, color="#6B7280"),
                
                ft.Container(height=16),
                
                # Summary
                ft.Row([
                    self._build_stat_card("Overdue Books", 
                                         str(summary_result.get('overdue_books', 0)), 
                                         "Books past due"),
                    ft.Container(width=16),
                    self._build_stat_card("Transactions", 
                                         str(summary_result.get('overdue_transactions', 0)), 
                                         "Overdue records"),
                    ft.Container(width=16),
                    self._build_stat_card("Members", 
                                         str(summary_result.get('affected_members', 0)), 
                                         "With overdue items"),
                ]),
                
                ft.Container(height=24),
                
                # Overdue list
                ft.Text("Overdue Items List", size=14, weight=ft.FontWeight.BOLD, color="#1F2937"),
                ft.Container(height=12),
                ft.Text("Books that are past their due date and not yet returned", size=12, color="#6B7280"),
                ft.Container(height=12),
                self._build_overdue_table(overdue_list),
            ], spacing=0)
            
        except Exception as ex:
            print(f"Error in overdue list: {ex}")
            return ft.Text(f"Error loading overdue list: {str(ex)}", color="#EF4444")
    
    def _build_new_members_report(self, from_date=None, to_date=None):
        """Báo cáo thành viên mới"""
        try:
            # Xây dựng điều kiện WHERE cho khoảng thời gian
            date_condition = ""
            if from_date:
                from_date_obj = datetime.strptime(from_date, "%m/%d/%Y")
                date_condition = f"WHERE DATE(u.created_at) >= '{from_date_obj.strftime('%Y-%m-%d')}'"
                if to_date:
                    to_date_obj = datetime.strptime(to_date, "%m/%d/%Y")
                    date_condition = f"WHERE DATE(u.created_at) BETWEEN '{from_date_obj.strftime('%Y-%m-%d')}' AND '{to_date_obj.strftime('%Y-%m-%d')}'"
            elif to_date:
                to_date_obj = datetime.strptime(to_date, "%m/%d/%Y")
                date_condition = f"WHERE DATE(u.created_at) <= '{to_date_obj.strftime('%Y-%m-%d')}'"
            else:
                # Nếu không có ngày, hiển thị 30 ngày gần nhất
                date_condition = f"WHERE DATE(u.created_at) >= DATE_SUB(CURDATE(), INTERVAL 30 DAY)"
            
            # Query thành viên mới
            query = f"""
                SELECT 
                    u.user_id,
                    u.fullname as member_name,
                    u.email,
                    u.phone,
                    u.address,
                    u.created_at as join_date,
                    u.status,
                    u.role_name,
                    u.totalFineDebt,
                    COUNT(DISTINCT bt.transaction_id) as total_borrows,
                    COUNT(DISTINCT CASE WHEN bt.borrower_status = 'OVERDUE' THEN bt.transaction_id END) as overdue_borrows
                FROM users u
                LEFT JOIN borrowing_transaction bt ON u.user_id = bt.member_id
                {date_condition}
                AND u.role_name = 'MEMBER'
                GROUP BY u.user_id, u.fullname, u.email, u.phone, u.address, u.created_at, u.status, u.role_name, u.totalFineDebt
                ORDER BY u.created_at DESC
                LIMIT 50
            """
            
            new_members = fetch_all(query) or []
            
            # Thống kê tổng
            stats_query = f"""
                SELECT 
                    COUNT(DISTINCT u.user_id) as total_new_members,
                    AVG(u.totalFineDebt) as avg_fine_debt,
                    SUM(u.totalFineDebt) as total_fine_debt
                FROM users u
                {date_condition}
                AND u.role_name = 'MEMBER'
            """
            stats_result = fetch_one(stats_query) or {}
            
            return ft.Column([
                ft.Text("New Members Report", size=16, weight=ft.FontWeight.BOLD, color="#1F2937"),
                ft.Container(height=12),
                ft.Text(f"Period: {from_date or 'Last 30 days'} - {to_date or 'Now'}", size=12, color="#6B7280"),
                
                ft.Container(height=16),
                
                # Summary
                ft.Row([
                    self._build_stat_card("New Members", 
                                         str(stats_result.get('total_new_members', 0)), 
                                         "Registered in period"),
                    ft.Container(width=16),
                    self._build_stat_card("Avg. Fine Debt", 
                                         f"{stats_result.get('avg_fine_debt', 0):,.0f} VND", 
                                         "Average fine debt"),
                    ft.Container(width=16),
                    self._build_stat_card("Total Fine Debt", 
                                         f"{stats_result.get('total_fine_debt', 0):,.0f} VND", 
                                         "All new members"),
                ]),
                
                ft.Container(height=24),
                
                # Members table
                ft.Text("New Members Details", size=14, weight=ft.FontWeight.BOLD, color="#1F2937"),
                ft.Container(height=12),
                ft.Text("Members who registered during the selected period", size=12, color="#6B7280"),
                ft.Container(height=12),
                self._build_new_members_table(new_members),
            ], spacing=0)
            
        except Exception as ex:
            print(f"Error in new members report: {ex}")
            return ft.Text(f"Error loading new members: {str(ex)}", color="#EF4444")
    
    def _build_stat_card(self, title, value, subtitle):
        """Card thống kê tổng quan"""
        return ft.Container(
            content=ft.Column([
                ft.Text(title, size=11, color="#9CA3AF"),
                ft.Container(height=6),
                ft.Text(value, size=28, weight=ft.FontWeight.BOLD, color="#111827"),
                ft.Container(height=4),
                ft.Text(subtitle, size=11, color="#9CA3AF"),
            ], spacing=0, horizontal_alignment=ft.CrossAxisAlignment.START),
            padding=ft.padding.all(20),
            bgcolor="#F9FAFB",
            border_radius=8,
            expand=1,
        )
    
    def _build_category_statistics_table(self, data):
        """Bảng thống kê theo thể loại"""
        if not data:
            return ft.Text("No category data available", size=14, color="#6B7280")
        
        table_rows = []
        for i, row in enumerate(data):
            # Tính tỷ lệ phần trăm
            total_copies = row.get('total_copies', 0)
            available_copies = row.get('available_copies', 0)
            on_loan = total_copies - available_copies if total_copies else 0
            
            table_rows.append(
                ft.DataRow(cells=[
                    ft.DataCell(ft.Text(str(i+1), size=13, color="#374151")),
                    ft.DataCell(ft.Text(row['category'], size=13, color="#374151")),
                    ft.DataCell(ft.Text(str(row['total_books']), size=13, color="#374151")),
                    ft.DataCell(ft.Text(str(total_copies), size=13, color="#374151")),
                    ft.DataCell(ft.Text(str(available_copies), size=13, color="#10B981")),
                    ft.DataCell(ft.Text(str(on_loan), size=13, color="#F59E0B")),
                ])
            )
        
        return ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("#", size=10, color="#9CA3AF", weight=ft.FontWeight.W_600)),
                ft.DataColumn(ft.Text("CATEGORY", size=10, color="#9CA3AF", weight=ft.FontWeight.W_600)),
                ft.DataColumn(ft.Text("UNIQUE BOOKS", size=10, color="#9CA3AF", weight=ft.FontWeight.W_600)),
                ft.DataColumn(ft.Text("TOTAL COPIES", size=10, color="#9CA3AF", weight=ft.FontWeight.W_600)),
                ft.DataColumn(ft.Text("AVAILABLE", size=10, color="#9CA3AF", weight=ft.FontWeight.W_600)),
                ft.DataColumn(ft.Text("ON LOAN", size=10, color="#9CA3AF", weight=ft.FontWeight.W_600)),
            ],
            rows=table_rows,
            horizontal_lines=ft.border.BorderSide(0.5, "#E5E7EB"),
            heading_row_height=36,
            data_row_min_height=44,
            column_spacing=60,
            width=9999,
        )
    
    def _build_borrowing_table(self, data):
        """Bảng thống kê mượn trả"""
        if not data:
            return ft.Text("No borrowing data for selected period", size=14, color="#6B7280")
        
        table_rows = []
        for row in data:
            borrow_date = row['borrow_date'].strftime("%m/%d/%Y") if row['borrow_date'] else "N/A"
            
            table_rows.append(
                ft.DataRow(cells=[
                    ft.DataCell(ft.Text(borrow_date, size=13, color="#111827")),
                    ft.DataCell(ft.Text(str(row['transactions_count']), size=13, color="#111827")),
                    ft.DataCell(ft.Text(str(row['books_borrowed']), size=13, color="#111827")),
                    ft.DataCell(ft.Text(str(row['transactions_returned']), size=13, color="#111827")),
                    ft.DataCell(ft.Text(str(row['overdue_count']), size=13, color="#EF4444" if row['overdue_count'] > 0 else "#111827")),
                ])
            )
        
        return ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("DATE", size=11, color="#9CA3AF", weight=ft.FontWeight.W_600)),
                ft.DataColumn(ft.Text("TRANSACTIONS", size=11, color="#9CA3AF", weight=ft.FontWeight.W_600)),
                ft.DataColumn(ft.Text("BOOKS BORROWED", size=11, color="#9CA3AF", weight=ft.FontWeight.W_600)),
                ft.DataColumn(ft.Text("TRANSACTIONS RETURNED", size=11, color="#9CA3AF", weight=ft.FontWeight.W_600)),
                ft.DataColumn(ft.Text("OVERDUE", size=11, color="#9CA3AF", weight=ft.FontWeight.W_600)),
            ],
            rows=table_rows,
            heading_row_height=40,
            data_row_min_height=48,
            column_spacing=80,
            width=9999,
        )
    
    def _build_most_borrowed_table(self, data):
        """Bảng sách được mượn nhiều nhất"""
        if not data:
            return ft.Text("No borrowing data for selected period", size=14, color="#6B7280")
        
        table_rows = []
        for i, row in enumerate(data):
            title = row['title'][:40] + ("..." if len(row['title']) > 40 else "")
            author = row['author_name'] or "Unknown"
            
            # Tính tỷ lệ sẵn có
            availability_pct = (row['available_copies'] / row['total_copies'] * 100) if row['total_copies'] > 0 else 0
            
            availability_badge = ft.Container(
                content=ft.Text(
                    f"{availability_pct:.0f}%", 
                    size=10, 
                    color="#FFFFFF",
                    weight=ft.FontWeight.W_600
                ),
                bgcolor="#10B981" if availability_pct >= 50 else ("#F59E0B" if availability_pct >= 20 else "#EF4444"),
                padding=ft.padding.symmetric(horizontal=8, vertical=4),
                border_radius=12,
            )
            
            table_rows.append(
                ft.DataRow(cells=[
                    ft.DataCell(ft.Text(str(i+1), size=13, color="#111827")),
                    ft.DataCell(ft.Text(title, size=13, color="#111827")),
                    ft.DataCell(ft.Text(author, size=13, color="#111827")),
                    ft.DataCell(ft.Text(row['category_name'] or "Unknown", size=13, color="#111827")),
                    ft.DataCell(ft.Text(str(row['borrow_count']), size=13, color="#111827", weight=ft.FontWeight.W_600)),
                    ft.DataCell(ft.Text(f"{row['price']:,.0f} VND" if row['price'] else "N/A", size=13, color="#111827")),
                    ft.DataCell(availability_badge),
                ])
            )
        
        return ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("#", size=11, color="#9CA3AF", weight=ft.FontWeight.W_600)),
                ft.DataColumn(ft.Text("TITLE", size=11, color="#9CA3AF", weight=ft.FontWeight.W_600)),
                ft.DataColumn(ft.Text("AUTHOR", size=11, color="#9CA3AF", weight=ft.FontWeight.W_600)),
                ft.DataColumn(ft.Text("CATEGORY", size=11, color="#9CA3AF", weight=ft.FontWeight.W_600)),
                ft.DataColumn(ft.Text("BORROW COUNT", size=11, color="#9CA3AF", weight=ft.FontWeight.W_600)),
                ft.DataColumn(ft.Text("PRICE", size=11, color="#9CA3AF", weight=ft.FontWeight.W_600)),
                ft.DataColumn(ft.Text("AVAILABILITY", size=11, color="#9CA3AF", weight=ft.FontWeight.W_600)),
            ],
            rows=table_rows,
            heading_row_height=40,
            data_row_min_height=48,
            column_spacing=60,
            width=9999,
        )
    
    def _build_overdue_table(self, data):
        """Bảng danh sách quá hạn"""
        if not data:
            return ft.Text("No overdue items", size=14, color="#6B7280")
        
        table_rows = []
        for row in data:
            borrow_date = row['borrow_date'].strftime("%m/%d/%Y") if row['borrow_date'] else "N/A"
            due_date = row['due_date'].strftime("%m/%d/%Y") if row['due_date'] else "N/A"
            days_overdue = row['days_overdue'] or 0
            
            # Xác định màu cho days overdue
            days_color = "#EF4444"  # Đỏ cho quá hạn
            if days_overdue <= 7:
                days_color = "#F59E0B"  # Cam cho quá hạn nhẹ
            elif days_overdue <= 3:
                days_color = "#EAB308"  # Vàng
            
            table_rows.append(
                ft.DataRow(cells=[
                    ft.DataCell(ft.Text(str(row['user_id']), size=13, color="#111827")),
                    ft.DataCell(ft.Text(row['member_name'][:20], size=13, color="#111827")),
                    ft.DataCell(ft.Text(row['title'][:30] + ("..." if len(row['title']) > 30 else ""), size=13, color="#111827")),
                    ft.DataCell(ft.Text(row['author_name'] or "Unknown", size=13, color="#111827")),
                    ft.DataCell(ft.Text(borrow_date, size=13, color="#111827")),
                    ft.DataCell(ft.Text(due_date, size=13, color="#111827")),
                    ft.DataCell(ft.Text(str(days_overdue), size=13, color=days_color, weight=ft.FontWeight.W_600)),
                ])
            )
        
        return ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("MEMBER ID", size=11, color="#9CA3AF", weight=ft.FontWeight.W_600)),
                ft.DataColumn(ft.Text("MEMBER NAME", size=11, color="#9CA3AF", weight=ft.FontWeight.W_600)),
                ft.DataColumn(ft.Text("BOOK TITLE", size=11, color="#9CA3AF", weight=ft.FontWeight.W_600)),
                ft.DataColumn(ft.Text("AUTHOR", size=11, color="#9CA3AF", weight=ft.FontWeight.W_600)),
                ft.DataColumn(ft.Text("BORROW DATE", size=11, color="#9CA3AF", weight=ft.FontWeight.W_600)),
                ft.DataColumn(ft.Text("DUE DATE", size=11, color="#9CA3AF", weight=ft.FontWeight.W_600)),
                ft.DataColumn(ft.Text("DAYS OVERDUE", size=11, color="#9CA3AF", weight=ft.FontWeight.W_600)),
            ],
            rows=table_rows,
            heading_row_height=40,
            data_row_min_height=48,
            column_spacing=60,
            width=9999,
        )
    
    def _build_new_members_table(self, data):
        """Bảng thành viên mới"""
        if not data:
            return ft.Text("No new members for selected period", size=14, color="#6B7280")
        
        table_rows = []
        for i, row in enumerate(data):
            join_date = row['join_date'].strftime("%m/%d/%Y") if row['join_date'] else "N/A"
            
            # Status badge
            status_badge = ft.Container(
                content=ft.Text(
                    row['status'].upper() if row['status'] else "UNKNOWN", 
                    size=10, 
                    color="#FFFFFF",
                    weight=ft.FontWeight.W_600
                ),
                bgcolor="#10B981" if (row['status'] and row['status'].upper() == 'ACTIVE') else "#EF4444",
                padding=ft.padding.symmetric(horizontal=8, vertical=4),
                border_radius=12,
            )
            
            # Fine debt
            fine_debt = row['totalFineDebt'] or 0
            fine_color = "#EF4444" if fine_debt > 0 else "#6B7280"
            
            table_rows.append(
                ft.DataRow(cells=[
                    ft.DataCell(ft.Text(str(i+1), size=13, color="#111827")),
                    ft.DataCell(ft.Text(str(row['user_id']), size=13, color="#111827")),
                    ft.DataCell(ft.Text(row['member_name'], size=13, color="#111827")),
                    ft.DataCell(ft.Text(row['email'][:25] if row['email'] else "", size=13, color="#111827")),
                    ft.DataCell(ft.Text(join_date, size=13, color="#111827")),
                    ft.DataCell(ft.Text(str(row['total_borrows'] or 0), size=13, color="#111827")),
                    ft.DataCell(ft.Text(str(row['overdue_borrows'] or 0), size=13, color="#EF4444" if row['overdue_borrows'] else "#111827")),
                    ft.DataCell(ft.Text(f"{fine_debt:,.0f} VND" if fine_debt else "0 VND", size=13, color=fine_color)),
                    ft.DataCell(status_badge),
                ])
            )
        
        return ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("#", size=11, color="#9CA3AF", weight=ft.FontWeight.W_600)),
                ft.DataColumn(ft.Text("MEMBER ID", size=11, color="#9CA3AF", weight=ft.FontWeight.W_600)),
                ft.DataColumn(ft.Text("NAME", size=11, color="#9CA3AF", weight=ft.FontWeight.W_600)),
                ft.DataColumn(ft.Text("EMAIL", size=11, color="#9CA3AF", weight=ft.FontWeight.W_600)),
                ft.DataColumn(ft.Text("JOIN DATE", size=11, color="#9CA3AF", weight=ft.FontWeight.W_600)),
                ft.DataColumn(ft.Text("TOTAL BORROWS", size=11, color="#9CA3AF", weight=ft.FontWeight.W_600)),
                ft.DataColumn(ft.Text("OVERDUE", size=11, color="#9CA3AF", weight=ft.FontWeight.W_600)),
                ft.DataColumn(ft.Text("FINE DEBT", size=11, color="#9CA3AF", weight=ft.FontWeight.W_600)),
                ft.DataColumn(ft.Text("STATUS", size=11, color="#9CA3AF", weight=ft.FontWeight.W_600)),
            ],
            rows=table_rows,
            heading_row_height=40,
            data_row_min_height=48,
            column_spacing=50,
            width=9999,
        )
    
    def _show_error(self, message):
        """Hiển thị thông báo lỗi"""
        if self.page_ref:
            self.page_ref.snack_bar = ft.SnackBar(
                content=ft.Text(message, color="#FFFFFF"),
                bgcolor="#EF4444",
                duration=3000,
            )
            self.page_ref.snack_bar.open = True
            self.page_ref.update()
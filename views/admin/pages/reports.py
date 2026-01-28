# views/admin/pages/reports.py
import flet as ft


class ReportsPage:
    """Trang báo cáo thống kê"""
    
    def __init__(self):
        self.report_type = None
        self.from_date = None
        self.to_date = None
        self.report_content = None
        
    def build(self):
        """Xây dựng giao diện chính"""
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
        # Hiển thị báo cáo mẫu
        self.report_content.content = self._build_sample_report()
        self.report_content.visible = True
        self.report_content.update()
    
    def _build_sample_report(self):
        """Báo cáo mẫu - Total Book Statistics"""
        return ft.Column([
            # Overall summary
            ft.Text("Overall summary", size=16, weight=ft.FontWeight.BOLD, color="#1F2937"),
            ft.Container(height=16),
            ft.Row([
                self._build_stat_card("Total copies", "12,345", "All books in catalog"),
                ft.Container(width=16),
                self._build_stat_card("Loans in period", "420", "Borrowing statistics"),
                ft.Container(width=16),
                self._build_stat_card("Overdue items", "37", "Still not returned"),
                ft.Container(width=16),
                self._build_stat_card("New members", "3", "Registered this period"),
            ]),
            
            ft.Container(height=32),
            
            # Total Book Statistics
            ft.Text("Total Book Statistics", size=16, weight=ft.FontWeight.BOLD, color="#1F2937"),
            ft.Container(height=16),
            self._build_book_statistics_table(),
            
            ft.Container(height=32),
            
            # Borrowing Statistics
            ft.Text("Borrowing Statistics", size=16, weight=ft.FontWeight.BOLD, color="#1F2937"),
            ft.Text("Daily counts of loans, returns and overdue items for the chosen period.", size=12, color="#6B7280"),
            ft.Container(height=12),
            self._build_borrowing_statistics_table(),
            
            ft.Container(height=32),
            
            # Most Borrowed Books
            ft.Text("Most Borrowed Books", size=16, weight=ft.FontWeight.BOLD, color="#1F2937"),
            ft.Text("Titles with the highest loan counts in the selected period.", size=12, color="#6B7280"),
            ft.Container(height=12),
            self._build_most_borrowed_table(),
            
            ft.Container(height=32),
            
            # Overdue List
            ft.Text("Overdue List", size=16, weight=ft.FontWeight.BOLD, color="#1F2937"),
            ft.Text("Members who currently hold items past their due date.", size=12, color="#6B7280"),
            ft.Container(height=12),
            self._build_overdue_list_table(),
            
            ft.Container(height=32),
            
            # New Members
            ft.Text("New Members", size=16, weight=ft.FontWeight.BOLD, color="#1F2937"),
            ft.Text("Members who registered during the selected period; this report requires a timeframe.", size=12, color="#6B7280"),
            ft.Container(height=12),
            self._build_new_members_table(),
        ], spacing=0)
    
    def _build_stat_card(self, title, value, subtitle):
        """Card thống kê tổng quan - Giống hình 1"""
        return ft.Container(
            content=ft.Column([
                ft.Text(title, size=11, color="#9CA3AF"),
                ft.Container(height=6),
                ft.Text(value, size=28, weight=ft.FontWeight.BOLD, color="#111827"),
                ft.Container(height=4),
                ft.Text(subtitle, size=11, color="#9CA3AF"),
            ], spacing=0, horizontal_alignment=ft.CrossAxisAlignment.START),
            padding=ft.padding.all(20),
            bgcolor="#F9FAFB",  # NỀN XÁM NHẠT
            border_radius=8,
            expand=1,
        )
    
    def _build_book_statistics_table(self):
        """Bảng Total Book Statistics - Có đường kẻ ngang mỏng"""
        rows = [
            ("Fiction", "4,500", "3,900", "550", "50"),
            ("Non-fiction", "3,000", "2,600", "350", "50"),
            ("Textbooks / reference", "2,000", "1,700", "250", "50"),
            ("Children / YA", "2,845", "2,000", "800", "45"),
        ]
        
        table_rows = []
        for category, total, available, on_loan, lost in rows:
            table_rows.append(
                ft.DataRow(cells=[
                    ft.DataCell(ft.Text(category, size=13, color="#374151")),
                    ft.DataCell(ft.Text(total, size=13, color="#374151")),
                    ft.DataCell(ft.Text(available, size=13, color="#374151")),
                    ft.DataCell(ft.Text(on_loan, size=13, color="#374151")),
                    ft.DataCell(ft.Text(lost, size=13, color="#374151")),
                ])
            )
        
        return ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("CATEGORY", size=10, color="#9CA3AF", weight=ft.FontWeight.W_600)),
                ft.DataColumn(ft.Text("TOTAL", size=10, color="#9CA3AF", weight=ft.FontWeight.W_600)),
                ft.DataColumn(ft.Text("AVAILABLE", size=10, color="#9CA3AF", weight=ft.FontWeight.W_600)),
                ft.DataColumn(ft.Text("ON LOAN", size=10, color="#9CA3AF", weight=ft.FontWeight.W_600)),
                ft.DataColumn(ft.Text("LOST / WITHDRAWN", size=10, color="#9CA3AF", weight=ft.FontWeight.W_600)),
            ],
            rows=table_rows,
            horizontal_lines=ft.border.BorderSide(0.5, "#E5E7EB"),  # ĐƯỜNG KẺ MỎNG
            heading_row_height=36,
            data_row_min_height=44,
            column_spacing=100,
            width=9999,
        )
    
    def _build_borrowing_statistics_table(self):
        """Bảng Borrowing Statistics - KHÔNG CÓ HORIZONTAL LINES"""
        rows = [
            ("01/01/2026", "35", "28", "30"),
            ("02/01/2026", "40", "32", "34"),
            ("03/01/2026", "28", "30", "33"),
            ("04/01/2026", "45", "38", "36"),
            ("05/01/2026", "32", "34", "35"),
        ]
        
        table_rows = []
        for date, borrowed, returned, overdue in rows:
            table_rows.append(
                ft.DataRow(cells=[
                    ft.DataCell(ft.Text(date, size=13, color="#111827")),
                    ft.DataCell(ft.Text(borrowed, size=13, color="#111827")),
                    ft.DataCell(ft.Text(returned, size=13, color="#111827")),
                    ft.DataCell(ft.Text(overdue, size=13, color="#111827")),
                ])
            )
        
        return ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("DATE", size=11, color="#9CA3AF", weight=ft.FontWeight.W_600)),
                ft.DataColumn(ft.Text("BOOKS BORROWED", size=11, color="#9CA3AF", weight=ft.FontWeight.W_600)),
                ft.DataColumn(ft.Text("BOOKS RETURNED", size=11, color="#9CA3AF", weight=ft.FontWeight.W_600)),
                ft.DataColumn(ft.Text("OVERDUE AT END OF DAY", size=11, color="#9CA3AF", weight=ft.FontWeight.W_600)),
            ],
            rows=table_rows,
            # BỎ horizontal_lines
            heading_row_height=40,
            data_row_min_height=48,
            column_spacing=120,
            width=9999,
        )
    
    def _build_most_borrowed_table(self):
        """Bảng Most Borrowed Books - KHÔNG CÓ HORIZONTAL LINES"""
        rows = [
            ("1", "Harlem Shuffle", "Colson Whitehead", "56"),
            ("2", "Fourth Wing", "Rebecca Yarros", "48"),
            ("3", "Lessons in Chemistry", "Bonnie Garmus", "44"),
            ("4", "Project Hail Mary", "Andy Weir", "39"),
            ("5", "The Midnight Library", "Matt Haig", "35"),
        ]
        
        table_rows = []
        for rank, title, author, count in rows:
            table_rows.append(
                ft.DataRow(cells=[
                    ft.DataCell(ft.Text(rank, size=13, color="#111827")),
                    ft.DataCell(ft.Text(title, size=13, color="#111827")),
                    ft.DataCell(ft.Text(author, size=13, color="#111827")),
                    ft.DataCell(ft.Text(count, size=13, color="#111827")),
                ])
            )
        
        return ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("RANK", size=11, color="#9CA3AF", weight=ft.FontWeight.W_600)),
                ft.DataColumn(ft.Text("TITLE", size=11, color="#9CA3AF", weight=ft.FontWeight.W_600)),
                ft.DataColumn(ft.Text("AUTHOR", size=11, color="#9CA3AF", weight=ft.FontWeight.W_600)),
                ft.DataColumn(ft.Text("BORROW COUNT", size=11, color="#9CA3AF", weight=ft.FontWeight.W_600)),
            ],
            rows=table_rows,
            heading_row_height=40,
            data_row_min_height=48,
            column_spacing=120,
            width=9999,
        )
    
    def _build_overdue_list_table(self):
        """Bảng Overdue List - KHÔNG CÓ HORIZONTAL LINES"""
        rows = [
            ("123 Nguyen Van A", "Harlem Shuffle", "05/01/2026", "2"),
            ("124 Tran Thi B", "Database System Concepts", "03/01/2026", "4"),
            ("125 Le Van C", "Data Structures & Algorithms", "30/12/2025", "8"),
        ]
        
        table_rows = []
        for member, book, due_date, days_overdue in rows:
            table_rows.append(
                ft.DataRow(cells=[
                    ft.DataCell(ft.Text(member, size=13, color="#111827")),
                    ft.DataCell(ft.Text(book, size=13, color="#111827")),
                    ft.DataCell(ft.Text(due_date, size=13, color="#111827")),
                    ft.DataCell(ft.Text(days_overdue, size=13, color="#111827")),
                ])
            )
        
        return ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("MEMBER", size=11, color="#9CA3AF", weight=ft.FontWeight.W_600)),
                ft.DataColumn(ft.Text("BOOK", size=11, color="#9CA3AF", weight=ft.FontWeight.W_600)),
                ft.DataColumn(ft.Text("DUE DATE", size=11, color="#9CA3AF", weight=ft.FontWeight.W_600)),
                ft.DataColumn(ft.Text("DAYS OVERDUE", size=11, color="#9CA3AF", weight=ft.FontWeight.W_600)),
            ],
            rows=table_rows,
            heading_row_height=40,
            data_row_min_height=48,
            column_spacing=120,
            width=9999,
        )
    
    def _build_new_members_table(self):
        """Bảng New Members - KHÔNG CÓ HORIZONTAL LINES"""
        rows = [
            ("123", "Nguyen Van A", "01/01/2026"),
            ("124", "Tran Thi B", "02/01/2026"),
            ("125", "Le Van C", "03/01/2026"),
        ]
        
        table_rows = []
        for member_id, name, reg_date in rows:
            table_rows.append(
                ft.DataRow(cells=[
                    ft.DataCell(ft.Text(member_id, size=13, color="#111827")),
                    ft.DataCell(ft.Text(name, size=13, color="#111827")),
                    ft.DataCell(ft.Text(reg_date, size=13, color="#111827")),
                ])
            )
        
        return ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("MEMBER ID", size=11, color="#9CA3AF", weight=ft.FontWeight.W_600)),
                ft.DataColumn(ft.Text("NAME", size=11, color="#9CA3AF", weight=ft.FontWeight.W_600)),
                ft.DataColumn(ft.Text("REGISTRATION DATE", size=11, color="#9CA3AF", weight=ft.FontWeight.W_600)),
            ],
            rows=table_rows,
            heading_row_height=40,
            data_row_min_height=48,
            column_spacing=120,
            width=9999,
        )
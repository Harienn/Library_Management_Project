# views/admin/pages/dashboard.py - PHIÊN BẢN ĐÃ SỬA HOÀN TOÀN

import flet as ft
from datetime import datetime, date
import mysql.connector
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class DashboardPage:
    def __init__(self, navigate_callback):
        self.navigate = navigate_callback
        self.db_connection = None
        self.init_database()
    
    def init_database(self):
        """Khởi tạo kết nối database"""
        try:
            self.db_connection = mysql.connector.connect(
                host=os.getenv('DB_HOST', 'localhost'),
                user=os.getenv('DB_USER', 'root'),
                password=os.getenv('DB_PASSWORD', ''),
                database=os.getenv('DB_NAME', 'LibraryDB'),
                port=os.getenv('DB_PORT', 3306)
            )
            print("Database connected successfully for dashboard")
        except mysql.connector.Error as err:
            print(f"Error connecting to database: {err}")
    
    def get_today_transactions_count(self):
        """Số giao dịch mượn/trả hôm nay"""
        if not self.db_connection:
            return 0
        
        try:
            cursor = self.db_connection.cursor(dictionary=True)
            query = """
                SELECT COUNT(*) as count 
                FROM BORROWING_TRANSACTION 
                WHERE DATE(borrow_date) = CURDATE() 
                   OR DATE(return_date) = CURDATE()
            """
            cursor.execute(query)
            result = cursor.fetchone()
            cursor.close()
            return result['count'] if result else 0
        except Exception as e:
            print(f"Error getting today transactions: {e}")
            return 0
    
    def get_current_borrowing_count(self):
        """Số sách đang được mượn"""
        if not self.db_connection:
            return 0
        
        try:
            cursor = self.db_connection.cursor(dictionary=True)
            query = """
                SELECT COUNT(*) as count
                FROM BORROWING_TRANSACTION_DETAILS btd
                JOIN BORROWING_TRANSACTION bt ON btd.transaction_id = bt.transaction_id
                WHERE bt.borrower_status IN ('BORROWED', 'OVERDUE')
            """
            cursor.execute(query)
            result = cursor.fetchone()
            cursor.close()
            return result['count'] if result else 0
        except Exception as e:
            print(f"Error getting current borrowing: {e}")
            return 0
    
    def get_overdue_today_count(self):
        """Số sách quá hạn hôm nay"""
        if not self.db_connection:
            return 0
        
        try:
            cursor = self.db_connection.cursor(dictionary=True)
            query = """
                SELECT COUNT(*) as count
                FROM BORROWING_TRANSACTION
                WHERE borrower_status = 'OVERDUE'
                AND due_date <= CURDATE()
            """
            cursor.execute(query)
            result = cursor.fetchone()
            cursor.close()
            return result['count'] if result else 0
        except Exception as e:
            print(f"Error getting overdue today: {e}")
            return 0
    
    def get_today_fines_amount(self):
        """Tổng tiền phạt đã xử lý hôm nay"""
        if not self.db_connection:
            return "0 VND"
        
        try:
            cursor = self.db_connection.cursor(dictionary=True)
            query = """
                SELECT COALESCE(SUM(amount), 0) as total
                FROM FINE
                WHERE DATE(paid_date) = CURDATE()
                AND fine_status = 'PAID'
            """
            cursor.execute(query)
            result = cursor.fetchone()
            cursor.close()
            
            total = result['total'] if result else 0
            return f"{total:,.0f} VND"
        except Exception as e:
            print(f"Error getting today fines: {e}")
            return "0 VND"
    
    def get_current_borrowing_data(self):
        """Dữ liệu sách đang mượn"""
        if not self.db_connection:
            return []
        
        try:
            cursor = self.db_connection.cursor(dictionary=True)
            query = """
                SELECT 
                    bt.transaction_id,
                    u.user_id as member_id,
                    u.fullname as member_name,
                    b.title as book_title,
                    DATE_FORMAT(bt.borrow_date, '%d/%m/%Y') as borrow_date_formatted,
                    DATE_FORMAT(bt.due_date, '%d/%m/%Y') as due_date_formatted,
                    bt.borrower_status
                FROM BORROWING_TRANSACTION bt
                JOIN USERS u ON bt.member_id = u.user_id
                JOIN BORROWING_TRANSACTION_DETAILS btd ON bt.transaction_id = btd.transaction_id
                JOIN BOOKS b ON btd.book_id = b.book_id
                WHERE bt.borrower_status IN ('BORROWED', 'OVERDUE')
                ORDER BY bt.due_date ASC
                LIMIT 5
            """
            cursor.execute(query)
            results = cursor.fetchall()
            cursor.close()
            return results
        except Exception as e:
            print(f"Error getting current borrowing data: {e}")
            return []
    
    def get_recent_fines_data(self):
        """Dữ liệu phạt gần đây"""
        if not self.db_connection:
            return []
        
        try:
            cursor = self.db_connection.cursor(dictionary=True)
            query = """
                SELECT 
                    u.user_id as member_id,
                    u.fullname as member_name,
                    bt.transaction_id,
                    fr.violation_type,
                    CASE
                        WHEN fr.violation_type = 'OVERDUE' THEN CONCAT('Overdue ', btd.days_late, ' days')
                        WHEN fr.violation_type = 'DAMAGED' THEN CONCAT('Damaged ', ROUND(btd.damage_percentage, 0), '%')
                        WHEN fr.violation_type = 'LOST' THEN 'Lost 100%'
                        ELSE fr.violation_type
                    END as reason,
                    CONCAT(FORMAT(f.amount, 0), ' VND') as amount_formatted,
                    f.fine_status
                FROM FINE f
                JOIN FINE_RULES fr ON f.rule_id = fr.rule_id
                JOIN BORROWING_TRANSACTION_DETAILS btd ON f.transaction_detail_id = btd.transaction_detail_id
                JOIN BORROWING_TRANSACTION bt ON btd.transaction_id = bt.transaction_id
                JOIN USERS u ON bt.member_id = u.user_id
                ORDER BY f.created_at DESC
                LIMIT 5
            """
            cursor.execute(query)
            results = cursor.fetchall()
            cursor.close()
            return results
        except Exception as e:
            print(f"Error getting recent fines data: {e}")
            return []
    
    def build(self):
        try:
            # Lấy dữ liệu thống kê từ database
            today_transactions = self.get_today_transactions_count()
            current_borrowing = self.get_current_borrowing_count()
            overdue_today = self.get_overdue_today_count()
            today_fines = self.get_today_fines_amount()
            
            # Stats cards row với dữ liệu thực
            stats = ft.Row([
                self._stat_card("Transactions today", str(today_transactions), "Borrow + Return"),
                self._stat_card("Books currently on loan", str(current_borrowing), "All members"),
                self._stat_card("Overdue today", str(overdue_today), "Due or overdue today"),
                self._stat_card("Fines processed today", today_fines, "Collected at this desk"),
            ], spacing=16)
            
            # Current borrowing table với dữ liệu thực
            borrowing_section = self._current_borrowing_table()
            
            # Recent fines table với dữ liệu thực
            fines_section = self._recent_fines_table()
            
            # Bottom row
            bottom_row = ft.Row([
                self._quick_actions(),
                self._short_reports(),
            ], spacing=16)
            
            return ft.Column([
                stats,
                borrowing_section,
                fines_section,
                bottom_row,
            ], spacing=16, scroll=ft.ScrollMode.AUTO)
        
        except Exception as e:
            print(f"Error loading dashboard: {e}")
            return ft.Text(f"Error loading dashboard: {str(e)}", color="red", size=16)
    
    def _stat_card(self, title, value, subtitle):
        """Stat card đơn giản"""
        return ft.Container(
            content=ft.Column([
                ft.Text(title, size=12, color="#6B7280"),
                ft.Text(value, size=24, weight=ft.FontWeight.BOLD, color="#1F2937"),
                ft.Text(subtitle, size=11, color="#9CA3AF"),
            ], spacing=4),
            padding=16,
            bgcolor="#FFFFFF",  # MÀU TRẮNG
            border_radius=8,
            border=ft.border.all(1, "#E5E7EB"),
            expand=1,
        )
    
    def _current_borrowing_table(self):
        """Current borrowing table với dữ liệu thực"""
        data = self.get_current_borrowing_data()
        
        rows = []
        for item in data:
            status_color = "#2563EB" if item['borrower_status'] == 'BORROWED' else "#DC2626"
            status_text = "Borrowing" if item['borrower_status'] == 'BORROWED' else "Overdue"
            
            rows.append(
                ft.DataRow(cells=[
                    ft.DataCell(ft.Text(str(item['transaction_id']), size=13)),
                    ft.DataCell(ft.Text(str(item['member_id']), size=13)),
                    ft.DataCell(ft.Text(item['member_name'], size=13)),
                    ft.DataCell(ft.Text(item['book_title'][:30] + "..." if len(item['book_title']) > 30 else item['book_title'], size=13)),
                    ft.DataCell(ft.Text(item['borrow_date_formatted'], size=13)),
                    ft.DataCell(ft.Text(item['due_date_formatted'], size=13)),
                    ft.DataCell(ft.Text(status_text, size=13, color=status_color, weight=ft.FontWeight.W_500)),
                ])
            )
        
        # Nếu không có dữ liệu
        if not rows:
            rows.append(
                ft.DataRow(cells=[
                    ft.DataCell(ft.Text("No data", size=13, color="#9CA3AF")),
                    ft.DataCell(ft.Text("", size=13)),
                    ft.DataCell(ft.Text("", size=13)),
                    ft.DataCell(ft.Text("", size=13)),
                    ft.DataCell(ft.Text("", size=13)),
                    ft.DataCell(ft.Text("", size=13)),
                    ft.DataCell(ft.Text("", size=13)),
                ])
            )
        
        return ft.Container(
            content=ft.Column([
                ft.Row([
                    ft.Text("Current borrowing", size=16, weight=ft.FontWeight.BOLD, color="#1F2937"),
                    ft.Container(expand=True),
                    ft.TextButton(
                        content=ft.Text('Go to "Borrow / Return"', color="#0891B2", size=13),  # MÀU CYAN
                        on_click=lambda _: self.navigate("/admin/borrow"),
                    ),
                ]),
                ft.DataTable(
                    columns=[
                        ft.DataColumn(ft.Text("TRANSACTION ID", size=11, weight=ft.FontWeight.BOLD, color="#6B7280")),
                        ft.DataColumn(ft.Text("MEMBER ID", size=11, weight=ft.FontWeight.BOLD, color="#6B7280")),
                        ft.DataColumn(ft.Text("MEMBER NAME", size=11, weight=ft.FontWeight.BOLD, color="#6B7280")),
                        ft.DataColumn(ft.Text("BOOK", size=11, weight=ft.FontWeight.BOLD, color="#6B7280")),
                        ft.DataColumn(ft.Text("BORROWED", size=11, weight=ft.FontWeight.BOLD, color="#6B7280")),
                        ft.DataColumn(ft.Text("DUE DATE", size=11, weight=ft.FontWeight.BOLD, color="#6B7280")),
                        ft.DataColumn(ft.Text("STATUS", size=11, weight=ft.FontWeight.BOLD, color="#6B7280")),
                    ],
                    rows=rows,
                    border=ft.border.all(1, "#E5E7EB"),
                    horizontal_lines=ft.border.BorderSide(1, "#F3F4F6"),
                    heading_row_color="#F9FAFB",
                ),
            ], spacing=12),
            padding=20,
            bgcolor="#FFFFFF",  # MÀU TRẮNG
            border_radius=8,
            border=ft.border.all(1, "#E5E7EB"),
        )
    
    def _recent_fines_table(self):
        """Recent fines table với dữ liệu thực"""
        data = self.get_recent_fines_data()
        
        rows = []
        for item in data:
            status_color = "#059669" if item['fine_status'] == 'PAID' else "#EA580C"
            status_text = "Paid" if item['fine_status'] == 'PAID' else "Unpaid"
            
            rows.append(
                ft.DataRow(cells=[
                    ft.DataCell(ft.Text(str(item['member_id']), size=13)),
                    ft.DataCell(ft.Text(item['member_name'], size=13)),
                    ft.DataCell(ft.Text(str(item['transaction_id']), size=13)),
                    ft.DataCell(ft.Text(item['reason'], size=13)),
                    ft.DataCell(ft.Text(item['amount_formatted'], size=13)),
                    ft.DataCell(ft.Text(status_text, size=13, color=status_color, weight=ft.FontWeight.W_500)),
                ])
            )
        
        # Nếu không có dữ liệu
        if not rows:
            rows.append(
                ft.DataRow(cells=[
                    ft.DataCell(ft.Text("No data", size=13, color="#9CA3AF")),
                    ft.DataCell(ft.Text("", size=13)),
                    ft.DataCell(ft.Text("", size=13)),
                    ft.DataCell(ft.Text("", size=13)),
                    ft.DataCell(ft.Text("", size=13)),
                    ft.DataCell(ft.Text("", size=13)),
                ])
            )
        
        return ft.Container(
            content=ft.Column([
                ft.Row([
                    ft.Text("Recent fines", size=16, weight=ft.FontWeight.BOLD, color="#1F2937"),
                    ft.Container(expand=True),
                    ft.TextButton(
                        content=ft.Text('Go to "View fines"', color="#0891B2", size=13),  # MÀU CYAN
                        on_click=lambda _: self.navigate("/admin/fines"),
                    ),
                ]),
                ft.DataTable(
                    columns=[
                        ft.DataColumn(ft.Text("MEMBER ID", size=11, weight=ft.FontWeight.BOLD, color="#6B7280")),
                        ft.DataColumn(ft.Text("MEMBER NAME", size=11, weight=ft.FontWeight.BOLD, color="#6B7280")),
                        ft.DataColumn(ft.Text("TRANSACTION ID", size=11, weight=ft.FontWeight.BOLD, color="#6B7280")),
                        ft.DataColumn(ft.Text("REASON", size=11, weight=ft.FontWeight.BOLD, color="#6B7280")),
                        ft.DataColumn(ft.Text("AMOUNT", size=11, weight=ft.FontWeight.BOLD, color="#6B7280")),
                        ft.DataColumn(ft.Text("PAYMENT STATUS", size=11, weight=ft.FontWeight.BOLD, color="#6B7280")),
                    ],
                    rows=rows,
                    border=ft.border.all(1, "#E5E7EB"),
                    horizontal_lines=ft.border.BorderSide(1, "#F3F4F6"),
                    heading_row_color="#F9FAFB",
                ),
            ], spacing=12),
            padding=20,
            bgcolor="#FFFFFF",  # MÀU TRẮNG
            border_radius=8,
            border=ft.border.all(1, "#E5E7EB"),
        )
    
    def _quick_actions(self):
        """Quick actions với click handlers"""
        actions_data = [
            ("Create borrowing transaction", "Open Borrow / Return", "/admin/borrow"),
            ("Return books & close fines", "Borrow / Return", "/admin/borrow"),
            ("Update fine as paid", 'Open "View fines"', "/admin/fines"),
            ("Search member by Member ID", "Manage users", "/admin/members"),
        ]
        
        action_items = []
        for title, link_text, route in actions_data:
            action_items.append(
                ft.Row([
                    ft.Text(title, size=13, color="#1F2937"),
                    ft.Container(expand=True),
                    ft.TextButton(
                        content=ft.Text(link_text, size=12),
                        style=ft.ButtonStyle(color="#0891B2", padding=0),  # MÀU CYAN
                        on_click=lambda e, r=route: self.navigate(r),
                    ),
                ], spacing=8, expand=True)
            )
        
        return ft.Container(
            content=ft.Column([
                ft.Text("Quick actions", size=15, weight=ft.FontWeight.BOLD, color="#1F2937"),
                ft.Column(action_items, spacing=8),
            ], spacing=12),
            padding=20,
            bgcolor="#FFFFFF",  # MÀU TRẮNG
            border_radius=8,
            border=ft.border.all(1, "#E5E7EB"),
            expand=1,
        )
    
    def _short_reports(self):
        """Short reports với click handlers"""
        reports_data = [
            ("Overdue today", "/admin/reports"),
            ("Unpaid fines", "/admin/fines"),
            ("Most borrowed this week", "/admin/reports"),
            ("Active members", "/admin/members"),
        ]
        
        chips_row1 = []
        chips_row2 = []
        
        for i, (label, route) in enumerate(reports_data):
            chip = ft.Container(
                content=ft.Text(label, size=12, color="#374151"),
                padding=ft.padding.symmetric(horizontal=12, vertical=6),
                bgcolor="#F3F4F6",
                border_radius=16,
                on_click=lambda e, r=route: self.navigate(r),
                ink=True,
            )
            if i < 2:
                chips_row1.append(chip)
            else:
                chips_row2.append(chip)
        
        return ft.Container(
            content=ft.Column([
                ft.Text("Short reports", size=15, weight=ft.FontWeight.BOLD, color="#1F2937"),
                ft.Text("Quick access to common reports for daily circulation work.", size=12, color="#6B7280"),
                ft.Row(chips_row1, spacing=8),
                ft.Row(chips_row2, spacing=8),
            ], spacing=8),
            padding=20,
            bgcolor="#FFFFFF",  # MÀU TRẮNG
            border_radius=8,
            border=ft.border.all(1, "#E5E7EB"),
            expand=1,
        )
    
    def close_connection(self):
        """Đóng kết nối database"""
        if self.db_connection:
            self.db_connection.close()
            print("Dashboard database connection closed")
# views/admin/pages/view_fines.py
import flet as ft
import mysql.connector
from datetime import datetime
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class ViewFinesPage:
    def __init__(self, page=None):
        self.page = page
        self.selected_transaction = None
        self.db_connection = None
        self.penalties_data = []
        self.penalty_rules_data = []
        
        # Khởi tạo database connection
        self.init_database()
        
        # Load dữ liệu ban đầu
        self.load_penalties_data()
        self.load_penalty_rules()
        
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
            print("Database connected successfully for fines page")
        except mysql.connector.Error as err:
            print(f"Error connecting to database: {err}")
            # Fallback to sample data if database connection fails
            self.load_sample_data()
    
    def load_sample_data(self):
        """Load dữ liệu mẫu nếu không kết nối được database"""
        print("Loading sample data for fines...")
        self.penalties_data = [
            {
                "fine_id": 1,
                "transaction_id": 3,
                "member": "2 - Trần Thị B",
                "book": "Đắc nhân tâm",
                "type": "Late return",
                "overdue_days": 5,
                "amount": "100,000 VND",
                "status": "PAID",
                "borrowing_date": "20/02/2024",
                "due_date": "05/03/2024",
                "return_date": "10/03/2024",
                "late_penalty_per_day": "20,000 VND",
                "system_amount": "100,000 VND",
                "adjusted_amount": "100,000 VND",
                "member_id": 2,
                "transaction_detail_id": 5
            },
            {
                "fine_id": 2,
                "transaction_id": 1,
                "member": "1 - Nguyễn Văn A",
                "book": "Tôi thấy hoa vàng trên cỏ xanh",
                "type": "Late return",
                "overdue_days": 0,
                "amount": "0 VND",
                "status": "UNPAID",
                "borrowing_date": "10/01/2024",
                "due_date": "24/01/2024",
                "return_date": "23/01/2024",
                "late_penalty_per_day": "20,000 VND",
                "system_amount": "0 VND",
                "adjusted_amount": "0 VND",
                "member_id": 1,
                "transaction_detail_id": 1
            },
            {
                "fine_id": 3,
                "transaction_id": 1,
                "member": "1 - Nguyễn Văn A",
                "book": "Chí Phèo",
                "type": "Damaged",
                "overdue_days": 0,
                "amount": "19,500 VND",
                "status": "PAID",
                "borrowing_date": "10/01/2024",
                "due_date": "24/01/2024",
                "return_date": "23/01/2024",
                "late_penalty_per_day": "20,000 VND",
                "system_amount": "19,500 VND",
                "adjusted_amount": "19,500 VND",
                "member_id": 1,
                "transaction_detail_id": 2
            }
        ]
        
        self.penalty_rules_data = [
            {"title": "Late-due penalty per day", "value": "20,000 VND / day"},
            {"title": "Maximum penalty per item", "value": "200,000 VND"},
            {"title": "Damaged book penalty", "value": "30% of replacement cost"},
            {"title": "Lost book penalty", "value": "100% of replacement cost"},
            {"title": "Borrowing restriction", "value": "Any unpaid penalty > 0 VND blocks new borrowing"},
        ]
    
    def load_penalties_data(self, status_filter="All", search_term=""):
        """Load dữ liệu phạt từ database"""
        if not self.db_connection:
            self.load_sample_data()
            return
            
        try:
            cursor = self.db_connection.cursor(dictionary=True)
            
            # Build query based on filters
            query = """
            SELECT 
                f.fine_id,
                CONCAT(u.user_id, ' - ', u.fullname) as member,
                b.title as book,
                CASE 
                    WHEN fr.violation_type = 'OVERDUE' THEN 'Late return'
                    WHEN fr.violation_type = 'DAMAGED' THEN 'Damaged'
                    WHEN fr.violation_type = 'LOST' THEN 'Lost'
                    ELSE fr.violation_type
                END as type,
                btd.days_late as overdue_days,
                CONCAT(FORMAT(f.amount, 0), ' VND') as amount,
                UPPER(f.fine_status) as status,
                DATE_FORMAT(bt.borrow_date, '%d/%m/%Y') as borrowing_date,
                DATE_FORMAT(bt.due_date, '%d/%m/%Y') as due_date,
                DATE_FORMAT(bt.return_date, '%d/%m/%Y') as return_date,
                CONCAT(FORMAT(fr.overdue_rate, 0), ' VND / day') as late_penalty_per_day,
                CONCAT(FORMAT(f.amount, 0), ' VND') as system_amount,
                CONCAT(FORMAT(f.amount, 0), ' VND') as adjusted_amount,
                u.user_id as member_id,
                btd.transaction_detail_id,
                bt.transaction_id,
                f.amount as raw_amount,
                f.fine_status as original_status
            FROM FINE f
            JOIN FINE_RULES fr ON f.rule_id = fr.rule_id
            JOIN BORROWING_TRANSACTION_DETAILS btd ON f.transaction_detail_id = btd.transaction_detail_id
            JOIN BORROWING_TRANSACTION bt ON btd.transaction_id = bt.transaction_id
            JOIN USERS u ON bt.member_id = u.user_id
            JOIN BOOKS b ON btd.book_id = b.book_id
            WHERE 1=1
            """
            
            params = []
            
            # Apply status filter
            if status_filter != "All":
                query += " AND f.fine_status = %s"
                params.append(status_filter.upper())
            
            # Apply search filter
            if search_term:
                search_term_like = f"%{search_term}%"
                query += """
                AND (
                    f.fine_id LIKE %s OR
                    u.user_id LIKE %s OR
                    u.fullname LIKE %s OR
                    b.title LIKE %s
                )
                """
                params.extend([search_term_like, search_term_like, search_term_like, search_term_like])
            
            query += " ORDER BY f.fine_status, f.fine_id DESC"
            
            print(f"Executing query: {query}")
            print(f"With params: {params}")
            
            cursor.execute(query, params)
            self.penalties_data = cursor.fetchall()
            cursor.close()
            
            print(f"Loaded {len(self.penalties_data)} penalties from database")
            
        except mysql.connector.Error as err:
            print(f"Error loading penalties data: {err}")
            self.load_sample_data()
        except Exception as e:
            print(f"Unexpected error: {e}")
            self.load_sample_data()
    
    def load_penalty_rules(self):
        """Lấy quy tắc phạt từ database"""
        if not self.db_connection:
            return
            
        try:
            cursor = self.db_connection.cursor(dictionary=True)
            cursor.execute("""
                SELECT 
                    violation_type,
                    overdue_rate,
                    max_late_penalty,
                    damage_rate,
                    lost_book_fine
                FROM FINE_RULES 
                WHERE is_active = TRUE
                ORDER BY rule_id
            """)
            
            fine_rules = cursor.fetchall()
            cursor.close()
            
            self.penalty_rules_data = []
            
            # Format rules for display
            for rule in fine_rules:
                if rule['violation_type'] == 'OVERDUE':
                    self.penalty_rules_data.append({
                        "title": "Late-due penalty per day",
                        "value": f"{rule['overdue_rate']:,.0f} VND / day"
                    })
                    if rule['max_late_penalty']:
                        self.penalty_rules_data.append({
                            "title": "Maximum penalty per item",
                            "value": f"{rule['max_late_penalty']:,.0f} VND"
                        })
                elif rule['violation_type'] == 'DAMAGED':
                    self.penalty_rules_data.append({
                        "title": "Damaged book penalty",
                        "value": f"{rule['damage_rate']*100:.0f}% of replacement cost"
                    })
                elif rule['violation_type'] == 'LOST':
                    self.penalty_rules_data.append({
                        "title": "Lost book penalty",
                        "value": f"{rule['lost_book_fine']*100:.0f}% of replacement cost"
                    })
            
            # Add borrowing restriction rule
            self.penalty_rules_data.append({
                "title": "Borrowing restriction",
                "value": "Any unpaid penalty > 0 VND blocks new borrowing"
            })
            
        except mysql.connector.Error as err:
            print(f"Error loading penalty rules: {err}")
            # Keep sample rules
    
    def save_penalty(self, fine_id, adjusted_amount, status, notes):
        """Lưu thay đổi phạt vào database"""
        if not self.db_connection:
            self.show_snackbar("Không thể kết nối database", "error")
            return False
            
        try:
            cursor = self.db_connection.cursor()
            
            # Parse adjusted amount (remove currency and format)
            try:
                amount_str = str(adjusted_amount).replace('VND', '').replace(',', '').strip()
                amount = float(amount_str) if amount_str else 0
            except ValueError as e:
                print(f"Error parsing amount: {e}")
                amount = 0
            
            # Update fine record
            update_query = """
            UPDATE FINE 
            SET amount = %s, 
                fine_status = %s,
                paid_date = CASE WHEN %s = 'PAID' THEN CURDATE() ELSE NULL END
            WHERE fine_id = %s
            """
            
            cursor.execute(update_query, (amount, status.upper(), status.upper(), fine_id))
            
            # Insert note if provided
            if notes:
                try:
                    # Create FINE_NOTES table if it doesn't exist
                    cursor.execute("""
                        CREATE TABLE IF NOT EXISTS FINE_NOTES (
                            note_id INT PRIMARY KEY AUTO_INCREMENT,
                            fine_id INT NOT NULL,
                            note TEXT,
                            created_by VARCHAR(50),
                            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                            FOREIGN KEY (fine_id) REFERENCES FINE(fine_id)
                        )
                    """)
                    
                    cursor.execute("""
                        INSERT INTO FINE_NOTES (fine_id, note, created_by)
                        VALUES (%s, %s, %s)
                    """, (fine_id, notes, "Librarian"))
                except Exception as e:
                    print(f"Error saving note: {e}")
                    # Continue without note if there's an error
            
            # Update user's total fine debt
            try:
                cursor.execute("""
                    UPDATE USERS u
                    SET totalFineDebt = (
                        SELECT COALESCE(SUM(f.amount), 0)
                        FROM FINE f
                        JOIN BORROWING_TRANSACTION_DETAILS btd ON f.transaction_detail_id = btd.transaction_detail_id
                        JOIN BORROWING_TRANSACTION bt ON btd.transaction_id = bt.transaction_id
                        WHERE bt.member_id = u.user_id
                        AND f.fine_status = 'UNPAID'
                    )
                    WHERE u.user_id = (
                        SELECT bt.member_id
                        FROM FINE f
                        JOIN BORROWING_TRANSACTION_DETAILS btd ON f.transaction_detail_id = btd.transaction_detail_id
                        JOIN BORROWING_TRANSACTION bt ON btd.transaction_id = bt.transaction_id
                        WHERE f.fine_id = %s
                        LIMIT 1
                    )
                """, (fine_id,))
            except Exception as e:
                print(f"Error updating user fine debt: {e}")
            
            self.db_connection.commit()
            cursor.close()
            
            self.show_snackbar("Đã lưu thay đổi thành công", "success")
            return True
            
        except mysql.connector.Error as err:
            print(f"Error saving penalty: {err}")
            self.show_snackbar(f"Lỗi khi lưu: {err}", "error")
            return False
    
    def show_snackbar(self, message, message_type="info"):
        """Hiển thị thông báo"""
        if self.page:
            color_map = {
                "success": "#10B981",
                "error": "#EF4444",
                "warning": "#F59E0B",
                "info": "#3B82F6"
            }
            color = color_map.get(message_type, "#3B82F6")
            
            self.page.snack_bar = ft.SnackBar(
                content=ft.Text(message, color="white"),
                bgcolor=color
            )
            self.page.snack_bar.open = True
            self.page.update()
    
    def refresh_data(self, e=None):
        """Refresh dữ liệu từ database"""
        search_term = self.search_field.value if hasattr(self, 'search_field') else ""
        status_filter = self.status_filter.value if hasattr(self, 'status_filter') else "All"
        
        self.load_penalties_data(status_filter, search_term)
        
        # Rebuild table
        if hasattr(self, 'penalty_radio_group'):
            self.penalty_radio_group.content.content = self._build_penalties_table_content()
            self.penalty_radio_group.update()
        
        self.show_snackbar("Đã làm mới dữ liệu", "success")
    
    def build(self):
        # Penalty detail section (sẽ update khi select)
        self.penalty_detail_section = ft.Container()
        
        self.main_content = ft.Column([
            # Header
            ft.Row([
                ft.Text("Pending penalties", size=20, weight=ft.FontWeight.BOLD, color="#1F2937"),
                ft.Container(expand=True),
                ft.ElevatedButton(
                    "Refresh",
                    bgcolor="#E5E7EB",
                    color="#111827",
                    height=36,
                    on_click=self.refresh_data
                ),
            ]),
            
            ft.Text(
                "Select a transaction to review and update its penalty details.",
                size=12,
                color="#6B7280",
            ),
            
            ft.Container(height=12),
            
            # Search penalties
            self._build_search(),
            
            ft.Container(height=12),
            
            # Penalties table
            self._build_penalties_table(),
            
            ft.Container(height=20),
            
            # Penalty detail (dynamic)
            self.penalty_detail_section,
            
            ft.Container(height=20),
            
            # Penalty rules
            self._build_penalty_rules(),
        ], spacing=0)
        
        return ft.Container(
            content=self.main_content,
            padding=ft.padding.all(16),
            bgcolor="#FFFFFF",
            border_radius=14,
            border=ft.border.all(1, "#E5E7EB"),
        )
    
    def _build_search(self):
        """Search bar"""
        self.search_field = ft.TextField(
            hint_text="Fine ID, member ID, name, book title...",
            border_color="#D1D5DB",
            text_size=13,
            border_radius=6,
            height=40,
            expand=True,
            on_submit=self.refresh_data
        )
        
        self.status_filter = ft.Dropdown(
            options=[
                ft.dropdown.Option("All"),
                ft.dropdown.Option("Unpaid"),
                ft.dropdown.Option("Paid"),
            ],
            value="All",
            border_color="#D1D5DB",
            text_size=13,
            border_radius=6,
            height=40,
            width=120,
            
        )
        self.status_filter.on_change = lambda e: self.refresh_data(e)
        print(f"Flet version: {ft.__version__} if hasattr(ft, '__version__') else 'unknown'")
        # Search button
        search_btn = ft.ElevatedButton(
            "Search",
            bgcolor="#3B82F6",
            color="#FFFFFF",
            height=40,
            on_click=self.refresh_data
        )
        
        return ft.Row([
            ft.Column([
                ft.Text("Search penalties", size=12, color="#374151"),
                self.search_field,
            ], spacing=4, expand=True),
            ft.Container(width=12),
            ft.Column([
                ft.Text("Filter by status", size=12, color="#374151"),
                self.status_filter,
            ], spacing=4),
            ft.Container(width=12),
            ft.Column([
                ft.Text("", size=12, color="#374151"),
                search_btn,
            ], spacing=4),
        ])
    
    def _build_penalties_table(self):
        """Table penalties"""
        
        table_content = self._build_penalties_table_content()
        
        # RadioGroup với content
        self.penalty_radio_group = ft.RadioGroup(
            content=ft.Container(
                content=table_content,
                expand=True,
            ),
            on_change=self.on_penalty_selected,
        )
        
        return self.penalty_radio_group
    
    def _build_penalties_table_content(self):
        """Build table content from data"""
        rows = []
        for penalty in self.penalties_data:
            is_paid = penalty["status"] == "PAID"
            
            # Type badge color
            type_color = "#2563EB"
            type_bg = "#EFF6FF"
            if penalty["type"] == "Damaged":
                type_color = "#D97706"
                type_bg = "#FEF3C7"
            elif penalty["type"] == "Lost":
                type_color = "#DC2626"
                type_bg = "#FEE2E2"
            
            rows.append(
                ft.DataRow(
                    cells=[
                        # Radio button
                        ft.DataCell(
                            ft.Radio(
                                value=str(penalty["fine_id"]),
                                fill_color="#2563EB",
                            )
                        ),
                        # Fine ID
                        ft.DataCell(ft.Text(str(penalty["fine_id"]), size=12, color="#374151")),
                        # Member
                        ft.DataCell(ft.Text(penalty["member"], size=12, color="#374151")),
                        # Book
                        ft.DataCell(ft.Text(penalty["book"], size=12, color="#374151")),
                        # Type
                        ft.DataCell(
                            ft.Container(
                                content=ft.Text(penalty["type"], size=11, color=type_color, weight=ft.FontWeight.W_500),
                                bgcolor=type_bg,
                                padding=ft.padding.symmetric(horizontal=8, vertical=4),
                                border_radius=4,
                            )
                        ),
                        # Overdue days
                        ft.DataCell(ft.Text(str(penalty["overdue_days"]), size=12, color="#374151")),
                        # Amount
                        ft.DataCell(ft.Text(penalty["amount"], size=12, color="#374151", weight=ft.FontWeight.W_500)),
                        # Status
                        ft.DataCell(
                            ft.Container(
                                content=ft.Text(
                                    penalty["status"],
                                    size=11,
                                    color="#15803D" if is_paid else "#B91C1C",
                                    weight=ft.FontWeight.W_500
                                ),
                                bgcolor="#DCFCE7" if is_paid else "#FEE2E2",
                                padding=ft.padding.symmetric(horizontal=10, vertical=4),
                                border_radius=4,
                            )
                        ),
                    ],
                )
            )
        
        return ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("", size=11, color="#9CA3AF")),
                ft.DataColumn(ft.Text("Fine ID", size=11, color="#9CA3AF", weight=ft.FontWeight.W_600)),
                ft.DataColumn(ft.Text("Member", size=11, color="#9CA3AF", weight=ft.FontWeight.W_600)),
                ft.DataColumn(ft.Text("Book", size=11, color="#9CA3AF", weight=ft.FontWeight.W_600)),
                ft.DataColumn(ft.Text("Type", size=11, color="#9CA3AF", weight=ft.FontWeight.W_600)),
                ft.DataColumn(ft.Text("Overdue days", size=11, color="#9CA3AF", weight=ft.FontWeight.W_600)),
                ft.DataColumn(ft.Text("Amount", size=11, color="#9CA3AF", weight=ft.FontWeight.W_600)),
                ft.DataColumn(ft.Text("Status", size=11, color="#9CA3AF", weight=ft.FontWeight.W_600)),
            ],
            rows=rows,
            horizontal_lines=ft.border.BorderSide(1, "#E5E7EB"),
            heading_row_height=32,
            data_row_min_height=52,
            column_spacing=16,
            width=9999,
        )
    
    def on_penalty_selected(self, e):
        """Khi chọn penalty - UPDATE DETAIL Ở DƯỚI"""
        self.selected_transaction = e.control.value
        
        # Tìm penalty data
        penalty = next((p for p in self.penalties_data if str(p["fine_id"]) == self.selected_transaction), None)
        
        if penalty:
            # Load additional details if needed
            penalty = self.load_penalty_details(penalty)
            
            # Update penalty detail section
            self.penalty_detail_section.content = self._build_penalty_detail(penalty)
            self.penalty_detail_section.update()
        else:
            # Clear detail section if no penalty found
            self.penalty_detail_section.content = None
            self.penalty_detail_section.update()
    
    def load_penalty_details(self, penalty):
        """Load thêm chi tiết nếu cần"""
        # Kiểm tra nếu cần tính toán lại số tiền
        if not self.db_connection:
            return penalty
            
        try:
            cursor = self.db_connection.cursor(dictionary=True)
            
            # Gọi stored procedure để tính toán lại
            cursor.callproc("sp_calculate_fine", [penalty["transaction_detail_id"]])
            
            for result in cursor.stored_results():
                row = result.fetchone()
                if row:
                    penalty["system_amount"] = f"{row[0]:,.0f} VND"
                    penalty["adjusted_amount"] = f"{row[0]:,.0f} VND"
            
            cursor.close()
            
        except Exception as e:
            print(f"Error calculating fine: {e}")
            # Nếu lỗi, giữ nguyên giá trị
        
        return penalty
    
    def _build_penalty_detail(self, penalty):
        """Chi tiết penalty khi select"""
        
        # Type badge color
        type_color = "#2563EB"
        type_bg = "#EFF6FF"
        if penalty["type"] == "Damaged":
            type_color = "#D97706"
            type_bg = "#FEF3C7"
        elif penalty["type"] == "Lost":
            type_color = "#DC2626"
            type_bg = "#FEE2E2"
        
        # Transaction & member
        transaction_info = ft.Row([
            ft.Column([
                ft.Text("Transaction ID", size=11, color="#6B7280"),
                ft.Text(str(penalty.get("transaction_id", "N/A")), size=13, color="#1F2937"),
            ], spacing=4, expand=1),
            ft.Column([
                ft.Text("Member", size=11, color="#6B7280"),
                ft.Text(penalty["member"], size=13, color="#1F2937"),
            ], spacing=4, expand=2),
            ft.Column([
                ft.Text("Book", size=11, color="#6B7280"),
                ft.Text(penalty["book"], size=13, color="#1F2937"),
            ], spacing=4, expand=2),
            ft.Column([
                ft.Text("Violation", size=11, color="#6B7280"),
                ft.Container(
                    content=ft.Text(penalty["type"], size=11, color=type_color, weight=ft.FontWeight.W_500),
                    bgcolor=type_bg,
                    padding=ft.padding.symmetric(horizontal=8, vertical=4),
                    border_radius=4,
                ),
            ], spacing=4, expand=1),
            ft.Column([
                ft.Text("Overdue days", size=11, color="#6B7280"),
                ft.Text(f"{penalty['overdue_days']} day(s)", size=13, color="#1F2937"),
            ], spacing=4, expand=1),
        ])
        
        # Borrowing dates
        dates_info = ft.Row([
            ft.Column([
                ft.Text("Borrowing date", size=11, color="#6B7280"),
                ft.Text(penalty["borrowing_date"], size=13, color="#1F2937"),
            ], spacing=4, expand=1),
            ft.Column([
                ft.Text("Due date", size=11, color="#6B7280"),
                ft.Text(penalty["due_date"], size=13, color="#1F2937"),
            ], spacing=4, expand=1),
            ft.Column([
                ft.Text("Actual return date", size=11, color="#6B7280"),
                ft.Text(penalty["return_date"] if penalty["return_date"] else "Not returned", size=13, color="#1F2937"),
            ], spacing=4, expand=1),
        ])
        
        # Form fields
        self.late_penalty_field = ft.TextField(
            value=penalty.get("late_penalty_per_day", "20,000 VND"),
            border_color="#D1D5DB",
            text_size=13,
            border_radius=6,
            height=44,
            read_only=True,
            content_padding=ft.padding.symmetric(horizontal=12, vertical=10),
        )
        
        self.system_amount_field = ft.TextField(
            value=penalty["system_amount"],
            border_color="#D1D5DB",
            text_size=13,
            border_radius=6,
            height=44,
            read_only=True,
            content_padding=ft.padding.symmetric(horizontal=12, vertical=10),
        )
        
        self.adjusted_amount_field = ft.TextField(
            value=penalty["adjusted_amount"],
            border_color="#D1D5DB",
            text_size=13,
            border_radius=6,
            height=44,
            content_padding=ft.padding.symmetric(horizontal=12, vertical=10),
        )
        
        self.status_dropdown = ft.Dropdown(
            options=[
                ft.dropdown.Option("PAID"),
                ft.dropdown.Option("UNPAID"),
            ],
            value=penalty["status"],
            border_color="#D1D5DB",
            text_size=13,
            border_radius=6,
            height=44,
            content_padding=ft.padding.symmetric(horizontal=12, vertical=10),
        )
        
        self.staff_notes_field = ft.TextField(
            hint_text="Reason for adjustment, exemption, payment reference, etc.",
            border_color="#D1D5DB",
            text_size=13,
            border_radius=6,
            multiline=True,
            min_lines=3,
            max_lines=3,
            content_padding=ft.padding.all(12),
            expand=True,
        )
        
        # Penalty calculation
        penalty_calculation = ft.Row([
            ft.Column([
                ft.Text("Late penalty per day", size=11, color="#374151"),
                self.late_penalty_field,
            ], spacing=4, expand=1),
            ft.Column([
                ft.Text("System calculated amount", size=11, color="#374151"),
                self.system_amount_field,
            ], spacing=4, expand=1),
            ft.Column([
                ft.Text("Adjusted amount (optional)", size=11, color="#374151"),
                self.adjusted_amount_field,
            ], spacing=4, expand=1),
            ft.Column([
                ft.Text("Penalty status", size=11, color="#374151"),
                self.status_dropdown,
            ], spacing=4, expand=1),
        ], spacing=12)
        
        # Buttons
        reset_btn = ft.OutlinedButton(
            "Reset changes",
            height=40,
            style=ft.ButtonStyle(
                color="#6B7280",
                side=ft.border.BorderSide(1, "#D1D5DB"),
            ),
            on_click=lambda e: self.reset_penalty_fields(penalty)
        )
        
        save_btn = ft.ElevatedButton(
            "Save penalty",
            bgcolor="#2563EB",
            color="#FFFFFF",
            height=40,
            on_click=lambda e: self.save_selected_penalty(penalty)
        )
        
        # Note at bottom
        note_text = ft.Text(
            "While penalties are Unpaid, the system blocks new borrowing for this member.",
            size=11,
            color="#6B7280",
            italic=True,
        )
        
        return ft.Column([
            ft.Text(f"Penalty #{penalty['fine_id']}", size=14, weight=ft.FontWeight.BOLD, color="#1F2937"),
            ft.Text(
                "Review the transaction, then confirm or adjust the penalty amount and status.",
                size=12,
                color="#6B7280",
            ),
            
            ft.Container(height=16),
            ft.Divider(height=1, color="#E5E7EB"),
            ft.Container(height=16),
            
            # Transaction & member
            ft.Text("Transaction & member", size=12, color="#1F2937", weight=ft.FontWeight.W_600),
            ft.Container(height=4),
            transaction_info,
            
            ft.Container(height=16),
            ft.Divider(height=1, color="#E5E7EB"),
            ft.Container(height=16),
            
            # Borrowing dates
            ft.Text("Borrowing dates", size=12, color="#1F2937", weight=ft.FontWeight.W_600),
            ft.Container(height=4),
            dates_info,
            
            ft.Container(height=16),
            ft.Divider(height=1, color="#E5E7EB"),
            ft.Container(height=16),
            
            # Penalty calculation
            ft.Text("Penalty calculation", size=12, color="#1F2937", weight=ft.FontWeight.W_600),
            ft.Container(height=8),
            penalty_calculation,
            
            ft.Container(height=12),
            
            # Staff notes
            ft.Text("Staff notes", size=11, color="#374151"),
            ft.Container(height=4),
            self.staff_notes_field,
            
            ft.Container(height=16),
            
            # Buttons
            ft.Row([
                ft.Container(expand=True),
                reset_btn,
                ft.Container(width=12),
                save_btn,
            ]),
            
            ft.Container(height=8),
            note_text,
        ], spacing=0)
    
    def reset_penalty_fields(self, penalty):
        """Reset các field về giá trị ban đầu"""
        self.adjusted_amount_field.value = penalty["adjusted_amount"]
        self.status_dropdown.value = penalty["status"]
        self.staff_notes_field.value = ""
        
        # Update UI
        self.adjusted_amount_field.update()
        self.status_dropdown.update()
        self.staff_notes_field.update()
        
        self.show_snackbar("Đã reset về giá trị ban đầu", "info")
    
    def save_selected_penalty(self, penalty):
        """Lưu penalty đã chọn"""
        fine_id = penalty["fine_id"]
        adjusted_amount = self.adjusted_amount_field.value
        status = self.status_dropdown.value
        notes = self.staff_notes_field.value
        
        if not fine_id:
            self.show_snackbar("Vui lòng chọn một penalty để lưu", "error")
            return
        
        success = self.save_penalty(fine_id, adjusted_amount, status, notes)
        
        if success:
            # Refresh data
            self.refresh_data()
            # Reset selection
            self.selected_transaction = None
            self.penalty_detail_section.content = None
            self.penalty_detail_section.update()
    
    def _build_penalty_rules(self):
        """Penalty rules"""
        
        # Use loaded rules or sample rules
        rules_data = self.penalty_rules_data if self.penalty_rules_data else self.get_sample_rules()
        
        rules_widgets = []
        for rule in rules_data:
            rules_widgets.append(
                ft.Row([
                    ft.Text(rule["title"], size=12, color="#374151"),
                    ft.Container(expand=True),
                    ft.Text(rule["value"], size=12, color="#374151", weight=ft.FontWeight.W_500),
                ])
            )
        
        return ft.Column([
            ft.Text("Penalty rules", size=14, weight=ft.FontWeight.BOLD, color="#1F2937"),
            ft.Text(
                "Global rules used to calculate penalties for late, damaged and lost items.",
                size=12,
                color="#6B7280",
            ),
            
            ft.Container(height=12),
            
            ft.Container(
                content=ft.Column(rules_widgets, spacing=8),
                padding=ft.padding.all(12),
                bgcolor="#F9FAFB",
                border_radius=6,
                border=ft.border.all(1, "#E5E7EB"),
            ),
        ], spacing=0)
    
    def get_sample_rules(self):
        """Quy tắc mẫu khi không kết nối được database"""
        return [
            {"title": "Late-due penalty per day", "value": "20,000 VND / day"},
            {"title": "Maximum penalty per item", "value": "200,000 VND"},
            {"title": "Damaged book penalty", "value": "30% of replacement cost"},
            {"title": "Lost book penalty", "value": "100% of replacement cost"},
            {"title": "Borrowing restriction", "value": "Any unpaid penalty > 0 VND blocks new borrowing"},
        ]
    
    def close_connection(self):
        """Đóng kết nối database"""
        if self.db_connection:
            self.db_connection.close()
            print("Database connection closed")
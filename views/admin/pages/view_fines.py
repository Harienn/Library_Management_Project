# views/admin/pages/view_fines.py
import flet as ft


class ViewFinesPage:
    def __init__(self):
        self.selected_transaction = None
        self.penalties_data = [
            {
                "transaction_id": "23",
                "member": "123 - Nguyen Van A",
                "book": "Harlem Shuffle",
                "type": "Late return",
                "overdue_days": "2",
                "amount": "40,000 VND",
                "status": "Unpaid",
                "borrowing_date": "20/12/2025",
                "due_date": "05/01/2026",
                "return_date": "07/01/2026",
                "late_penalty_per_day": "20,000 VND",
                "system_amount": "40,000 VND",
                "adjusted_amount": "40,000 VND",
            },
            {
                "transaction_id": "15",
                "member": "123 - Nguyen Van A",
                "book": "Nona the Ninth",
                "type": "Damaged",
                "overdue_days": "0",
                "amount": "60,000 VND",
                "status": "Unpaid",
                "borrowing_date": "28/12/2025",
                "due_date": "12/01/2026",
                "return_date": "12/01/2026",
                "late_penalty_per_day": "20,000 VND",
                "system_amount": "60,000 VND",
                "adjusted_amount": "60,000 VND",
            },
            {
                "transaction_id": "19",
                "member": "125 - Le Van C",
                "book": "Data Structures & Algorithms",
                "type": "Lost",
                "overdue_days": "5",
                "amount": "300,000 VND",
                "status": "Unpaid",
                "borrowing_date": "20/12/2025",
                "due_date": "04/01/2026",
                "return_date": "09/01/2026",
                "late_penalty_per_day": "20,000 VND",
                "system_amount": "300,000 VND",
                "adjusted_amount": "300,000 VND",
            },
            {
                "transaction_id": "24",
                "member": "124 - Tran Thi B",
                "book": "Database System Concepts",
                "type": "Late return",
                "overdue_days": "1",
                "amount": "20,000 VND",
                "status": "Paid",
                "borrowing_date": "02/01/2026",
                "due_date": "16/01/2026",
                "return_date": "17/01/2026",
                "late_penalty_per_day": "20,000 VND",
                "system_amount": "20,000 VND",
                "adjusted_amount": "20,000 VND",
            },
        ]
        
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
            padding=ft.Padding(14, 14, 16, 16),
            bgcolor="#FFFFFF",
            border_radius=14,
            border=ft.Border.all(1, "#E5E7EB"),
        )
    
    def _build_search(self):
        """Search bar"""
        self.search_field = ft.TextField(
            hint_text="Transaction ID, member ID, name, book title...",
            border_color="#D1D5DB",
            text_size=13,
            border_radius=6,
            height=40,
            expand=True,
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
        ])
    
    def _build_penalties_table(self):
        """Table penalties"""
        
        rows = []
        for penalty in self.penalties_data:
            is_paid = penalty["status"] == "Paid"
            
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
                                value=penalty["transaction_id"],
                                fill_color="#2563EB",
                            )
                        ),
                        # Transaction ID
                        ft.DataCell(ft.Text(penalty["transaction_id"], size=12, color="#374151")),
                        # Member
                        ft.DataCell(ft.Text(penalty["member"], size=12, color="#374151")),
                        # Book
                        ft.DataCell(ft.Text(penalty["book"], size=12, color="#374151")),
                        # Type
                        ft.DataCell(
                            ft.Container(
                                content=ft.Text(penalty["type"], size=11, color=type_color, weight=ft.FontWeight.W_500),
                                bgcolor=type_bg,
                                padding=ft.Padding(8, 4, 8, 4),
                                border_radius=4,
                            )
                        ),
                        # Overdue days
                        ft.DataCell(ft.Text(penalty["overdue_days"], size=12, color="#374151")),
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
                                padding=ft.Padding(10, 4, 10, 4),
                                border_radius=4,
                            )
                        ),
                    ],
                )
            )
        
        table = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("", size=11, color="#9CA3AF")),
                ft.DataColumn(ft.Text("Transaction ID", size=11, color="#9CA3AF", weight=ft.FontWeight.W_600)),
                ft.DataColumn(ft.Text("Member", size=11, color="#9CA3AF", weight=ft.FontWeight.W_600)),
                ft.DataColumn(ft.Text("Book", size=11, color="#9CA3AF", weight=ft.FontWeight.W_600)),
                ft.DataColumn(ft.Text("Type", size=11, color="#9CA3AF", weight=ft.FontWeight.W_600)),
                ft.DataColumn(ft.Text("Overdue days", size=11, color="#9CA3AF", weight=ft.FontWeight.W_600)),
                ft.DataColumn(ft.Text("Amount", size=11, color="#9CA3AF", weight=ft.FontWeight.W_600)),
                ft.DataColumn(ft.Text("Status", size=11, color="#9CA3AF", weight=ft.FontWeight.W_600)),
            ],
            rows=rows,
            horizontal_lines=ft.border.BorderSide(1, "#E5E7EB"),  # CHỈ CÓ ĐƯỜNG NGANG
            heading_row_height=32,
            data_row_min_height=52,
            column_spacing=16,
            width=9999,  # TABLE FULL WIDTH
        )
        
        # RadioGroup với content - BỎ SCROLL
        self.penalty_radio_group = ft.RadioGroup(
            content=ft.Container(
                content=table,
                expand=True,
            ),
            on_change=self.on_penalty_selected,
        )
        
        return self.penalty_radio_group
    
    def on_penalty_selected(self, e):
        """Khi chọn penalty - UPDATE DETAIL Ở DƯỚI"""
        self.selected_transaction = e.control.value
        
        # Tìm penalty data
        penalty = next((p for p in self.penalties_data if p["transaction_id"] == self.selected_transaction), None)
        
        if penalty:
            # Update penalty detail section
            self.penalty_detail_section.content = self._build_penalty_detail(penalty)
            self.penalty_detail_section.update()
    
    def _build_penalty_detail(self, penalty):
        """Chi tiết penalty khi select - Layout theo hình 2"""
        
        # Type badge color
        type_color = "#2563EB"
        type_bg = "#EFF6FF"
        if penalty["type"] == "Damaged":
            type_color = "#D97706"
            type_bg = "#FEF3C7"
        elif penalty["type"] == "Lost":
            type_color = "#DC2626"
            type_bg = "#FEE2E2"
        
        # Transaction & member - CHỈ HIỂN THỊ TEXT, KHÔNG CÓ BORDER
        transaction_info = ft.Row([
            ft.Column([
                ft.Text("Transaction ID", size=11, color="#6B7280"),
                ft.Text(penalty["transaction_id"], size=13, color="#1F2937"),
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
                    padding=ft.Padding(8, 4, 8, 4),
                    border_radius=4,
                ),
            ], spacing=4, expand=1),
            ft.Column([
                ft.Text("Overdue days", size=11, color="#6B7280"),
                ft.Text(f"{penalty['overdue_days']} day(s)", size=13, color="#1F2937"),
            ], spacing=4, expand=1),
        ])
        
        # Borrowing dates - CHỈ HIỂN THỊ TEXT, KHÔNG CÓ BORDER
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
                ft.Text(penalty["return_date"], size=13, color="#1F2937"),
            ], spacing=4, expand=1),
        ])
        
        # Penalty calculation - 4 TEXTFIELDS DÀI RA
        penalty_calculation = ft.Row([
            ft.Column([
                ft.Text("Late penalty per day", size=11, color="#374151"),
                ft.TextField(
                    value=penalty.get("late_penalty_per_day", "20,000 VND"),
                    border_color="#D1D5DB",
                    text_size=13,
                    border_radius=6,
                    height=44,
                    read_only=True,
                    content_padding=ft.padding.symmetric(horizontal=12, vertical=10),
                ),
            ], spacing=4, expand=1),
            ft.Column([
                ft.Text("System calculated amount", size=11, color="#374151"),
                ft.TextField(
                    value=penalty["system_amount"],
                    border_color="#D1D5DB",
                    text_size=13,
                    border_radius=6,
                    height=44,
                    read_only=True,
                    content_padding=ft.padding.symmetric(horizontal=12, vertical=10),
                ),
            ], spacing=4, expand=1),
            ft.Column([
                ft.Text("Adjusted amount (optional)", size=11, color="#374151"),
                ft.TextField(
                    value=penalty["adjusted_amount"],
                    border_color="#D1D5DB",
                    text_size=13,
                    border_radius=6,
                    height=44,
                    content_padding=ft.padding.symmetric(horizontal=12, vertical=10),
                ),
            ], spacing=4, expand=1),
            ft.Column([
                ft.Text("Penalty status", size=11, color="#374151"),
                ft.Dropdown(
                    options=[
                        ft.dropdown.Option("Paid"),
                        ft.dropdown.Option("Unpaid"),
                    ],
                    value=penalty["status"],
                    border_color="#D1D5DB",
                    text_size=13,
                    border_radius=6,
                    height=44,
                    content_padding=ft.padding.symmetric(horizontal=12, vertical=10),
                ),
            ], spacing=4, expand=1),
        ], spacing=12)
        
        # Staff notes - FULL WIDTH
        staff_notes_field = ft.TextField(
            hint_text="Reason for adjustment, exemption, payment reference, etc.",
            border_color="#D1D5DB",
            text_size=13,
            border_radius=6,
            multiline=True,
            min_lines=3,
            max_lines=3,
            content_padding=ft.padding.all(12),
            expand=True,  # FULL WIDTH
        )
        
        # Buttons
        reset_btn = ft.OutlinedButton(
            "Reset changes",
            height=40,
            style=ft.ButtonStyle(
                color="#6B7280",
                side=ft.BorderSide(1, "#D1D5DB"),
            ),
        )
        
        save_btn = ft.ElevatedButton(
            "Save penalty",
            bgcolor="#2563EB",
            color="#FFFFFF",
            height=40,
        )
        
        # Note at bottom
        note_text = ft.Text(
            "While penalties are Unpaid, the system blocks new borrowing for this member.",
            size=11,
            color="#6B7280",
            italic=True,
        )
        
        return ft.Column([
            ft.Text(f"Penalty for transaction #{penalty['transaction_id']}", size=14, weight=ft.FontWeight.BOLD, color="#1F2937"),
            ft.Text(
                "Review the transaction, then confirm or adjust the penalty amount and status.",
                size=12,
                color="#6B7280",
            ),
            
            ft.Container(height=16),
            ft.Divider(height=1, color="#E5E7EB"),  # ĐƯỜNG THẲNG NGĂN CÁCH HEADER
            ft.Container(height=16),
            
            # Transaction & member
            ft.Text("Transaction & member", size=12, color="#1F2937", weight=ft.FontWeight.W_600),
            ft.Container(height=4),
            transaction_info,
            
            ft.Container(height=16),
            ft.Divider(height=1, color="#E5E7EB"),  # ĐƯỜNG THẲNG NGĂN CÁCH
            ft.Container(height=16),
            
            # Borrowing dates
            ft.Text("Borrowing dates", size=12, color="#1F2937", weight=ft.FontWeight.W_600),
            ft.Container(height=4),
            dates_info,
            
            ft.Container(height=16),
            ft.Divider(height=1, color="#E5E7EB"),  # ĐƯỜNG THẲNG NGĂN CÁCH
            ft.Container(height=16),
            
            # Penalty calculation
            ft.Text("Penalty calculation", size=12, color="#1F2937", weight=ft.FontWeight.W_600),
            ft.Container(height=8),
            penalty_calculation,
            
            ft.Container(height=12),
            
            # Staff notes - FULL WIDTH
            ft.Text("Staff notes", size=11, color="#374151"),
            ft.Container(height=4),
            staff_notes_field,
            
            ft.Container(height=16),
            
            # Buttons - RESET VÀ SAVE KỀ NHAU Ở BÊN PHẢI
            ft.Row([
                ft.Container(expand=True),
                reset_btn,
                ft.Container(width=12),
                save_btn,
            ]),
            
            ft.Container(height=8),
            note_text,
        ], spacing=0)
    
    def _build_penalty_rules(self):
        """Penalty rules"""
        
        rules_data = [
            {
                "title": "Late-due penalty per day",
                "value": "20,000 VND / day",
            },
            {
                "title": "Maximum penalty per item",
                "value": "300,000 VND",
            },
            {
                "title": "Damaged book penalty",
                "value": "Percentage of replacement cost (configurable %)",
            },
            {
                "title": "Lost book penalty",
                "value": "100% of replacement cost",
            },
            {
                "title": "Borrowing restriction",
                "value": "Any unpaid penalty > 0 VND blocks new borrowing",
            },
        ]
        
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
                padding=ft.Padding(12, 12, 12, 12),
                bgcolor="#F9FAFB",
                border_radius=6,
                border=ft.Border.all(1, "#E5E7EB"),
            ),
        ], spacing=0)
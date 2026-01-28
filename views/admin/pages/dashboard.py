# views/admin/pages/dashboard.py
import flet as ft

class DashboardPage:
    def __init__(self, navigate_callback):
        self.navigate = navigate_callback
    
    def build(self):
        try:
            # Stats cards row
            stats = ft.Row([
                self._stat_card("Transactions today", "24", "Borrow + Return"),
                self._stat_card("Books currently on loan", "320", "All members"),
                self._stat_card("Overdue today", "25", "Due or overdue today"),
                self._stat_card("Fines processed today", "420,000 VND", "Collected at this desk"),
            ], spacing=16)
            
            # Current borrowing table
            borrowing_section = self._current_borrowing_table()
            
            # Recent fines table
            fines_section = self._recent_fines_table()
            
            # Current borrowing table
            borrowing_centered = ft.Container(
                content=borrowing_section,
                margin=ft.Margin(100, 0, 100, 0),
            )
            
            # Recent fines table centered
            fines_centered = ft.Container(
                content=fines_section,
                margin=ft.Margin(100, 0, 100, 0),
            )
            
            # Bottom row
            bottom_row = ft.Row([
                self._quick_actions(),
                self._short_reports(),
            ], spacing=16)
            
            return ft.Column([
                stats,
                borrowing_centered,
                fines_centered,
                bottom_row,
            ], spacing=16, scroll=ft.ScrollMode.AUTO)
        
        except Exception as e:
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
            bgcolor=ft.Colors.WHITE,
            border_radius=8,
            border=ft.Border.all(1, "#E5E7EB"),
            expand=1,
        )
    
    def _current_borrowing_table(self):
        """Current borrowing table"""
        return ft.Container(
            content=ft.Column([
                ft.Row([
                    ft.Text("Current borrowing", size=16, weight=ft.FontWeight.BOLD, color="#1F2937"),
                    ft.Container(expand=True),
                    ft.TextButton(
                        content=ft.Text('Go to "Borrow / Return"', color=ft.Colors.CYAN_600, size=13),
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
                    rows=[
                        ft.DataRow(cells=[
                            ft.DataCell(ft.Text("23", size=13)),
                            ft.DataCell(ft.Text("123", size=13)),
                            ft.DataCell(ft.Text("Nguyen Van A", size=13)),
                            ft.DataCell(ft.Text("Chain of Gold", size=13)),
                            ft.DataCell(ft.Text("01/01/2026", size=13)),
                            ft.DataCell(ft.Text("16/01/2026", size=13)),
                            ft.DataCell(ft.Text("Borrowing", size=13, color="#2563EB", weight=ft.FontWeight.W_500)),
                        ]),
                        ft.DataRow(cells=[
                            ft.DataCell(ft.Text("15", size=13)),
                            ft.DataCell(ft.Text("123", size=13)),
                            ft.DataCell(ft.Text("Nguyen Van A", size=13)),
                            ft.DataCell(ft.Text("Nona the Ninth", size=13)),
                            ft.DataCell(ft.Text("30/12/2025", size=13)),
                            ft.DataCell(ft.Text("14/01/2026", size=13)),
                            ft.DataCell(ft.Text("Overdue", size=13, color="#DC2626", weight=ft.FontWeight.W_500)),
                        ]),
                        ft.DataRow(cells=[
                            ft.DataCell(ft.Text("10", size=13)),
                            ft.DataCell(ft.Text("123", size=13)),
                            ft.DataCell(ft.Text("Nguyen Van A", size=13)),
                            ft.DataCell(ft.Text("Financial Feminist", size=13)),
                            ft.DataCell(ft.Text("27/12/2025", size=13)),
                            ft.DataCell(ft.Text("11/01/2026", size=13)),
                            ft.DataCell(ft.Text("Borrowing", size=13, color="#2563EB", weight=ft.FontWeight.W_500)),
                        ]),
                        ft.DataRow(cells=[
                            ft.DataCell(ft.Text("24", size=13)),
                            ft.DataCell(ft.Text("124", size=13)),
                            ft.DataCell(ft.Text("Tran Thi B", size=13)),
                            ft.DataCell(ft.Text("Database System Concepts", size=13)),
                            ft.DataCell(ft.Text("02/01/2026", size=13)),
                            ft.DataCell(ft.Text("17/01/2026", size=13)),
                            ft.DataCell(ft.Text("Borrowing", size=13, color="#2563EB", weight=ft.FontWeight.W_500)),
                        ]),
                        ft.DataRow(cells=[
                            ft.DataCell(ft.Text("19", size=13)),
                            ft.DataCell(ft.Text("125", size=13)),
                            ft.DataCell(ft.Text("Le Van C", size=13)),
                            ft.DataCell(ft.Text("Data Structures & Algorithms", size=13)),
                            ft.DataCell(ft.Text("26/12/2025", size=13)),
                            ft.DataCell(ft.Text("10/01/2026", size=13)),
                            ft.DataCell(ft.Text("Overdue", size=13, color="#DC2626", weight=ft.FontWeight.W_500)),
                        ]),
                    ],
                    border=ft.Border.all(1, "#E5E7EB"),
                    horizontal_lines=ft.BorderSide(1, "#F3F4F6"),
                    heading_row_color="#F9FAFB",
                ),
            ], spacing=12),
            padding=20,
            bgcolor=ft.Colors.WHITE,
            border_radius=8,
            border=ft.Border.all(1, "#E5E7EB"),
        )
    
    def _recent_fines_table(self):
        """Recent fines table"""
        return ft.Container(
            content=ft.Column([
                ft.Row([
                    ft.Text("Recent fines", size=16, weight=ft.FontWeight.BOLD, color="#1F2937"),
                    ft.Container(expand=True),
                    ft.TextButton(
                        content=ft.Text('Go to "View fines"', color=ft.Colors.CYAN_600, size=13),
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
                    rows=[
                        ft.DataRow(cells=[
                            ft.DataCell(ft.Text("123", size=13)),
                            ft.DataCell(ft.Text("Nguyen Van A", size=13)),
                            ft.DataCell(ft.Text("5", size=13)),
                            ft.DataCell(ft.Text("Overdue 3 days", size=13)),
                            ft.DataCell(ft.Text("60,000 VND", size=13)),
                            ft.DataCell(ft.Text("Paid", size=13, color="#059669", weight=ft.FontWeight.W_500)),
                        ]),
                        ft.DataRow(cells=[
                            ft.DataCell(ft.Text("123", size=13)),
                            ft.DataCell(ft.Text("Nguyen Van A", size=13)),
                            ft.DataCell(ft.Text("3", size=13)),
                            ft.DataCell(ft.Text("Damaged 30%", size=13)),
                            ft.DataCell(ft.Text("90,000 VND", size=13)),
                            ft.DataCell(ft.Text("Unpaid", size=13, color="#EA580C", weight=ft.FontWeight.W_500)),
                        ]),
                        ft.DataRow(cells=[
                            ft.DataCell(ft.Text("123", size=13)),
                            ft.DataCell(ft.Text("Nguyen Van A", size=13)),
                            ft.DataCell(ft.Text("2", size=13)),
                            ft.DataCell(ft.Text("Lost 100%", size=13)),
                            ft.DataCell(ft.Text("320,000 VND", size=13)),
                            ft.DataCell(ft.Text("Unpaid", size=13, color="#EA580C", weight=ft.FontWeight.W_500)),
                        ]),
                        ft.DataRow(cells=[
                            ft.DataCell(ft.Text("124", size=13)),
                            ft.DataCell(ft.Text("Tran Thi B", size=13)),
                            ft.DataCell(ft.Text("18", size=13)),
                            ft.DataCell(ft.Text("Overdue 2 days", size=13)),
                            ft.DataCell(ft.Text("40,000 VND", size=13)),
                            ft.DataCell(ft.Text("Unpaid", size=13, color="#EA580C", weight=ft.FontWeight.W_500)),
                        ]),
                        ft.DataRow(cells=[
                            ft.DataCell(ft.Text("125", size=13)),
                            ft.DataCell(ft.Text("Le Van C", size=13)),
                            ft.DataCell(ft.Text("14", size=13)),
                            ft.DataCell(ft.Text("Overdue 5 days", size=13)),
                            ft.DataCell(ft.Text("100,000 VND", size=13)),
                            ft.DataCell(ft.Text("Unpaid", size=13, color="#EA580C", weight=ft.FontWeight.W_500)),
                        ]),
                    ],
                    border=ft.Border.all(1, "#E5E7EB"),
                    horizontal_lines=ft.BorderSide(1, "#F3F4F6"),
                    heading_row_color="#F9FAFB",
                ),
            ], spacing=12),
            padding=20,
            bgcolor=ft.Colors.WHITE,
            border_radius=8,
            border=ft.Border.all(1, "#E5E7EB"),
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
                        style=ft.ButtonStyle(color=ft.Colors.CYAN_600, padding=0),
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
            bgcolor=ft.Colors.WHITE,
            border_radius=8,
            border=ft.Border.all(1, "#E5E7EB"),
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
                padding=ft.Padding(12, 6, 12, 6),
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
            bgcolor=ft.Colors.WHITE,
            border_radius=8,
            border=ft.Border.all(1, "#E5E7EB"),
            expand=1,
        )
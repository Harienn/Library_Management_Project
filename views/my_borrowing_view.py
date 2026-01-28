# views/my_borrowing_view.py
"""
My Borrowing View - GIỐNG 100% THIẾT KẾ
✅ Tất cả text, headers, columns đầy đủ
✅ Fine breakdown chi tiết
✅ Data từ database thật
"""
import flet as ft
from datetime import datetime
from services.borrow_service import (
    get_member_borrowing, 
    get_member_borrowing_history,
    get_member_stats,
    get_borrowing_detail,
    can_extend_borrowing,
    extend_borrowing,
    calculate_new_due_date,
    get_fine_notification,
)
from components.header import Header
from components.navbar import NavBar


class MyBorrowingView:
    def __init__(self, page: ft.Page, current_user: dict, navigate=None, on_logout=None):
        self.page = page
        self.current_user = current_user
        self.navigate = navigate
        self.on_logout = on_logout
        
        self.borrowing_list = []
        self.history_list = []
        self.stats = {}
    
    def build(self):
        """Build main view"""
        header = Header(self.page, self.current_user, self.navigate, self.on_logout)
        navbar = NavBar(self.page, self.current_user, self.navigate, "/my_borrowing")
        
        if not self.current_user:
            content = self.build_guest_view()
        else:
            content = self.build_member_view()
        
        main_content = ft.Column([
            header.build(),
            navbar.build(),
            content,
        ], spacing=0, expand=True)
        
        return ft.View(
            route="/my_borrowing",
            controls=[ft.Container(
                content=main_content,
                bgcolor=ft.Colors.GREY_50,
                expand=True,
            )],
        )
    
    def build_guest_view(self):
        """Guest view"""
        guest_card = ft.Container(
            content=ft.Column([
                ft.Text("This feature is for members only", size=18, weight=ft.FontWeight.BOLD),
                ft.Container(height=4),
                ft.Text("As a guest, you can search and view book information, but you cannot:", size=13, color=ft.Colors.GREY_700),
                ft.Container(height=12),
                ft.Text("• Borrow books or see your borrowing information.", size=13),
                ft.Text("• Request extension of borrowing period.", size=13),
                ft.Text("• View history and penalties (overdue, damaged, lost).", size=13),
                ft.Container(height=20),
                ft.Text("Why create a member profile?", size=18, weight=ft.FontWeight.BOLD),
                ft.Container(height=4),
                ft.Text("After registering and completing your profile, you will be able to:", size=13, color=ft.Colors.GREY_700),
                ft.Container(height=12),
                ft.Text("• Borrow books and view your borrowing information online.", size=13),
                ft.Text("• Request borrowing extensions (extension of due date) when allowed.", size=13),
                ft.Text("• View history and all penalties (overdue, damaged, lost).", size=13),
                ft.Text("• Receive notifications and reminders from the library.", size=13),
                ft.Container(height=20),
                ft.Row([
                    ft.FilledButton("Create member account", bgcolor=ft.Colors.CYAN_400, color=ft.Colors.WHITE,
                        on_click=lambda _: self.navigate("/register") if self.navigate else None,
                        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8), padding=ft.Padding(20, 12, 20, 12))),
                    ft.OutlinedButton("Login instead", on_click=lambda _: self.navigate("/login") if self.navigate else None,
                        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8), side=ft.BorderSide(1, ft.Colors.GREY_400), padding=ft.Padding(20, 12, 20, 12))),
                ], spacing=12),
            ], spacing=0), padding=24, bgcolor=ft.Colors.WHITE, border_radius=10, border=ft.Border.all(1, ft.Colors.GREY_200), width=500)

        return ft.Container(content=ft.Column([
            ft.Container(height=24),
            ft.Text("My borrowing", size=26, weight=ft.FontWeight.BOLD),
            ft.Container(height=4),
            ft.Text("You need a member account to view borrowing information and penalties.", size=13, color=ft.Colors.GREY_600),
            ft.Container(height=24),
            guest_card,
            ft.Container(height=40),
        ], scroll="auto"), padding=ft.Padding(left=40, right=40, top=0, bottom=0), expand=True)
    
    def build_member_view(self):
        """Member view - EXACTLY như thiết kế"""
        self.load_data()
        
        return ft.Container(content=ft.Column([
            self._build_title(),
            self._build_stats(),
            self._build_current_borrowing(),
            self._build_history(),
        ], spacing=20, scroll=ft.ScrollMode.AUTO), padding=ft.padding.only(left=40, right=40, top=20, bottom=40), expand=True)
    
    def load_data(self):
        """Load data từ database"""
        try:
            user_id = self.current_user.get("user_id")
            self.borrowing_list = get_member_borrowing(user_id)
            self.history_list = get_member_borrowing_history(user_id)
            self.stats = get_member_stats(user_id)
            
            # ✅ DEBUG: Print data structure
            print(f"\n=== DEBUG LOAD DATA ===")
            print(f"✓ Loaded: {len(self.borrowing_list)} borrowed, {len(self.history_list)} history")
            print(f"✓ Stats: {self.stats}")
            if self.history_list:
                print(f"✓ Sample history record keys: {list(self.history_list[0].keys())}")
                print(f"✓ Sample history record: {self.history_list[0]}")
            print(f"======================\n")
        except Exception as e:
            print(f"✗ Error loading data: {e}")
            import traceback
            traceback.print_exc()
            self.borrowing_list = []
            self.history_list = []
            self.stats = {}
    
    def refresh_data(self):
        """Refresh sau khi extend"""
        self.load_data()
        self.page.views[-1] = self.build()
        self.page.update()
    
    def _build_title(self):
        """✅ Title + Description - EXACTLY như thiết kế"""
        return ft.Container(
            content=ft.Column([
                ft.Text("My borrowing", size=24, weight=ft.FontWeight.BOLD, color="#1F2937"),
                ft.Container(height=4),
                ft.Text("View your current borrowing, extension options and fines.", size=13, color="#6B7280"),
            ], spacing=0),
            padding=20,
            bgcolor="white",
            border_radius=10,
        )
    
    def _build_stats(self):
        """✅ Stats cards - EXACTLY như thiết kế"""
        current = self.stats.get('current_borrowed', 0)
        fines = self.stats.get('total_unpaid_fines', 0)
        
        return ft.Row([
            # Card 1
            ft.Container(
                content=ft.Column([
                    ft.Text("Books currently borrowed", size=12, color="#9CA3AF"),
                    ft.Container(height=8),
                    ft.Text(f"{current} / 10", size=32, weight=ft.FontWeight.BOLD, color="#1F2937"),
                    ft.Container(height=4),
                    ft.Text("Maximum 10 books at the same time.", size=11, color="#9CA3AF"),
                ], spacing=0, horizontal_alignment=ft.CrossAxisAlignment.START),
                bgcolor="white",
                padding=20,
                border_radius=10,
                expand=1,
            ),
            ft.Container(width=20),
            # Card 2
            ft.Container(
                content=ft.Column([
                    ft.Text("Outstanding fines", size=12, color="#9CA3AF"),
                    ft.Container(height=8),
                    ft.Text(f"{fines:,.0f} VND", size=32, weight=ft.FontWeight.BOLD, color="#1F2937"),
                    ft.Container(height=4),
                    ft.Text("Borrowing may be blocked if fines exceed the limit.", size=11, color="#9CA3AF"),
                ], spacing=0, horizontal_alignment=ft.CrossAxisAlignment.START),
                bgcolor="white",
                padding=20,
                border_radius=10,
                expand=1,
            ),
        ], spacing=0)
    
    def _build_current_borrowing(self):
        """✅ Current borrowing - EXACTLY như thiết kế"""
        # Title row
        title_row = ft.Container(
            content=ft.Row([
                ft.Text("Current borrowing", size=16, weight=ft.FontWeight.BOLD, color="#1F2937"),
                ft.Container(expand=True),
                ft.Text("Extend all eligible", size=12, color="#4BC1D2"),
            ]),
            padding=15,
        )
        
        # ✅ HEADER ROW - ĐẦY ĐỦ
        header = ft.Container(
            content=ft.Row([
                ft.Text("TRANSACTION ID", size=10, weight=ft.FontWeight.BOLD, width=100, color="#6B7280"),
                ft.Text("BOOK", size=10, weight=ft.FontWeight.BOLD, width=250, color="#6B7280"),
                ft.Text("BORROWED", size=10, weight=ft.FontWeight.BOLD, width=90, color="#6B7280"),
                ft.Text("DUE DATE", size=10, weight=ft.FontWeight.BOLD, width=90, color="#6B7280"),
                ft.Text("STATUS", size=10, weight=ft.FontWeight.BOLD, width=100, color="#6B7280"),
                ft.Text("EXTENSION", size=10, weight=ft.FontWeight.BOLD, width=120, color="#6B7280"),
            ], spacing=10),
            padding=15,
            bgcolor=ft.Colors.GREY_100,
        )
        
        # DATA ROWS
        rows = []
        for borrow in self.borrowing_list:
            tid = borrow.get("transaction_id")
            status = borrow.get("borrower_status", "BORROWED")
            renew_count = borrow.get("renew_week_count", 0)
            
            if status == "OVERDUE":
                status_bg, status_color, status_text = "#FEE2E2", "#DC2626", "Overdue"
            else:
                status_bg, status_color, status_text = "#DBEAFE", "#2563EB", "Borrowing"
            
            def make_handler(t):
                return lambda e: self.show_extend_dialog(t)
            
            rows.append(ft.Container(
                content=ft.Row([
                    ft.Text(str(tid), size=13, width=100, color="#374151"),
                    ft.Text(borrow.get("book_title", "")[:35], size=13, width=250, color="#374151"),
                    ft.Text(self._format_date(borrow.get("borrow_date")), size=13, width=90, color="#374151"),
                    ft.Text(self._format_date(borrow.get("due_date")), size=13, width=90, color="#374151"),
                    ft.Container(
                        content=ft.Text(status_text, size=11, color=status_color, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER),
                        bgcolor=status_bg,
                        padding=ft.padding.symmetric(horizontal=10, vertical=5),
                        border_radius=12,
                        width=100,
                    ),
                    ft.ElevatedButton("Extend", bgcolor="white", color="#4BC1D2",
                        on_click=make_handler(tid), disabled=renew_count >= 2 or status == "OVERDUE", width=100,
                        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8))),
                ], spacing=10),
                padding=15,
                border=ft.border.only(bottom=ft.border.BorderSide(1, "#E5E7EB")),
            ))
        
        if not rows:
            rows.append(ft.Container(content=ft.Text("No books borrowed", size=14, color="#9CA3AF"), padding=40))
        
        return ft.Container(
            content=ft.Column([title_row, header, ft.Column(rows, spacing=0)], spacing=0),
            bgcolor="white",
            border_radius=10,
        )
    
    def _build_history(self):
        """✅ History & fines - EXACTLY như thiết kế"""
        # Title row
        title_row = ft.Container(
            content=ft.Row([
                ft.Text("History & fines", size=16, weight=ft.FontWeight.BOLD, color="#1F2937"),
                ft.Container(expand=True),
                ft.TextButton(
                    "View full history", 
                    style=ft.ButtonStyle(color="#4BC1D2"),
                    on_click=self.handle_view_full_history,  # ✅ FIX: Direct method call
                ),
            ]),
            padding=15,
        )
        
        # ✅ HEADER ROW - TẤT CẢ 10 COLUMNS
        header = ft.Container(
            content=ft.Row([
                ft.Text("TRANSACTION ID", size=10, weight=ft.FontWeight.BOLD, width=90, color="#6B7280"),
                ft.Text("BOOK", size=10, weight=ft.FontWeight.BOLD, width=130, color="#6B7280"),
                ft.Text("BORROWED", size=10, weight=ft.FontWeight.BOLD, width=80, color="#6B7280"),
                ft.Text("RETURNED", size=10, weight=ft.FontWeight.BOLD, width=80, color="#6B7280"),
                ft.Text("STATUS", size=10, weight=ft.FontWeight.BOLD, width=85, color="#6B7280"),
                ft.Text("OVERDUE DAYS", size=10, weight=ft.FontWeight.BOLD, width=75, color="#6B7280"),
                ft.Text("DAMAGE / LOST", size=10, weight=ft.FontWeight.BOLD, width=95, color="#6B7280"),
                ft.Text("FINE AMOUNT", size=10, weight=ft.FontWeight.BOLD, width=85, color="#6B7280"),
                ft.Text("PAYMENT DATE", size=10, weight=ft.FontWeight.BOLD, width=85, color="#6B7280"),
                ft.Text("PAYMENT STATUS", size=10, weight=ft.FontWeight.BOLD, width=90, color="#6B7280"),
            ], spacing=6),
            padding=15,
            bgcolor=ft.Colors.GREY_100,
        )
        
        # DATA ROWS + Calculate breakdown
        rows = []
        overdue_paid = 0
        damage_unpaid = 0
        lost_unpaid = 0
        
        for record in self.history_list:
            # ✅ Support multiple field name variations
            status = record.get("status") or record.get("borrower_status", "RETURNED")
            fine = record.get("fine") or record.get("fine_amount", 0)
            payment = record.get("payment_status", "NONE")
            days_late = record.get("days_late", 0) or 0
            damage_pct = record.get("damage_percentage") or record.get("damage_precentage", 0) or 0
            
            # ✅ Calculate breakdown - FIXED LOGIC
            # Overdue fines (paid) - check both "Paid" and "PAID"
            if days_late > 0 and payment.upper() == "PAID":
                overdue_paid += fine
            
            # Damage fines (unpaid) - check both "Unpaid" and "UNPAID"
            if status == "DAMAGED" and payment.upper() == "UNPAID":
                damage_unpaid += fine
            
            # Lost fines (unpaid)
            if status == "LOST" and payment.upper() == "UNPAID":
                lost_unpaid += fine
            
            # Status colors
            status_colors = {"RETURNED": ("#D1FAE5", "#059669"), "LOST": ("#FEE2E2", "#DC2626"), "DAMAGED": ("#FEF3C7", "#F59E0B")}
            status_bg, status_color = status_colors.get(status, ("#E5E7EB", "#6B7280"))
            payment_color = "#059669" if payment == "PAID" else "#DC2626"
            
            # Damage/Lost text
            if damage_pct > 0:
                damage_text = f"Damaged {damage_pct}%"
            elif status == "LOST":
                damage_text = "Lost (100%)"
            else:
                damage_text = "-"
            
            rows.append(ft.Container(
                content=ft.Row([
                    ft.Text(str(record.get("transaction_id")), size=12, width=90, color="#374151"),
                    ft.Text(record.get("book_title", "")[:18], size=12, width=130, color="#374151"),
                    ft.Text(self._format_date(record.get("borrow_date")), size=12, width=80, color="#374151"),
                    ft.Text(self._format_date(record.get("return_date")), size=12, width=80, color="#374151"),
                    ft.Container(
                        content=ft.Text(status[:8], size=10, color=status_color, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER),
                        bgcolor=status_bg, padding=ft.padding.symmetric(horizontal=6, vertical=3), border_radius=10, width=85),
                    ft.Text(str(days_late) if days_late > 0 else "0", size=12, width=75, color="#374151"),
                    ft.Text(damage_text, size=12, width=95, color="#374151"),
                    ft.Text(f"{fine:,.0f} VND" if fine > 0 else "0 VND", size=12, width=85, color="#374151"),
                    ft.Text(self._format_date(record.get("payment_date")), size=12, width=85, color="#374151"),
                    ft.Text(payment if payment != "NONE" else "Paid", size=12, color=payment_color, width=90),
                ], spacing=6),
                padding=12,
                border=ft.border.only(bottom=ft.border.BorderSide(1, "#E5E7EB")),
            ))
        
        if not rows:
            rows.append(ft.Container(content=ft.Text("No history", size=14, color="#9CA3AF"), padding=20))
        
        # ✅ SUMMARY - BREAKDOWN ĐẦY ĐỦ
        total_unpaid = damage_unpaid + lost_unpaid
        summary = ft.Container(
            content=ft.Column([
                ft.Text(f"Overdue fines: {overdue_paid:,.0f} VND (Paid)", size=12, color="#6B7280"),
                ft.Text(f"Damage fines: {damage_unpaid:,.0f} VND (Unpaid)", size=12, color="#6B7280"),
                ft.Text(f"Lost book fines: {lost_unpaid:,.0f} VND (Unpaid)", size=12, color="#6B7280"),
                ft.Divider(height=8, color="#E5E7EB"),
                ft.Row([
                    ft.Text("Total unpaid fines: ", size=13, weight=ft.FontWeight.BOLD, color="#1F2937"),
                    ft.Container(expand=True),
                    ft.Text(f"{total_unpaid:,.0f} VND", size=14, color="#DC2626", weight=ft.FontWeight.BOLD),
                ]),
            ], spacing=8),
            padding=15,
            bgcolor=ft.Colors.GREY_50,
        )
        
        return ft.Container(
            content=ft.Column([
                title_row, header, 
                ft.Column(rows, spacing=0, scroll=ft.ScrollMode.AUTO, height=400), 
                summary
            ], spacing=0),
            bgcolor="white",
            border_radius=10,
        )
    
    def _format_date(self, date_obj):
        if not date_obj:
            return "-"
        if isinstance(date_obj, str):
            try:
                date_obj = datetime.strptime(date_obj, '%Y-%m-%d').date()
            except:
                return str(date_obj)
        return date_obj.strftime('%d/%m/%Y')
    
    def show_extend_dialog(self, transaction_id):
        """Show extend dialog với popup đầy đủ"""
        try:
            detail = get_borrowing_detail(transaction_id)
            if not detail:
                self._show_simple_message("Error", "Cannot get transaction details")
                return
            
            can_extend, reason = can_extend_borrowing(transaction_id)
            new_due_date = calculate_new_due_date(detail['due_date'], 15)
            extensions_used = detail['renew_week_count'] or 0
            
            content = ft.Column([
                ft.Text("Please review the information below before confirming the extension.", size=12, color=ft.Colors.GREY_700),
                ft.Container(height=20),
                self._info_row("Member ID", str(detail['member_id'])),
                self._info_row("Member name", detail['member_name']),
                self._info_row("Transaction ID", str(detail['transaction_id'])),
                self._info_row("Book", detail['book_title']),
                self._info_row("Current status", "Borrowing", is_status=True),
                ft.Divider(height=20, color=ft.Colors.GREY_300),
                self._info_row("Borrowed date", self._format_date(detail['borrow_date'])),
                self._info_row("Current due date", self._format_date(detail['due_date'])),
                ft.Divider(height=10, color=ft.Colors.GREY_300),
                self._info_row("New due date after extension", self._format_date(new_due_date), highlight=True),
                self._info_row("Number of extensions used", f"{extensions_used + 1} / 2"),
                ft.Divider(height=20, color=ft.Colors.GREY_300),
                ft.Container(content=ft.Text(
                    "Extension is only allowed when the borrowing is not overdue, you have not reached the maximum number of extensions, and there are no blocking penalties on your account.",
                    size=11, color=ft.Colors.GREY_600, text_align=ft.TextAlign.CENTER), padding=12, bgcolor=ft.Colors.GREY_100, border_radius=8),
            ], spacing=8, tight=True)
            
            if not can_extend:
                content.controls.append(ft.Container(content=ft.Text(f"⚠️ {reason}", size=13, color=ft.Colors.RED_700, weight=ft.FontWeight.BOLD), padding=ft.padding.only(top=12)))
            
            def close_dialog(e=None):
                dialog.open = False
                self.page.update()
            
            dialog = ft.AlertDialog(modal=True, title=ft.Text("Extend borrowing period", size=20, weight=ft.FontWeight.BOLD),
                content=ft.Container(content=content, width=500, padding=20),
                actions=[ft.TextButton("Cancel", on_click=close_dialog),
                    ft.ElevatedButton("Confirm extension", bgcolor=ft.Colors.LIGHT_BLUE_400, color=ft.Colors.WHITE, 
                        disabled=not can_extend, on_click=lambda e: self._confirm_extension(transaction_id, close_dialog))],
                actions_alignment=ft.MainAxisAlignment.END)
            
            self.page.overlay.append(dialog)
            dialog.open = True
            self.page.update()
        except Exception as e:
            print(f"❌ Error: {e}")
    
    def _info_row(self, label, value, is_status=False, highlight=False):
        if is_status:
            value_widget = ft.Container(content=ft.Text(value, size=11, color=ft.Colors.WHITE, weight=ft.FontWeight.BOLD),
                bgcolor=ft.Colors.BLUE_400, padding=ft.padding.symmetric(horizontal=12, vertical=4), border_radius=12)
        elif highlight:
            value_widget = ft.Text(value, size=13, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_700)
        else:
            value_widget = ft.Text(value, size=13, weight=ft.FontWeight.BOLD)
        
        return ft.Row([ft.Text(label, size=12, color=ft.Colors.GREY_700, expand=True), value_widget], 
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
    
    def _confirm_extension(self, transaction_id, close_dialog_callback):
        success, message, new_due = extend_borrowing(transaction_id)
        close_dialog_callback()
        
        if success:
            self._show_simple_message("Success", f"Extension successful! New due date: {self._format_date(new_due)}")
            self.refresh_data()
        else:
            self._show_simple_message("Error", message)
    
    def _show_simple_message(self, title, message):
        def close(e):
            msg_dialog.open = False
            self.page.update()
        
        msg_dialog = ft.AlertDialog(modal=True, title=ft.Text(title), content=ft.Text(message), 
            actions=[ft.TextButton("OK", on_click=close)])
        self.page.overlay.append(msg_dialog)
        msg_dialog.open = True
        self.page.update()
    def handle_view_full_history(self, e):
        """✅ Handle View full history button click"""
        print("🔍 View full history clicked!")
        print(f"Navigate to /fine_notification")
        
        if self.navigate:
            self.navigate("/fine_notification")
        else:
            print("❌ Navigate function not available")
            self._show_simple_message("Error", "Navigation not available")
# components/borrowing_slip_dialog.py
"""
Borrowing Slip Dialog - Popup gia hạn mượn sách
✅ CHÍNH XÁC theo ảnh UI: Extend borrowing period
✅ Tương thích với database: BORROWING_TRANSACTION, renew_week_count
"""
import flet as ft
from datetime import datetime
from services.borrow_service import (
    get_borrowing_detail, 
    can_extend_borrowing, 
    extend_borrowing,
    calculate_new_due_date
)

class BorrowingSlipDialog:
    """
    Dialog để hiển thị thông tin mượn sách và cho phép gia hạn
    
    Business rules:
    1. Sách chưa quá hạn (current_date <= due_date)
    2. Chưa vượt số lần gia hạn (renew_week_count < 2, tối đa 2 lần)
    3. Tài khoản không bị khóa (status != 'BLOCKED')
    4. Không có phí phạt chưa thanh toán (totalFineDebt = 0)
    """
    
    def __init__(self, page, transaction_id, on_success_callback=None):
        self.page = page
        self.transaction_id = transaction_id
        self.on_success_callback = on_success_callback
        self.dialog = None
        
    def build(self):
        """Build the dialog - Match exact design from image"""
        # Load borrowing detail
        detail = get_borrowing_detail(self.transaction_id)
        
        if not detail:
            return self._build_error_dialog("Transaction not found")
        
        # Check if can extend
        can_extend, reason = can_extend_borrowing(self.transaction_id)
        
        # Calculate new due date
        new_due_date = calculate_new_due_date(detail['due_date'], extension_days=15)
        
        # Extensions info
        extensions_used = detail['renew_week_count'] or 0
        max_extensions = 2
        
        # === BUILD DIALOG CONTENT ===
        content_column = ft.Column([
            # Subtitle text
            ft.Text(
                "Please review the information below before confirming the extension.",
                size=12,
                color=ft.Colors.GREY_700,
            ),
            
            ft.Container(height=20),
            
            # Member info section
            self._info_row("Member ID", str(detail['member_id'])),
            self._info_row("Member name", detail['member_name']),
            self._info_row("Transaction ID", str(detail['transaction_id'])),
            self._info_row("Book", detail['book_title']),
            self._info_row("Current status", "Borrowing", is_status=True),
            
            ft.Divider(height=20, thickness=1, color=ft.Colors.GREY_300),
            
            # Date info section
            self._info_row("Borrowed date", self._format_date(detail['borrow_date'])),
            self._info_row("Current due date", self._format_date(detail['due_date'])),
            
            ft.Divider(height=10, thickness=1, color=ft.Colors.GREY_300),
            
            self._info_row("New due date after extension", 
                          self._format_date(new_due_date), 
                          highlight=True),
            self._info_row("Number of extensions used", 
                          f"{extensions_used + 1} / {max_extensions}"),
            
            ft.Divider(height=20, thickness=1, color=ft.Colors.GREY_300),
            
            # Warning message box
            ft.Container(
                content=ft.Text(
                    "Extension is only allowed when the borrowing is not overdue, "
                    "you have not reached the maximum number of extensions, and there "
                    "are no blocking penalties on your account.",
                    size=11,
                    color=ft.Colors.GREY_600,
                    text_align=ft.TextAlign.CENTER,
                ),
                padding=12,
                bgcolor=ft.Colors.GREY_100,
                border_radius=8,
            ),
            
            # Error message (if cannot extend)
            ft.Container(
                content=ft.Text(
                    f"⚠️ {reason}",
                    size=13,
                    color=ft.Colors.RED_700,
                    weight=ft.FontWeight.BOLD,
                ),
                padding=ft.padding.only(top=12),
                visible=not can_extend,
            ),
            
        ], spacing=8, tight=True)
        
        # === ACTION BUTTONS ===
        self.dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text(
                "Extend borrowing period",
                size=20,
                weight=ft.FontWeight.BOLD,
            ),
            content=ft.Container(
                content=content_column,
                width=500,
                padding=20,
            ),
            actions=[
                ft.TextButton(
                    "Cancel",
                    on_click=lambda e: self._close_dialog(),
                ),
                ft.ElevatedButton(
                    "Confirm extension",
                    bgcolor=ft.Colors.LIGHT_BLUE_400,
                    color=ft.Colors.WHITE,
                    disabled=not can_extend,
                    on_click=lambda e: self._handle_confirm_extension(),
                ),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        
        return self.dialog
    
    def _info_row(self, label, value, is_status=False, highlight=False):
        """
        Create an information row matching the exact design
        
        Layout: [Label (left-aligned, expand)] [Value (right-aligned)]
        """
        # Prepare value widget
        if is_status:
            # Status badge: "Borrowing" with blue background
            value_widget = ft.Container(
                content=ft.Text(
                    value,
                    size=11,
                    color=ft.Colors.WHITE,
                    weight=ft.FontWeight.BOLD,
                ),
                bgcolor=ft.Colors.BLUE_400,
                padding=ft.padding.symmetric(horizontal=12, vertical=4),
                border_radius=12,
            )
        elif highlight:
            # Highlighted value (New due date)
            value_widget = ft.Text(
                value,
                size=13,
                weight=ft.FontWeight.BOLD,
                color=ft.Colors.BLUE_700,
            )
        else:
            # Normal value
            value_widget = ft.Text(
                value,
                size=13,
                weight=ft.FontWeight.BOLD,
                color=ft.Colors.BLACK,
            )
        
        return ft.Row([
            ft.Text(
                label,
                size=12,
                color=ft.Colors.GREY_700,
                expand=True,
            ),
            value_widget,
        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
    
    def _format_date(self, date_obj):
        """Format date to DD/MM/YYYY"""
        if not date_obj:
            return "-"
        if isinstance(date_obj, str):
            try:
                date_obj = datetime.strptime(date_obj, '%Y-%m-%d').date()
            except:
                return str(date_obj)
        return date_obj.strftime('%d/%m/%Y')
    
    def _handle_confirm_extension(self):
        """Handle confirm extension button click"""
        # Perform extension
        success, message, new_due_date = extend_borrowing(self.transaction_id)
        
        if success:
            # Show success message
            self._show_success_message(
                f"Extension successful! New due date: {self._format_date(new_due_date)}"
            )
            self._close_dialog()
            
            # Call callback to refresh parent view
            if self.on_success_callback:
                self.on_success_callback()
        else:
            # Show error message
            self._show_error_message(f"Extension failed: {message}")
    
    def _close_dialog(self):
        """Close the dialog"""
        if self.dialog:
            self.dialog.open = False
            self.page.update()
    
    def _show_success_message(self, message):
        """Show success snackbar"""
        self.page.snack_bar = ft.SnackBar(
            content=ft.Row([
                ft.Icon(ft.icons.CHECK_CIRCLE, color=ft.Colors.WHITE),
                ft.Text(message, color=ft.Colors.WHITE),
            ], spacing=8),
            bgcolor=ft.Colors.GREEN_700,
            duration=3000,
        )
        self.page.snack_bar.open = True
        self.page.update()
    
    def _show_error_message(self, message):
        """Show error snackbar"""
        self.page.snack_bar = ft.SnackBar(
            content=ft.Row([
                ft.Icon(ft.icons.ERROR, color=ft.Colors.WHITE),
                ft.Text(message, color=ft.Colors.WHITE),
            ], spacing=8),
            bgcolor=ft.Colors.RED_700,
            duration=3000,
        )
        self.page.snack_bar.open = True
        self.page.update()
    
    def _build_error_dialog(self, error_message):
        """Build error dialog"""
        return ft.AlertDialog(
            modal=True,
            title=ft.Text("Error", color=ft.Colors.RED_600),
            content=ft.Text(error_message),
            actions=[
                ft.TextButton("OK", on_click=lambda e: self._close_dialog())
            ],
        )
    
    def show(self):
        """Show the dialog"""
        dialog = self.build()
        self.page.dialog = dialog
        dialog.open = True
        self.page.update()


def show_borrowing_slip(page, transaction_id, on_success_callback=None):
    """
    Helper function để show borrowing slip dialog
    
    Usage:
        from components.borrowing_slip_dialog import show_borrowing_slip
        show_borrowing_slip(self.page, transaction_id, on_success_callback=self.refresh_data)
    """
    dialog = BorrowingSlipDialog(page, transaction_id, on_success_callback)
    dialog.show()
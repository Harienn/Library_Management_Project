# components/borrowing_slip_dialog.py
"""
✅ Borrowing Slip Dialog - Popup gia hạn mượn sách
Hiển thị thông tin chi tiết + xác nhận gia hạn
"""
import flet as ft
from datetime import datetime
from services.borrow_service import (
    get_borrowing_detail, 
    can_extend_borrowing, 
    extend_borrowing,
    calculate_new_due_date
)


def show_borrowing_slip(page, transaction_id, on_success_callback=None):
    """
    ✅ BORROWING SLIP DIALOG
    Hiển thị thông tin mượn sách và cho phép gia hạn
    
    Args:
        page: ft.Page
        transaction_id: ID của giao dịch mượn
        on_success_callback: hàm gọi khi gia hạn thành công
    """
    
    def format_date(date_obj):
        """Format date to DD/MM/YYYY"""
        if not date_obj:
            return "-"
        if isinstance(date_obj, str):
            try:
                date_obj = datetime.strptime(date_obj, '%Y-%m-%d').date()
            except:
                return str(date_obj)
        return date_obj.strftime('%d/%m/%Y')
    
    def info_row(label, value, is_status=False, highlight=False):
        """Create an information row"""
        if is_status:
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
            value_widget = ft.Text(
                value,
                size=13,
                weight=ft.FontWeight.BOLD,
                color=ft.Colors.BLUE_700,
            )
        else:
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
    
    def close_dialog(e=None):
        if dialog.open:
            dialog.open = False
            page.update()
    
    def handle_confirm_extension(e):
        """Handle confirm extension button click"""
        success, message, new_due_date = extend_borrowing(transaction_id)
        
        if success:
            show_success_message(f"Extension successful! New due date: {format_date(new_due_date)}")
            close_dialog()
            if on_success_callback:
                on_success_callback()
        else:
            show_error_message(f"Extension failed: {message}")
    
    def show_success_message(message):
        """Show success snackbar"""
        page.snack_bar = ft.SnackBar(
            content=ft.Row([
                ft.Icon(ft.Icons.CHECK_CIRCLE, color=ft.Colors.WHITE),
                ft.Text(message, color=ft.Colors.WHITE),
            ], spacing=8),
            bgcolor=ft.Colors.GREEN_700,
            duration=3000,
        )
        page.snack_bar.open = True
        page.update()
    
    def show_error_message(message):
        """Show error snackbar"""
        page.snack_bar = ft.SnackBar(
            content=ft.Row([
                ft.Icon(ft.Icons.ERROR, color=ft.Colors.WHITE),
                ft.Text(message, color=ft.Colors.WHITE),
            ], spacing=8),
            bgcolor=ft.Colors.RED_700,
            duration=3000,
        )
        page.snack_bar.open = True
        page.update()
    
    # Load borrowing detail
    detail = get_borrowing_detail(transaction_id)
    
    if not detail:
        error_dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Error", color=ft.Colors.RED_600),
            content=ft.Text("Transaction not found"),
            actions=[
                ft.TextButton("OK", on_click=close_dialog)
            ],
        )
        page.dialog = error_dialog
        error_dialog.open = True
        page.update()
        return
    
    # Check if can extend
    can_extend, reason = can_extend_borrowing(transaction_id)
    
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
        info_row("Member ID", str(detail['member_id'])),
        info_row("Member name", detail['member_name']),
        info_row("Transaction ID", str(detail['transaction_id'])),
        info_row("Book", detail['book_title']),
        info_row("Current status", "Borrowing", is_status=True),
        
        ft.Divider(height=20, thickness=1, color=ft.Colors.GREY_300),
        
        # Date info section
        info_row("Borrowed date", format_date(detail['borrow_date'])),
        info_row("Current due date", format_date(detail['due_date'])),
        
        ft.Divider(height=10, thickness=1, color=ft.Colors.GREY_300),
        
        info_row("New due date after extension", 
                format_date(new_due_date), 
                highlight=True),
        info_row("Number of extensions used", 
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
    
    # === CREATE DIALOG ===
    dialog = ft.AlertDialog(
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
                on_click=close_dialog,
            ),
            ft.ElevatedButton(
                "Confirm extension",
                bgcolor=ft.Colors.LIGHT_BLUE_400,
                color=ft.Colors.WHITE,
                disabled=not can_extend,
                on_click=handle_confirm_extension,
            ),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )
    
    page.dialog = dialog
    dialog.open = True
    page.update()
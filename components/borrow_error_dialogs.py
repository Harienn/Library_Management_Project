# components/borrow_error_dialogs.py
"""
✅ Borrow Error Dialogs - Các thông báo lỗi khi mượn sách
Gồm: Nợ phạt, Tối đa 10 cuốn, Profile chưa đủ, v.v.
"""
import flet as ft


def show_unpaid_fines_error(page, fine_info, on_view_fines=None):
    """
    ⚠️ UNPAID FINES DIALOG
    Hiển thị khi user nợ phạt và không thể mượn sách
    
    Args:
        page: ft.Page
        fine_info: dict từ get_member_fines() với breakdown
        on_view_fines: callback để xem fine_notification
    """
    
    overdue = fine_info.get('overdue_fines', 0)
    damage = fine_info.get('damage_fines', 0)
    lost = fine_info.get('lost_fines', 0)
    total = fine_info.get('total_unpaid_fines', 0)
    
    def close_dialog(e=None):
        if dialog.open:
            dialog.open = False
            page.update()
    
    def view_fines(e):
        if dialog.open:
            dialog.open = False
            page.update()
        if on_view_fines:
            on_view_fines()
    
    # Build fine breakdown list
    fine_items = []
    if overdue > 0:
        fine_items.append(
            ft.Row([
                ft.Icon(ft.Icons.CALENDAR_TODAY, size=18, color=ft.Colors.ORANGE_700),
                ft.Container(width=10),
                ft.Column([
                    ft.Text("Overdue Fines", size=12, weight=ft.FontWeight.BOLD, color=ft.Colors.GREY_900),
                    ft.Text("Late return fees", size=11, color=ft.Colors.GREY_600),
                ], spacing=0, expand=True),
                ft.Text(f"{overdue:,.0f} VND", size=12, weight=ft.FontWeight.BOLD, color=ft.Colors.ORANGE_700),
            ], spacing=0),
        )
    
    if damage > 0:
        fine_items.append(
            ft.Row([
                ft.Icon(ft.Icons.WARNING_AMBER, size=18, color=ft.Colors.RED_700),
                ft.Container(width=10),
                ft.Column([
                    ft.Text("Damage Fines", size=12, weight=ft.FontWeight.BOLD, color=ft.Colors.GREY_900),
                    ft.Text("Book damage compensation", size=11, color=ft.Colors.GREY_600),
                ], spacing=0, expand=True),
                ft.Text(f"{damage:,.0f} VND", size=12, weight=ft.FontWeight.BOLD, color=ft.Colors.RED_700),
            ], spacing=0),
        )
    
    if lost > 0:
        fine_items.append(
            ft.Row([
                ft.Icon(ft.Icons.BLOCK, size=18, color=ft.Colors.RED_900),
                ft.Container(width=10),
                ft.Column([
                    ft.Text("Lost Book Fines", size=12, weight=ft.FontWeight.BOLD, color=ft.Colors.GREY_900),
                    ft.Text("Book replacement cost", size=11, color=ft.Colors.GREY_600),
                ], spacing=0, expand=True),
                ft.Text(f"{lost:,.0f} VND", size=12, weight=ft.FontWeight.BOLD, color=ft.Colors.RED_900),
            ], spacing=0),
        )
    
    content = ft.Column([
        # Error icon
        ft.Row([
            ft.Container(
                content=ft.Icon(ft.Icons.BLOCK_FLIPPED, size=60, color=ft.Colors.RED_600),
                alignment=ft.Alignment(0.5, 0),
            ),
        ]),
        
        ft.Container(height=16),
        
        # Error title
        ft.Text(
            "Cannot Borrow Books",
            size=20,
            weight=ft.FontWeight.BOLD,
            color=ft.Colors.RED_700,
            text_align=ft.TextAlign.CENTER,
        ),
        
        ft.Container(height=8),
        
        # Error message
        ft.Text(
            "You have outstanding fines that must be paid before borrowing.",
            size=13,
            color=ft.Colors.GREY_700,
            text_align=ft.TextAlign.CENTER,
        ),
        
        ft.Container(height=24),
        
        # Fine breakdown
        ft.Container(
            content=ft.Column(
                [
                    ft.Column(fine_items, spacing=12),
                    ft.Container(height=12),
                    ft.Divider(height=1, color=ft.Colors.GREY_300),
                    ft.Container(height=12),
                    ft.Row([
                        ft.Text("Total Unpaid Fines:", size=13, weight=ft.FontWeight.BOLD, expand=True, color=ft.Colors.GREY_900),
                        ft.Text(f"{total:,.0f} VND", size=14, weight=ft.FontWeight.BOLD, color=ft.Colors.RED_700),
                    ]),
                ],
                spacing=0,
            ),
            padding=20,
            bgcolor=ft.Colors.RED_50,
            border_radius=8,
            border=ft.Border.all(1, ft.Colors.RED_200),
        ),
        
        ft.Container(height=20),
        
        # Info
        ft.Container(
            content=ft.Column([
                ft.Row([
                    ft.Icon(ft.Icons.INFO, size=18, color=ft.Colors.BLUE_600),
                    ft.Container(width=10),
                    ft.Text("How to Pay Fines", size=12, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_900),
                ]),
                ft.Container(height=10),
                ft.Text(
                    "Visit the library counter or contact the staff to pay your outstanding fines. "
                    "Once paid, you'll be able to borrow books immediately.",
                    size=12,
                    color=ft.Colors.BLUE_800,
                ),
            ], spacing=0),
            padding=15,
            bgcolor=ft.Colors.BLUE_50,
            border_radius=8,
        ),
        
        ft.Container(height=24),
    ], spacing=0, scroll="auto")
    
    dialog = ft.AlertDialog(
        modal=True,
        title=None,
        content=ft.Container(
            content=content,
            width=500,
            padding=24,
        ),
        actions=[
            ft.TextButton("Close", on_click=close_dialog),
            ft.ElevatedButton(
                "View All Fines",
                bgcolor=ft.Colors.CYAN_400,
                color=ft.Colors.WHITE,
                on_click=view_fines,
            ),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )
    
    page.overlay.append(dialog)
    dialog.open = True
    page.update()


def show_max_borrowing_error(page, current_borrowed, max_limit=10):
    """
    ⚠️ MAX BORROWING DIALOG
    Hiển thị khi user đã mượn tối đa (10 cuốn)
    
    Args:
        page: ft.Page
        current_borrowed: số sách đang mượn
        max_limit: tối đa (mặc định 10)
    """
    
    def close_dialog(e=None):
        if dialog.open:
            dialog.open = False
            page.update()
    
    content = ft.Column([
        # Warning icon
        ft.Row([
            ft.Container(
                content=ft.Icon(ft.Icons.SENTIMENT_VERY_DISSATISFIED, size=60, color=ft.Colors.ORANGE_600),
                alignment=ft.Alignment(0.5, 0),
            ),
        ]),
        
        ft.Container(height=16),
        
        # Title
        ft.Text(
            "Borrowing Limit Reached",
            size=20,
            weight=ft.FontWeight.BOLD,
            color=ft.Colors.ORANGE_800,
            text_align=ft.TextAlign.CENTER,
        ),
        
        ft.Container(height=8),
        
        # Message
        ft.Text(
            "You have reached the maximum number of books you can borrow at once.",
            size=13,
            color=ft.Colors.GREY_700,
            text_align=ft.TextAlign.CENTER,
        ),
        
        ft.Container(height=24),
        
        # Current status
        ft.Container(
            content=ft.Column([
                ft.Row([
                    ft.Text("Currently Borrowing:", size=12, weight=ft.FontWeight.BOLD, width=150, color=ft.Colors.GREY_600),
                    ft.Text(f"{current_borrowed} books", size=12, weight=ft.FontWeight.BOLD, color=ft.Colors.ORANGE_700),
                ]),
                ft.Container(height=12),
                ft.Row([
                    ft.Text("Maximum Limit:", size=12, weight=ft.FontWeight.BOLD, width=150, color=ft.Colors.GREY_600),
                    ft.Text(f"{max_limit} books", size=12, weight=ft.FontWeight.BOLD, color=ft.Colors.GREY_900),
                ]),
                ft.Container(height=12),
                
                # Progress bar
                ft.ClipRRect(
                    clip_behavior=ft.ClipBehavior.ANTI_ALIAS,
                    border_radius=ft.border_radius.all(8),
                    content=ft.Container(
                        content=ft.Row([
                            ft.Container(
                                width=(current_borrowed / max_limit) * 300,
                                height=24,
                                bgcolor=ft.Colors.ORANGE_600,
                            ),
                        ]),
                        width=300,
                        height=24,
                        bgcolor=ft.Colors.GREY_300,
                    ),
                ),
            ], spacing=0),
            padding=20,
            bgcolor=ft.Colors.ORANGE_50,
            border_radius=8,
            border=ft.Border.all(1, ft.Colors.ORANGE_200),
        ),
        
        ft.Container(height=20),
        
        # Action required
        ft.Container(
            content=ft.Column([
                ft.Row([
                    ft.Icon(ft.Icons.INFO_OUTLINE, size=18, color=ft.Colors.BLUE_600),
                    ft.Container(width=10),
                    ft.Text("What to Do", size=12, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_900),
                ]),
                ft.Container(height=10),
                ft.Text(
                    "To borrow more books, please return at least "
                    f"{current_borrowed - max_limit + 1} book(s) first.",
                    size=12,
                    color=ft.Colors.BLUE_800,
                ),
                ft.Container(height=8),
                ft.Text(
                    "Check 'My Borrowing' to see your current books and their due dates.",
                    size=12,
                    color=ft.Colors.BLUE_800,
                ),
            ], spacing=0),
            padding=15,
            bgcolor=ft.Colors.BLUE_50,
            border_radius=8,
        ),
        
        ft.Container(height=24),
    ], spacing=0, scroll="auto")
    
    dialog = ft.AlertDialog(
        modal=True,
        title=None,
        content=ft.Container(
            content=content,
            width=500,
            padding=24,
        ),
        actions=[
            ft.TextButton("Close", on_click=close_dialog),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )
    
    page.overlay.append(dialog)
    dialog.open = True
    page.update()


def show_book_not_available(page, book_title):
    """
    ℹ️ BOOK NOT AVAILABLE DIALOG
    Hiển thị khi sách không còn
    
    Args:
        page: ft.Page
        book_title: tên sách
    """
    
    def close_dialog(e=None):
        if dialog.open:
            dialog.open = False
            page.update()
    
    content = ft.Column([
        ft.Row([
            ft.Container(
                content=ft.Icon(ft.Icons.LIBRARY_BOOKS, size=60, color=ft.Colors.GREY_600),
                alignment=ft.Alignment(0.5, 0),
            ),
        ]),
        
        ft.Container(height=16),
        
        ft.Text(
            "Book Not Available",
            size=20,
            weight=ft.FontWeight.BOLD,
            color=ft.Colors.GREY_800,
            text_align=ft.TextAlign.CENTER,
        ),
        
        ft.Container(height=20),
        
        ft.Container(
            content=ft.Column([
                ft.Text(f'"{book_title}"', size=14, weight=ft.FontWeight.BOLD, color=ft.Colors.GREY_900),
                ft.Container(height=10),
                ft.Text(
                    "All copies of this book are currently borrowed. "
                    "Please try again later or ask the staff for availability information.",
                    size=12,
                    color=ft.Colors.GREY_700,
                ),
            ], spacing=0),
            padding=20,
            bgcolor=ft.Colors.GREY_100,
            border_radius=8,
        ),
        
        ft.Container(height=24),
    ], spacing=0)
    
    dialog = ft.AlertDialog(
        modal=True,
        title=None,
        content=ft.Container(
            content=content,
            width=480,
            padding=24,
        ),
        actions=[
            ft.TextButton("Close", on_click=close_dialog),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )
    
    page.overlay.append(dialog)
    dialog.open = True
    page.update()
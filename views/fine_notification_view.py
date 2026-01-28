# views/fine_notification_view.py
"""
Fine Notification View - Hiển thị thông báo phạt
✅ Match thiết kế exactly
✅ Responsive layout
✅ Member info + fine details
"""
import flet as ft
from services.borrow_service import get_fine_notification
from components.header import Header
from components.navbar import NavBar


class FineNotificationView:
    def __init__(self, page: ft.Page, current_user: dict, navigate=None, on_logout=None):
        self.page = page
        self.current_user = current_user
        self.navigate = navigate
        self.on_logout = on_logout
    
    def build(self):
        """Build the fine notification view"""
        header = Header(self.page, self.current_user, self.navigate, self.on_logout)
        navbar = NavBar(self.page, self.current_user, self.navigate, "/fine_notification")
        
        # Get fine notification data
        fine_data = None
        if self.current_user:
            member_id = self.current_user.get("user_id")
            fine_data = get_fine_notification(member_id)
        
        # Build content
        if not fine_data or not fine_data.get('has_unpaid'):
            content = self._build_no_fines_view()
        else:
            content = self._build_fine_notification_view(fine_data)
        
        main_content = ft.Column(
            [
                header.build(),
                navbar.build(),
                content,
            ],
            spacing=0,
            expand=True,
        )
        
        return ft.View(
            route="/fine_notification",
            controls=[
                ft.Container(
                    content=main_content,
                    bgcolor=ft.Colors.GREY_50,
                    expand=True,
                )
            ],
        )
    
    def _build_no_fines_view(self):
        """View khi không có phạt"""
        return ft.Container(
            content=ft.Column(
                [
                    ft.Container(height=40),
                    ft.Text("Fine Status", size=24, weight=ft.FontWeight.BOLD),
                    ft.Container(height=8),
                    ft.Text(
                        "You have no unpaid fines. Keep up the good work!",
                        size=14,
                        color=ft.Colors.GREY_600,
                    ),
                    ft.Container(height=40),
                    ft.Container(
                        content=ft.Column(
                            [
                                ft.Icon(ft.Icons.CHECK_CIRCLE, size=64, color=ft.Colors.GREEN_400),
                                ft.Container(height=16),
                                ft.Text(
                                    "All Clear!",
                                    size=20,
                                    weight=ft.FontWeight.BOLD,
                                    text_align=ft.TextAlign.CENTER,
                                ),
                                ft.Text(
                                    "Your account is in good standing",
                                    size=13,
                                    color=ft.Colors.GREY_600,
                                    text_align=ft.TextAlign.CENTER,
                                ),
                            ],
                            spacing=0,
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        ),
                        padding=40,
                        bgcolor=ft.Colors.WHITE,
                        border_radius=10,
                    ),
                ],
                scroll="auto",
            ),
            padding=ft.Padding(left=40, right=40, top=0, bottom=40),
            expand=True,
        )
    
    def _build_fine_notification_view(self, fine_data):
        """View khi có phạt chưa thanh toán"""
        # ⚠️ Banner
        banner = ft.Container(
            content=ft.Row(
                [
                    ft.Icon(ft.Icons.WARNING, size=32, color=ft.Colors.RED_700),
                    ft.Container(width=8),
                    ft.Text(
                        "FINE NOTIFICATION",
                        size=14,
                        weight=ft.FontWeight.BOLD,
                        color=ft.Colors.RED_700,
                    ),
                ],
                spacing=0,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            padding=ft.padding.symmetric(horizontal=16, vertical=12),
            bgcolor=ft.Colors.RED_50,
            border_radius=20,
        )
        
        # Main notification card
        notification_card = ft.Container(
            content=ft.Column(
                [
                    # Title
                    ft.Text(
                        "You have unpaid library fines",
                        size=20,
                        weight=ft.FontWeight.BOLD,
                    ),
                    ft.Container(height=8),
                    ft.Text(
                        "Please review the information below. Your borrowing or extension may be blocked until fines are paid.",
                        size=13,
                        color=ft.Colors.GREY_600,
                    ),
                    ft.Container(height=20),
                    
                    # Member info
                    ft.Row(
                        [
                            ft.Column(
                                [
                                    ft.Text("Member ID", size=12, color=ft.Colors.GREY_700),
                                    ft.Container(height=4),
                                    ft.Text(
                                        str(fine_data['member_id']),
                                        size=14,
                                        weight=ft.FontWeight.BOLD,
                                    ),
                                ],
                                spacing=0,
                                expand=True,
                            ),
                            ft.Column(
                                [
                                    ft.Text("Member name", size=12, color=ft.Colors.GREY_700),
                                    ft.Container(height=4),
                                    ft.Text(
                                        fine_data['member_name'],
                                        size=14,
                                        weight=ft.FontWeight.BOLD,
                                    ),
                                ],
                                spacing=0,
                                expand=True,
                            ),
                        ],
                        spacing=20,
                    ),
                    ft.Container(height=20),
                    
                    # Fine details box
                    ft.Container(
                        content=ft.Column(
                            [
                                self._fine_row(
                                    "Overdue fines (unpaid)",
                                    f"{fine_data['overdue_fines']:,.0f} VND"
                                ),
                                self._fine_row(
                                    "Damage fines (unpaid)",
                                    f"{fine_data['damage_fines']:,.0f} VND"
                                ),
                                self._fine_row(
                                    "Lost book fines (unpaid)",
                                    f"{fine_data['lost_fines']:,.0f} VND"
                                ),
                                ft.Divider(height=16, color=ft.Colors.GREY_300),
                                self._fine_row(
                                    "Total unpaid fines",
                                    f"{fine_data['total_unpaid_fines']:,.0f} VND",
                                    is_total=True,
                                ),
                            ],
                            spacing=8,
                        ),
                        padding=20,
                        bgcolor=ft.Colors.RED_50,
                        border_radius=10,
                    ),
                    ft.Container(height=20),
                    
                    # Info text
                    ft.Text(
                        "According to the library rules, borrowing and extension can be blocked when unpaid fines exceed the allowed limit. Please contact the library desk to pay your fines or ask for clarification.",
                        size=12,
                        color=ft.Colors.GREY_600,
                    ),
                    ft.Container(height=24),
                    
                    # Action buttons
                    ft.Row(
                        [
                            ft.OutlinedButton(
                                "View borrowing & fines",
                                on_click=lambda _: self.navigate("/my_borrowing") if self.navigate else None,
                                style=ft.ButtonStyle(
                                    shape=ft.RoundedRectangleBorder(radius=24),
                                    padding=ft.Padding(24, 12, 24, 12),
                                ),
                            ),
                            ft.FilledButton(
                                "View library rules",
                                bgcolor=ft.Colors.RED_600,
                                color=ft.Colors.WHITE,
                                on_click=lambda _: self.navigate("/instruction") if self.navigate else None,
                                style=ft.ButtonStyle(
                                    shape=ft.RoundedRectangleBorder(radius=24),
                                    padding=ft.Padding(24, 12, 24, 12),
                                ),
                            ),
                        ],
                        spacing=12,
                    ),
                ],
                spacing=0,
            ),
            padding=32,
            bgcolor=ft.Colors.WHITE,
            border_radius=12,
            border=ft.Border.all(2, ft.Colors.RED_200),
        )
        
        return ft.Container(
            content=ft.Column(
                [
                    ft.Container(height=24),
                    banner,
                    ft.Container(height=24),
                    notification_card,
                    ft.Container(height=40),
                ],
                scroll="auto",
            ),
            padding=ft.Padding(left=40, right=40, top=0, bottom=0),
            expand=True,
        )
    
    def _fine_row(self, label, value, is_total=False):
        """Helper để tạo row hiển thị fine"""
        if is_total:
            return ft.Row(
                [
                    ft.Text(label, size=13, weight=ft.FontWeight.BOLD, expand=True),
                    ft.Text(
                        value,
                        size=14,
                        weight=ft.FontWeight.BOLD,
                        color=ft.Colors.RED_700,
                    ),
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            )
        else:
            return ft.Row(
                [
                    ft.Text(label, size=12, color=ft.Colors.GREY_700, expand=True),
                    ft.Text(value, size=12, weight=ft.FontWeight.BOLD),
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            )
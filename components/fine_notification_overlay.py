# components/fine_notification_overlay.py
"""
Fine Notification Overlay Component
✅ Hiển thị thông báo khoản phạt khi user login/register
✅ Dismissable - User có thể đóng để tiếp tục
✅ Hiển thị chi tiết các khoản phạt
"""
import flet as ft


class FineNotificationOverlay:
    def __init__(self, page, fine_info, on_dismiss=None):
        """
        Args:
            page: Flet page object
            fine_info: Dict chứa thông tin phạt từ get_member_fines()
            on_dismiss: Callback khi user đóng notification
        """
        self.page = page
        self.fine_info = fine_info
        self.on_dismiss = on_dismiss
        self.overlay_container = None
    
    def show(self):
        """Hiển thị overlay notification"""
        total_unpaid = self.fine_info.get('total_unpaid_fines', 0)
        
        if total_unpaid <= 0:
            # Không có phạt, không hiển thị
            return
        
        print(f"⚠️ Showing fine notification: {total_unpaid:,.0f} VND")
        
        def close_overlay(e):
            print("Closing fine notification")
            if self.overlay_container in self.page.overlay:
                self.page.overlay.remove(self.overlay_container)
            self.page.update()
            
            # Call dismiss callback
            if self.on_dismiss:
                self.on_dismiss()
        
        def go_to_fines(e):
            print("Navigate to fines")
            if self.overlay_container in self.page.overlay:
                self.page.overlay.remove(self.overlay_container)
            self.page.update()
            
            # Navigate to My Borrowing (History & Fines tab)
            if hasattr(self.page, 'go') and callable(self.page.go):
                self.page.go("/my_borrowing")
            
            if self.on_dismiss:
                self.on_dismiss()
        
        # Build fine breakdown
        overdue_fines = self.fine_info.get('overdue_fines', 0)
        damage_fines = self.fine_info.get('damage_fines', 0)
        lost_fines = self.fine_info.get('lost_fines', 0)
        
        fine_breakdown = []
        
        if overdue_fines > 0:
            fine_breakdown.append(
                ft.Row([
                    ft.Icon(ft.Icons.ACCESS_TIME, size=18, color=ft.Colors.ORANGE_600),
                    ft.Container(width=8),
                    ft.Text(
                        f"Overdue fines: {overdue_fines:,.0f} VND",
                        size=14,
                        color=ft.Colors.GREY_800,
                    ),
                ], spacing=0)
            )
        
        if damage_fines > 0:
            fine_breakdown.append(
                ft.Row([
                    ft.Icon(ft.Icons.BROKEN_IMAGE, size=18, color=ft.Colors.RED_600),
                    ft.Container(width=8),
                    ft.Text(
                        f"Damage fines: {damage_fines:,.0f} VND",
                        size=14,
                        color=ft.Colors.GREY_800,
                    ),
                ], spacing=0)
            )
        
        if lost_fines > 0:
            fine_breakdown.append(
                ft.Row([
                    ft.Icon(ft.Icons.HELP_OUTLINE, size=18, color=ft.Colors.PURPLE_600),
                    ft.Container(width=8),
                    ft.Text(
                        f"Lost book fines: {lost_fines:,.0f} VND",
                        size=14,
                        color=ft.Colors.GREY_800,
                    ),
                ], spacing=0)
            )
        
        # Tạo dialog box
        dialog_box = ft.Container(
            content=ft.Column([
                # Header with close button
                ft.Row([
                    ft.Row([
                        ft.Icon(ft.Icons.WARNING_AMBER_ROUNDED, color=ft.Colors.RED_600, size=32),
                        ft.Container(width=12),
                        ft.Text(
                            "Outstanding Fines",
                            size=24,
                            weight=ft.FontWeight.BOLD,
                            color=ft.Colors.GREY_900,
                        ),
                    ]),
                    ft.Container(expand=True),
                    ft.IconButton(
                        icon=ft.Icons.CLOSE,
                        icon_color=ft.Colors.GREY_600,
                        tooltip="Close",
                        on_click=close_overlay,
                    ),
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                
                ft.Container(height=15),
                
                # Total amount in big red box
                ft.Container(
                    content=ft.Column([
                        ft.Text(
                            "Total Amount Due",
                            size=14,
                            color=ft.Colors.RED_700,
                            weight=ft.FontWeight.W_500,
                        ),
                        ft.Container(height=5),
                        ft.Text(
                            f"{total_unpaid:,.0f} VND",
                            size=32,
                            weight=ft.FontWeight.BOLD,
                            color=ft.Colors.RED_800,
                        ),
                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                    padding=20,
                    bgcolor=ft.Colors.RED_50,
                    border_radius=10,
                    border=ft.Border.all(2, ft.Colors.RED_200),
                ),
                
                ft.Container(height=20),
                
                # Warning message
                ft.Container(
                    content=ft.Row([
                        ft.Icon(ft.Icons.INFO_OUTLINE, size=20, color=ft.Colors.AMBER_700),
                        ft.Container(width=10),
                        ft.Text(
                            "You have unpaid fines. Please pay to continue borrowing books.",
                            size=14,
                            color=ft.Colors.GREY_800,
                            weight=ft.FontWeight.W_500,
                        ),
                    ]),
                    padding=15,
                    bgcolor=ft.Colors.AMBER_50,
                    border_radius=8,
                    border=ft.Border.all(1, ft.Colors.AMBER_200),
                ),
                
                ft.Container(height=20),
                
                # Fine breakdown
                ft.Text(
                    "Fine Breakdown:",
                    size=15,
                    weight=ft.FontWeight.BOLD,
                    color=ft.Colors.GREY_900,
                ),
                
                ft.Container(height=10),
                
                ft.Column(fine_breakdown, spacing=12),
                
                ft.Container(height=25),
                
                ft.Divider(color=ft.Colors.GREY_300, height=1),
                
                ft.Container(height=20),
                
                # Action buttons
                ft.Row([
                    ft.OutlinedButton(
                        "Close",
                        on_click=close_overlay,
                        style=ft.ButtonStyle(
                            shape=ft.RoundedRectangleBorder(radius=8),
                            side=ft.BorderSide(1, ft.Colors.GREY_400),
                            padding=ft.Padding(20, 12, 20, 12),
                        ),
                    ),
                    ft.Container(expand=True),
                    ft.ElevatedButton(
                        "View Details & Pay",
                        bgcolor=ft.Colors.RED_600,
                        color=ft.Colors.WHITE,
                        on_click=go_to_fines,
                        icon=ft.Icons.PAYMENT,
                        style=ft.ButtonStyle(
                            shape=ft.RoundedRectangleBorder(radius=8),
                            padding=ft.Padding(20, 12, 20, 12),
                        ),
                    ),
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                
                ft.Container(height=10),
                
                # Footer note
                ft.Text(
                    "You can close this notification and view your borrowing history normally. "
                    "Go to My Borrowing → History & Fines to pay.",
                    size=12,
                    color=ft.Colors.GREY_600,
                    text_align=ft.TextAlign.CENTER,
                ),
            ], spacing=0),
            width=550,
            padding=30,
            bgcolor=ft.Colors.WHITE,
            border_radius=15,
            shadow=ft.BoxShadow(
                spread_radius=0,
                blur_radius=30,
                color=ft.Colors.with_opacity(0.3, ft.Colors.BLACK),
                offset=ft.Offset(0, 10),
            ),
        )
        
        # Overlay container (full screen with semi-transparent background)
        self.overlay_container = ft.Container(
            content=dialog_box,
            alignment=ft.Alignment(0, 0),
            bgcolor=ft.Colors.with_opacity(0.7, ft.Colors.BLACK),
            expand=True,
        )
        
        # Add to page overlay
        print("Adding fine notification overlay to page...")
        self.page.overlay.append(self.overlay_container)
        self.page.update()
        print("✅ Fine notification overlay displayed!")
    
    def hide(self):
        """Ẩn overlay"""
        if self.overlay_container and self.overlay_container in self.page.overlay:
            self.page.overlay.remove(self.overlay_container)
            self.page.update()


def show_fine_notification(page, fine_info, on_dismiss=None):
    """
    Helper function để hiển thị fine notification
    
    Args:
        page: Flet page object
        fine_info: Dict từ get_member_fines()
        on_dismiss: Callback khi đóng
    
    Usage:
        from components.fine_notification_overlay import show_fine_notification
        
        # Sau khi login thành công
        if user:
            from services.borrow_service import get_member_fines
            fine_info = get_member_fines(user['user_id'])
            
            if fine_info['total_unpaid_fines'] > 0:
                show_fine_notification(page, fine_info)
    """
    overlay = FineNotificationOverlay(page, fine_info, on_dismiss)
    overlay.show()
    return overlay
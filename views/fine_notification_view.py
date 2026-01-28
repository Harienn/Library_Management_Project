# views/fine_notification_view.py
"""
Fine Notification View - Clean design như ảnh 2
✅ Không có back button
✅ Không có title "2.3. Fine Notification"
✅ Chỉ hiển thị notification box
✅ Lấy dữ liệu thật từ database
"""
import flet as ft
from services.borrow_service import get_member_fines

try:
    from components.header import Header
    from components.navbar import NavBar
    HAS_HEADER_NAVBAR = True
except:
    HAS_HEADER_NAVBAR = False
    print("⚠️ Header/NavBar not found, using simple layout")


class FineNotificationView:
    def __init__(self, page, current_user, navigate, on_logout):
        self.page = page
        self.current_user = current_user
        self.navigate = navigate
        self.on_logout = on_logout
    
    def build(self):
        """Build fine notification view - Clean design"""
        
        # Content
        if not self.current_user:
            content = self.build_guest_view()
        else:
            content = self.build_member_view()
        
        return ft.View(
            route="/fine_notification",
            controls=[ft.Container(
                content=content,
                bgcolor=ft.Colors.WHITE,
                expand=True,
            )],
        )
    
    def build_guest_view(self):
        """Guest view"""
        return ft.Container(
            content=ft.Column([
                ft.Container(height=100),
                ft.Text("🔒", size=60),
                ft.Container(height=20),
                ft.Text("Please login to view fine information", 
                    size=18, weight=ft.FontWeight.BOLD),
                ft.Container(height=20),
                ft.ElevatedButton(
                    "Login",
                    bgcolor=ft.Colors.CYAN_400,
                    color=ft.Colors.WHITE,
                    on_click=lambda _: self.navigate("/login") if self.navigate else None,
                ),
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            padding=40,
            expand=True,
        )
    
    def build_member_view(self):
        """Member view - Clean notification box only (như ảnh 2)"""
        user_id = self.current_user.get('user_id')
        member_id = self.current_user.get('user_id')
        member_name = self.current_user.get('fullname', 'N/A')
        
        # Get fine info from database
        try:
            fine_info = get_member_fines(user_id)
            overdue_fines = fine_info.get('overdue_fines', 0)
            damage_fines = fine_info.get('damage_fines', 0)
            lost_fines = fine_info.get('lost_fines', 0)
            total_unpaid = fine_info.get('total_unpaid_fines', 0)
            
            print(f"📊 Fine data loaded:")
            print(f"  - Overdue: {overdue_fines:,.0f} VND")
            print(f"  - Damage: {damage_fines:,.0f} VND")
            print(f"  - Lost: {lost_fines:,.0f} VND")
            print(f"  - Total: {total_unpaid:,.0f} VND")
        except Exception as e:
            print(f"❌ Error getting fines: {e}")
            import traceback
            traceback.print_exc()
            overdue_fines = damage_fines = lost_fines = total_unpaid = 0
        
        # ✅ Fine breakdown rows - Always show all 3 types
        breakdown_rows = [
            ft.Row([
                ft.Text("Overdue fines (unpaid)", size=14, expand=True, color="#6B7280"),
                ft.Text(f"{overdue_fines:,.0f} VND", size=14, weight=ft.FontWeight.BOLD, color="#1F2937"),
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            
            ft.Row([
                ft.Text("Damage fines (unpaid)", size=14, expand=True, color="#6B7280"),
                ft.Text(f"{damage_fines:,.0f} VND", size=14, weight=ft.FontWeight.BOLD, color="#1F2937"),
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            
            ft.Row([
                ft.Text("Lost book fines (unpaid)", size=14, expand=True, color="#6B7280"),
                ft.Text(f"{lost_fines:,.0f} VND", size=14, weight=ft.FontWeight.BOLD, color="#1F2937"),
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
        ]
        
        # ✅ Fine notification badge
        fine_badge = ft.Container(
            content=ft.Row([
                ft.Text("⚠️", size=16),
                ft.Container(width=8),
                ft.Text(
                    "FINE NOTIFICATION",
                    size=12,
                    weight=ft.FontWeight.BOLD,
                    color="#DC2626",
                ),
            ]),
            padding=ft.padding.symmetric(horizontal=16, vertical=8),
            bgcolor="#FEE2E2",
            border_radius=20,
        )
        
        # ✅ Main notification box (như ảnh 2)
        notification_box = ft.Container(
            content=ft.Column([
                # Badge
                fine_badge,
                ft.Container(height=24),
                
                # Title
                ft.Text(
                    "You have unpaid library fines" if total_unpaid > 0 else "Your fine information", 
                    size=24, 
                    weight=ft.FontWeight.BOLD,
                    color="#1F2937",
                ),
                ft.Container(height=8),
                
                # Description
                ft.Text(
                    "Please review the information below. Your borrowing or extension may be blocked until fines are paid."
                    if total_unpaid > 0 else "No outstanding fines.",
                    size=14, 
                    color="#9CA3AF",
                ),
                ft.Container(height=24),
                
                # Member info
                ft.Row([
                    ft.Text("Member ID", size=14, color="#9CA3AF", expand=True),
                    ft.Text(str(member_id), size=14, weight=ft.FontWeight.BOLD, color="#1F2937"),
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ft.Container(height=8),
                ft.Row([
                    ft.Text("Member name", size=14, color="#9CA3AF", expand=True),
                    ft.Text(member_name, size=14, weight=ft.FontWeight.BOLD, color="#1F2937"),
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                
                ft.Container(height=24),
                
                # ✅ Fine breakdown box (màu hồng nhạt như ảnh 2)
                ft.Container(
                    content=ft.Column([
                        *breakdown_rows,
                        ft.Container(height=8),
                        ft.Divider(height=1, color="#F3D0D0", thickness=1),
                        ft.Container(height=8),
                        ft.Row([
                            ft.Text("Total unpaid fines", size=16, weight=ft.FontWeight.BOLD, expand=True, color="#1F2937"),
                            ft.Text(
                                f"{total_unpaid:,.0f} VND", 
                                size=16, 
                                weight=ft.FontWeight.BOLD, 
                                color="#DC2626" if total_unpaid > 0 else "#059669"
                            ),
                        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                    ], spacing=12),
                    padding=24,
                    bgcolor="#FEF2F2" if total_unpaid > 0 else "#F0FDF4",
                    border_radius=12,
                ),
                
                ft.Container(height=24),
                
                # Warning text
                ft.Text(
                    "According to the library rules, borrowing and extension can be blocked when unpaid fines exceed the allowed limit. "
                    "Please contact the library desk to pay your fines or ask for clarification.",
                    size=13, 
                    color="#9CA3AF",
                ) if total_unpaid > 0 else ft.Container(),
                
                ft.Container(height=24) if total_unpaid > 0 else ft.Container(height=16),
                
                # ✅ Action buttons (như ảnh 2)
                ft.Row([
                    ft.OutlinedButton(
                        "View borrowing & fines",
                        on_click=lambda _: self.navigate("/my_borrowing") if self.navigate else None,
                        style=ft.ButtonStyle(
                            color="#6B7280",
                            side=ft.BorderSide(1, "#D1D5DB"),
                            padding=ft.padding.symmetric(horizontal=20, vertical=12),
                            shape=ft.RoundedRectangleBorder(radius=8),
                        ),
                    ),
                    ft.ElevatedButton(
                        "View library rules",
                        bgcolor="#EF4444" if total_unpaid > 0 else ft.Colors.CYAN_400,
                        color=ft.Colors.WHITE,
                        on_click=lambda _: self.navigate("/instruction") if self.navigate else None,
                        style=ft.ButtonStyle(
                            padding=ft.padding.symmetric(horizontal=20, vertical=12),
                            shape=ft.RoundedRectangleBorder(radius=8),
                        ),
                    ),
                ], spacing=12),
                
            ], spacing=0),
            padding=40,
            bgcolor=ft.Colors.WHITE,
            border_radius=16,
            border=ft.Border.all(1, "#FCA5A5" if total_unpaid > 0 else "#D1FAE5"),
            shadow=ft.BoxShadow(
                spread_radius=0,
                blur_radius=10,
                color=ft.Colors.with_opacity(0.1, ft.Colors.BLACK),
                offset=ft.Offset(0, 4),
            ),
        )
        
        # ✅ Return only the notification box centered
        return ft.Container(
            content=ft.Column([
                ft.Container(height=60),
                notification_box,
                ft.Container(height=60),
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            padding=40,
            expand=True,
        )
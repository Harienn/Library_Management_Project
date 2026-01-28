# views/admin/components/sidebar.py
import flet as ft

class Sidebar:
    def __init__(self, current_route, navigate_callback, user_role="Librarian"):
        self.current_route = current_route
        self.navigate = navigate_callback
        self.user_role = user_role
        self.on_logout = None  # SẼ ĐƯỢC GÁN TỪ ADMIN_APP
    
    def build(self):
        menu_sections = [
            ("GENERAL", [
                ("Dashboard", "/admin", "▣", False),
            ]),
            ("MANAGEMENT", [
                ("Manage books", "/admin/books", "📚", False),
                ("Manage members", "/admin/members", "👥", False),
                ("Manage librarians", "/admin/librarians", "👨‍💼", True),  # ← requires_admin=True
            ]),
            ("CIRCULATION & FINES", [
                ("Borrow / Return", "/admin/borrow", "⇄", False),
                ("View fines", "/admin/fines", "▲", False),
            ]),
            ("REPORTS", [
                ("View statistical report", "/admin/reports", "▣", False),
            ]),
        ]
        
        menu_items = []
        
        for section_name, items in menu_sections:
            menu_items.append(
                ft.Text(
                    section_name,
                    size=10,
                    weight=ft.FontWeight.BOLD,
                    color="#6B7280",
                    margin=ft.Margin(20, 16, 0, 8),
                )
            )
            
            for label, route, icon, requires_admin in items:
                # BỎ QUA menu item nếu requires_admin=True và user không phải Admin
                if requires_admin and self.user_role != "Admin":
                    continue  # ← SKIP item này, không render
                
                is_active = self.current_route == route
                
                menu_items.append(
                    ft.Container(
                        content=ft.Row([
                            ft.Text(icon, size=14, color=ft.Colors.CYAN_400 if is_active else "#9CA3AF"),
                            ft.Text(
                                label,
                                size=13,
                                color=ft.Colors.WHITE if is_active else "#D1D5DB",
                                weight=ft.FontWeight.W_500 if is_active else ft.FontWeight.NORMAL,
                            ),
                        ], spacing=12),
                        padding=ft.Padding(20, 10, 20, 10),
                        bgcolor="#1E293B" if is_active else ft.Colors.TRANSPARENT,
                        border_radius=6,
                        margin=ft.Margin(8, 0, 8, 2),
                        on_click=lambda e, r=route: self.navigate(r),
                        ink=True,
                    )
                )
        
        footer = ft.Container(
            content=ft.Column([
                ft.Divider(height=1, color="#374151"),
                ft.Container(
                    content=ft.Column([
                        ft.Text(f"Logged in as: {self.user_role}", size=11, color="#9CA3AF"),
                        ft.Text(f"{self.user_role.lower()}@rary.local", size=12, color="#D1D5DB"),
                        ft.Container(
                            content=ft.Text("LOGOUT", size=11, color=ft.Colors.WHITE, weight=ft.FontWeight.BOLD),
                            padding=ft.Padding(12, 6, 12, 6),
                            bgcolor="#DC2626",
                            border_radius=4,
                            margin=ft.Margin(0, 8, 0, 0),
                            on_click=lambda _: self.on_logout() if self.on_logout else None,
                            ink=True,
                        ),
                    ], spacing=2),
                    padding=ft.Padding(20, 12, 20, 12),
                ),
            ], spacing=0),
            margin=ft.Margin(0, 20, 0, 0),
        )
        
        return ft.Container(
            content=ft.Column([
                ft.Container(
                    content=ft.Column([
                        ft.Text("LibrarySystem", size=18, weight=ft.FontWeight.BOLD, color=ft.Colors.CYAN_400),
                        ft.Text(f"{self.user_role} dashboard", size=11, color="#9CA3AF"),
                    ], spacing=2),
                    padding=ft.Padding(20, 20, 20, 16),
                ),
                ft.Divider(height=1, color="#374151"),
                ft.Column(controls=menu_items, scroll=ft.ScrollMode.AUTO, expand=True),
                footer,
            ], spacing=0),
            width=240,
            bgcolor="#0F172A",
        )
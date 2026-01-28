# views/instruction_view.py
import flet as ft
from components.header import Header
from components.navbar import NavBar


class InstructionView:
    def __init__(self, page, current_user, navigate, on_logout=None):
        self.page = page
        self.current_user = current_user
        self.navigate = navigate
        self.on_logout = on_logout
    
    def build(self):
        header = Header(self.page, self.current_user, self.navigate, self.on_logout)
        navbar = NavBar(self.page, self.current_user, self.navigate, "/instruction")
        
        # === BORROWING RULES (CỘT TRÁI) ===
        borrowing_rules = ft.Container(
            content=ft.Column([
                ft.Text("Borrowing rules", size=18, weight=ft.FontWeight.BOLD),
                ft.Container(height=8),
                ft.Text(
                    "The rules below are examples and can be adjusted based on your project specification.",
                    size=12,
                    color=ft.Colors.GREY_600,
                ),
                ft.Container(height=12),
                ft.Text("• Each member can borrow up to 10 books at the same time.", size=13),
                ft.Text("• Standard borrowing period: 15 days per book.", size=13),
                ft.Text("• Each borrowing can be extended up to 2 times when it is not overdue and there are no blocking penalties.", size=13),
                ft.Text("• Overdue fine: 20,000 VND per book per day overdue.", size=13),
                ft.Text("• Damaged books: compensation fee based on percentage of damage and book price.", size=13),
                ft.Text("• Lost books: compensation equal to 100% of the book price (and processing fee if applicable).", size=13),
                ft.Text("• Borrowing and extension may be blocked if unpaid fines exceed the allowed limit or books are long overdue.", size=13),
                
                ft.Container(height=20),
                
                ft.Text("Penalty principles", size=18, weight=ft.FontWeight.BOLD),
                ft.Container(height=12),
                ft.Text("• Fines apply if a book is overdue, damaged or lost according to the rules above.", size=13),
                ft.Text("• Unpaid penalties will appear in 'My borrowing & fines' and may block new borrowing or extensions.", size=13),  # SỬA DÒNG NÀY
                ft.Text("• Members should check due dates regularly and request extensions before the due date.", size=13),
            ], spacing=4),
            padding=20,
            bgcolor=ft.Colors.WHITE,
            border_radius=10,
            border=ft.Border.all(1, ft.Colors.GREY_200),
            expand=True,
        )
        
        # === LIBRARY INFORMATION (CỘT PHẢI) ===
        library_info = ft.Container(
            content=ft.Column([
                ft.Text("Library information", size=18, weight=ft.FontWeight.BOLD),
                ft.Container(height=12),
                ft.Text("Library name: Library", size=13),
                ft.Text("Address: 123 Library Street, District X, City Y", size=13),
                ft.Text("Email: library@example.com", size=13),
                ft.Text("Phone: (084) 0123 456 789", size=13),
                
                ft.Container(height=16),
                
                ft.Text("Opening hours :", size=13, weight=ft.FontWeight.BOLD),
                ft.Container(height=4),
                ft.Text("• Monday – Friday: 8:00 – 17:00", size=13),
                ft.Text("• Saturday: 8:00 – 15:00", size=13),
                ft.Text("• Sunday and public holidays: closed", size=13),
                
                ft.Container(height=20),
                
                ft.Text("Using the online system", size=18, weight=ft.FontWeight.BOLD),
                ft.Container(height=12),
                ft.Text("• Guest users can search and view book information.", size=13),
                ft.Text("• Members can borrow books, request extensions, view history and fines.", size=13),
                ft.Text("• For detailed guidance, please refer to your project documentation or user guide.", size=13),
            ], spacing=4),
            padding=20,
            bgcolor=ft.Colors.WHITE,
            border_radius=10,
            border=ft.Border.all(1, ft.Colors.GREY_200),
            expand=True,
        )
        
        # === SCROLLABLE CONTENT ===
        scrollable_content = ft.Container(
            content=ft.Column([
                ft.Container(height=24),
                
                ft.Text("Library rules & information", size=26, weight=ft.FontWeight.BOLD),
                ft.Container(height=4),
                ft.Text(
                    "Read the main borrowing rules and basic information about the library.",
                    size=13,
                    color=ft.Colors.GREY_600,
                ),
                
                ft.Container(height=24),
                
                # 2 CỘT
                ft.Row([
                    borrowing_rules,
                    ft.Container(width=20),
                    library_info,
                ], spacing=0, vertical_alignment="start"),
                
                ft.Container(height=40),
            ], scroll="auto"),
            padding=ft.Padding(left=40, right=40, top=0, bottom=0),
            expand=True,
        )
        
        # === MAIN LAYOUT ===
        main_content = ft.Column([
            header.build(),
            navbar.build(),
            scrollable_content,
        ], spacing=0, expand=True)
        
        return ft.View(
            route="/instruction",
            controls=[
                ft.Container(
                    content=main_content,
                    padding=0,
                    bgcolor=ft.Colors.GREY_50,
                    expand=True,
                )
            ],
        )

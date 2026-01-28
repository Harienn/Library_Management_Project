# views/book_detail_view.py - ENHANCED BORROW HANDLER
"""
Book Detail View - ENHANCED VERSION
✅ Confirmation dialog before borrowing
✅ Detailed error notifications for all cases
✅ Transaction ID display on success
"""
import flet as ft
from database.db import fetch_one, fetch_all
from services.borrow_service import check_borrow_eligibility, borrow_book


class BookDetailView:
    def __init__(self, page, current_user, navigate, on_logout, book_data=None):
        self.page = page
        self.current_user = current_user
        self.navigate = navigate
        self.on_logout = on_logout
        self.book_data = book_data or {}
        
        print(f"🔍 BookDetailView init with book_data: {self.book_data}")
        
        if self.book_data and self.book_data.get("book_id"):
            book_id = self.book_data.get("book_id")
            full_data = self.get_book_detail(book_id)
            if full_data:
                self.book_data = full_data
                print(f"✅ Loaded book: {self.book_data.get('title')}")

    def get_book_detail(self, book_id):
        """Get full book details"""
        try:
            sql = """
                SELECT 
                    b.book_id, b.title, b.isbn, b.publish_date,
                    b.total_copies, b.available_copies, b.is_reference_only,
                    b.publisher, b.summary, b.image_url, b.price, b.book_status,
                    a.author_name, a.author_id, c.category_name, c.category_id
                FROM BOOKS b
                LEFT JOIN AUTHORS a ON b.author_id = a.author_id
                LEFT JOIN CATEGORIES c ON b.category_id = c.category_id
                WHERE b.book_id = %s
            """
            return fetch_one(sql, (book_id,)) or {}
        except Exception as e:
            print(f"❌ Error loading book: {e}")
            return {}

    # ================= ENHANCED BORROW HANDLER =================
    
    def handle_borrow(self, e=None):
        """
        ✅ ENHANCED: Kiểm tra điều kiện trước → Hiện confirmation dialog
        """
        print("\n" + "="*60)
        print("📚 BORROW BUTTON CLICKED")
        print("="*60)
        
        if not self.current_user:
            print("❌ User not logged in")
            self.show_login_required_dialog()
            return
        
        member_id = self.current_user.get('user_id')
        book_id = self.book_data.get('book_id')
        
        print(f"👤 Member ID: {member_id}")
        print(f"📖 Book ID: {book_id}")
        
        # ✅ STEP 1: Check eligibility
        can_borrow, reason, details = check_borrow_eligibility(member_id, book_id)
        
        print(f"✓ Can borrow: {can_borrow}")
        print(f"✓ Reason: {reason}")
        print(f"✓ Details: {details}")
        
        if not can_borrow:
            # Show specific error dialog based on reason
            self.show_borrow_error_dialog(reason, details)
            return
        
        # ✅ STEP 2: Show confirmation dialog
        self.show_borrow_confirmation_dialog(details)
    
    def show_borrow_confirmation_dialog(self, details):
        """
        ✅ Hiển thị dialog xác nhận thông tin trước khi mượn
        """
        book_title = self.book_data.get('title', 'N/A')
        author = self.book_data.get('author_name', 'Unknown')
        isbn = self.book_data.get('isbn', 'N/A')
        borrow_period = details.get('borrow_period', 15)
        current_borrowed = details.get('current_borrowed', 0)
        
        def confirm_borrow(e):
            dialog.open = False
            self.page.update()
            self.execute_borrow()
        
        def cancel_borrow(e):
            dialog.open = False
            self.page.update()
        
        dialog = ft.AlertDialog(
            modal=True,
            title=ft.Row([
                ft.Icon(ft.icons.INFO_OUTLINE, color=ft.Colors.CYAN_600, size=30),
                ft.Container(width=10),
                ft.Text(
                    "Confirm Borrowing",
                    size=20,
                    weight=ft.FontWeight.BOLD,
                    color=ft.Colors.GREY_900,
                ),
            ]),
            content=ft.Container(
                content=ft.Column([
                    ft.Text(
                        "Please confirm the following information:",
                        size=14,
                        color=ft.Colors.GREY_700,
                    ),
                    ft.Container(height=16),
                    
                    # Book info
                    ft.Container(
                        content=ft.Column([
                            ft.Text("📚 Book Information:", size=13, weight=ft.FontWeight.BOLD),
                            ft.Container(height=8),
                            ft.Text(f"Title: {book_title}", size=12),
                            ft.Text(f"Author: {author}", size=12),
                            ft.Text(f"ISBN: {isbn}", size=12),
                        ], spacing=4),
                        padding=12,
                        bgcolor=ft.Colors.BLUE_50,
                        border_radius=8,
                    ),
                    
                    ft.Container(height=12),
                    
                    # Borrowing info
                    ft.Container(
                        content=ft.Column([
                            ft.Text("📅 Borrowing Details:", size=13, weight=ft.FontWeight.BOLD),
                            ft.Container(height=8),
                            ft.Text(f"Borrowing period: {borrow_period} days", size=12),
                            ft.Text(f"Current borrowed books: {current_borrowed}/10", size=12),
                            ft.Text(
                                "⚠️ Late return will incur a fine of 20,000 VND/day",
                                size=11,
                                color=ft.Colors.ORANGE_700,
                                italic=True,
                            ),
                        ], spacing=4),
                        padding=12,
                        bgcolor=ft.Colors.ORANGE_50,
                        border_radius=8,
                    ),
                    
                    ft.Container(height=16),
                    
                    ft.Text(
                        "Do you want to proceed with borrowing this book?",
                        size=13,
                        weight=ft.FontWeight.W_500,
                        color=ft.Colors.GREY_800,
                    ),
                ], spacing=0, tight=True),
                width=450,
            ),
            actions=[
                ft.TextButton(
                    "Cancel",
                    on_click=cancel_borrow,
                    style=ft.ButtonStyle(
                        color=ft.Colors.GREY_600,
                    ),
                ),
                ft.FilledButton(
                    "Confirm Borrow",
                    on_click=confirm_borrow,
                    style=ft.ButtonStyle(
                        bgcolor=ft.Colors.CYAN_400,
                    ),
                ),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        
        self.page.dialog = dialog
        dialog.open = True
        self.page.update()
    
    def execute_borrow(self):
        """
        ✅ Thực hiện mượn sách sau khi confirm
        """
        try:
            member_id = self.current_user.get('user_id')
            book_id = self.book_data.get('book_id')
            
            print(f"\n🔄 Executing borrow...")
            print(f"   Member: {member_id}")
            print(f"   Book: {book_id}")
            
            success, message, transaction_id = borrow_book(member_id, book_id)
            
            print(f"✓ Success: {success}")
            print(f"✓ Message: {message}")
            print(f"✓ Transaction ID: {transaction_id}")
            
            if success and transaction_id:
                # ✅ Success: Show transaction info
                self.show_borrow_success_dialog(transaction_id, self.book_data.get('title'))
            else:
                # ❌ Failed
                self.show_error_snackbar(message)
                
        except Exception as error:
            print(f"❌ Error executing borrow: {error}")
            import traceback
            traceback.print_exc()
            self.show_error_snackbar(f"System error: {str(error)}")
    
    def show_borrow_success_dialog(self, transaction_id, book_title):
        """
        ✅ Hiển thị thông báo thành công với transaction ID
        """
        def view_my_borrowing(e):
            dialog.open = False
            self.page.update()
            self.navigate("/my_borrowing")
        
        def close_dialog(e):
            dialog.open = False
            self.page.update()
        
        dialog = ft.AlertDialog(
            modal=True,
            title=ft.Row([
                ft.Icon(ft.icons.CHECK_CIRCLE, color=ft.Colors.GREEN_600, size=30),
                ft.Container(width=10),
                ft.Text(
                    "Book Borrowed Successfully!",
                    size=20,
                    weight=ft.FontWeight.BOLD,
                    color=ft.Colors.GREEN_700,
                ),
            ]),
            content=ft.Container(
                content=ft.Column([
                    ft.Text(
                        "Your borrowing request has been processed successfully.",
                        size=14,
                        color=ft.Colors.GREY_700,
                    ),
                    ft.Container(height=16),
                    
                    # Transaction info
                    ft.Container(
                        content=ft.Column([
                            ft.Row([
                                ft.Text("Transaction ID:", size=13, weight=ft.FontWeight.BOLD),
                                ft.Text(
                                    f"#{transaction_id}",
                                    size=13,
                                    color=ft.Colors.CYAN_700,
                                    weight=ft.FontWeight.BOLD,
                                ),
                            ]),
                            ft.Container(height=8),
                            ft.Text(
                                f"📚 Book: {book_title}",
                                size=12,
                                color=ft.Colors.GREY_700,
                            ),
                        ], spacing=0),
                        padding=12,
                        bgcolor=ft.Colors.GREEN_50,
                        border_radius=8,
                        border=ft.Border.all(1, ft.Colors.GREEN_200),
                    ),
                    
                    ft.Container(height=16),
                    
                    ft.Text(
                        "💡 View details in My Borrowing section",
                        size=12,
                        color=ft.Colors.CYAN_600,
                        italic=True,
                    ),
                ], spacing=0, tight=True),
                width=400,
            ),
            actions=[
                ft.TextButton(
                    "Close",
                    on_click=close_dialog,
                ),
                ft.FilledButton(
                    "View My Borrowing",
                    on_click=view_my_borrowing,
                    style=ft.ButtonStyle(
                        bgcolor=ft.Colors.CYAN_400,
                    ),
                ),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        
        self.page.dialog = dialog
        dialog.open = True
        self.page.update()
    
    def show_borrow_error_dialog(self, reason, details):
        """
        ✅ Hiển thị dialog lỗi chi tiết theo từng trường hợp
        """
        def close_dialog(e):
            dialog.open = False
            self.page.update()
        
        def go_to_profile(e):
            dialog.open = False
            self.page.update()
            self.navigate("/my_profile")
        
        def go_to_my_borrowing(e):
            dialog.open = False
            self.page.update()
            self.navigate("/my_borrowing")
        
        # ✅ Customize dialog based on reason
        if reason == "PROFILE_INCOMPLETE":
            title_text = "⚠️ Profile Incomplete"
            title_color = ft.Colors.ORANGE_700
            message = details.get('message', 'Please complete your profile')
            bg_color = ft.Colors.ORANGE_50
            border_color = ft.Colors.ORANGE_200
            action_button = ft.FilledButton(
                "Complete Profile",
                on_click=go_to_profile,
                style=ft.ButtonStyle(bgcolor=ft.Colors.ORANGE_600),
            )
            
        elif reason == "HAS_FINES":
            total_fine = details.get('total_fine_debt', 0)
            overdue = details.get('overdue_fines', 0)
            damage = details.get('damage_fines', 0)
            lost = details.get('lost_fines', 0)
            
            title_text = "⚠️ Unpaid Fines"
            title_color = ft.Colors.RED_700
            
            fine_breakdown = []
            if overdue > 0:
                fine_breakdown.append(f"• Overdue fines: {overdue:,.0f} VND")
            if damage > 0:
                fine_breakdown.append(f"• Damage fines: {damage:,.0f} VND")
            if lost > 0:
                fine_breakdown.append(f"• Lost book fines: {lost:,.0f} VND")
            
            message = f"You have unpaid fines totaling {total_fine:,.0f} VND.\n\n" + "\n".join(fine_breakdown) + "\n\nPlease pay your fines to continue borrowing."
            
            bg_color = ft.Colors.RED_50
            border_color = ft.Colors.RED_200
            action_button = ft.FilledButton(
                "View My Borrowing",
                on_click=go_to_my_borrowing,
                style=ft.ButtonStyle(bgcolor=ft.Colors.RED_600),
            )
            
        elif reason == "MAX_BOOKS":
            current = details.get('current_borrowed', 0)
            max_allowed = details.get('max_allowed', 10)
            
            title_text = "⚠️ Maximum Limit Reached"
            title_color = ft.Colors.ORANGE_700
            message = f"You have borrowed the maximum number of books ({current}/{max_allowed}).\n\nPlease return some books to continue borrowing."
            bg_color = ft.Colors.ORANGE_50
            border_color = ft.Colors.ORANGE_200
            action_button = ft.FilledButton(
                "View My Borrowing",
                on_click=go_to_my_borrowing,
                style=ft.ButtonStyle(bgcolor=ft.Colors.ORANGE_600),
            )
            
        elif reason == "REFERENCE_ONLY":
            title_text = "📖 Reference Only"
            title_color = ft.Colors.BLUE_700
            message = "This book is reference-only and cannot be borrowed.\n\nYou can read it in the library."
            bg_color = ft.Colors.BLUE_50
            border_color = ft.Colors.BLUE_200
            action_button = None
            
        elif reason == "BOOK_NOT_AVAILABLE":
            title_text = "❌ Not Available"
            title_color = ft.Colors.RED_700
            message = "This book is currently not available.\n\nPlease check back later."
            bg_color = ft.Colors.RED_50
            border_color = ft.Colors.RED_200
            action_button = None
            
        elif reason == "ACCOUNT_BLOCKED":
            title_text = "🔒 Account Blocked"
            title_color = ft.Colors.RED_700
            message = "Your account has been blocked.\n\nPlease contact the library for assistance."
            bg_color = ft.Colors.RED_50
            border_color = ft.Colors.RED_200
            action_button = None
            
        else:
            # Default error
            title_text = "❌ Cannot Borrow"
            title_color = ft.Colors.RED_700
            message = details.get('message', 'An error occurred')
            bg_color = ft.Colors.RED_50
            border_color = ft.Colors.RED_200
            action_button = None
        
        # Build dialog
        actions = [ft.TextButton("Close", on_click=close_dialog)]
        if action_button:
            actions.append(action_button)
        
        dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text(
                title_text,
                size=20,
                weight=ft.FontWeight.BOLD,
                color=title_color,
            ),
            content=ft.Container(
                content=ft.Column([
                    ft.Container(
                        content=ft.Text(
                            message,
                            size=13,
                            color=ft.Colors.GREY_800,
                        ),
                        padding=12,
                        bgcolor=bg_color,
                        border_radius=8,
                        border=ft.Border.all(1, border_color),
                    ),
                ], spacing=0, tight=True),
                width=400,
            ),
            actions=actions,
            actions_alignment=ft.MainAxisAlignment.END,
        )
        
        self.page.dialog = dialog
        dialog.open = True
        self.page.update()
    
    def show_login_required_dialog(self):
        """Hiển thị dialog yêu cầu đăng nhập"""
        def go_to_login(e):
            dialog.open = False
            self.page.update()
            self.navigate("/login")
        
        def close_dialog(e):
            dialog.open = False
            self.page.update()
        
        dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text(
                "🔒 Login Required",
                size=20,
                weight=ft.FontWeight.BOLD,
                color=ft.Colors.CYAN_700,
            ),
            content=ft.Text(
                "You need to log in to borrow books.\n\nPlease log in or create an account to continue.",
                size=13,
            ),
            actions=[
                ft.TextButton("Cancel", on_click=close_dialog),
                ft.FilledButton(
                    "Login",
                    on_click=go_to_login,
                    style=ft.ButtonStyle(bgcolor=ft.Colors.CYAN_400),
                ),
            ],
        )
        
        self.page.dialog = dialog
        dialog.open = True
        self.page.update()
    
    def show_error_snackbar(self, message):
        """Hiển thị error snackbar"""
        self.page.snack_bar = ft.SnackBar(
            content=ft.Text(message, color=ft.Colors.WHITE),
            bgcolor=ft.Colors.RED_700,
            duration=3000,
        )
        self.page.snack_bar.open = True
        self.page.update()
    
    # ================= BUILD METHODS (keep existing) =================
    
    def build(self):
        """Build complete book detail page"""
        # ... (keep existing build methods)
        # This would include all the existing layout code
        pass
    
    def build_borrow_button(self, available, is_reference):
        """Build borrow button"""
        if is_reference:
            return ft.Container(
                content=ft.Text(
                    "📖 This is a reference-only book. Cannot be borrowed.",
                    size=12,
                    color="#92400E",
                ),
                padding=15,
                bgcolor="#FEF3C7",
                border_radius=8,
            )
        
        if not self.current_user:
            return ft.Container(
                content=ft.Column([
                    ft.Text(
                        "🔒 Guests can view book information. To borrow, please log in.",
                        size=12,
                        color="#666",
                    ),
                    ft.Container(height=10),
                    ft.ElevatedButton(
                        "Login to borrow",
                        bgcolor=ft.Colors.CYAN_400,
                        color=ft.Colors.WHITE,
                        on_click=lambda _: self.navigate("/login")
                    ),
                ]),
                padding=15,
                bgcolor="#E8F5E9",
                border_radius=8,
            )
        
        return ft.ElevatedButton(
            "Borrow This Book" if available else "Not Available",
            disabled=not available,
            bgcolor=ft.Colors.CYAN_400 if available else ft.Colors.GREY_400,
            color=ft.Colors.WHITE,
            on_click=self.handle_borrow if available else None,
        )
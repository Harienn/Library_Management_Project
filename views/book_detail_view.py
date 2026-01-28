# views/book_detail_view.py - ENHANCED BORROW HANDLER
"""
<<<<<<< HEAD
Book Detail View - Complete with all sections
=======
Book Detail View - ENHANCED VERSION
✅ Confirmation dialog before borrowing
✅ Detailed error notifications for all cases
✅ Transaction ID display on success
>>>>>>> version-2
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
        
<<<<<<< HEAD
        try:
            print("📦 Building breadcrumb...")
            breadcrumb = self.build_breadcrumb()
            
            print("📦 Building main info...")
            main_info = self.build_main_info()
            
            print("📦 Building copies notes...")
            copies_notes = self.build_copies_notes()
            
            print("📦 Building more by author...")
            more_by_author = self.build_more_by_author()
            
            print("📦 Building same genre...")
            same_genre = self.build_same_genre()
            
            print("📦 Building header...")
            # Simple header (NO ICONS)
            user_name = "Guest"
            if self.current_user:
                user_name = self.current_user.get('fullname', 'User')
            
            simple_header = ft.Container(
                content=ft.Row([
                    ft.TextButton(
                        "← Back",
                        style=ft.ButtonStyle(color=ft.Colors.WHITE),
                        on_click=lambda _: self.navigate("/books"),
                    ),
                    ft.Text("Library System", size=18, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
                    ft.Container(expand=True),
                    ft.Text(f"Hello, {user_name}", size=14, color=ft.Colors.WHITE),
                    ft.Container(width=10),
                    ft.TextButton(
                        "🏠 Home",
                        style=ft.ButtonStyle(color=ft.Colors.WHITE),
                        on_click=lambda _: self.navigate("/"),
                    ),
                ], alignment=ft.MainAxisAlignment.START),
                padding=ft.padding.symmetric(horizontal=20, vertical=10),
                bgcolor=ft.Colors.CYAN_400,
            )
            
            print("📦 Assembling content...")
            content = ft.Column([
                simple_header,
                ft.Container(
                    content=ft.Column([
                        breadcrumb,
                        main_info,
                        copies_notes,
                        more_by_author,
                        same_genre,
                        ft.Container(height=40),
                    ], scroll=ft.ScrollMode.AUTO),
                    expand=True,
=======
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
>>>>>>> version-2
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
<<<<<<< HEAD
            return self.build_error_view(str(e))

    def build_error_view(self, error_msg=None):
        """Build error view (NO ICONS)"""
        return ft.View(
            "/book_detail",
            [ft.Container(
=======
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
>>>>>>> version-2
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
        
<<<<<<< HEAD
        # Cover
        cover_url = self.book_data.get("image_url")
        if cover_url:
            try:
                cover_content = ft.Image(
                    src=cover_url,
                    width=200,
                    height=300,
                    fit=ft.ImageFit.COVER,
                )
            except:
                cover_content = ft.Container(
                    content=ft.Text("📚", size=80),
                    width=200,
                    height=300,
                    bgcolor="#B2EBF2",
                    alignment=ft.Alignment(0, 0),
                )
        else:
            cover_content = ft.Container(
                content=ft.Text("📚", size=80),
                width=200,
                height=300,
                bgcolor="#B2EBF2",
                alignment=ft.Alignment(0, 0),
=======
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
>>>>>>> version-2
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
        
<<<<<<< HEAD
        cover = ft.Container(
            content=cover_content,
            border_radius=8,
            border=ft.border.all(1, "#E5E7EB"),
        )
        
        # Badge
        if is_reference:
            badge_text, badge_color = "Reference Only", "#F59E0B"
        elif available:
            badge_text, badge_color = "Available", "#10B981"
        else:
            badge_text, badge_color = "Not Available", "#EF4444"
        
        badge = ft.Container(
            content=ft.Text(badge_text, size=12, color=ft.Colors.WHITE, weight=ft.FontWeight.BOLD),
            bgcolor=badge_color,
            padding=ft.padding.symmetric(horizontal=20, vertical=8),
            border_radius=20,
            margin=ft.margin.only(top=15),
        )
        
        # Details
        details = ft.Column([
            ft.Text(self.book_data.get("title", "Unknown Title"), size=32, weight=ft.FontWeight.BOLD, color="#111827"),
            ft.Container(height=15),
            self.info_row("Author:", self.book_data.get("author_name") or "Unknown Author"),
            self.info_row("Category:", self.book_data.get("category_name") or "Unknown"),
            self.info_row("ISBN:", self.book_data.get("isbn") or "N/A"),
            self.info_row("Published:", str(self.book_data.get("publish_date") or "N/A")),
            self.info_row("Publisher:", self.book_data.get("publisher") or "Unknown"),
            ft.Container(height=15),
            self.build_tags(),
            ft.Container(height=25),
            self.build_borrow_section(available, is_reference),
            ft.Container(height=25),
            ft.Text("Summary", size=18, weight=ft.FontWeight.BOLD, color="#111827"),
            ft.Container(height=10),
            ft.Text(
                self.book_data.get("summary") or "No summary available for this book.",
                size=13,
                color="#444"
            ),
        ], spacing=3)
        
        return ft.Container(
            content=ft.Row([
                ft.Column([cover, badge], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                ft.Container(width=40),
                details,
            ], vertical_alignment=ft.CrossAxisAlignment.START),
            padding=ft.padding.symmetric(horizontal=40, vertical=20),
        )

    def info_row(self, label, value):
        """Info row helper"""
        return ft.Row([
            ft.Text(label, size=13, color="#666", weight=ft.FontWeight.BOLD, width=100),
            ft.Text(str(value), size=13, color="#333"),
        ], spacing=5)

    def build_tags(self):
        """Build category tags"""
        category = self.book_data.get("category_name", "")
        tags = []
        
        if "Văn học" in category or "Fiction" in category:
            tags = ["Fiction", "Literature"]
        elif "Khoa học" in category or "Science" in category:
            tags = ["Science", "Educational"]
        elif "Kỹ năng" in category:
            tags = ["Self-help", "Skills"]
        elif "Kinh tế" in category:
            tags = ["Business", "Economics"]
        elif category:
            tags = [category]
        
        if not tags:
            return ft.Container()
        
        return ft.Row([
            ft.Container(
                content=ft.Text(tag, size=11, color="#1E88E5"),
                bgcolor="#E3F2FD",
                padding=ft.padding.symmetric(horizontal=12, vertical=6),
                border_radius=15,
            ) for tag in tags[:3]
        ], spacing=10)

    def build_borrow_section(self, available, is_reference):
        """Borrow button or message"""
=======
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
>>>>>>> version-2
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
<<<<<<< HEAD
        )

    def build_copies_notes(self):
        """Copies info and notes"""
        total = self.book_data.get("total_copies", 0)
        available = self.book_data.get("available_copies", 0)
        borrowed = total - available
        
        copies = ft.Container(
            content=ft.Column([
                ft.Text("📚 Copies in the library", size=16, weight=ft.FontWeight.BOLD, color="#111827"),
                ft.Container(height=10),
                ft.Text(f"• {total} books on shelf", size=13, color="#374151"),
                ft.Text(
                    f"• {borrowed} currently borrowed" if borrowed > 0 else "• All available",
                    size=13,
                    color="#374151"
                ),
            ], spacing=5),
            padding=20,
            bgcolor=ft.Colors.WHITE,
            border_radius=8,
            expand=1,
        )
        
        price = self.book_data.get("price", 0)
        status = self.book_data.get("book_status", "AVAILABLE")
        
        notes = ft.Container(
            content=ft.Column([
                ft.Text("ℹ️ Quick notes", size=16, weight=ft.FontWeight.BOLD, color="#111827"),
                ft.Container(height=10),
                ft.Text(
                    f"• Price: {price:,.0f} VND" if price else "• Price: N/A",
                    size=13,
                    color="#374151"
                ),
                ft.Text(f"• Status: {status}", size=13, color="#374151"),
            ], spacing=5),
            padding=20,
            bgcolor=ft.Colors.WHITE,
            border_radius=8,
            expand=1,
        )
        
        return ft.Container(
            content=ft.Row([copies, ft.Container(width=20), notes]),
            padding=ft.padding.symmetric(horizontal=40, vertical=20),
        )

    def build_more_by_author(self):
        """More books by this author"""
        author_id = self.book_data.get("author_id")
        book_id = self.book_data.get("book_id")
        
        if not author_id:
            return ft.Container()
        
        books = self.get_books_by_author(author_id, book_id)
        if not books:
            return ft.Container()
        
        return ft.Container(
            content=ft.Column([
                ft.Text("More books by this author", size=18, weight=ft.FontWeight.BOLD, color="#111827"),
                ft.Container(height=20),
                ft.Row(
                    [self.create_book_card(book) for book in books],
                    spacing=15,
                    scroll=ft.ScrollMode.AUTO
                ),
            ]),
            padding=ft.padding.symmetric(horizontal=40, vertical=20),
        )

    def build_same_genre(self):
        """You may also like"""
        category_id = self.book_data.get("category_id")
        book_id = self.book_data.get("book_id")
        
        if not category_id:
            return ft.Container()
        
        books = self.get_books_by_category(category_id, book_id)
        if not books:
            return ft.Container()
        
        return ft.Container(
            content=ft.Column([
                ft.Text("You may also like", size=18, weight=ft.FontWeight.BOLD, color="#111827"),
                ft.Container(height=20),
                ft.Row(
                    [self.create_book_card(book) for book in books],
                    spacing=15,
                    scroll=ft.ScrollMode.AUTO
                ),
            ]),
            padding=ft.padding.symmetric(horizontal=40, vertical=20),
        )

    def create_book_card(self, book):
        """Create small book card"""
        title = book.get("title", "")
        available = book.get("available_copies", 0) > 0
        book_id = book.get("book_id")
        
        def on_click(e):
            if self.page.data is None:
                self.page.data = {}
            self.page.data['selected_book'] = {"book_id": book_id}
            self.navigate("/book_detail")
        
        return ft.Container(
            content=ft.Column([
                ft.Container(
                    content=ft.Text("📚", size=60),
                    width=140,
                    height=200,
                    bgcolor="#B2EBF2",
                    alignment=ft.Alignment(0, 0),
                    border_radius=8,
                    on_click=on_click,
                    ink=True,
                ),
                ft.Container(height=10),
                ft.Text(title[:30], size=13, weight=ft.FontWeight.BOLD, max_lines=2, color="#111827"),
                ft.Container(height=10),
                ft.ElevatedButton(
                    "Borrow" if available else "Not available",
                    disabled=not available,
                    width=140,
                    bgcolor=ft.Colors.CYAN_400 if available else ft.Colors.GREY_400,
                    color=ft.Colors.WHITE,
                ),
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            padding=10,
        )

    def handle_borrow(self, e):
        """Handle borrow book"""
        try:
            from services.borrow_service import borrow_book
            
            book_id = self.book_data.get("book_id")
            member_id = self.current_user.get("user_id")
            
            success, message = borrow_book(member_id, book_id)
            
            self.page.snack_bar = ft.SnackBar(
                content=ft.Text(message, color=ft.Colors.WHITE),
                bgcolor=ft.Colors.GREEN_700 if success else ft.Colors.RED_700,
            )
            self.page.snack_bar.open = True
            self.page.update()
            
            if success:
                import time
                time.sleep(1)
                self.navigate("/my_borrowing")
        
        except Exception as error:
            print(f"Error borrowing book: {error}")
            self.page.snack_bar = ft.SnackBar(
                content=ft.Text(f"Error: {str(error)}", color=ft.Colors.WHITE),
                bgcolor=ft.Colors.RED_700,
            )
            self.page.snack_bar.open = True
            self.page.update()
=======
        )
>>>>>>> version-2

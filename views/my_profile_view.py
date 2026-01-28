# views/my_profile_view.py
import flet as ft
from components.header import Header
from components.navbar import NavBar


class MyProfileView:
    def __init__(self, page, current_user, navigate, on_logout=None):
        self.page = page
        self.current_user = current_user
        self.navigate = navigate
        self.on_logout = on_logout

    def build(self):
        header = Header(self.page, self.current_user, self.navigate, self.on_logout)
        navbar = NavBar(self.page, self.current_user, self.navigate, "/my_profile")

        if not self.current_user:
            content = self.build_guest_view()
        else:
            content = self.build_member_view()

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
            route="/my_profile",
            controls=[
                ft.Container(
                    content=main_content,
                    bgcolor=ft.Colors.GREY_50,
                    expand=True,
                )
            ],
        )

    # ================= GUEST VIEW =================

    def build_guest_view(self):
        guest_card = ft.Container(
            content=ft.Column(
                [
                    ft.Text("Guest capabilities", size=18, weight=ft.FontWeight.BOLD),
                    ft.Container(height=4),
                    ft.Text(
                        "As a guest, you can:",
                        size=13,
                        color=ft.Colors.GREY_700,
                    ),
                    ft.Container(height=12),
                    ft.Text("• Search and filter books in the library catalog.", size=13),
                    ft.Text(
                        "• View detailed book information (cover, title, author, category, summary).",
                        size=13,
                    ),
                    ft.Text("• Browse featured and latest books on the homepage.", size=13),
                    ft.Container(height=20),
                    ft.Text(
                        "Why create a member profile?",
                        size=18,
                        weight=ft.FontWeight.BOLD,
                    ),
                    ft.Container(height=4),
                    ft.Text(
                        "After registering and completing your profile, you will be able to:",
                        size=13,
                        color=ft.Colors.GREY_700,
                    ),
                    ft.Container(height=12),
                    ft.Text(
                        "• Borrow books and view your borrowing information online.", size=13
                    ),
                    ft.Text(
                        "• Request borrowing extensions (extension of due date) when allowed.",
                        size=13,
                    ),
                    ft.Text(
                        "• View history and all penalties (overdue, damaged, lost).",
                        size=13,
                    ),
                    ft.Text(
                        "• Receive notifications and reminders from the library.", size=13
                    ),
                    ft.Container(height=20),
                    ft.Row(
                        [
                            ft.FilledButton(
                                "Create member account",
                                bgcolor=ft.Colors.CYAN_400,
                                color=ft.Colors.WHITE,
                                on_click=lambda _: self.navigate("/register"),
                                style=ft.ButtonStyle(
                                    shape=ft.RoundedRectangleBorder(radius=8),
                                    padding=ft.Padding(20, 12, 20, 12),
                                ),
                            ),
                            ft.OutlinedButton(
                                "Login instead",
                                on_click=lambda _: self.navigate("/login"),
                                style=ft.ButtonStyle(
                                    shape=ft.RoundedRectangleBorder(radius=8),
                                    side=ft.BorderSide(1, ft.Colors.GREY_400),
                                    padding=ft.Padding(20, 12, 20, 12),
                                ),
                            ),
                        ],
                        spacing=12,
                    ),
                ],
                spacing=0,
            ),
            padding=24,
            bgcolor=ft.Colors.WHITE,
            border_radius=10,
            border=ft.Border.all(1, ft.Colors.GREY_200),
        )

        return ft.Container(
            content=ft.Column(
                [
                    ft.Container(height=24),
                    ft.Text("My profile", size=26, weight=ft.FontWeight.BOLD),
                    ft.Container(height=4),
                    ft.Text(
                        "You are currently using the system as a guest. To borrow books and manage your account, please register as a member.",
                        size=13,
                        color=ft.Colors.GREY_600,
                    ),
                    ft.Container(height=24),
                    guest_card,
                    ft.Container(height=40),
                ],
                scroll="auto",
            ),
            padding=ft.Padding(left=40, right=40, top=0, bottom=0),
            expand=True,
        )

    # ================= MEMBER VIEW =================

    def build_member_view(self):
        user = self.current_user or {}

        member_id = user.get("user_id", "123")
        fullname = user.get("fullname", "Nguyen Van A")
        email = user.get("email", "member@example.com")
        phone = user.get("phone", "")
        gender = user.get("gender", "")
        address = user.get("address", "")
<<<<<<< HEAD
=======
        total_fine_debt = user.get("totalFineDebt", 0)
        
        # ✅ Tạo refs cho các fields
        fullname_field = ft.Ref[ft.TextField]()
        phone_field = ft.Ref[ft.TextField]()
        gender_field = ft.Ref[ft.Dropdown]()
        address_field = ft.Ref[ft.TextField]()
        save_message = ft.Ref[ft.Text]()
        
        def handle_save_profile(e):
            """Xử lý lưu thông tin profile"""
            new_fullname = fullname_field.current.value
            new_phone = phone_field.current.value
            new_gender = gender_field.current.value
            new_address = address_field.current.value
            
            if not new_fullname or len(new_fullname.strip()) == 0:
                save_message.current.value = "❌ Please enter your full name"
                save_message.current.color = ft.Colors.RED_600
                save_message.current.visible = True
                self.page.update()
                return
            
            user_id = self.current_user.get('user_id')
            success, message = update_user_profile(
                user_id,
                new_fullname,
                new_phone,
                new_gender,
                new_address
            )
            
            if success:
                save_message.current.value = "✓ " + message
                save_message.current.color = ft.Colors.GREEN_600
                save_message.current.visible = True
                
                self.current_user['fullname'] = new_fullname
                self.current_user['phone'] = new_phone
                self.current_user['gender'] = new_gender
                self.current_user['address'] = new_address
                
                self.page.update()
                
                import time
                import threading
                def hide_success():
                    time.sleep(3)
                    save_message.current.visible = False
                    self.page.update()
                threading.Thread(target=hide_success, daemon=True).start()
            else:
                save_message.current.value = "❌ " + message
                save_message.current.color = ft.Colors.RED_600
                save_message.current.visible = True
                self.page.update()
>>>>>>> version-2

        # ✅ UPDATED: Tạo các field với label riêng biệt (hiển thị bên ngoài)
        def create_labeled_field(label_text, field_widget):
            """Helper function to create a field with external label"""
            return ft.Column(
                [
                    ft.Text(
                        label_text,
                        size=12,
                        color=ft.Colors.GREY_700,
                        weight=ft.FontWeight.W_500,
                    ),
                    ft.Container(height=4),
                    field_widget,
                ],
                spacing=0,
            )

        # Member ID field (read-only)
        member_id_field = ft.TextField(
            value=str(member_id),
            read_only=True,
            border_color=ft.Colors.GREY_300,
            bgcolor=ft.Colors.GREY_100,
            filled=True,
        )

        # Card status field (read-only)
        card_status_field = ft.TextField(
            value="Active",
            read_only=True,
            border_color=ft.Colors.GREY_300,
            bgcolor=ft.Colors.GREY_100,
            filled=True,
        )

        # Full name field
        fullname_input = ft.TextField(
            ref=fullname_field,
            value=fullname,
            hint_text="Enter your full name",
            border_color=ft.Colors.GREY_400,
            focused_border_color=ft.Colors.CYAN_400,
            filled=True,
            bgcolor=ft.Colors.WHITE,
        )

        # Email field (read-only)
        email_input = ft.TextField(
            value=email,
            read_only=True,
            border_color=ft.Colors.GREY_300,
            bgcolor=ft.Colors.GREY_100,
            filled=True,
        )

        # Phone field
        phone_input = ft.TextField(
            ref=phone_field,
            value=phone,
            hint_text="Enter phone number",
            border_color=ft.Colors.GREY_400,
            focused_border_color=ft.Colors.CYAN_400,
            filled=True,
            bgcolor=ft.Colors.WHITE,
        )

        # Gender dropdown
        gender_dropdown = ft.Dropdown(
            ref=gender_field,
            value=gender if gender else None,
            hint_text="Select",
            options=[
                ft.dropdown.Option("Male"),
                ft.dropdown.Option("Female"),
                ft.dropdown.Option("Other"),
            ],
            border_color=ft.Colors.GREY_400,
            focused_border_color=ft.Colors.CYAN_400,
            filled=True,
            bgcolor=ft.Colors.WHITE,
        )

        # Address field
        address_input = ft.TextField(
            ref=address_field,
            value=address,
            hint_text="Street, district, city",
            multiline=True,
            min_lines=2,
            max_lines=3,
            border_color=ft.Colors.GREY_400,
            focused_border_color=ft.Colors.CYAN_400,
            filled=True,
            bgcolor=ft.Colors.WHITE,
        )

        # Save message text
        save_message_text = ft.Text(
            ref=save_message,
            visible=False,
            size=13,
        )

        # ✅ Personal Information Card
        personal_info = ft.Container(
            content=ft.Column(
                [
                    ft.Text("Personal information", size=18, weight=ft.FontWeight.BOLD),
                    ft.Container(height=16),
                    
                    # Row 1: Member ID and Card Status
                    ft.Row(
                        [
                            ft.Container(
                                content=create_labeled_field("Member ID", member_id_field),
                                expand=1,
                            ),
                            ft.Container(
                                content=create_labeled_field("Card status", card_status_field),
                                expand=1,
                            ),
                        ],
                        spacing=16,
                    ),
                    
                    ft.Container(height=12),
<<<<<<< HEAD
                    ft.Row(
                        [
                            ft.TextField(
                                label="Member ID",
                                value=str(member_id),
                                disabled=True,
                                expand=1,
                            ),
                            ft.TextField(
                                label="Card status",
                                value="Active",
                                disabled=True,
=======
                    
                    # Full name field
                    create_labeled_field("Full name", fullname_input),
                    
                    ft.Container(height=12),
                    
                    # Email field
                    create_labeled_field("Email address", email_input),
                    
                    ft.Container(height=12),
                    
                    # Row 2: Phone and Gender
                    ft.Row(
                        [
                            ft.Container(
                                content=create_labeled_field("Phone number", phone_input),
                                expand=1,
                            ),
                            ft.Container(
                                content=create_labeled_field("Gender", gender_dropdown),
>>>>>>> version-2
                                expand=1,
                            ),
                        ],
                        spacing=16,
                    ),
<<<<<<< HEAD
                    ft.TextField(label="Full name", value=fullname),
                    ft.TextField(label="Email address", value=email),
                    ft.Row(
                        [
                            ft.TextField(
                                label="Phone number", value=phone, expand=1
                            ),
                            ft.Dropdown(
                                label="Gender",
                                value=gender if gender else None,
                                options=[
                                    ft.dropdown.Option("Male"),
                                    ft.dropdown.Option("Female"),
                                    ft.dropdown.Option("Other"),
                                ],
                                expand=1,
                            ),
                        ],
                        spacing=16,
                    ),
                    ft.TextField(
                        label="Address", value=address, multiline=True
                    ),
=======
                    
                    ft.Container(height=12),
                    
                    # Address field
                    create_labeled_field("Address", address_input),
                    
>>>>>>> version-2
                    ft.Container(height=16),
                    
                    # Save button
                    ft.FilledButton(
                        "Save changes",
                        bgcolor=ft.Colors.CYAN_400,
                        color=ft.Colors.WHITE,
                        style=ft.ButtonStyle(
                            shape=ft.RoundedRectangleBorder(radius=8),
                            padding=ft.Padding(20, 14, 20, 14),
                        ),
                        on_click=lambda e: None,  # TODO DB
                    ),
                    
                    ft.Container(height=8),
                    save_message_text,
                    
                    ft.Container(height=8),
                    
                    # Info message
                    ft.Text(
                        "New members must complete personal information before borrowing books.",
                        size=12,
                        color=ft.Colors.CYAN_600,
                    ),
                ],
                spacing=0,
            ),
            padding=24,
            bgcolor=ft.Colors.WHITE,
            border_radius=10,
            border=ft.Border.all(1, ft.Colors.GREY_200),
            expand=1,
        )

<<<<<<< HEAD
=======
        # ================= CHANGE PASSWORD SECTION =================
        
        password_error_text = ft.Text(
            visible=False,
            size=13,
        )
        
        # ✅ Current Password with Show/Hide
        current_password_field = ft.TextField(
            hint_text="Enter current password",
            password=True,
            border_color=ft.Colors.GREY_400,
            focused_border_color=ft.Colors.CYAN_400,
            filled=True,
            bgcolor=ft.Colors.WHITE,
        )
        
        current_show_hide_container = ft.Container()
        
        def build_current_password_button():
            is_hidden = current_password_field.password
            btn = ft.TextButton(
                "Show" if is_hidden else "Hide",
                on_click=lambda e: toggle_current_password()
            )
            current_show_hide_container.content = btn
            return btn
        
        def toggle_current_password():
            current_password_field.password = not current_password_field.password
            build_current_password_button()
            self.page.update()
        
        current_password_field.suffix = current_show_hide_container
        build_current_password_button()
        
        # ✅ New Password with Show/Hide
        new_password_field = ft.TextField(
            hint_text="Enter new password (min 8 characters)",
            password=True,
            border_color=ft.Colors.GREY_400,
            focused_border_color=ft.Colors.CYAN_400,
            filled=True,
            bgcolor=ft.Colors.WHITE,
        )
        
        new_show_hide_container = ft.Container()
        
        def build_new_password_button():
            is_hidden = new_password_field.password
            btn = ft.TextButton(
                "Show" if is_hidden else "Hide",
                on_click=lambda e: toggle_new_password()
            )
            new_show_hide_container.content = btn
            return btn
        
        def toggle_new_password():
            new_password_field.password = not new_password_field.password
            build_new_password_button()
            self.page.update()
        
        new_password_field.suffix = new_show_hide_container
        build_new_password_button()
        
        # ✅ Confirm New Password with Show/Hide
        confirm_new_password_field = ft.TextField(
            hint_text="Re-enter your new password",
            password=True,
            border_color=ft.Colors.GREY_400,
            focused_border_color=ft.Colors.CYAN_400,
            filled=True,
            bgcolor=ft.Colors.WHITE,
        )
        
        confirm_show_hide_container = ft.Container()
        
        def build_confirm_password_button():
            is_hidden = confirm_new_password_field.password
            btn = ft.TextButton(
                "Show" if is_hidden else "Hide",
                on_click=lambda e: toggle_confirm_password()
            )
            confirm_show_hide_container.content = btn
            return btn
        
        def toggle_confirm_password():
            confirm_new_password_field.password = not confirm_new_password_field.password
            build_confirm_password_button()
            self.page.update()
        
        confirm_new_password_field.suffix = confirm_show_hide_container
        build_confirm_password_button()
        
        def show_password_error(message):
            password_error_text.value = message
            password_error_text.color = ft.Colors.RED_600
            password_error_text.visible = True
            self.page.update()
        
        def hide_password_error():
            password_error_text.visible = False
            self.page.update()
        
        def handle_change_password(e):
            hide_password_error()
            
            if not current_password_field.value:
                show_password_error("Please enter current password")
                return
            
            if not new_password_field.value:
                show_password_error("Please enter new password")
                return
            
            if not confirm_new_password_field.value:
                show_password_error("Please confirm new password")
                return
            
            if new_password_field.value != confirm_new_password_field.value:
                show_password_error("New passwords do not match")
                return
            
            if len(new_password_field.value) < 8:
                show_password_error("Password must be at least 8 characters long")
                return
            
            user_id = self.current_user.get('user_id')
            success, message = change_user_password(
                user_id,
                current_password_field.value,
                new_password_field.value
            )
            
            if success:
                password_error_text.value = "✓ " + message
                password_error_text.color = ft.Colors.GREEN_600
                password_error_text.visible = True
                
                current_password_field.value = ""
                new_password_field.value = ""
                confirm_new_password_field.value = ""
                
                self.page.update()
                
                import time
                import threading
                def hide_success():
                    time.sleep(3)
                    password_error_text.visible = False
                    self.page.update()
                threading.Thread(target=hide_success, daemon=True).start()
            else:
                password_error_text.color = ft.Colors.RED_600
                show_password_error(message)

        # ✅ Tạo danh sách controls động
        password_info_controls = [
            ft.Text("Maximum books allowed: 10", size=13),
            ft.Text("Standard borrowing period: 15 days", size=13),
        ]
        
        # ✅ CHỈ THÊM FINES KHI > 0
        if total_fine_debt > 0:
            password_info_controls.append(
                ft.Text(
                    f"Current outstanding fines: {total_fine_debt:,.0f} VND",
                    size=13,
                    color=ft.Colors.RED_600,
                )
            )
            password_info_controls.append(
                ft.Text(
                    "Borrowing status: Blocked when fines exceed limit or books are overdue.",
                    size=13,
                    color=ft.Colors.RED_400,
                )
            )

        # ✅ Change Password Card
>>>>>>> version-2
        change_password = ft.Container(
            content=ft.Column(
                [
                    ft.Text("Change password", size=18, weight=ft.FontWeight.BOLD),
<<<<<<< HEAD
                    ft.Container(height=12),
                    ft.TextField(
                        label="Current password",
                        password=True,
                        can_reveal_password=True,
                    ),
                    ft.TextField(
                        label="New password",
                        password=True,
                        can_reveal_password=True,
                    ),
                    ft.TextField(
                        label="Confirm new password",
                        password=True,
                        can_reveal_password=True,
                    ),
=======
                    ft.Container(height=16),
                    
                    password_error_text,
                    ft.Container(height=8),
                    
                    # Current password
                    create_labeled_field("Current password", current_password_field),
>>>>>>> version-2
                    ft.Container(height=12),
                    
                    # New password
                    create_labeled_field("New password", new_password_field),
                    ft.Container(height=12),
                    
                    # Confirm new password
                    create_labeled_field("Confirm new password", confirm_new_password_field),
                    
                    ft.Container(height=16),
                    ft.FilledButton(
                        "Update password",
                        bgcolor=ft.Colors.CYAN_400,
                        color=ft.Colors.WHITE,
                        style=ft.ButtonStyle(
                            shape=ft.RoundedRectangleBorder(radius=8),
                            padding=ft.Padding(20, 14, 20, 14),
                        ),
                        on_click=lambda e: None,  # TODO DB
                    ),
                    ft.Container(height=16),
<<<<<<< HEAD
                    ft.Text("Maximum books allowed: 10", size=13),
                    ft.Text("Standard borrowing period: 15 days", size=13),
                    ft.Text("Current outstanding fines: 410,000 VND", size=13),
                    ft.Text(
                        "Borrowing status: Blocked when fines exceed limit or books are overdue.",
                        size=13,
                        color=ft.Colors.RED_400,
                    ),
=======
                    *password_info_controls,
>>>>>>> version-2
                ],
                spacing=0,
            ),
            padding=24,
            bgcolor=ft.Colors.WHITE,
            border_radius=10,
            border=ft.Border.all(1, ft.Colors.GREY_200),
            expand=1,
        )

        return ft.Container(
            content=ft.Column(
                [
                    ft.Container(height=24),
                    ft.Text("My profile", size=26, weight=ft.FontWeight.BOLD),
                    ft.Container(height=4),
                    ft.Text(
                        "Update your personal information and change your password.",
                        size=13,
                        color=ft.Colors.GREY_600,
                    ),
                    ft.Container(height=24),
                    ft.Row(
                        [
                            personal_info,
                            change_password,
                        ],
                        spacing=24,
                    ),
                    ft.Container(height=40),
                ],
                scroll="auto",
            ),
            padding=ft.Padding(left=40, right=40, top=0, bottom=0),
            expand=True,
        )
# views/admin/pages/manage_members.py

import flet as ft
from database.db import get_connection
from services.member_service import fetch_all_members, insert_member, update_member, delete_member, check_email_exists

class ManageMembersPage:
    def __init__(self):
        self.current_member_id = None
        self.page_ref = None
        self.keyword = None

    def build(self, page: ft.Page = None):
        """QUAN TRỌNG: Luôn gán page_ref mới mỗi lần build"""
        if page:
            self.page_ref = page
            print(f"=== DEBUG: page_ref set in build: {self.page_ref} ===")
        
        # Tạo container cho table để có thể refresh riêng
        self.table_container = ft.Container(
            content=self._build_table_content(),
            expand=True,
        )
        
        content = ft.Column([
            # Header
            ft.Row([
                ft.Text("Member list", size=16, weight=ft.FontWeight.BOLD, color="#1F2937"),
                ft.Container(expand=True),
                ft.Row([
                    ft.ElevatedButton(
                        "Refresh",
                        bgcolor="#6B7280",
                        color="#FFFFFF",
                        height=36,
                        on_click=self.refresh_table_click,
                    ),
                    ft.Container(width=8),
                    ft.ElevatedButton(
                        "+ Add member",
                        bgcolor="#E5E7EB",
                        color="#111827",
                        on_click=self.reset_form,
                        height=36,
                    ),
                ]),
            ]),
            
            ft.Text(
                "Card status: Active or Temporarily Locked (usually because of unpaid penalties). Locked members cannot borrow or log in.",
                size=12,
                color="#6B7280",
            ),
            
            ft.Container(height=8),
            
            # Form
            self._build_form(),
            
            # Toolbar
            self._build_toolbar(),
            
            # Table container (sẽ được cập nhật động)
            self.table_container,
            
            # Note
            ft.Text(
                "Editing a member here should reflect on their My profile screen, since both use the same set of fields.",
                size=11,
                color="#6B7280",
                italic=True,
            ),
        ], spacing=10)
        
        self.main_container = ft.Container(
            content=content,
            padding=ft.padding.all(16),
            bgcolor="#FFFFFF",
            border_radius=14,
            border=ft.border.all(1, "#E5E7EB"),
        )
        
        return self.main_container
    
    def refresh_table_click(self, e):
        """Xử lý khi click nút Refresh"""
        print("=== DEBUG: Refreshing table via button ===")
        print(f"=== DEBUG: page_ref in refresh_table_click: {self.page_ref} ===")
        self._refresh_table_only()
        self.show_success("Table refreshed")
    
    def reset_form(self, e=None):
        """Reset form"""
        print("=== DEBUG: Resetting form ===")
        self.current_member_id = None
        
        # Reset tất cả field về giá trị mặc định
        if hasattr(self, 'member_id_field'):
            self.member_id_field.value = ""
            self.member_id_field.disabled = False
            self.member_id_field.update()
            
        if hasattr(self, 'fullname_field'):
            self.fullname_field.value = ""
            self.fullname_field.update()
            
        if hasattr(self, 'email_field'):
            self.email_field.value = ""
            self.email_field.update()
            
        if hasattr(self, 'phone_field'):
            self.phone_field.value = ""
            self.phone_field.update()
            
        if hasattr(self, 'gender_field'):
            self.gender_field.value = "Select"
            self.gender_field.update()
            
        if hasattr(self, 'address_field'):
            self.address_field.value = ""
            self.address_field.update()
            
        if hasattr(self, 'card_status_field'):
            self.card_status_field.value = "Active"
            self.card_status_field.update()
        
        # Update UI
        if e and hasattr(e, 'page'):
            e.page.update()
        elif self.page_ref:
            self.page_ref.update()
            
        self.show_success("Form reset successfully")
    
    def edit_member(self, member_data, e):
        """Load dữ liệu member vào form"""
        try:
            print(f"=== DEBUG: Editing member: {member_data} ===")
            self.current_member_id = member_data["user_id"]
            
            # Cập nhật giá trị cho các field
            self.member_id_field.value = str(member_data["user_id"])
            self.member_id_field.disabled = True  # Không cho sửa ID khi edit
            
            self.fullname_field.value = member_data["fullname"] if member_data["fullname"] else ""
            self.email_field.value = member_data["email"] if member_data["email"] else ""
            
            # Xử lý "-" cho phone, gender, address
            phone_value = member_data["phone"]
            self.phone_field.value = "" if phone_value == "-" or not phone_value else phone_value
            
            gender_value = member_data["gender"]
            self.gender_field.value = "Select" if gender_value == "-" or not gender_value else gender_value
            
            address_value = member_data["address"]
            self.address_field.value = "" if address_value == "-" or not address_value else address_value
            
            # Map user_status sang card_status
            user_status = member_data.get("user_status", "ACTIVE")
            self.card_status_field.value = "Active" if user_status == "ACTIVE" else "Temporarily Locked"
            
            # Update UI
            self.member_id_field.update()
            self.fullname_field.update()
            self.email_field.update()
            self.phone_field.update()
            self.gender_field.update()
            self.address_field.update()
            self.card_status_field.update()
            
            # Scroll to top
            if e and hasattr(e, 'page'):
                try:
                    e.page.window_scroll_to(0, 0)
                except:
                    pass
                
            self.show_success(f"Loaded member: {member_data['fullname']}")
                
        except Exception as ex:
            print(f"=== DEBUG: Error in edit_member: {ex} ===")
            import traceback
            traceback.print_exc()
            self.show_error(f"Error loading member data: {str(ex)}")
    
    def _build_form(self):
        """Form theo thiết kế mới - 2 cột"""
        
        # Fields
        self.member_id_field = ft.TextField(
            hint_text="Auto-generated for new members",
            border_color="#D1D5DB",
            text_size=13,
            border_radius=6,
            height=40,
            expand=True,
            disabled=False,
            read_only=True,  # Không cho nhập vì tự động tạo
        )
        
        self.card_status_field = ft.Dropdown(
            options=[
                ft.dropdown.Option("Active"),
                ft.dropdown.Option("Temporarily Locked"),
            ],
            value="Active",
            border_color="#D1D5DB",
            text_size=13,
            border_radius=6,
            height=40,
            expand=True,
        )
        
        self.fullname_field = ft.TextField(
            hint_text="Nguyen Van A",
            border_color="#D1D5DB",
            text_size=13,
            border_radius=6,
            height=40,
            expand=True,
        )
        
        self.email_field = ft.TextField(
            hint_text="member@example.com",
            border_color="#D1D5DB",
            text_size=13,
            border_radius=6,
            height=40,
            expand=True,
        )
        
        self.phone_field = ft.TextField(
            hint_text="09xx xxx xxx",
            border_color="#D1D5DB",
            text_size=13,
            border_radius=6,
            height=40,
            expand=True,
        )
        
        self.gender_field = ft.Dropdown(
            options=[
                ft.dropdown.Option("Select"),
                ft.dropdown.Option("Male"),
                ft.dropdown.Option("Female"),
                ft.dropdown.Option("Other"),
            ],
            value="Select",
            border_color="#D1D5DB",
            text_size=13,
            border_radius=6,
            height=40,
            expand=True,
        )
        
        self.address_field = ft.TextField(
            hint_text="Street, district, city",
            border_color="#D1D5DB",
            text_size=13,
            border_radius=6,
            multiline=True,
            min_lines=3,
            max_lines=3,
            expand=True,
        )
        
        # Layout
        return ft.Column([
            # Row 1: Member ID + Card status
            ft.Row([
                ft.Column([
                    ft.Text("Member ID", size=12, color="#374151"),
                    self.member_id_field,
                ], spacing=4, expand=1),
                ft.Container(width=16),
                ft.Column([
                    ft.Text("Card status", size=12, color="#374151"),
                    self.card_status_field,
                ], spacing=4, expand=1),
            ]),
            
            # Row 2: Full name + Email
            ft.Row([
                ft.Column([
                    ft.Text("Full name", size=12, color="#374151"),
                    self.fullname_field,
                ], spacing=4, expand=1),
                ft.Container(width=16),
                ft.Column([
                    ft.Text("Email address", size=12, color="#374151"),
                    self.email_field,
                ], spacing=4, expand=1),
            ]),
            
            # Row 3: Phone + Gender
            ft.Row([
                ft.Column([
                    ft.Text("Phone number", size=12, color="#374151"),
                    self.phone_field,
                ], spacing=4, expand=1),
                ft.Container(width=16),
                ft.Column([
                    ft.Text("Gender", size=12, color="#374151"),
                    self.gender_field,
                ], spacing=4, expand=1),
            ]),
            
            # Row 4: Address - FULL WIDTH
            ft.Column([
                ft.Text("Address", size=12, color="#374151"),
                self.address_field,
            ], spacing=4),
            
            # Row 5: Save button
            ft.ElevatedButton(
                "Save member",
                bgcolor="#2563EB",
                color="#FFFFFF",
                height=40,
                expand=True,
                on_click=self.save_member,
            ),
        ], spacing=12)
    
    def _build_toolbar(self):
        """Search toolbar"""
        self.search_input = ft.TextField(
            hint_text="Search by Member ID, name or email...",
            border_radius=999,
            border_color="#D1D5DB",
            text_size=14,
            height=40,
            expand=True,
            on_submit=lambda e: self.search_members_action(e),
        )
        
        self.search_type = ft.Dropdown(
            options=[
                ft.dropdown.Option("all", "All fields"),
                ft.dropdown.Option("id", "Member ID"),
                ft.dropdown.Option("name", "Name"),
                ft.dropdown.Option("email", "Email"),
            ],
            value="all",
            border_radius=999,
            border_color="#D1D5DB",
            text_size=13,
            width=140,
            height=40,
        )
        
        return ft.Container(
            content=ft.Row([
                self.search_input,
                self.search_type,
                ft.ElevatedButton(
                    "Search",
                    bgcolor="#2563EB",
                    color="#FFFFFF",
                    height=40,
                    on_click=self.search_members_action,
                ),
            ], spacing=8),
            margin=ft.margin.symmetric(vertical=10),
        )
    
    def _build_table_content(self):
        """Xây dựng nội dung table có thể refresh được"""
        try:
            members = fetch_all_members()
            print(f"=== DEBUG: Fetched {len(members)} members ===")
            
        except Exception as ex:
            print(f"=== DEBUG: Error fetching members: {ex} ===")
            self.show_error(f"Error loading members: {str(ex)}")
            members = []
        
        rows = []
        for idx, m in enumerate(members, start=1):
            try:
                is_active = m.get("user_status", "ACTIVE") == "ACTIVE"
                
                # Format data
                phone = m.get("phone", "-")
                gender = m.get("gender", "-")
                address = m.get("address", "-")
                
                rows.append(
                    ft.DataRow(cells=[
                        ft.DataCell(ft.Text(str(idx), size=12, color="#374151")),
                        ft.DataCell(ft.Text(str(m["user_id"]), size=12, color="#374151")),
                        ft.DataCell(ft.Text(m["fullname"], size=12, color="#374151")),
                        ft.DataCell(ft.Text(m.get("email", "-"), size=12, color="#374151")),
                        ft.DataCell(ft.Text(phone, size=12, color="#374151")),
                        ft.DataCell(ft.Text(gender, size=12, color="#374151")),
                        ft.DataCell(ft.Text(address, size=12, color="#374151", no_wrap=False)),
                        ft.DataCell(
                            ft.Container(
                                content=ft.Text(
                                    "Active" if is_active else "Locked",
                                    size=11,
                                    color="#15803D" if is_active else "#B91C1C",
                                    weight=ft.FontWeight.W_600,
                                ),
                                bgcolor="#DCFCE7" if is_active else "#FEE2E2",
                                padding=ft.padding.symmetric(horizontal=10, vertical=4),
                                border_radius=4,
                            )
                        ),
                        ft.DataCell(
                            ft.Row([
                                ft.ElevatedButton(
                                    "Edit",
                                    bgcolor="#3B82F6",
                                    color="#FFFFFF",
                                    height=36,
                                    on_click=lambda e, data=m: self.edit_member(data, e),
                                    style=ft.ButtonStyle(
                                        shape=ft.RoundedRectangleBorder(radius=20),
                                        padding=ft.padding.symmetric(horizontal=24, vertical=0),
                                    ),
                                ),
                                ft.ElevatedButton(
                                    "Delete",
                                    bgcolor="#EF4444",
                                    color="#FFFFFF",
                                    height=36,
                                    on_click=lambda e, mid=m["user_id"]: self.confirm_delete(mid, e),
                                    style=ft.ButtonStyle(
                                        shape=ft.RoundedRectangleBorder(radius=20),
                                        padding=ft.padding.symmetric(horizontal=24, vertical=0),
                                    ),
                                ),
                            ], spacing=8)
                        ),
                    ])
                )
            except Exception as ex:
                print(f"=== DEBUG: Error processing member {m}: {ex} ===")
                continue

        table = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("#", size=12, weight=ft.FontWeight.BOLD)),
                ft.DataColumn(ft.Text("MEMBER ID", size=12, weight=ft.FontWeight.BOLD)),
                ft.DataColumn(ft.Text("FULL NAME", size=12, weight=ft.FontWeight.BOLD)),
                ft.DataColumn(ft.Text("EMAIL", size=12, weight=ft.FontWeight.BOLD)),
                ft.DataColumn(ft.Text("PHONE", size=12, weight=ft.FontWeight.BOLD)),
                ft.DataColumn(ft.Text("GENDER", size=12, weight=ft.FontWeight.BOLD)),
                ft.DataColumn(ft.Text("ADDRESS", size=12, weight=ft.FontWeight.BOLD)),
                ft.DataColumn(ft.Text("STATUS", size=12, weight=ft.FontWeight.BOLD)),
                ft.DataColumn(ft.Text("ACTIONS", size=12, weight=ft.FontWeight.BOLD)),
            ],
            rows=rows,
            horizontal_lines=ft.border.BorderSide(1, "#E5E7EB"),
            heading_row_height=36,
            data_row_min_height=56,
            column_spacing=20,
            expand=True,
        )

        return ft.Row([table], scroll=ft.ScrollMode.AUTO, expand=True)
    
    def search_members_action(self, e):
        """Xử lý tìm kiếm"""
        self._refresh_table_only()
        self.show_success("Search completed")

    def save_member(self, e):
        """Lưu thông tin thành viên"""
        try:
            print("=== DEBUG: Starting save_member ===")
            print(f"=== DEBUG: page_ref in save_member: {self.page_ref} ===")
            
            # Validate required fields
            if not self.fullname_field.value or not self.fullname_field.value.strip():
                self.show_error("❌ Full name is required")
                return
            
            email = self.email_field.value.strip() if self.email_field.value else ""
            if not email:
                self.show_error("❌ Email is required")
                return
            
            # Validate email format
            if "@" not in email or "." not in email:
                self.show_error("❌ Please enter a valid email address")
                return
            
            # Kiểm tra email trùng (chỉ khi thêm mới hoặc email thay đổi khi edit)
            if not self.current_member_id:
                email_exists = check_email_exists(email)
                if email_exists:
                    self.show_error("❌ Email already exists. Please use a different email.")
                    return
            
            # Chuẩn bị data
            data = {
                "fullname": self.fullname_field.value.strip(),
                "email": email,
                "phone": self.phone_field.value.strip() if self.phone_field.value and self.phone_field.value.strip() else None,
                "gender": self.gender_field.value if self.gender_field.value != "Select" else None,
                "address": self.address_field.value.strip() if self.address_field.value and self.address_field.value.strip() else None,
                "user_status": "ACTIVE" if self.card_status_field.value == "Active" else "LOCKED",
            }
            
            print(f"=== DEBUG: Data to save: {data} ===")
            print(f"=== DEBUG: Current member ID: {self.current_member_id} ===")
            
            # Nếu có current_member_id (đang edit)
            if self.current_member_id:
                data["user_id"] = self.current_member_id
                try:
                    print("=== DEBUG: Calling update_member ===")
                    success = update_member(data)
                    print(f"=== DEBUG: Update result: {success} ===")
                    
                    if success:
                        # Refresh table trước
                        self._refresh_table_only()
                        # Hiện thông báo thành công
                        self.show_success(f"✅ Member '{data['fullname']}' updated successfully!")
                        # Reset form
                        self.reset_form(e)
                    else:
                        self.show_error("❌ Failed to update member. Please try again.")
                        
                except Exception as ex:
                    print(f"=== DEBUG: Exception in update_member: {ex} ===")
                    import traceback
                    traceback.print_exc()
                    self.show_error(f"❌ Error updating member: {str(ex)}")
                    
            else:
                # Thêm mới
                try:
                    print("=== DEBUG: Calling insert_member ===")
                    member_id = insert_member(data)
                    print(f"=== DEBUG: Insert result - Member ID: {member_id} ===")
                    
                    if member_id and member_id > 0:
                        # Refresh table trước
                        self._refresh_table_only()
                        # Hiện thông báo thành công
                        self.show_success(f"✅ Member '{data['fullname']}' added successfully! (ID: {member_id})")
                        # Reset form
                        self.reset_form(e)
                    else:
                        self.show_error("❌ Failed to add member. Please try again.")
                        
                except Exception as ex:
                    print(f"=== DEBUG: Exception in insert_member: {ex} ===")
                    import traceback
                    traceback.print_exc()
                    self.show_error(f"❌ Error adding member: {str(ex)}")
            
        except Exception as ex:
            print(f"=== DEBUG: Unexpected error in save_member: {ex} ===")
            import traceback
            traceback.print_exc()
            self.show_error(f"❌ Unexpected error: {str(ex)}")
    
    def confirm_delete(self, member_id, e=None):
        """Hiển thị dialog xác nhận xóa"""
        print(f"=== DEBUG: confirm_delete called for member_id: {member_id} ===")
        print(f"=== DEBUG: page_ref in confirm_delete: {self.page_ref} ===")
        
        if not self.page_ref:
            print("=== DEBUG: No page_ref, cannot show dialog ===")
            self.show_error("❌ System error: Cannot show dialog")
            return
        
        def yes_action(e):
            print(f"=== DEBUG: yes_action triggered ===")
            try:
                print(f"=== DEBUG: Deleting member with ID: {member_id} ===")
                success = delete_member(member_id)
                print(f"=== DEBUG: Delete result: {success} ===")
                
                if success:
                    self.show_success("✅ Member deleted successfully")
                    # Kiểm tra nếu đang edit member bị xóa thì reset form
                    if self.current_member_id == member_id:
                        self.reset_form()
                else:
                    self.show_error("❌ Failed to delete member")
                
                # Đóng dialog
                if self.page_ref and hasattr(self.page_ref, 'dialog'):
                    self.page_ref.dialog.open = False
                    self.page_ref.update()
                
                # Refresh table
                self._refresh_table_only()
                
            except Exception as ex:
                print(f"=== DEBUG: Exception in delete: {ex} ===")
                import traceback
                traceback.print_exc()
                self.show_error(f"❌ Error deleting member: {str(ex)}")
        
        def cancel_action(e):
            print("=== DEBUG: Cancel action triggered ===")
            # Đóng dialog khi cancel
            if self.page_ref and hasattr(self.page_ref, 'dialog'):
                self.page_ref.dialog.open = False
                self.page_ref.update()

        # Tạo dialog
        print("=== DEBUG: Creating dialog ===")
        self.page_ref.dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Confirm Delete"),
            content=ft.Text(f"Are you sure you want to delete member ID: {member_id}?\nThis action cannot be undone."),
            actions=[
                ft.TextButton("Cancel", on_click=cancel_action),
                ft.ElevatedButton(
                    "Delete", 
                    bgcolor="#EF4444", 
                    color="#FFFFFF",
                    on_click=yes_action,
                ),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        self.page_ref.dialog.open = True
        self.page_ref.update()
        print("=== DEBUG: Dialog opened ===")
    
    def _refresh_table_only(self):
        """Chỉ refresh table mà không rebuild toàn bộ page"""
        print("=== DEBUG: _refresh_table_only called ===")
        print(f"=== DEBUG: page_ref in _refresh_table_only: {self.page_ref} ===")
        
        if not self.page_ref:
            print("=== DEBUG: No page_ref, cannot refresh ===")
            return
            
        try:
            # Cập nhật table container
            print("=== DEBUG: Building new table content ===")
            self.table_container.content = self._build_table_content()
            print("=== DEBUG: Updating page ===")
            self.page_ref.update()
            print("=== DEBUG: Page updated successfully ===")
        except Exception as ex:
            print(f"=== DEBUG: Error in _refresh_table_only: {ex} ===")
            import traceback
            traceback.print_exc()
            self.show_error(f"❌ Error refreshing table: {str(ex)}")
    
    def refresh_table(self):
        """Refresh table - gọi từ bên ngoài"""
        print("=== DEBUG: refresh_table called ===")
        self._refresh_table_only()
    
    def show_success(self, message):
        """Hiển thị thông báo thành công"""
        print(f"=== DEBUG show_success: {message} ===")
        if not self.page_ref:
            print("=== DEBUG: No page_ref available ===")
            return
        
        try:
            # Tạo snackbar mới
            snack_bar = ft.SnackBar(
                content=ft.Row([
                    ft.Icon(ft.icons.CHECK_CIRCLE, color="#FFFFFF", size=20),
                    ft.Text(message, color="#FFFFFF", size=14),
                ], tight=True, spacing=8),
                bgcolor="#10B981",
                duration=3000,
                behavior=ft.SnackBarBehavior.FLOATING,
            )
            
            # Gán và hiển thị
            self.page_ref.snack_bar = snack_bar
            self.page_ref.snack_bar.open = True
            self.page_ref.update()
            print("=== DEBUG: Success snackbar displayed ===")
        except Exception as ex:
            print(f"=== DEBUG: Error showing success message: {ex} ===")

    def show_error(self, message):
        """Hiển thị thông báo lỗi"""
        print(f"=== DEBUG show_error: {message} ===")
        if not self.page_ref:
            print("=== DEBUG: No page_ref available ===")
            return
        
        try:
            # Tạo snackbar mới
            snack_bar = ft.SnackBar(
                content=ft.Row([
                    ft.Icon(ft.icons.ERROR, color="#FFFFFF", size=20),
                    ft.Text(message, color="#FFFFFF", size=14),
                ], tight=True, spacing=8),
                bgcolor="#EF4444",
                duration=4000,  # Lỗi hiển thị lâu hơn 1 giây
                behavior=ft.SnackBarBehavior.FLOATING,
            )
            
            # Gán và hiển thị
            self.page_ref.snack_bar = snack_bar
            self.page_ref.snack_bar.open = True
            self.page_ref.update()
            print("=== DEBUG: Error snackbar displayed ===")
        except Exception as ex:
            print(f"=== DEBUG: Error showing error message: {ex} ===")
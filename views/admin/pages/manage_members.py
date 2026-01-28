# views/admin/pages/manage_members.py

import flet as ft
from database.db import get_connection
from services.member_service import fetch_all_members, insert_member, update_member
from services.member_service import (
    fetch_all_members,
    insert_member,
    update_member,
)

class ManageMembersPage:
    def __init__(self):
        self.current_member_id = None
        self.page_ref = None

    def set_page(self, page):
        """Set page reference để hiển thị snackbar"""
        self.page_ref = page
    
    def show_success(self, message):
        """Hiển thị thông báo thành công"""
        if self.page_ref:
            self.page_ref.snack_bar = ft.SnackBar(
                content=ft.Text(message, color="#FFFFFF"),
                bgcolor="#10B981",
            )
            self.page_ref.snack_bar.open = True
            self.page_ref.update()
    
    def show_error(self, message):
        """Hiển thị thông báo lỗi"""
        if self.page_ref:
            self.page_ref.snack_bar = ft.SnackBar(
                content=ft.Text(message, color="#FFFFFF"),
                bgcolor="#EF4444",
            )
            self.page_ref.snack_bar.open = True
            self.page_ref.update()
        
    def build(self, page: ft.Page = None):
        if page:
            self.page_ref = page
        content = ft.Column([
            # Header
            ft.Row([
                ft.Text("Member list", size=16, weight=ft.FontWeight.BOLD, color="#1F2937"),
                ft.Container(expand=True),
                ft.ElevatedButton(
                    "+ Add member",
                    bgcolor="#E5E7EB",
                    color="#111827",
                    on_click=self.reset_form,
                ),
            ]),
            
            ft.Text(
                "Card status: Active or Temporarily Locked (usually because of unpaid penalties). Locked members cannot borrow or log in. [web:110][web:136]",
                size=12,
                color="#6B7280",
            ),
            
            ft.Container(height=8),
            
            # Form
            self._build_form(),
            
            # Toolbar
            self._build_toolbar(),
            
            # Table
            self._build_table(),
            
            # Note
            ft.Text(
                "Editing a member here should reflect on their My profile screen, since both use the same set of fields. [web:131][web:120]",
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
            border=ft.Border.all(1, "#E5E7EB"),
        )
        
        return self.main_container
    
    def reset_form(self, e=None):
        """Reset form"""
        self.current_member_id = None
        self.member_id_field.value = ""
        self.fullname_field.value = ""
        self.email_field.value = ""
        self.phone_field.value = ""
        self.gender_field.value = "Select"
        self.address_field.value = ""
        self.card_status_field.value = "Active"
        if e:
            e.page.update()
    
    def edit_member(self, member_data, e):
        """Load dữ liệu member vào form"""
        self.current_member_id = member_data["member_id"]
        self.member_id_field.value = member_data["member_id"]
        self.fullname_field.value = member_data["fullname"]
        self.email_field.value = member_data["email"]
        
        # Xử lý "-" cho phone, gender, address
        self.phone_field.value = "" if member_data["phone"] == "-" else member_data["phone"]
        self.gender_field.value = "Select" if member_data["gender"] == "-" else member_data["gender"]
        self.address_field.value = "" if member_data["address"] == "-" else member_data["address"]
        
        self.card_status_field.value = member_data["status"]
        
        # Update UI
        e.page.update()
    
    def _build_form(self):
        """Form theo thiết kế mới - 2 cột"""
        
        # Fields
        self.member_id_field = ft.TextField(
            hint_text="123",
            border_color="#D1D5DB",
            text_size=13,
            border_radius=6,
            height=40,
            expand=True,
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
            width=600,
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
            width=600,
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
        return ft.Container(
            content=ft.Row([
                ft.TextField(
                    hint_text="Search by Member ID, name or email...",
                    border_radius=999,
                    border_color="#D1D5DB",
                    text_size=14,
                    height=40,
                    expand=True,
                ),
                ft.Dropdown(
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
                ),
                ft.ElevatedButton(
                    "Search",
                    bgcolor="#2563EB",
                    color="#FFFFFF",
                    height=40,
                ),
            ], spacing=8),
            margin=ft.margin.symmetric(vertical=10),  # SỬA: ft.margin thay vì ft.Margin
        )
    def _build_table(self):
        members = fetch_all_members()

        rows = []
        for idx, m in enumerate(members, start=1):
            is_active = m["user_status"] == "ACTIVE"

            rows.append(
                ft.DataRow(cells=[
                    ft.DataCell(ft.Text(str(idx), size=12)),
                    ft.DataCell(ft.Text(m["user_id"], size=12)),
                    ft.DataCell(ft.Text(m["fullname"], size=12)),
                    ft.DataCell(ft.Text(m["email"] or "-", size=12)),
                    ft.DataCell(ft.Text(m["phone"] or "-", size=12)),
                    ft.DataCell(ft.Text(m["gender"] or "-", size=12)),
                    ft.DataCell(ft.Text(m["address"] or "-", size=12, no_wrap=False)),
                    ft.DataCell(
                        ft.Container(
                            content=ft.Text(
                                m["user_status"],
                                size=11,
                                color="#15803D" if is_active else "#B91C1C"
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
                            )
                        ])
                    ),
                ])
            )

        self.table = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("#")),
                ft.DataColumn(ft.Text("MEMBER ID")),
                ft.DataColumn(ft.Text("FULL NAME")),
                ft.DataColumn(ft.Text("EMAIL")),
                ft.DataColumn(ft.Text("PHONE")),
                ft.DataColumn(ft.Text("GENDER")),
                ft.DataColumn(ft.Text("ADDRESS")),
                ft.DataColumn(ft.Text("STATUS")),
                ft.DataColumn(ft.Text("ACTIONS")),
            ],
            rows=rows,
        )

        return ft.Row([self.table], scroll=ft.ScrollMode.AUTO)
    

    def save_member(self, e):
        # Kiểm tra dữ liệu bắt buộc
        if not self.fullname_field.value.strip():
            self.show_error("Full name is required")
            return
        
        if not self.email_field.value.strip():
            self.show_error("Email is required")
            return
        
        try:
            # Chuẩn bị data
            data = {
                "fullname": self.fullname_field.value.strip(),
                "email": self.email_field.value.strip(),
                "phone": self.phone_field.value.strip(),
                "gender": self.gender_field.value if self.gender_field.value != "Select" else "",
                "address": self.address_field.value.strip(),
                "user_status": "ACTIVE" if self.card_status_field.value == "Active" else "LOCKED",
            }
            
            # Nếu có member_id (đang edit)
            if self.current_member_id:
                data["user_id"] = self.current_member_id
                try:
                    update_member(data)
                    self.show_success("Member updated successfully")
                    self.reset_form(e)
                    self.refresh_table()
                except Exception as ex:
                    print(f"Error updating member: {ex}")
                    self.show_error(f"Error updating member: {str(ex)}")
            else:
                # Thêm mới
                try:
                    member_id = insert_member(data)
                    self.show_success(f"Member added successfully (ID: {member_id})")
                    self.reset_form(e)
                    self.refresh_table()
                except Exception as ex:
                    print(f"Error inserting member: {ex}")
                    self.show_error(f"Error adding member: {str(ex)}")
                    
        except Exception as ex:
            print(f"Unexpected error in save_member: {ex}")
            import traceback
            traceback.print_exc()
            self.show_error(f"Unexpected error: {str(ex)}")


    def reload_table(self, page):
        self.table_container.controls.clear()

        members = fetch_all_members()
        rows = []

        for idx, m in enumerate(members, start=1):
            is_active = m["status"] == "Active"

            rows.append(
                ft.DataRow(cells=[
                    ft.DataCell(ft.Text(str(idx))),
                    ft.DataCell(ft.Text(m["member_id"])),
                    ft.DataCell(ft.Text(m["fullname"])),
                    ft.DataCell(ft.Text(m["email"])),
                    ft.DataCell(ft.Text(m["phone"])),
                    ft.DataCell(ft.Text(m["gender"])),
                    ft.DataCell(ft.Text(m["address"], no_wrap=False)),
                    ft.DataCell(
                        ft.Container(
                            content=ft.Text(
                                m["status"],
                                color="#15803D" if is_active else "#B91C1C",
                                size=11
                            ),
                            bgcolor="#DCFCE7" if is_active else "#FEE2E2",
                            padding=ft.Padding(8, 4, 8, 4),
                            border_radius=4,
                        )
                    ),
                    ft.DataCell(
                        ft.Row([
                            ft.ElevatedButton(
                                "Edit",
                                on_click=lambda e, mem=m: self.edit_member(mem, e)
                            ),
                            ft.ElevatedButton(
                                "Lock" if is_active else "Unlock",
                                bgcolor="#EF4444" if is_active else "#6B7280",
                                on_click=lambda e, mid=m["member_id"], s=is_active:
                                    self.toggle_status(mid, s, e)
                            )
                        ])
                    )
                ])
            )

        self.table_container.controls.append(
            ft.DataTable(columns=self.columns, rows=rows)
        )
        page.update()
    def edit_member(self, m, e):
        self.current_member_id = m["user_id"]

        self.member_id_field.value = m["user_id"]
        self.fullname_field.value = m["fullname"]
        self.email_field.value = m["email"] or ""
        self.phone_field.value = m["phone"] or ""
        self.gender_field.value = m["gender"] or "Select"
        self.address_field.value = m["address"] or ""
        self.card_status_field.value = "Active" if m["user_status"] == "ACTIVE" else "Temporarily Locked"

        e.page.update()
    def refresh_table(self):
        """Đơn giản chỉ update page để reload toàn bộ"""
        if self.page_ref:
            self.page_ref.update()
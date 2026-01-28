# views/admin/pages/manage_members.py
import flet as ft


class ManageMembersPage:
    def __init__(self):
        self.current_member_id = None
        
    def build(self):
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
            padding=ft.Padding(14, 14, 16, 16),
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
            margin=ft.Margin(0, 10, 0, 10),
        )
    
    def _build_table(self):
        """Table với scroll ngang"""
        members = [
            {
                "number": "1",
                "member_id": "123",
                "fullname": "Nguyen Van A",
                "email": "memberA@example.com",
                "phone": "0901234567",
                "gender": "Male",
                "address": "123 Le Loi, District 1, HCMC",
                "status": "Temporarily Locked",
            },
            {
                "number": "2",
                "member_id": "124",
                "fullname": "Tran Thi B",
                "email": "memberB@example.com",
                "phone": "0912345678",
                "gender": "Female",
                "address": "456 Nguyen Hue, District 1, HCMC",
                "status": "Active",
            },
            {
                "number": "3",
                "member_id": "125",
                "fullname": "Le Van C",
                "email": "memberC@example.com",
                "phone": "0923456789",
                "gender": "Male",
                "address": "789 Tran Hung Dao, District 5, HCMC",
                "status": "Active",
            },
        ]
        
        rows = []
        for member in members:
            is_active = member["status"] == "Active"
            
            # Buttons dựa vào status
            action_buttons = []
            action_buttons.append(
                ft.ElevatedButton(
                    "Edit", 
                    bgcolor="#3B82F6", 
                    color="#FFFFFF", 
                    height=36,
                    on_click=lambda e, m=member: self.edit_member(m, e),
                    style=ft.ButtonStyle(
                        shape=ft.RoundedRectangleBorder(radius=20),
                        padding=ft.Padding(24, 0, 24, 0),
                    ),
                )
            )
            
            if is_active:
                action_buttons.append(
                    ft.ElevatedButton(
                        "Lock", 
                        bgcolor="#EF4444", 
                        color="#FFFFFF", 
                        height=36,
                        style=ft.ButtonStyle(
                            shape=ft.RoundedRectangleBorder(radius=20),
                            padding=ft.Padding(24, 0, 24, 0),
                        ),
                    )
                )
            else:
                action_buttons.append(
                    ft.ElevatedButton(
                        "Unlock", 
                        bgcolor="#6B7280", 
                        color="#FFFFFF", 
                        height=36,
                        style=ft.ButtonStyle(
                            shape=ft.RoundedRectangleBorder(radius=20),
                            padding=ft.Padding(24, 0, 24, 0),
                        ),
                    )
                )
            
            rows.append(
                ft.DataRow(cells=[
                    # Number
                    ft.DataCell(ft.Text(member["number"], size=12, color="#374151")),
                    # Member ID
                    ft.DataCell(ft.Text(member["member_id"], size=12, color="#374151")),
                    # Full name
                    ft.DataCell(ft.Text(member["fullname"], size=12, color="#374151")),
                    # Email
                    ft.DataCell(ft.Text(member["email"], size=12, color="#374151")),
                    # Phone
                    ft.DataCell(ft.Text(member["phone"], size=12, color="#374151")),
                    # Gender
                    ft.DataCell(ft.Text(member["gender"], size=12, color="#374151")),
                    # Address
                    ft.DataCell(ft.Text(member["address"], size=12, color="#374151", no_wrap=False)),
                    # Status
                    ft.DataCell(
                        ft.Container(
                            content=ft.Text(
                                member["status"], 
                                size=11, 
                                color="#15803D" if is_active else "#B91C1C",
                                weight=ft.FontWeight.W_500
                            ),
                            bgcolor="#DCFCE7" if is_active else "#FEE2E2",
                            padding=ft.Padding(10, 4, 10, 4),
                            border_radius=4,
                        )
                    ),
                    # Actions
                    ft.DataCell(
                        ft.Row(action_buttons, spacing=8)
                    ),
                ])
            )
        
        table = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("#", size=11, color="#9CA3AF", weight=ft.FontWeight.W_600)),
                ft.DataColumn(ft.Text("MEMBER ID", size=11, color="#9CA3AF", weight=ft.FontWeight.W_600)),
                ft.DataColumn(ft.Text("FULL NAME", size=11, color="#9CA3AF", weight=ft.FontWeight.W_600)),
                ft.DataColumn(ft.Text("EMAIL", size=11, color="#9CA3AF", weight=ft.FontWeight.W_600)),
                ft.DataColumn(ft.Text("PHONE", size=11, color="#9CA3AF", weight=ft.FontWeight.W_600)),
                ft.DataColumn(ft.Text("GENDER", size=11, color="#9CA3AF", weight=ft.FontWeight.W_600)),
                ft.DataColumn(ft.Text("ADDRESS", size=11, color="#9CA3AF", weight=ft.FontWeight.W_600)),
                ft.DataColumn(ft.Text("STATUS", size=11, color="#9CA3AF", weight=ft.FontWeight.W_600)),
                ft.DataColumn(ft.Text("ACTIONS", size=11, color="#9CA3AF", weight=ft.FontWeight.W_600)),
            ],
            rows=rows,
            horizontal_lines=ft.BorderSide(1, "#E5E7EB"),
            heading_row_height=36,
            data_row_min_height=56,
            column_spacing=20,
        )
        
        return ft.Row(
            [table],
            scroll=ft.ScrollMode.AUTO,
        )
    
    def save_member(self, e):
        """Save member"""
        print(f"Save member: {self.member_id_field.value} - {self.fullname_field.value}")
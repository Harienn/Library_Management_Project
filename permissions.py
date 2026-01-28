# permissions.py

PERMISSIONS = {
    # ===== GUEST & MEMBER =====
    "home": "GUEST",
    "books": "GUEST",
    "instruction": "GUEST",
    "my_borrowing": "MEMBER",
    "my_profile": "MEMBER",

    # ===== LIBRARIAN (có tất cả quyền Member + thêm) =====
    "dashboard": "LIBRARIAN",
    "manage_books": "LIBRARIAN",
    "manage_members": "LIBRARIAN",
    "borrow_return": "LIBRARIAN",
    "view_fines": "LIBRARIAN",
    "reports": "LIBRARIAN",

    # ===== ADMIN ONLY (có tất cả quyền Librarian + thêm) =====
    "manage_librarians": "ADMIN",
}
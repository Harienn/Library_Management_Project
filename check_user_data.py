# check_user_data.py
from database.db import fetch_all, fetch_one

# Thay YOUR_USER_ID bằng ID user bạn đang login
# Kiểm tra trong database xem user_id của bạn là bao nhiêu
user_id = 2  # Thử với user_id = 2 (hoặc thử 1, 3, 4...)

print("=== Checking Tables ===")
tables = fetch_all("SHOW TABLES")
print("Available tables:", tables)

print("\n=== User Info ===")
try:
    # Thử cả chữ hoa và chữ thường
    user = fetch_one("SELECT * FROM USERS WHERE user_id = %s", (user_id,))
    if not user:
        user = fetch_one("SELECT * FROM users WHERE user_id = %s", (user_id,))
    print(user)
except Exception as e:
    print(f"Error: {e}")

print("\n=== Current Borrowing ===")
try:
    borrowing = fetch_all("""
        SELECT 
            bt.*,
            b.title as book_title
        FROM BORROWING_TRANSACTION bt
        LEFT JOIN BORROWING_TRANSACTION_DETAILS btd ON bt.transaction_id = btd.transaction_id
        LEFT JOIN BOOKS b ON btd.book_id = b.book_id
        WHERE bt.member_id = %s AND bt.borrower_status = 'BORROWED'
    """, (user_id,))
    print(f"Found {len(borrowing)} borrowed books")
    for b in borrowing:
        print(f"  - {b}")
except Exception as e:
    print(f"Error: {e}")

print("\n=== History ===")
try:
    history = fetch_all("""
        SELECT 
            bt.*,
            b.title as book_title
        FROM BORROWING_TRANSACTION bt
        LEFT JOIN BORROWING_TRANSACTION_DETAILS btd ON bt.transaction_id = btd.transaction_id
        LEFT JOIN BOOKS b ON btd.book_id = b.book_id
        WHERE bt.member_id = %s AND bt.borrower_status IN ('RETURNED', 'LOST')
    """, (user_id,))
    print(f"Found {len(history)} history records")
    for h in history:
        print(f"  - {h}")
except Exception as e:
    print(f"Error: {e}")
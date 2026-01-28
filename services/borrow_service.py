# services/borrow_service.py
"""
Borrow Service - COMPLETE VERSION
✅ All functions ready to use
✅ Check eligibility + Execute borrow
✅ Fine debt checking
✅ Max borrowing limit checking
✅ Extend borrowing support
"""
from database.db import execute, fetch_one, fetch_all, get_connection
from datetime import date, timedelta


def check_borrow_eligibility(member_id, book_id):
    """
    ✅ Kiểm tra chi tiết điều kiện mượn sách
    
    Returns:
        (can_borrow: bool, reason: str, details: dict)
        
    Possible reasons:
    - "OK" : Có thể mượn
    - "PROFILE_INCOMPLETE" : Chưa điền đủ thông tin
    - "HAS_FINES" : Đang nợ phạt
    - "MAX_BOOKS" : Đã mượn tối đa 10 cuốn
    - "BOOK_NOT_AVAILABLE" : Sách không khả dụng
    - "REFERENCE_ONLY" : Sách chỉ đọc tại chỗ
    - "ACCOUNT_BLOCKED" : Tài khoản bị khóa
    """
    try:
        # 1. Kiểm tra thông tin user
        user_info = fetch_one(
            """
            SELECT 
                user_id, fullname, phone, gender, address, 
                status, totalFineDebt
            FROM USERS 
            WHERE user_id = %s
            """,
            (member_id,)
        )
        
        if not user_info:
            return False, "User not found", {}
        
        # 2. Kiểm tra account status
        if user_info.get('status') == 'BLOCKED':
            return False, "ACCOUNT_BLOCKED", {
                'message': 'Your account is blocked. Please contact the library.'
            }
        
        # 3. Kiểm tra profile hoàn thiện
        missing_fields = []
        if not user_info.get('fullname') or not user_info['fullname'].strip():
            missing_fields.append('Full name')
        if not user_info.get('phone') or not user_info['phone'].strip():
            missing_fields.append('Phone number')
        if not user_info.get('gender'):
            missing_fields.append('Gender')
        if not user_info.get('address') or not user_info['address'].strip():
            missing_fields.append('Address')
        
        if missing_fields:
            return False, "PROFILE_INCOMPLETE", {
                'missing_fields': missing_fields,
                'message': f'Please complete your profile: {", ".join(missing_fields)}'
            }
        
        # 4. Kiểm tra nợ phạt
        total_fine_debt = user_info.get('totalFineDebt', 0) or 0
        if total_fine_debt > 0:
            fines_detail = get_member_fines(member_id)
            return False, "HAS_FINES", {
                'total_fine_debt': total_fine_debt,
                'overdue_fines': fines_detail.get('overdue_fines', 0),
                'damage_fines': fines_detail.get('damage_fines', 0),
                'lost_fines': fines_detail.get('lost_fines', 0),
                'message': f'You have unpaid fines: {total_fine_debt:,.0f} VND. Please pay to continue borrowing.'
            }
        
        # 5. Kiểm tra số lượng sách đang mượn
        current_borrowed = fetch_one(
            """
            SELECT COUNT(*) as count 
            FROM BORROWING_TRANSACTION bt
            JOIN BORROWING_TRANSACTION_DETAILS btd ON bt.transaction_id = btd.transaction_id
            WHERE bt.member_id = %s AND bt.borrower_status IN ('BORROWED', 'OVERDUE')
            """,
            (member_id,)
        )
        
        borrowed_count = current_borrowed.get('count', 0) if current_borrowed else 0
        
        if borrowed_count >= 10:
            return False, "MAX_BOOKS", {
                'current_borrowed': borrowed_count,
                'max_allowed': 10,
                'message': 'You have reached the maximum borrowing limit (10 books). Please return books to continue borrowing.'
            }
        
        # 6. Kiểm tra sách
        book = fetch_one(
            """
            SELECT 
                book_id, title, available_copies, 
                is_reference_only, book_status, author_id
            FROM BOOKS 
            WHERE book_id = %s
            """,
            (book_id,)
        )
        
        if not book:
            return False, "BOOK_NOT_FOUND", {
                'message': 'Book not found'
            }
        
        if book.get('is_reference_only'):
            return False, "REFERENCE_ONLY", {
                'book_title': book.get('title'),
                'message': 'This is a reference-only book. Cannot be borrowed.'
            }
        
        if book.get('available_copies', 0) <= 0:
            return False, "BOOK_NOT_AVAILABLE", {
                'book_title': book.get('title'),
                'message': 'This book is currently not available.'
            }
        
        # ✅ Tất cả điều kiện đều OK
        return True, "OK", {
            'user_name': user_info.get('fullname'),
            'book_title': book.get('title'),
            'current_borrowed': borrowed_count,
            'borrow_period': 15,  # days
            'message': 'You can borrow this book.'
        }
        
    except Exception as e:
        print(f"❌ Error checking borrow eligibility: {e}")
        import traceback
        traceback.print_exc()
        return False, "ERROR", {
            'message': f'System error: {str(e)}'
        }


def borrow_book(member_id, book_id):
    """
    ✅ Mượn sách - Trả về transaction_id để hiển thị confirmation
    
    Returns:
        (success: bool, message: str, transaction_id: int)
    """
    try:
        # Kiểm tra điều kiện trước
        can_borrow, reason, details = check_borrow_eligibility(member_id, book_id)
        
        if not can_borrow:
            return False, details.get('message', reason), None
        
        # Lấy thông tin book
        book = fetch_one(
            "SELECT book_id, title FROM BOOKS WHERE book_id = %s",
            (book_id,)
        )
        
        if not book:
            return False, "Book not found", None
        
        # Tạo transaction
        borrow_date = date.today()
        due_date = borrow_date + timedelta(days=15)
        
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute(
            """
            INSERT INTO BORROWING_TRANSACTION 
            (member_id, borrow_date, due_date, borrower_status, renew_week_count)
            VALUES (%s, %s, %s, 'BORROWED', 0)
            """,
            (member_id, borrow_date, due_date)
        )
        
        transaction_id = cursor.lastrowid
        
        # Insert transaction detail
        cursor.execute(
            """
            INSERT INTO BORROWING_TRANSACTION_DETAILS 
            (transaction_id, book_id, item_status)
            VALUES (%s, %s, 'BORROWED')
            """,
            (transaction_id, book_id)
        )
        
        # Update book availability
        cursor.execute(
            """
            UPDATE BOOKS
            SET available_copies = available_copies - 1
            WHERE book_id = %s
            """,
            (book_id,)
        )
        
        conn.commit()
        cursor.close()
        conn.close()
        
        print(f"✅ Book borrowed successfully! Transaction ID: {transaction_id}")
        
        return True, "Book borrowed successfully!", transaction_id
        
    except Exception as e:
        print(f"❌ Error in borrow_book: {e}")
        import traceback
        traceback.print_exc()
        return False, f"Error: {str(e)}", None


def sync_user_total_fine_debt(member_id):
    """🔄 SYNC: Đồng bộ totalFineDebt trong USERS table với FINE table"""
    try:
        fines = get_member_fines(member_id)
        total_unpaid = fines['total_unpaid_fines']
        
        update_query = """
        UPDATE USERS 
        SET totalFineDebt = %s
        WHERE user_id = %s
        """
        execute(update_query, (total_unpaid, member_id))
        
        print(f"✅ Synced totalFineDebt for user {member_id}: {total_unpaid:,.0f} VND")
        return True
        
    except Exception as e:
        print(f"❌ Error syncing totalFineDebt: {e}")
        return False


def get_member_fines(member_id):
    """Lấy chi tiết fines của member"""
    try:
        query = """
        SELECT 
            fr.violation_type,
            f.fine_status,
            SUM(f.amount) as total_amount
        FROM FINE f
        JOIN BORROWING_TRANSACTION_DETAILS btd ON f.transaction_detail_id = btd.transaction_detail_id
        JOIN BORROWING_TRANSACTION bt ON btd.transaction_id = bt.transaction_id
        JOIN FINE_RULES fr ON f.rule_id = fr.rule_id
        WHERE bt.member_id = %s
        GROUP BY fr.violation_type, f.fine_status
        """
        
        results = fetch_all(query, (member_id,))
        
        overdue_unpaid = 0
        damage_unpaid = 0
        lost_unpaid = 0
        total_unpaid = 0
        
        for record in results:
            violation_type = record.get('violation_type')
            amount = record.get('total_amount') or 0
            status = record.get('fine_status')
            
            if status == 'UNPAID':
                if violation_type == 'OVERDUE':
                    overdue_unpaid += amount
                elif violation_type == 'DAMAGED':
                    damage_unpaid += amount
                elif violation_type == 'LOST':
                    lost_unpaid += amount
                total_unpaid += amount
        
        result = {
            'overdue_fines': overdue_unpaid,
            'damage_fines': damage_unpaid,
            'lost_fines': lost_unpaid,
            'total_unpaid_fines': total_unpaid,
            'has_unpaid': total_unpaid > 0,
        }
        
        return result
        
    except Exception as e:
        print(f"❌ Error in get_member_fines: {e}")
        return {
            'overdue_fines': 0,
            'damage_fines': 0,
            'lost_fines': 0,
            'total_unpaid_fines': 0,
            'has_unpaid': False
        }


def get_member_borrowing(member_id):
    """Lấy danh sách sách đang mượn của member"""
    try:
        query = """
        SELECT 
            bt.transaction_id,
            bt.member_id,
            b.book_id,
            b.title as book_title,
            b.image_url,
            a.author_name,
            bt.borrow_date,
            bt.due_date,
            bt.borrower_status,
            bt.renew_week_count,
            btd.item_status,
            GREATEST(0, DATEDIFF(CURRENT_DATE, bt.due_date)) AS days_overdue,
            CASE 
                WHEN CURRENT_DATE > bt.due_date THEN GREATEST(0, DATEDIFF(CURRENT_DATE, bt.due_date)) * 20000
                ELSE 0
            END AS overdue_fine
        FROM BORROWING_TRANSACTION bt
        JOIN BORROWING_TRANSACTION_DETAILS btd ON bt.transaction_id = btd.transaction_id
        JOIN BOOKS b ON btd.book_id = b.book_id
        LEFT JOIN AUTHORS a ON b.author_id = a.author_id
        WHERE bt.member_id = %s AND bt.borrower_status IN ('BORROWED', 'OVERDUE')
        ORDER BY bt.borrow_date DESC
        """
        
        result = fetch_all(query, (member_id,))
        return result if result else []
    except Exception as e:
        print(f"Error in get_member_borrowing: {e}")
        return []


def get_member_stats(member_id):
    """Lấy thống kê member"""
    sync_user_total_fine_debt(member_id)
    
    sql_borrowed = """
        SELECT COUNT(*) as count 
        FROM BORROWING_TRANSACTION bt
        JOIN BORROWING_TRANSACTION_DETAILS btd ON bt.transaction_id = btd.transaction_id
        WHERE bt.member_id = %s AND bt.borrower_status IN ('BORROWED', 'OVERDUE')
    """
    borrowed = fetch_one(sql_borrowed, (member_id,))
    
    fines = get_member_fines(member_id)
    
    sql_overdue = """
        SELECT COUNT(*) as count 
        FROM BORROWING_TRANSACTION 
        WHERE member_id = %s AND borrower_status = 'OVERDUE'
    """
    overdue = fetch_one(sql_overdue, (member_id,))
    
    return {
        'current_borrowed': borrowed['count'] if borrowed else 0,
        'total_unpaid_fines': fines['total_unpaid_fines'],
        'overdue_count': overdue['count'] if overdue else 0
    }


def can_extend_borrowing(transaction_id):
    """Kiểm tra có thể gia hạn không"""
    detail = get_borrowing_detail(transaction_id)
    
    if not detail:
        return False, "Transaction not found"
    
    today = date.today()
    due_date = detail['due_date']
    if isinstance(due_date, str):
        from datetime import datetime
        due_date = datetime.strptime(due_date, '%Y-%m-%d').date()
    
    if today > due_date:
        days_over = (today - due_date).days
        return False, f"Book is overdue by {days_over} days. Please return it first."
    
    max_renews = 2
    renew_count = detail['renew_week_count'] or 0
    
    if renew_count >= max_renews:
        return False, f"Maximum extensions reached ({renew_count}/{max_renews})"
    
    if detail['user_status'] == 'BLOCKED':
        return False, "Your account is blocked. Please contact the library."
    
    total_fine = detail['total_fine_debt'] or 0
    if total_fine > 0:
        return False, f"You have unpaid fines: {total_fine:,.0f} VND. Please pay first."
    
    return True, "OK"


def get_borrowing_detail(transaction_id):
    """Lấy chi tiết borrowing transaction"""
    sql = """
        SELECT 
            bt.transaction_id,
            bt.member_id,
            u.fullname AS member_name,
            b.book_id,
            b.title AS book_title,
            b.isbn,
            a.author_name,
            bt.borrow_date,
            bt.due_date,
            bt.borrower_status,
            bt.renew_week_count,
            DATEDIFF(CURRENT_DATE, bt.due_date) AS days_overdue,
            u.status AS user_status,
            u.totalFineDebt AS total_fine_debt
        FROM BORROWING_TRANSACTION bt
        JOIN USERS u ON bt.member_id = u.user_id
        JOIN BORROWING_TRANSACTION_DETAILS btd ON bt.transaction_id = btd.transaction_id
        JOIN BOOKS b ON btd.book_id = b.book_id
        LEFT JOIN AUTHORS a ON b.author_id = a.author_id
        WHERE bt.transaction_id = %s
    """
    detail = fetch_one(sql, (transaction_id,))
    
    if detail:
        sync_user_total_fine_debt(detail['member_id'])
        detail = fetch_one(sql, (transaction_id,))
    
    return detail


def extend_borrowing(transaction_id, extension_days=15):
    """Thực hiện gia hạn mượn sách"""
    can_extend, reason = can_extend_borrowing(transaction_id)
    
    if not can_extend:
        return False, reason, None
    
    detail = get_borrowing_detail(transaction_id)
    current_due_date = detail['due_date']
    if isinstance(current_due_date, str):
        from datetime import datetime
        current_due_date = datetime.strptime(current_due_date, '%Y-%m-%d').date()
    
    new_due_date = current_due_date + timedelta(days=extension_days)
    
    sql = """
        UPDATE BORROWING_TRANSACTION 
        SET 
            due_date = %s,
            renew_week_count = renew_week_count + 1
        WHERE transaction_id = %s
    """
    
    try:
        execute(sql, (new_due_date, transaction_id))
        return True, "Extension successful!", new_due_date
    except Exception as e:
        print(f"Error in extend_borrowing: {e}")
        return False, f"Database error: {str(e)}", None


def calculate_new_due_date(current_due_date, extension_days=15):
    """
    Tính ngày đến hạn mới sau khi gia hạn
    
    Args:
        current_due_date: Ngày đến hạn hiện tại (date hoặc string)
        extension_days: Số ngày gia hạn (mặc định 15)
    
    Returns:
        date: Ngày đến hạn mới
    """
    from datetime import datetime
    
    # Convert to date if string
    if isinstance(current_due_date, str):
        current_due_date = datetime.strptime(current_due_date, '%Y-%m-%d').date()
    
    # Calculate new due date
    new_due_date = current_due_date + timedelta(days=extension_days)
    
    return new_due_date


def get_member_borrowing_history(member_id):
    """Lấy lịch sử mượn sách của member"""
    try:
        query = """
        SELECT 
            bt.transaction_id,
            b.book_id,
            b.title as book_title,
            bt.borrow_date,
            bt.return_date,
            bt.due_date,
            bt.borrower_status as status,
            btd.transaction_detail_id,
            btd.item_status,
            COALESCE(btd.days_late, 0) as days_late,
            COALESCE(btd.damage_percentage, 0) as damage_percentage,
            COALESCE(
                (SELECT SUM(f2.amount) 
                 FROM FINE f2 
                 WHERE f2.transaction_detail_id = btd.transaction_detail_id),
                0
            ) as fine,
            CASE 
                WHEN EXISTS(
                    SELECT 1 FROM FINE f3 
                    WHERE f3.transaction_detail_id = btd.transaction_detail_id 
                    AND f3.fine_status = 'UNPAID'
                ) THEN 'UNPAID'
                WHEN EXISTS(
                    SELECT 1 FROM FINE f4 
                    WHERE f4.transaction_detail_id = btd.transaction_detail_id 
                    AND f4.fine_status = 'PAID'
                ) THEN 'PAID'
                ELSE 'NONE'
            END as payment_status,
            (SELECT MAX(f5.paid_date) 
             FROM FINE f5 
             WHERE f5.transaction_detail_id = btd.transaction_detail_id
            ) as payment_date
        FROM BORROWING_TRANSACTION bt
        JOIN BORROWING_TRANSACTION_DETAILS btd ON bt.transaction_id = btd.transaction_id
        JOIN BOOKS b ON btd.book_id = b.book_id
        WHERE bt.member_id = %s 
        AND (
            bt.borrower_status IN ('RETURNED', 'LOST', 'DAMAGED')
            OR EXISTS (
                SELECT 1 FROM FINE f 
                WHERE f.transaction_detail_id = btd.transaction_detail_id
            )
        )
        ORDER BY bt.borrow_date DESC
        LIMIT 20
        """
        
        results = fetch_all(query, (member_id,))
        return results if results else []
        
    except Exception as e:
        print(f"❌ Error in get_member_borrowing_history: {e}")
        import traceback
        traceback.print_exc()
        return []
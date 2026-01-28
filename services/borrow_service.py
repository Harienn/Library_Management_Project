# services/borrow_service.py
"""
<<<<<<< HEAD
Borrow Service - Xử lý mượn/trả sách
Bảng: TRANSACTIONS, BOOKS, USERS, FINES
=======
Borrow Service - COMPLETE VERSION
✅ All functions ready to use
✅ Check eligibility + Execute borrow
✅ Fine debt checking
✅ Max borrowing limit checking
✅ Extend borrowing support
>>>>>>> version-2
"""
from database.db import fetch_all, fetch_one, execute
from datetime import datetime, timedelta

# Constants
DEFAULT_BORROW_DAYS = 15
FINE_PER_DAY = 5000  # 5,000 VND per day


<<<<<<< HEAD
def create_borrow_transaction(user_id, book_id, librarian_id=None):
    """
    Tạo giao dịch mượn sách mới
    
    Args:
        user_id: ID của người mượn
        book_id: ID của sách
        librarian_id: ID của thủ thư xử lý (optional)
    
    Returns:
        dict: {'success': bool, 'message': str, 'transaction_id': int}
    """
=======
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
>>>>>>> version-2
    try:
        # 1. Kiểm tra user có active không
        user = fetch_one("SELECT * FROM USERS WHERE user_id = %s", (user_id,))
        if not user:
            return {'success': False, 'message': 'User not found'}
        if user['user_status'] != 'ACTIVE':
            return {'success': False, 'message': 'User account is not active'}
        
        # 2. Kiểm tra sách có available không
        book = fetch_one("SELECT * FROM BOOKS WHERE book_id = %s", (book_id,))
        if not book:
            return {'success': False, 'message': 'Book not found'}
        if book['available_copies'] <= 0:
            return {'success': False, 'message': 'No copies available'}
        if book['book_status'] != 'AVAILABLE':
            return {'success': False, 'message': f'Book is {book["book_status"]}'}
        
        # 3. Kiểm tra user có quá nhiều sách đang mượn không (max 5)
        current_borrows = fetch_one("""
            SELECT COUNT(*) as count 
            FROM TRANSACTIONS 
            WHERE user_id = %s AND transaction_status = 'BORROWED'
        """, (user_id,))
        
<<<<<<< HEAD
        if current_borrows and current_borrows['count'] >= 5:
            return {'success': False, 'message': 'Maximum 5 books can be borrowed at once'}
        
        # 4. Kiểm tra user có nợ phạt không
        if user['totalFineDebt'] > 0:
            return {'success': False, 'message': f'Please pay outstanding fine: {user["totalFineDebt"]:,.0f} VND'}
        
        # 5. Tạo transaction
        borrow_date = datetime.now().date()
        due_date = borrow_date + timedelta(days=DEFAULT_BORROW_DAYS)
        
        sql = """
            INSERT INTO TRANSACTIONS (
                user_id, book_id, borrow_date, due_date, 
                transaction_status, librarian_id
            )
            VALUES (%s, %s, %s, %s, 'BORROWED', %s)
        """
        
        execute(sql, (user_id, book_id, borrow_date, due_date, librarian_id))
        
        # 6. Lấy transaction_id vừa tạo
        result = fetch_one("SELECT LAST_INSERT_ID() as transaction_id")
        transaction_id = result['transaction_id'] if result else None
        
        # 7. Giảm available_copies (trigger sẽ tự động làm, nhưng để chắc chắn)
        execute("""
            UPDATE BOOKS 
            SET available_copies = available_copies - 1 
            WHERE book_id = %s
        """, (book_id,))
        
        return {
            'success': True, 
            'message': 'Book borrowed successfully',
            'transaction_id': transaction_id
        }
        
    except Exception as e:
        print(f"❌ Error creating borrow transaction: {e}")
        return {'success': False, 'message': str(e)}


def return_book(transaction_id):
    """
    Trả sách
    
    Args:
        transaction_id: ID của transaction
    
    Returns:
        dict: {'success': bool, 'message': str, 'fine_amount': float}
    """
    try:
        # 1. Lấy thông tin transaction
        transaction = fetch_one("""
            SELECT * FROM TRANSACTIONS WHERE transaction_id = %s
        """, (transaction_id,))
        
        if not transaction:
            return {'success': False, 'message': 'Transaction not found', 'fine_amount': 0}
        
        if transaction['transaction_status'] != 'BORROWED':
            return {'success': False, 'message': 'Book is not currently borrowed', 'fine_amount': 0}
        
        # 2. Cập nhật transaction
        return_date = datetime.now().date()
        
        execute("""
            UPDATE TRANSACTIONS 
            SET return_date = %s, transaction_status = 'RETURNED'
            WHERE transaction_id = %s
        """, (return_date, transaction_id))
        
        # 3. Tăng available_copies (trigger sẽ tự động làm)
        execute("""
            UPDATE BOOKS 
            SET available_copies = available_copies + 1 
            WHERE book_id = %s
        """, (transaction['book_id'],))
        
        # 4. Tính phạt nếu quá hạn
        fine_amount = 0
        if return_date > transaction['due_date']:
            days_overdue = (return_date - transaction['due_date']).days
            fine_amount = days_overdue * FINE_PER_DAY
            
            # Cập nhật fine_amount trong transaction
            execute("""
                UPDATE TRANSACTIONS 
                SET fine_amount = %s 
                WHERE transaction_id = %s
            """, (fine_amount, transaction_id))
            
            # Tạo fine record
            execute("""
                INSERT INTO FINES (
                    transaction_id, user_id, fine_amount, 
                    fine_reason, fine_status
                )
                VALUES (%s, %s, %s, %s, 'UNPAID')
            """, (
                transaction_id, 
                transaction['user_id'], 
                fine_amount,
                f'Overdue {days_overdue} days ({FINE_PER_DAY:,.0f} VND/day)'
            ))
            
            # Cập nhật totalFineDebt của user
            execute("""
                UPDATE USERS 
                SET totalFineDebt = totalFineDebt + %s
                WHERE user_id = %s
            """, (fine_amount, transaction['user_id']))
        
        return {
            'success': True, 
            'message': 'Book returned successfully',
            'fine_amount': fine_amount
        }
        
    except Exception as e:
        print(f"❌ Error returning book: {e}")
        return {'success': False, 'message': str(e), 'fine_amount': 0}


def get_user_transactions(user_id, status=None):
    """
    Lấy danh sách transactions của user
    
    Args:
        user_id: ID của user
        status: Lọc theo status (BORROWED, RETURNED, OVERDUE) - optional
    
    Returns:
        list: Danh sách transactions
    """
    where_clause = "WHERE t.user_id = %s"
    params = [user_id]
    
    if status:
        where_clause += " AND t.transaction_status = %s"
        params.append(status)
    
    sql = f"""
        SELECT 
            t.transaction_id,
            t.user_id,
            t.book_id,
            b.title,
            b.author,
            b.cover_image_url,
            t.borrow_date,
            t.due_date,
            t.return_date,
            t.transaction_status,
            t.fine_amount,
            CASE 
                WHEN t.transaction_status = 'BORROWED' AND t.due_date < CURDATE() THEN 'OVERDUE'
                ELSE t.transaction_status
            END as display_status,
            CASE
                WHEN t.transaction_status = 'BORROWED' AND t.due_date < CURDATE() 
                THEN DATEDIFF(CURDATE(), t.due_date)
                ELSE 0
            END as days_overdue
        FROM TRANSACTIONS t
        JOIN BOOKS b ON t.book_id = b.book_id
        {where_clause}
        ORDER BY t.borrow_date DESC
    """
    
    return fetch_all(sql, tuple(params))


def get_all_active_transactions():
    """
    Lấy tất cả transactions đang active (cho librarian/admin)
    
    Returns:
        list: Danh sách transactions đang mượn
    """
    sql = """
        SELECT 
            t.transaction_id,
            t.user_id,
            u.fullname as member_name,
            u.email,
            u.phone,
            t.book_id,
            b.title,
            b.author,
            t.borrow_date,
            t.due_date,
            t.transaction_status,
            CASE 
                WHEN t.due_date < CURDATE() THEN 'OVERDUE'
                ELSE 'BORROWED'
            END as display_status,
            CASE
                WHEN t.due_date < CURDATE() 
                THEN DATEDIFF(CURDATE(), t.due_date)
                ELSE 0
            END as days_overdue,
            CASE
                WHEN t.due_date < CURDATE() 
                THEN DATEDIFF(CURDATE(), t.due_date) * %s
                ELSE 0
            END as estimated_fine
        FROM TRANSACTIONS t
        JOIN USERS u ON t.user_id = u.user_id
        JOIN BOOKS b ON t.book_id = b.book_id
        WHERE t.transaction_status = 'BORROWED'
        ORDER BY t.due_date ASC
    """
    
    return fetch_all(sql, (FINE_PER_DAY,))


def get_overdue_transactions():
    """
    Lấy danh sách transactions quá hạn
    
    Returns:
        list: Danh sách transactions quá hạn
    """
    sql = """
        SELECT 
            t.transaction_id,
            t.user_id,
            u.fullname as member_name,
            u.email,
            u.phone,
            t.book_id,
            b.title,
            b.author,
            t.borrow_date,
            t.due_date,
            DATEDIFF(CURDATE(), t.due_date) as days_overdue,
            DATEDIFF(CURDATE(), t.due_date) * %s as estimated_fine
        FROM TRANSACTIONS t
        JOIN USERS u ON t.user_id = u.user_id
        JOIN BOOKS b ON t.book_id = b.book_id
        WHERE t.transaction_status = 'BORROWED'
        AND t.due_date < CURDATE()
        ORDER BY days_overdue DESC
    """
    
    return fetch_all(sql, (FINE_PER_DAY,))


def get_user_fines(user_id, status=None):
    """
    Lấy danh sách phạt của user
    
    Args:
        user_id: ID của user
        status: Lọc theo status (UNPAID, PAID, WAIVED) - optional
    
    Returns:
        list: Danh sách fines
    """
    where_clause = "WHERE f.user_id = %s"
    params = [user_id]
    
    if status:
        where_clause += " AND f.fine_status = %s"
        params.append(status)
    
    sql = f"""
        SELECT 
            f.fine_id,
            f.transaction_id,
            f.fine_amount,
            f.fine_reason,
            f.fine_status,
            f.paid_date,
            f.created_at,
            t.borrow_date,
            t.due_date,
            t.return_date,
            b.title as book_title,
            b.author
        FROM FINES f
        JOIN TRANSACTIONS t ON f.transaction_id = t.transaction_id
        JOIN BOOKS b ON t.book_id = b.book_id
        {where_clause}
        ORDER BY f.created_at DESC
    """
    
    return fetch_all(sql, tuple(params))


def pay_fine(fine_id):
    """
    Thanh toán phạt
    
    Args:
        fine_id: ID của fine
    
    Returns:
        dict: {'success': bool, 'message': str}
    """
    try:
        # Lấy thông tin fine
        fine = fetch_one("SELECT * FROM FINES WHERE fine_id = %s", (fine_id,))
        
        if not fine:
            return {'success': False, 'message': 'Fine not found'}
        
        if fine['fine_status'] == 'PAID':
            return {'success': False, 'message': 'Fine already paid'}
        
        # Cập nhật fine status
        execute("""
            UPDATE FINES 
            SET fine_status = 'PAID', paid_date = CURDATE()
            WHERE fine_id = %s
        """, (fine_id,))
        
        # Giảm totalFineDebt của user
        execute("""
            UPDATE USERS 
            SET totalFineDebt = totalFineDebt - %s
            WHERE user_id = %s
        """, (fine['fine_amount'], fine['user_id']))
        
        return {'success': True, 'message': 'Fine paid successfully'}
        
    except Exception as e:
        print(f"❌ Error paying fine: {e}")
        return {'success': False, 'message': str(e)}


def get_dashboard_stats():
    """
    Lấy thống kê cho dashboard
    
    Returns:
        dict: Các số liệu thống kê
    """
    today = datetime.now().date()
    
    # Transactions today
    transactions_today = fetch_one("""
=======
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
>>>>>>> version-2
        SELECT COUNT(*) as count 
        FROM TRANSACTIONS 
        WHERE DATE(created_at) = %s
    """, (today,))
    
<<<<<<< HEAD
    # Books on loan
    books_on_loan = fetch_one("""
=======
    fines = get_member_fines(member_id)
    
    sql_overdue = """
>>>>>>> version-2
        SELECT COUNT(*) as count 
        FROM TRANSACTIONS 
        WHERE transaction_status = 'BORROWED'
    """, ())
    
    # Overdue today
    overdue_today = fetch_one("""
        SELECT COUNT(*) as count 
        FROM TRANSACTIONS 
        WHERE transaction_status = 'BORROWED'
        AND due_date < %s
    """, (today,))
    
    # Fines collected today
    fines_today = fetch_one("""
        SELECT COALESCE(SUM(fine_amount), 0) as total
        FROM FINES
        WHERE fine_status = 'PAID'
        AND DATE(paid_date) = %s
    """, (today,))
    
    return {
<<<<<<< HEAD
        'transactions_today': transactions_today['count'] if transactions_today else 0,
        'books_on_loan': books_on_loan['count'] if books_on_loan else 0,
        'overdue_today': overdue_today['count'] if overdue_today else 0,
        'fines_today': fines_today['total'] if fines_today else 0
    }
=======
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
>>>>>>> version-2

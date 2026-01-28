# services/borrow_service.py
"""
Borrow Service - Xử lý mượn/trả sách
Bảng: TRANSACTIONS, BOOKS, USERS, FINES
"""
from database.db import fetch_all, fetch_one, execute
from datetime import datetime, timedelta

# Constants
DEFAULT_BORROW_DAYS = 15
FINE_PER_DAY = 5000  # 5,000 VND per day


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
        SELECT COUNT(*) as count 
        FROM TRANSACTIONS 
        WHERE DATE(created_at) = %s
    """, (today,))
    
    # Books on loan
    books_on_loan = fetch_one("""
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
        'transactions_today': transactions_today['count'] if transactions_today else 0,
        'books_on_loan': books_on_loan['count'] if books_on_loan else 0,
        'overdue_today': overdue_today['count'] if overdue_today else 0,
        'fines_today': fines_today['total'] if fines_today else 0
    }
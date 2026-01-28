# services/borrow_service.py
"""
Borrow Service - FIXED VERSION
✅ ĐỒNG BỘ totalFineDebt với FINE table
✅ Single source of truth cho fine calculations
✅ Debug logging
"""
from database.db import execute, fetch_one, fetch_all, get_connection
from datetime import date, timedelta


def sync_user_total_fine_debt(member_id):
    """
    🔄 SYNC: Đồng bộ totalFineDebt trong USERS table với FINE table
    """
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


def get_member_borrowing(member_id):
    """
    Lấy danh sách sách đang mượn của member
    """
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


def get_member_borrowing_history(member_id):
    """
    FIX: Lấy lịch sử mượn sách với breakdown đầy đủ
    ✅ Hiển thị TẤT CẢ transactions có fines (kể cả đang mượn)
    """
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
            
            -- Tính toán fines từ FINE table
            COALESCE(
                (SELECT SUM(f2.amount) 
                 FROM FINE f2 
                 WHERE f2.transaction_detail_id = btd.transaction_detail_id),
                0
            ) as fine,
            
            -- Payment status
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
            
            -- Payment date (latest)
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
        
        if results:
            print(f"📊 History records found: {len(results)}")
            for r in results[:3]:
                print(f"  - Transaction {r['transaction_id']}: Fine={r['fine']:,.0f}, Status={r['payment_status']}")
        
        return results if results else []
        
    except Exception as e:
        print(f"❌ Error in get_member_borrowing_history: {e}")
        import traceback
        traceback.print_exc()
        return []


def get_member_fines(member_id):
    """
    FIX: Lấy thông tin phạt breakdown từ FINE table (single source of truth)
    """
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
        
        print(f"\n📋 Fine breakdown for member {member_id}:")
        for r in results:
            print(f"  - {r['violation_type']}: {r['total_amount']:,.0f} VND ({r['fine_status']})")
        
        overdue_unpaid = 0
        damage_unpaid = 0
        lost_unpaid = 0
        total_unpaid = 0
        
        overdue_paid = 0
        damage_paid = 0
        lost_paid = 0
        
        for record in results:
            violation_type = record['violation_type']
            amount = record['total_amount'] or 0
            status = record['fine_status']
            
            if status == 'UNPAID':
                if violation_type == 'OVERDUE':
                    overdue_unpaid += amount
                elif violation_type == 'DAMAGED':
                    damage_unpaid += amount
                elif violation_type == 'LOST':
                    lost_unpaid += amount
                total_unpaid += amount
            elif status == 'PAID':
                if violation_type == 'OVERDUE':
                    overdue_paid += amount
                elif violation_type == 'DAMAGED':
                    damage_paid += amount
                elif violation_type == 'LOST':
                    lost_paid += amount
        
        result = {
            'overdue_fines': overdue_unpaid,
            'damage_fines': damage_unpaid,
            'lost_fines': lost_unpaid,
            'total_unpaid_fines': total_unpaid,
            'has_unpaid': total_unpaid > 0,
            'overdue_paid': overdue_paid,
            'damage_paid': damage_paid,
            'lost_paid': lost_paid,
        }
        
        print(f"💰 Total unpaid fines: {total_unpaid:,.0f} VND")
        
        return result
        
    except Exception as e:
        print(f"❌ Error in get_member_fines: {e}")
        import traceback
        traceback.print_exc()
        return {
            'overdue_fines': 0,
            'damage_fines': 0,
            'lost_fines': 0,
            'total_unpaid_fines': 0,
            'has_unpaid': False
        }


def get_fine_notification(member_id):
    """
    FIX: Lấy thông tin chi tiết notification - Sync trước khi hiển thị
    """
    try:
        # 🔄 SYNC totalFineDebt trước
        sync_user_total_fine_debt(member_id)
        
        # Lấy thông tin member
        member_query = """
        SELECT user_id, fullname, totalFineDebt, status
        FROM USERS
        WHERE user_id = %s
        """
        member = fetch_one(member_query, (member_id,))
        
        if not member:
            return None
        
        # Lấy chi tiết phạt từ FINE table
        fines = get_member_fines(member_id)
        
        result = {
            'member_id': member['user_id'],
            'member_name': member['fullname'],
            'account_status': member['status'],
            'overdue_fines': fines['overdue_fines'],
            'damage_fines': fines['damage_fines'],
            'lost_fines': fines['lost_fines'],
            'total_unpaid_fines': fines['total_unpaid_fines'],
            'has_unpaid': fines['has_unpaid'],
            'is_blocked': member['status'] == 'BLOCKED'
        }
        
        print(f"\n📢 Fine notification for {member['fullname']}:")
        print(f"   - Overdue: {result['overdue_fines']:,.0f} VND")
        print(f"   - Damage: {result['damage_fines']:,.0f} VND")
        print(f"   - Lost: {result['lost_fines']:,.0f} VND")
        print(f"   - TOTAL: {result['total_unpaid_fines']:,.0f} VND\n")
        
        return result
        
    except Exception as e:
        print(f"❌ Error in get_fine_notification: {e}")
        import traceback
        traceback.print_exc()
        return None


def get_member_stats(member_id):
    """
    FIX: Lấy thống kê - Sync trước khi lấy
    """
    # 🔄 Sync trước
    sync_user_total_fine_debt(member_id)
    
    # Số sách đang mượn
    sql_borrowed = """
        SELECT COUNT(*) as count 
        FROM BORROWING_TRANSACTION bt
        JOIN BORROWING_TRANSACTION_DETAILS btd ON bt.transaction_id = btd.transaction_id
        WHERE bt.member_id = %s AND bt.borrower_status IN ('BORROWED', 'OVERDUE')
    """
    borrowed = fetch_one(sql_borrowed, (member_id,))
    
    # Tổng phí phạt - LẤY TỪ FINE table
    fines = get_member_fines(member_id)
    
    # Số sách quá hạn
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


def get_borrowing_detail(transaction_id):
    """
    FIX: Lấy chi tiết - Sync total_fine_debt từ FINE table
    """
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
    
    # 🔄 Sync để đảm bảo total_fine_debt chính xác
    if detail:
        sync_user_total_fine_debt(detail['member_id'])
        # Lấy lại sau khi sync
        detail = fetch_one(sql, (transaction_id,))
    
    return detail


def can_extend_borrowing(transaction_id):
    """
    FIX: Kiểm tra - Sử dụng total_fine_debt đã được sync
    """
    detail = get_borrowing_detail(transaction_id)
    
    if not detail:
        return False, "Transaction not found"
    
    # Điều kiện 1: Sách chưa quá hạn
    today = date.today()
    due_date = detail['due_date']
    if isinstance(due_date, str):
        from datetime import datetime
        due_date = datetime.strptime(due_date, '%Y-%m-%d').date()
    
    if today > due_date:
        days_over = (today - due_date).days
        return False, f"Book is overdue by {days_over} days. Please return it first."
    
    # Điều kiện 2: Chưa vượt số lần gia hạn
    max_renews = 2
    renew_count = detail['renew_week_count'] or 0
    
    if renew_count >= max_renews:
        return False, f"Maximum extensions reached ({renew_count}/{max_renews})"
    
    # Điều kiện 3: Tài khoản không bị khóa
    if detail['user_status'] == 'BLOCKED':
        return False, "Your account is blocked. Please contact the library."
    
    # Điều kiện 4: Không có phí phạt chưa thanh toán (đã được sync)
    total_fine = detail['total_fine_debt'] or 0
    if total_fine > 0:
        return False, f"You have unpaid fines: {total_fine:,.0f} VND. Please pay first."
    
    return True, "OK"


def extend_borrowing(transaction_id, extension_days=15):
    """
    Thực hiện gia hạn mượn sách
    """
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
    Tính toán due_date mới sau khi gia hạn
    """
    from datetime import datetime
    if isinstance(current_due_date, str):
        current_due_date = datetime.strptime(current_due_date, '%Y-%m-%d').date()
    
    return current_due_date + timedelta(days=extension_days)


def borrow_book(member_id, book_id):
    """
    Cho phép member mượn sách
    ✅ YÊU CẦU: Member phải điền đầy đủ thông tin cá nhân
    """
    try:
        # ✅ 0. KIỂM TRA THÔNG TIN CÁ NHÂN ĐẦY ĐỦ
        user_info = fetch_one(
            """
            SELECT fullname, phone, gender, address 
            FROM USERS 
            WHERE user_id = %s
            """,
            (member_id,)
        )
        
        if not user_info:
            return False, "User not found"
        
        # Kiểm tra các trường bắt buộc
        if not user_info.get('fullname') or not user_info['fullname'].strip():
            return False, "Please complete your profile: Full name is required"
        
        if not user_info.get('phone') or not user_info['phone'].strip():
            return False, "Please complete your profile: Phone number is required"
        
        if not user_info.get('gender'):
            return False, "Please complete your profile: Gender is required"
        
        if not user_info.get('address') or not user_info['address'].strip():
            return False, "Please complete your profile: Address is required"
        
        print(f"✅ User {member_id} profile is complete")
        
        # 1. Kiểm tra sách còn không
        book = fetch_one(
            "SELECT book_id, available_copies, is_reference_only FROM BOOKS WHERE book_id = %s",
            (book_id,)
        )

        if not book:
            return False, "Book not found"
        
        if book.get("is_reference_only"):
            return False, "This is a reference-only book"
        
        if book["available_copies"] <= 0:
            return False, "Book is not available"

        # 2. Kiểm tra member đã mượn tối đa chưa (10 cuốn)
        current_borrowed = fetch_one(
            """
            SELECT COUNT(*) as count 
            FROM BORROWING_TRANSACTION bt
            JOIN BORROWING_TRANSACTION_DETAILS btd ON bt.transaction_id = btd.transaction_id
            WHERE bt.member_id = %s AND bt.borrower_status = 'BORROWED'
            """,
            (member_id,)
        )
        
        if current_borrowed and current_borrowed["count"] >= 10:
            return False, "You have reached the maximum borrowing limit (10 books)"

        # 3. Tạo transaction
        borrow_date = date.today()
        due_date = borrow_date + timedelta(days=15)
        
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute(
            """
            INSERT INTO BORROWING_TRANSACTION (member_id, borrow_date, due_date, borrower_status, renew_week_count)
            VALUES (%s, %s, %s, 'BORROWED', 0)
            """,
            (member_id, borrow_date, due_date)
        )
        
        transaction_id = cursor.lastrowid
        
        # Insert transaction detail
        cursor.execute(
            """
            INSERT INTO BORROWING_TRANSACTION_DETAILS (transaction_id, book_id, item_status)
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
        
        return True, "Book borrowed successfully!"

    except Exception as e:
        print(f"Error in borrow_book: {e}")
        return False, f"Error: {str(e)}"
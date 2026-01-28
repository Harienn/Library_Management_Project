# services/book_service.py
"""
Book Service - Tương thích với database LibraryDB
Bảng: BOOKS, AUTHORS, CATEGORIES, BORROWING_TRANSACTION, BORROWING_TRANSACTION_DETAILS
"""
from database.db import fetch_all, fetch_one, execute_query

def search_books(keyword=None, category_id=None, publish_year=None, status=None, 
                 page=1, per_page=15):
    """
    Tìm kiếm và lọc sách với pagination
    
    Args:
        keyword: Tìm theo title, author, ISBN
        category_id: Lọc theo category
        publish_year: Lọc theo năm xuất bản  
        status: Lọc theo trạng thái (AVAILABLE, BORROWED)
        page: Trang hiện tại
        per_page: Số sách mỗi trang
    
    Returns:
        dict: {
            'books': [...],
            'total': int,
            'page': int,
            'per_page': int,
            'total_pages': int
        }
    """
    
    # Build WHERE conditions
    conditions = []
    params = []
    
    if keyword:
        conditions.append("(b.title LIKE %s OR b.isbn LIKE %s OR a.author_name LIKE %s)")
        keyword_param = f"%{keyword}%"
        params.extend([keyword_param, keyword_param, keyword_param])
    
    if category_id and category_id != "All":
        conditions.append("b.category_id = %s")
        params.append(int(category_id))
    
    if publish_year and publish_year != "All":
        conditions.append("b.publish_date = %s")
        params.append(int(publish_year))
    
    if status and status != "All":
        if status == "AVAILABLE":
            conditions.append("b.available_copies > 0")
        elif status == "BORROWED":
            conditions.append("b.available_copies = 0")
    
    # Build WHERE clause
    where_clause = " AND ".join(conditions) if conditions else "1=1"
    
    # Count total
    count_sql = f"""
        SELECT COUNT(*) as total
        FROM BOOKS b
        LEFT JOIN AUTHORS a ON b.author_id = a.author_id
        WHERE {where_clause}
    """
    total_result = fetch_one(count_sql, tuple(params))
    total = total_result['total'] if total_result else 0
    
    # Calculate pagination
    total_pages = (total + per_page - 1) // per_page if total > 0 else 1
    offset = (page - 1) * per_page
    
    # Get books
    books_sql = f"""
        SELECT 
            b.book_id,
            b.title,
            b.isbn,
            b.author_id,
            a.author_name,
            b.category_id,
            c.category_name,
            b.publish_date,
            b.total_copies,
            b.available_copies,
            b.is_reference_only,
            b.publisher,
            b.summary,
            b.image_url,
            b.price,
            b.book_status,
            CASE 
                WHEN b.available_copies > 0 THEN 'AVAILABLE'
                ELSE 'BORROWED'
            END AS availability_status
        FROM BOOKS b
        LEFT JOIN AUTHORS a ON b.author_id = a.author_id
        LEFT JOIN CATEGORIES c ON b.category_id = c.category_id
        WHERE {where_clause}
        ORDER BY b.book_id DESC
        LIMIT %s OFFSET %s
    """
    
    params.extend([per_page, offset])
    books = fetch_all(books_sql, tuple(params))
    
    return {
        'books': books,
        'total': total,
        'page': page,
        'per_page': per_page,
        'total_pages': total_pages
    }


def get_all_categories():
    """Lấy tất cả categories để fill vào dropdown"""
    sql = "SELECT category_id, category_name FROM CATEGORIES ORDER BY category_name"
    return fetch_all(sql)


def get_all_publish_years():
    """Lấy tất cả năm xuất bản để fill vào dropdown"""
    sql = """
        SELECT DISTINCT publish_date 
        FROM BOOKS 
        WHERE publish_date IS NOT NULL 
        ORDER BY publish_date DESC
    """
    result = fetch_all(sql)
    return [str(row['publish_date']) for row in result]


def get_book_detail(book_id):
    """Lấy chi tiết một cuốn sách"""
    sql = """
        SELECT 
            b.*,
            a.author_name,
            a.biography AS author_bio,
            c.category_name,
            CASE 
                WHEN b.available_copies > 0 THEN 'AVAILABLE'
                ELSE 'BORROWED'
            END AS availability_status
        FROM BOOKS b
        LEFT JOIN AUTHORS a ON b.author_id = a.author_id
        LEFT JOIN CATEGORIES c ON b.category_id = c.category_id
        WHERE b.book_id = %s
    """
    return fetch_one(sql, (book_id,))


def check_book_availability(book_id):
    """
    Kiểm tra xem sách có sẵn để mượn không
    Returns: (is_available: bool, message: str)
    """
    book = get_book_detail(book_id)
    
    if not book:
        return False, "Book not found"
    
    if book['is_reference_only']:
        return False, "This is a reference-only book and cannot be borrowed"
    
    if book['available_copies'] <= 0:
        return False, "All copies are currently borrowed"
    
    return True, "Book is available"


def get_member_current_borrow_count(member_id):
    """Đếm số sách member đang mượn"""
    sql = """
        SELECT COUNT(*) as count
        FROM BORROWING_TRANSACTION bt
        JOIN BORROWING_TRANSACTION_DETAILS btd ON bt.transaction_id = btd.transaction_id
        WHERE bt.member_id = %s AND bt.borrower_status = 'BORROWED'
    """
    result = fetch_one(sql, (member_id,))
    return result['count'] if result else 0
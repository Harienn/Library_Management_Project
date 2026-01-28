# services/book_service.py
"""
Book Service - Tương thích với database LibraryDB
Bảng: BOOKS, AUTHORS, CATEGORIES, BORROWING_TRANSACTION, BORROWING_TRANSACTION_DETAILS
"""
from database.db import fetch_all, fetch_one, execute_query,execute, get_connection



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

def search_books_action(self, e):
        self.keyword = e.control.parent.controls[0].value
        self.refresh_table() 
def delete_book_by_isbn(isbn):
        sql = "DELETE FROM BOOKS WHERE isbn = %s"
        execute_query(sql, (isbn,))
def get_book_by_isbn(isbn):
    sql = "SELECT book_id FROM BOOKS WHERE isbn = %s"
    return fetch_one(sql, (isbn,))
def insert_book(data: dict):
        """
        Insert book với xử lý author và category
        
        data cần có:
        - author: tên tác giả (string)
        - category: tên thể loại (string)
        - Các trường khác...
        """
        
        # 1. Get or create author
        author_name = data.get("author", "").strip()
        if not author_name:
            author_id = None
        else:
            # Tìm hoặc tạo author
            author = fetch_one("SELECT author_id FROM AUTHORS WHERE author_name = %s", (author_name,))
            if author:
                author_id = author['author_id']
            else:
                # Tạo author mới
                execute_query("INSERT INTO AUTHORS (author_name) VALUES (%s)", (author_name,))
                author_id = get_last_insert_id()
        
        # 2. Get or create category
        category_name = data.get("category", "").strip()
        if not category_name:
            category_id = None
        else:
            # Tìm hoặc tạo category
            category = fetch_one("SELECT category_id FROM CATEGORIES WHERE category_name = %s", (category_name,))
            if category:
                category_id = category['category_id']
            else:
                # Tạo category mới
                execute_query("INSERT INTO CATEGORIES (category_name) VALUES (%s)", (category_name,))
                category_id = get_last_insert_id()
        
        # 3. Prepare other data
        isbn = data.get("isbn", "").strip()
        title = data.get("title", "").strip()
        publisher = data.get("publisher", "").strip()
        
        # Xử lý năm xuất bản
        publish_year = data.get("publish_year", "").strip()
        publish_date = int(publish_year) if publish_year and publish_year.isdigit() else None
        
        # Xử lý số lượng
        try:
            total_copies = int(data.get("total", "1"))
        except:
            total_copies = 1
        
        try:
            available_copies = int(data.get("available", total_copies))
        except:
            available_copies = total_copies
        
        # Xử lý giá
        try:
            price = float(data.get("price", "0").replace(".", "").replace(",", ""))
        except:
            price = 0
        
        # Xử lý summary
        summary = data.get("summary", "").strip()
        
        # Xử lý image_url
        image_url = data.get("cover_url", "").strip()
        
        # Xử lý status
        status_str = data.get("status", "Available").strip()
        book_status = "AVAILABLE" if status_str == "Available" else "NOT_AVAILABLE"
        
        # 4. Insert vào database
        sql = """
            INSERT INTO BOOKS 
            (isbn, title, author_id, category_id, publisher,
            publish_date, total_copies, available_copies, 
            price, summary, image_url, book_status)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        
        execute_query(sql, (
            isbn,
            title,
            author_id,
            category_id,
            publisher,
            publish_date,
            total_copies,
            available_copies,
            price,
            summary,
            image_url,
            book_status
        ))
        
        return get_last_insert_id()


def update_book(data: dict):
    """
    Update book với xử lý author và category
    data cần có:
    - isbn: ISBN của sách cần update
    - author: tên tác giả (string)
    - category: tên thể loại (string)
    """
    
    isbn = data.get("isbn", "").strip()
    if not isbn:
        return False
    
    # 1. Get or create author
    author_name = data.get("author", "").strip()
    if not author_name:
        author_id = None
    else:
        author = fetch_one("SELECT author_id FROM AUTHORS WHERE author_name = %s", (author_name,))
        if author:
            author_id = author['author_id']
        else:
            execute_query("INSERT INTO AUTHORS (author_name) VALUES (%s)", (author_name,))
            author_id = get_last_insert_id()
    
    # 2. Get or create category
    category_name = data.get("category", "").strip()
    if not category_name:
        category_id = None
    else:
        category = fetch_one("SELECT category_id FROM CATEGORIES WHERE category_name = %s", (category_name,))
        if category:
            category_id = category['category_id']
        else:
            execute_query("INSERT INTO CATEGORIES (category_name) VALUES (%s)", (category_name,))
            category_id = get_last_insert_id()
    
    # 3. Prepare other data
    title = data.get("title", "").strip()
    publisher = data.get("publisher", "").strip()
    
    # Xử lý năm xuất bản
    publish_year = data.get("publish_year", "").strip()
    publish_date = int(publish_year) if publish_year and publish_year.isdigit() else None
    
    # Xử lý số lượng
    try:
        total_copies = int(data.get("total", "1"))
    except:
        total_copies = 1
    
    try:
        available_copies = int(data.get("available", total_copies))
    except:
        available_copies = total_copies
    
    # Xử lý giá
    try:
        price = float(data.get("price", "0").replace(".", "").replace(",", ""))
    except:
        price = 0
    
    # Xử lý summary
    summary = data.get("summary", "").strip()
    
    # Xử lý image_url
    image_url = data.get("cover_url", "").strip()
    
    # Xử lý status
    status_str = data.get("status", "Available").strip()
    book_status = "AVAILABLE" if status_str == "Available" else "NOT_AVAILABLE"
    
    # 4. Update database
    sql = """
        UPDATE BOOKS SET
            title = %s,
            author_id = %s,
            category_id = %s,
            publisher = %s,
            publish_date = %s,
            total_copies = %s,
            available_copies = %s,
            price = %s,
            summary = %s,
            image_url = %s,
            book_status = %s
        WHERE isbn = %s
    """
    
    execute_query(sql, (
        title,
        author_id,
        category_id,
        publisher,
        publish_date,
        total_copies,
        available_copies,
        price,
        summary,
        image_url,
        book_status,
        isbn
    ))
    
    return True
def get_last_insert_id():
        result = fetch_one("SELECT LAST_INSERT_ID() AS id")
        return result["id"] if result else None
def get_or_create_author(name):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute(
        "SELECT author_id FROM authors WHERE name = %s",
        (name,)
    )
    row = cursor.fetchone()

    if row:
        return row["author_id"]

    cursor.execute(
        "INSERT INTO authors (name) VALUES (%s)",
        (name,)
    )
    conn.commit()
    return cursor.lastrowid
def get_or_create_category(name):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute(
        "SELECT category_id FROM categories WHERE name = %s",
        (name,)
    )
    row = cursor.fetchone()

    if row:
        return row["category_id"]

    cursor.execute(
        "INSERT INTO categories (name) VALUES (%s)",
        (name,)
    )
    conn.commit()
    return cursor.lastrowid


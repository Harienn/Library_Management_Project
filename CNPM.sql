-- Tạo cơ sở dữ liệu
CREATE DATABASE IF NOT EXISTS LibraryDB;
USE LibraryDB;

-- 1. Bảng USERS (Người dùng) - ĐÃ SỬA THEO DATA MODEL
CREATE TABLE USERS (
    user_id INT PRIMARY KEY AUTO_INCREMENT,
    fullname VARCHAR(30) NOT NULL,
    password VARCHAR(55) NOT NULL, -- ĐÃ SỬA: 55 thay vì 255
    created_at DATE NOT NULL,
    status VARCHAR(55) NOT NULL, -- ĐÃ SỬA: theo data model
    address VARCHAR(50),
    phone VARCHAR(20),
    email VARCHAR(50) UNIQUE NOT NULL,
    role_name VARCHAR(30) NOT NULL,
    gender VARCHAR(30),
    user_status VARCHAR(50) DEFAULT 'ACTIVE', -- Thêm cột user_status
    totalFineDebt DOUBLE DEFAULT 0, -- ĐÃ SỬA: đúng tên data model
    CONSTRAINT chk_role CHECK (role_name IN ('MEMBER', 'LIBRARIAN', 'ADMIN'))
);

-- 2. Bảng CATEGORIES (Thể loại sách)
CREATE TABLE CATEGORIES (
    category_id INT PRIMARY KEY AUTO_INCREMENT,
    category_name VARCHAR(30) UNIQUE NOT NULL
);

-- 3. Bảng AUTHORS (Tác giả)
CREATE TABLE AUTHORS (
    author_id INT PRIMARY KEY AUTO_INCREMENT,
    author_name VARCHAR(50) NOT NULL,
    biography TEXT
);

-- 4. Bảng BOOKS (Sách) - ĐÃ SỬA THEO DATA MODEL
CREATE TABLE BOOKS (
    book_id INT PRIMARY KEY AUTO_INCREMENT,
    title VARCHAR(50) NOT NULL,
    isbn VARCHAR(50) UNIQUE NOT NULL, -- ĐÃ SỬA: 50 thay vì 55
    author_id INT,
    category_id INT,
    publish_date INT, -- ĐÃ SỬA: publish_date thay vì publish_year
    total_copies INT NOT NULL DEFAULT 1,
    available_copies INT NOT NULL DEFAULT 0,
    is_reference_only BOOLEAN DEFAULT FALSE,
    publisher VARCHAR(30),
    summary TEXT,
    image_url TEXT,
    price FLOAT, -- ĐÃ SỬA: FLOAT thay vì DECIMAL
    book_status VARCHAR(20) DEFAULT 'AVAILABLE',
    FOREIGN KEY (category_id) REFERENCES CATEGORIES(category_id),
    FOREIGN KEY (author_id) REFERENCES AUTHORS(author_id)
);

-- 5. Bảng BORROWING_TRANSACTION (Giao dịch mượn) - ĐÃ SỬA THEO DATA MODEL
CREATE TABLE BORROWING_TRANSACTION (
    transaction_id INT PRIMARY KEY AUTO_INCREMENT,
    member_id INT NOT NULL,
    librarian_id INT, -- ĐÃ THÊM: theo data model
    borrow_date DATE NOT NULL,
    due_date DATE NOT NULL,
    return_date DATE,
    borrower_status VARCHAR(100) DEFAULT 'BORROWED', -- ĐÃ SỬA: borrower_status
    renew_week_count INT DEFAULT 0, -- ĐÃ SỬA: renew_week_count
    FOREIGN KEY (member_id) REFERENCES USERS(user_id),
    FOREIGN KEY (librarian_id) REFERENCES USERS(user_id)
);

-- 6. Bảng BORROWING_TRANSACTION_DETAILS (Chi tiết giao dịch mượn) - ĐÃ SỬA
CREATE TABLE BORROWING_TRANSACTION_DETAILS (
    transaction_detail_id INT PRIMARY KEY AUTO_INCREMENT,
    transaction_id INT NOT NULL,
    book_id INT NOT NULL,
    item_status VARCHAR(50) DEFAULT 'BORROWED',
    damage_precentage FLOAT DEFAULT 0, -- ĐÃ SỬA: đúng chính tả theo data model
    days_late INT DEFAULT 0,
    FOREIGN KEY (transaction_id) REFERENCES BORROWING_TRANSACTION(transaction_id),
    FOREIGN KEY (book_id) REFERENCES BOOKS(book_id)
);

-- 7. Bảng FINE_RULES (Quy tắc phạt) - ĐÃ SỬA THEO DATA MODEL
CREATE TABLE FINE_RULES (
    rule_id INT PRIMARY KEY AUTO_INCREMENT,
    violation_type VARCHAR(50) UNIQUE NOT NULL,
    lost_book_fine DECIMAL(10,2) NOT NULL,
    damage_rate FLOAT NOT NULL,
    overdue_rate DECIMAL(10,2) NOT NULL,
    max_late_penalty DECIMAL(10,2),
    is_active BOOLEAN DEFAULT TRUE
);

-- 8. Bảng FINE (Phạt) - ĐÃ SỬA THEO DATA MODEL
CREATE TABLE FINE (
    fine_id INT PRIMARY KEY AUTO_INCREMENT,
    rule_id INT NOT NULL,
    transaction_detail_id INT NOT NULL,
    fine_status VARCHAR(100) DEFAULT 'UNPAID',
    amount FLOAT NOT NULL,
    paid_date DATE,  -- Ngày thanh toán
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,  -- Ngày tạo
    FOREIGN KEY (rule_id) REFERENCES FINE_RULES(rule_id),
    FOREIGN KEY (transaction_detail_id) REFERENCES BORROWING_TRANSACTION_DETAILS(transaction_detail_id)
);


-- ==============================================
-- CHÈN DỮ LIỆU MẪU - ĐÃ ĐIỀU CHỈNH
-- ==============================================

-- 1. Chèn dữ liệu vào bảng CATEGORIES
INSERT INTO CATEGORIES (category_name) VALUES
('Văn học Việt Nam'),
('Văn học nước ngoài'),
('Khoa học'),
('Lịch sử'),
('Kinh tế'),
('Kỹ năng sống'),
('Công nghệ thông tin'),
('Tiểu thuyết'),
('Truyện ngắn'),
('Thơ');

-- 2. Chèn dữ liệu vào bảng AUTHORS
INSERT INTO AUTHORS (author_name, biography) VALUES
('Nguyễn Nhật Ánh', 'Nhà văn nổi tiếng Việt Nam với các tác phẩm cho tuổi mới lớn'),
('Nam Cao', 'Nhà văn hiện thực phê phán Việt Nam'),
('Haruki Murakami', 'Nhà văn Nhật Bản nổi tiếng thế giới'),
('Paulo Coelho', 'Nhà văn Brazil với tác phẩm nổi tiếng Nhà giả kim'),
('Stephen Hawking', 'Nhà vật lý lý thuyết, vũ trụ học người Anh'),
('Dale Carnegie', 'Tác giả nổi tiếng về sách kỹ năng sống'),
('Ngô Tất Tố', 'Nhà văn, nhà báo, học giả Việt Nam'),
('Tô Hoài', 'Nhà văn nổi tiếng với tác phẩm Dế Mèn phiêu lưu ký'),
('J.K. Rowling', 'Nhà văn Anh, tác giả bộ truyện Harry Potter'),
('Nguyễn Du', 'Đại thi hào dân tộc Việt Nam'),
('Trần Đăng Khoa', 'Nhà thơ thần đồng Việt Nam'),
('Nguyễn Ngọc Tư', 'Nhà văn nữ đương đại Việt Nam'),
('Adam Khoo', 'Tác giả, diễn giả người Singapore về phát triển bản thân'),
('Robert Kiyosaki', 'Tác giả nổi tiếng với bộ sách Dạy con làm giàu'),
('Nguyễn Phong', 'Tác giả về công nghệ thông tin');

-- 3. Chèn dữ liệu vào bảng USERS - ĐÃ ĐIỀU CHỈNH
INSERT INTO USERS (fullname, password, created_at, status, address, phone, email, role_name, gender, user_status, totalFineDebt) VALUES
('Nguyễn Văn A', 'hashed_password_1', '2023-01-15', 'ACTIVE', 'Hà Nội', '0912345678', 'nguyenvana@email.com', 'MEMBER', 'Nam', 'ACTIVE', 0),
('Trần Thị B', 'hashed_password_2', '2023-02-20', 'ACTIVE', 'TP HCM', '0923456789', 'tranthib@email.com', 'MEMBER', 'Nữ', 'ACTIVE', 0),
('Lê Văn C', 'hashed_password_3', '2023-03-10', 'ACTIVE', 'Đà Nẵng', '0934567890', 'levanc@email.com', 'MEMBER', 'Nam', 'ACTIVE', 0),
('Phạm Thị D', 'hashed_password_4', '2023-01-05', 'ACTIVE', 'Hải Phòng', '0945678901', 'phamthid@email.com', 'LIBRARIAN', 'Nữ', 'ACTIVE', 0),
('Hoàng Văn E', 'hashed_password_5', '2023-02-28', 'ACTIVE', 'Cần Thơ', '0956789012', 'hoangvane@email.com', 'ADMIN', 'Nam', 'ACTIVE', 0),
('Vũ Thị F', 'hashed_password_6', '2023-04-01', 'ACTIVE', 'Nghệ An', '0967890123', 'vuthif@email.com', 'MEMBER', 'Nữ', 'ACTIVE', 0),
('Đặng Văn G', 'hashed_password_7', '2023-03-15', 'BLOCKED', 'Thanh Hóa', '0978901234', 'dangvang@email.com', 'MEMBER', 'Nam', 'ACTIVE', 0),
('Bùi Thị H', 'hashed_password_8', '2023-02-10', 'ACTIVE', 'Quảng Ninh', '0989012345', 'buithih@email.com', 'MEMBER', 'Nữ', 'ACTIVE', 0),
('Đỗ Văn I', 'hashed_password_9', '2023-01-25', 'ACTIVE', 'Bình Dương', '0990123456', 'dovanii@email.com', 'LIBRARIAN', 'Nam', 'ACTIVE', 0),
('Ngô Thị K', 'hashed_password_10', '2023-04-05', 'ACTIVE', 'Đồng Nai', '0901234567', 'ngothik@email.com', 'MEMBER', 'Nữ', 'ACTIVE', 0);

-- 4. Chèn dữ liệu vào bảng BOOKS (20 cuốn sách) - ĐÃ ĐIỀU CHỈNH
INSERT INTO BOOKS (title, isbn, author_id, category_id, publish_date, total_copies, available_copies, is_reference_only, publisher, summary, price, book_status) VALUES
('Tôi thấy hoa vàng trên cỏ xanh', '978-604-2-12345-6', 1, 1, 2010, 5, 4, FALSE, 'NXB Trẻ', 'Câu chuyện về tuổi thơ ở miền quê Việt Nam', 85000, 'AVAILABLE'),
('Cho tôi xin một vé đi tuổi thơ', '978-604-1-23456-7', 1, 1, 2008, 3, 2, FALSE, 'NXB Trẻ', 'Hồi ức về tuổi thơ đầy mộng mơ', 90000, 'AVAILABLE'),
('Chí Phèo', '978-604-1-34567-8', 2, 1, 1941, 4, 3, FALSE, 'NXB Văn học', 'Tác phẩm kinh điển về người nông dân', 65000, 'AVAILABLE'),
('Rừng Na Uy', '978-604-1-45678-9', 3, 2, 1987, 2, 1, FALSE, 'NXB Hội Nhà văn', 'Tiểu thuyết về tình yêu và sự cô đơn', 120000, 'AVAILABLE'),
('Nhà giả kim', '978-604-1-56789-0', 4, 2, 1988, 6, 5, FALSE, 'NXB Văn hóa', 'Hành trình tìm kiếm ý nghĩa cuộc sống', 95000, 'AVAILABLE'),
('Lược sử thời gian', '978-604-1-67890-1', 5, 3, 1988, 3, 2, TRUE, 'NXB Khoa học', 'Khám phá vũ trụ và các lý thuyết vật lý', 150000, 'AVAILABLE'),
('Đắc nhân tâm', '978-604-1-78901-2', 6, 6, 1936, 8, 6, FALSE, 'NXB Tổng hợp', 'Nghệ thuật thu phục lòng người', 80000, 'AVAILABLE'),
('Tắt đèn', '978-604-1-89012-3', 7, 1, 1939, 4, 3, FALSE, 'NXB Văn học', 'Cuộc sống người nông dân trước cách mạng', 75000, 'AVAILABLE'),
('Dế Mèn phiêu lưu ký', '978-604-1-90123-4', 8, 1, 1941, 5, 4, FALSE, 'NXB Kim Đồng', 'Câu chuyện phiêu lưu của chú dế mèn', 60000, 'AVAILABLE'),
('Harry Potter và Hòn đá phù thủy', '978-604-1-01234-5', 9, 2, 1997, 4, 2, FALSE, 'NXB Trẻ', 'Cuộc phiêu lưu đầu tiên của Harry Potter', 110000, 'AVAILABLE'),
('Truyện Kiều', '978-604-2-11223-3', 10, 10, 1820, 3, 2, TRUE, 'NXB Văn học', 'Kiệt tác văn học dân tộc', 70000, 'AVAILABLE'),
('Góc sân và khoảng trời', '978-604-2-22334-4', 11, 10, 1968, 2, 1, FALSE, 'NXB Kim Đồng', 'Tập thơ của thần đồng thơ ca', 55000, 'AVAILABLE'),
('Cánh đồng bất tận', '978-604-2-33445-5', 12, 1, 2005, 3, 2, FALSE, 'NXB Trẻ', 'Tập truyện ngắn đương đại', 85000, 'AVAILABLE'),
('Tôi tài giỏi, bạn cũng thế', '978-604-2-44556-6', 13, 6, 1998, 5, 4, FALSE, 'NXB Phụ nữ', 'Phương pháp học tập hiệu quả', 100000, 'AVAILABLE'),
('Dạy con làm giàu tập 1', '978-604-2-55667-7', 14, 5, 1997, 4, 3, FALSE, 'NXB Trẻ', 'Kiến thức tài chính cơ bản', 90000, 'AVAILABLE'),
('Lập trình Java cơ bản', '978-604-2-66778-8', 15, 7, 2015, 3, 2, TRUE, 'NXB Khoa học kỹ thuật', 'Giáo trình lập trình Java', 120000, 'AVAILABLE'),
('1Q84', '978-604-2-77889-9', 3, 8, 2009, 2, 1, FALSE, 'NXB Hội Nhà văn', 'Tiểu thuyết giả tưởng đồ sộ', 180000, 'AVAILABLE'),
('Những người khốn khổ', '978-604-2-88990-0', NULL, 2, 1862, 2, 1, TRUE, 'NXB Văn học', 'Kiệt tác văn học thế giới', 130000, 'AVAILABLE'),
('Đi tìm lẽ sống', '978-604-2-99001-1', NULL, 6, 1946, 3, 2, FALSE, 'NXB Tổng hợp', 'Câu chuyện về ý nghĩa cuộc sống', 85000, 'AVAILABLE'),
('Clean Code', '978-604-3-00112-2', NULL, 7, 2008, 2, 1, TRUE, 'NXB Khoa học kỹ thuật', 'Nghệ thuật viết code sạch', 160000, 'AVAILABLE');

-- 5. Chèn dữ liệu vào bảng FINE_RULES
INSERT INTO FINE_RULES (violation_type, lost_book_fine, damage_rate, overdue_rate, max_late_penalty, is_active) VALUES
('OVERDUE', 0, 0, 20000, 200000, TRUE),
('DAMAGED', 0, 0.3, 0, NULL, TRUE),
('LOST', 1.0, 0, 0, NULL, TRUE);

-- 6. Chèn dữ liệu vào bảng BORROWING_TRANSACTION - ĐÃ ĐIỀU CHỈNH
INSERT INTO BORROWING_TRANSACTION (member_id, librarian_id, borrow_date, due_date, return_date, borrower_status, renew_week_count) VALUES
(1, 4, '2024-01-10', '2024-01-24', '2024-01-23', 'RETURNED', 0),
(1, 9, '2024-02-15', '2024-03-01', NULL, 'BORROWED', 1),
(2, 4, '2024-02-20', '2024-03-05', '2024-03-10', 'OVERDUE', 0),
(3, 9, '2024-03-01', '2024-03-15', NULL, 'BORROWED', 0),
(6, 4, '2024-02-28', '2024-03-13', NULL, 'BORROWED', 0),
(8, 9, '2024-03-05', '2024-03-19', NULL, 'BORROWED', 0);

-- 7. Chèn dữ liệu vào bảng BORROWING_TRANSACTION_DETAILS - ĐÃ ĐIỀU CHỈNH
INSERT INTO BORROWING_TRANSACTION_DETAILS (transaction_id, book_id, item_status, damage_precentage, days_late) VALUES
(1, 1, 'RETURNED', 0, 0),
(1, 3, 'RETURNED', 5, 0),
(2, 5, 'BORROWED', 0, 0),
(2, 8, 'BORROWED', 0, 0),
(3, 7, 'RETURNED', 0, 5),
(4, 10, 'BORROWED', 0, 0),
(4, 12, 'BORROWED', 0, 0),
(5, 14, 'BORROWED', 0, 0),
(6, 17, 'BORROWED', 0, 0);

-- 8. Chèn dữ liệu vào bảng FINE - ĐÃ ĐIỀU CHỈNH
INSERT INTO FINE (rule_id, transaction_detail_id, fine_status, amount, paid_date) VALUES
(1, 5, 'PAID', 100000, '2024-03-11'),
(1, 1, 'UNPAID', 0, NULL),
(2, 2, 'PAID', 19500, '2024-01-24');

-- 9. Cập nhật tổng nợ phạt cho người dùng
UPDATE USERS SET totalFineDebt = 100000 WHERE user_id = 2;

-- 10. Cập nhật số bản sách có sẵn
UPDATE BOOKS b
SET available_copies = b.total_copies - COALESCE(
    (SELECT COUNT(*) 
     FROM BORROWING_TRANSACTION_DETAILS btd
     JOIN BORROWING_TRANSACTION bt ON btd.transaction_id = bt.transaction_id
     WHERE btd.book_id = b.book_id 
     AND bt.borrower_status IN ('BORROWED', 'OVERDUE')), 0);

-- ==============================================
-- TẠO INDEX ĐỂ TỐI ƯU HIỆU SUẤT
-- ==============================================

CREATE INDEX idx_users_email ON USERS(email);
CREATE INDEX idx_books_isbn ON BOOKS(isbn);
CREATE INDEX idx_books_title ON BOOKS(title);
CREATE INDEX idx_transaction_member ON BORROWING_TRANSACTION(member_id);
CREATE INDEX idx_transaction_status ON BORROWING_TRANSACTION(borrower_status);
CREATE INDEX idx_transaction_dates ON BORROWING_TRANSACTION(borrow_date, due_date);
CREATE INDEX idx_fine_status ON FINE(fine_status);
CREATE INDEX idx_fine_transaction_detail ON FINE(transaction_detail_id);
CREATE INDEX idx_transaction_details_book ON BORROWING_TRANSACTION_DETAILS(book_id);

-- ==============================================
-- TẠO VIEW ĐỂ DỄ QUẢN LÝ - ĐÃ SỬA
-- ==============================================

-- View hiển thị thông tin mượn sách chi tiết
CREATE OR REPLACE VIEW vw_borrowing_details AS
SELECT 
    bt.transaction_id,
    u.user_id as member_id,
    u.fullname as member_name,
    l.user_id as librarian_id,
    l.fullname as librarian_name,
    b.book_id,
    b.title as book_title,
    b.isbn,
    a.author_name,
    bt.borrow_date,
    bt.due_date,
    bt.return_date,
    bt.borrower_status,
    btd.item_status,
    btd.damage_precentage,
    btd.days_late,
    DATEDIFF(IFNULL(bt.return_date, CURDATE()), bt.due_date) as actual_days_late
FROM BORROWING_TRANSACTION bt
JOIN USERS u ON bt.member_id = u.user_id
LEFT JOIN USERS l ON bt.librarian_id = l.user_id
JOIN BORROWING_TRANSACTION_DETAILS btd ON bt.transaction_id = btd.transaction_id
JOIN BOOKS b ON btd.book_id = b.book_id
LEFT JOIN AUTHORS a ON b.author_id = a.author_id;

-- View hiển thị phạt tổng hợp - ĐÃ SỬA
DROP VIEW IF EXISTS vw_fine_summary;

CREATE VIEW vw_fine_summary AS
SELECT 
    f.fine_id,
    u.user_id,
    u.fullname,
    u.email,
    b.title as book_title,
    fr.violation_type,
    f.amount,
    f.fine_status,
    f.created_at,
    f.paid_date
FROM FINE f
JOIN FINE_RULES fr ON f.rule_id = fr.rule_id
JOIN BORROWING_TRANSACTION_DETAILS btd ON f.transaction_detail_id = btd.transaction_detail_id
JOIN BORROWING_TRANSACTION bt ON btd.transaction_id = bt.transaction_id
JOIN USERS u ON bt.member_id = u.user_id
JOIN BOOKS b ON btd.book_id = b.book_id;

-- ==============================================
-- TẠO STORED PROCEDURE CƠ BẢN - ĐÃ SỬA
-- ==============================================

-- Procedure tìm sách theo tiêu chí - ĐÃ SỬA
DELIMITER //
CREATE PROCEDURE sp_search_books(
    IN p_search_term VARCHAR(100),
    IN p_category_id INT,
    IN p_author_id INT
)
BEGIN
    SELECT 
        b.book_id,
        b.title,
        b.isbn,
        a.author_name,
        c.category_name,
        b.publish_date,
        b.total_copies,
        b.available_copies,
        b.price,
        b.book_status
    FROM BOOKS b
    LEFT JOIN AUTHORS a ON b.author_id = a.author_id
    LEFT JOIN CATEGORIES c ON b.category_id = c.category_id
    WHERE (p_search_term IS NULL OR 
           b.title LIKE CONCAT('%', p_search_term, '%') OR
           b.isbn LIKE CONCAT('%', p_search_term, '%') OR
           a.author_name LIKE CONCAT('%', p_search_term, '%'))
      AND (p_category_id IS NULL OR b.category_id = p_category_id)
      AND (p_author_id IS NULL OR b.author_id = p_author_id)
      AND b.book_status = 'AVAILABLE'
    ORDER BY b.title;
END //
DELIMITER ;

-- Procedure tính phạt tự động - ĐÃ SỬA
DELIMITER //
CREATE PROCEDURE sp_calculate_fine(
    IN p_transaction_detail_id INT,
    OUT p_fine_amount FLOAT
)
BEGIN
    DECLARE v_days_late INT;
    DECLARE v_damage_precentage FLOAT;
    DECLARE v_book_price FLOAT;
    DECLARE v_overdue_fine FLOAT;
    DECLARE v_damage_fine FLOAT;
    
    -- Lấy thông tin cần thiết
    SELECT btd.days_late, btd.damage_precentage, b.price
    INTO v_days_late, v_damage_precentage, v_book_price
    FROM BORROWING_TRANSACTION_DETAILS btd
    JOIN BOOKS b ON btd.book_id = b.book_id
    WHERE btd.transaction_detail_id = p_transaction_detail_id;
    
    -- Tính phạt trả muộn
    IF v_days_late > 0 THEN
        SET v_overdue_fine = LEAST(v_days_late * 20000, 200000);
    ELSE
        SET v_overdue_fine = 0;
    END IF;
    
    -- Tính phạt hư hỏng
    IF v_damage_precentage > 0 THEN
        SET v_damage_fine = v_book_price * (v_damage_precentage / 100) * 0.3;
    ELSE
        SET v_damage_fine = 0;
    END IF;
    
    -- Tổng phạt
    SET p_fine_amount = v_overdue_fine + v_damage_fine;
END //
DELIMITER ;

-- ==============================================
-- KIỂM TRA DATABASE
-- ==============================================

-- Kiểm tra số lượng sách
SELECT COUNT(*) as TotalBooks FROM BOOKS;

-- Kiểm tra người dùng
SELECT user_id, fullname, email, role_name, status, user_status, totalFineDebt FROM USERS;

-- Kiểm tra giao dịch
SELECT * FROM vw_borrowing_details;

-- Kiểm tra view phạt
SELECT * FROM vw_fine_summary;

-- Test stored procedure
CALL sp_search_books('Java', NULL, NULL);


-- Tạo cơ sở dữ liệu
CREATE DATABASE IF NOT EXISTS LibraryDB;
USE LibraryDB;

-- Bảng BOOKS
DESCRIBE BOOKS;

-- Bảng AUTHORS  
DESCRIBE AUTHORS;

-- Bảng CATEGORIES
DESCRIBE CATEGORIES;

-- Bảng TAGS (nếu có)
DESCRIBE TAGS;

SELECT * FROM BOOKS WHERE title = 'Tôi thấy hoa vàng trên cỏ xanh';
DESCRIBE BORROWING_TRANSACTION_DETAILS;

-- 1. Check xem có sách đang mượn không
SELECT 
    bt.transaction_id,
    bt.member_id,
    b.title,
    bt.borrow_date,
    bt.due_date,
    bt.borrower_status
FROM BORROWING_TRANSACTION bt
JOIN BORROWING_TRANSACTION_DETAILS btd ON bt.transaction_id = btd.transaction_id
JOIN BOOKS b ON btd.book_id = b.book_id
WHERE bt.member_id = 1  -- Thay 1 bằng user_id của bạn
AND bt.borrower_status = 'BORROWED';

-- 2. Check có sách available không
SELECT book_id, title, available_copies 
FROM BOOKS 
WHERE available_copies > 0 
LIMIT 5;

-- Xem user hiện tại
SELECT user_id, fullname, role_name FROM USERS WHERE user_id = 1;


-- 1. Xem cấu trúc BORROWING_TRANSACTION
SHOW COLUMNS FROM BORROWING_TRANSACTION;

-- 2. Xem cấu trúc BORROWING_TRANSACTION_DETAILS
SHOW COLUMNS FROM BORROWING_TRANSACTION_DETAILS;

-- 3. Xem cấu trúc USERS
SHOW COLUMNS FROM USERS;

-- 4. Xem 1 record mẫu từ mỗi bảng
SELECT * FROM BORROWING_TRANSACTION LIMIT 1;
SELECT * FROM BORROWING_TRANSACTION_DETAILS LIMIT 1;
SELECT * FROM USERS LIMIT 1;

-- Xem sample data từ các bảng
SELECT * FROM BORROWING_TRANSACTION LIMIT 2;
SELECT * FROM BORROWING_TRANSACTION_DETAILS LIMIT 2;
SELECT * FROM BOOKS LIMIT 1;
SELECT * FROM USERS LIMIT 1;

-- Xem transactions của user
SELECT * FROM BORROWING_TRANSACTION WHERE member_id = 1;

-- Xem có sách nào available không
SELECT COUNT(*) as total_available FROM BOOKS WHERE available_copies > 0;


SELECT user_id, fullname, email, password, role_name
FROM USERS
WHERE role_name = 'MEMBER';

-- Thêm borrowing cho user Trần Thị B (user_id = 2)
INSERT INTO borrowing_transaction (member_id, borrow_date, due_date, borrower_status)
VALUES (2, '2024-01-20', '2024-02-03', 'BORROWED');

-- Lấy transaction_id vừa tạo
SET @transaction_id = LAST_INSERT_ID();

-- Thêm chi tiết mượn sách
INSERT INTO borrowing_transaction_details (transaction_id, book_id, item_status)
VALUES (@transaction_id, 1, 'BORROWED');

INSERT INTO borrowing_transaction_details (transaction_id, book_id, item_status)
VALUES (@transaction_id, 2, 'BORROWED');

SHOW COLUMNS FROM BORROWING_TRANSACTION_DETAILS;

USE LibraryDB;

-- Đổi tên column từ damage_precentage → damage_percentage
ALTER TABLE BORROWING_TRANSACTION_DETAILS 
CHANGE COLUMN damage_precentage damage_percentage FLOAT DEFAULT 0;

SHOW COLUMNS FROM BORROWING_TRANSACTION_DETAILS;
-- 1. Bảng USERS (Người dùng) - ĐÃ SỬA THEO DATA MODEL
CREATE TABLE USERS (
    user_id INT PRIMARY KEY AUTO_INCREMENT,
    fullname VARCHAR(30) NOT NULL,
    password VARCHAR(55) NOT NULL, -- ĐÃ SỬA: 55 thay vì 255
    created_at DATE NOT NULL,
    status VARCHAR(55) NOT NULL, -- ĐÃ SỬA: theo data model
    address VARCHAR(50),
    phone VARCHAR(20),
    email VARCHAR(50) UNIQUE NOT NULL,
    role_name VARCHAR(30) NOT NULL,
    gender VARCHAR(30),
    user_status VARCHAR(50) DEFAULT 'ACTIVE', -- Thêm cột user_status
    totalFineDebt DOUBLE DEFAULT 0, -- ĐÃ SỬA: đúng tên data model
    CONSTRAINT chk_role CHECK (role_name IN ('MEMBER', 'LIBRARIAN', 'ADMIN'))
);

-- 2. Bảng CATEGORIES (Thể loại sách)
CREATE TABLE CATEGORIES (
    category_id INT PRIMARY KEY AUTO_INCREMENT,
    category_name VARCHAR(30) UNIQUE NOT NULL
);

-- 3. Bảng AUTHORS (Tác giả)
CREATE TABLE AUTHORS (
    author_id INT PRIMARY KEY AUTO_INCREMENT,
    author_name VARCHAR(50) NOT NULL,
    biography TEXT
);

-- 4. Bảng BOOKS (Sách) - ĐÃ SỬA THEO DATA MODEL
CREATE TABLE BOOKS (
    book_id INT PRIMARY KEY AUTO_INCREMENT,
    title VARCHAR(50) NOT NULL,
    isbn VARCHAR(50) UNIQUE NOT NULL, -- ĐÃ SỬA: 50 thay vì 55
    author_id INT,
    category_id INT,
    publish_date INT, -- ĐÃ SỬA: publish_date thay vì publish_year
    total_copies INT NOT NULL DEFAULT 1,
    available_copies INT NOT NULL DEFAULT 0,
    is_reference_only BOOLEAN DEFAULT FALSE,
    publisher VARCHAR(30),
    summary TEXT,
    image_url TEXT,
    price FLOAT, -- ĐÃ SỬA: FLOAT thay vì DECIMAL
    book_status VARCHAR(20) DEFAULT 'AVAILABLE',
    FOREIGN KEY (category_id) REFERENCES CATEGORIES(category_id),
    FOREIGN KEY (author_id) REFERENCES AUTHORS(author_id)
);

-- 5. Bảng BORROWING_TRANSACTION (Giao dịch mượn) - ĐÃ SỬA THEO DATA MODEL
CREATE TABLE BORROWING_TRANSACTION (
    transaction_id INT PRIMARY KEY AUTO_INCREMENT,
    member_id INT NOT NULL,
    librarian_id INT, -- ĐÃ THÊM: theo data model
    borrow_date DATE NOT NULL,
    due_date DATE NOT NULL,
    return_date DATE,
    borrower_status VARCHAR(100) DEFAULT 'BORROWED', -- ĐÃ SỬA: borrower_status
    renew_week_count INT DEFAULT 0, -- ĐÃ SỬA: renew_week_count
    FOREIGN KEY (member_id) REFERENCES USERS(user_id),
    FOREIGN KEY (librarian_id) REFERENCES USERS(user_id)
);

-- 6. Bảng BORROWING_TRANSACTION_DETAILS (Chi tiết giao dịch mượn) - ĐÃ SỬA
CREATE TABLE BORROWING_TRANSACTION_DETAILS (
    transaction_detail_id INT PRIMARY KEY AUTO_INCREMENT,
    transaction_id INT NOT NULL,
    book_id INT NOT NULL,
    item_status VARCHAR(50) DEFAULT 'BORROWED',
    damage_precentage FLOAT DEFAULT 0, -- ĐÃ SỬA: đúng chính tả theo data model
    days_late INT DEFAULT 0,
    FOREIGN KEY (transaction_id) REFERENCES BORROWING_TRANSACTION(transaction_id),
    FOREIGN KEY (book_id) REFERENCES BOOKS(book_id)
);

-- 7. Bảng FINE_RULES (Quy tắc phạt) - ĐÃ SỬA THEO DATA MODEL
CREATE TABLE FINE_RULES (
    rule_id INT PRIMARY KEY AUTO_INCREMENT,
    violation_type VARCHAR(50) UNIQUE NOT NULL,
    lost_book_fine DECIMAL(10,2) NOT NULL,
    damage_rate FLOAT NOT NULL,
    overdue_rate DECIMAL(10,2) NOT NULL,
    max_late_penalty DECIMAL(10,2),
    is_active BOOLEAN DEFAULT TRUE
);

-- 8. Bảng FINE (Phạt) - ĐÃ SỬA THEO DATA MODEL
CREATE TABLE FINE (
    fine_id INT PRIMARY KEY AUTO_INCREMENT,
    rule_id INT NOT NULL,
    transaction_detail_id INT NOT NULL,
    fine_status VARCHAR(100) DEFAULT 'UNPAID',
    amount FLOAT NOT NULL,
    paid_date DATE,  -- Ngày thanh toán
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,  -- Ngày tạo
    FOREIGN KEY (rule_id) REFERENCES FINE_RULES(rule_id),
    FOREIGN KEY (transaction_detail_id) REFERENCES BORROWING_TRANSACTION_DETAILS(transaction_detail_id)
);


-- ==============================================
-- CHÈN DỮ LIỆU MẪU - ĐÃ ĐIỀU CHỈNH
-- ==============================================

-- 1. Chèn dữ liệu vào bảng CATEGORIES
INSERT INTO CATEGORIES (category_name) VALUES
('Văn học Việt Nam'),
('Văn học nước ngoài'),
('Khoa học'),
('Lịch sử'),
('Kinh tế'),
('Kỹ năng sống'),
('Công nghệ thông tin'),
('Tiểu thuyết'),
('Truyện ngắn'),
('Thơ');

-- 2. Chèn dữ liệu vào bảng AUTHORS
INSERT INTO AUTHORS (author_name, biography) VALUES
('Nguyễn Nhật Ánh', 'Nhà văn nổi tiếng Việt Nam với các tác phẩm cho tuổi mới lớn'),
('Nam Cao', 'Nhà văn hiện thực phê phán Việt Nam'),
('Haruki Murakami', 'Nhà văn Nhật Bản nổi tiếng thế giới'),
('Paulo Coelho', 'Nhà văn Brazil với tác phẩm nổi tiếng Nhà giả kim'),
('Stephen Hawking', 'Nhà vật lý lý thuyết, vũ trụ học người Anh'),
('Dale Carnegie', 'Tác giả nổi tiếng về sách kỹ năng sống'),
('Ngô Tất Tố', 'Nhà văn, nhà báo, học giả Việt Nam'),
('Tô Hoài', 'Nhà văn nổi tiếng với tác phẩm Dế Mèn phiêu lưu ký'),
('J.K. Rowling', 'Nhà văn Anh, tác giả bộ truyện Harry Potter'),
('Nguyễn Du', 'Đại thi hào dân tộc Việt Nam'),
('Trần Đăng Khoa', 'Nhà thơ thần đồng Việt Nam'),
('Nguyễn Ngọc Tư', 'Nhà văn nữ đương đại Việt Nam'),
('Adam Khoo', 'Tác giả, diễn giả người Singapore về phát triển bản thân'),
('Robert Kiyosaki', 'Tác giả nổi tiếng với bộ sáng Dạy con làm giàu'),
('Nguyễn Phong', 'Tác giả về công nghệ thông tin'),
('Victor Hugo', 'Tác giả Những người khốn khổ'), 
('Viktor Frankl', 'Tác giả Đi tìm lẽ sống'), 
('Robert C. Martin', 'Tác giả Clean Code');

-- 3. Chèn dữ liệu vào bảng USERS - ĐÃ ĐIỀU CHỈNH
INSERT INTO USERS (fullname, password, created_at, status, address, phone, email, role_name, gender, totalFineDebt) VALUES
('Nguyễn Văn A', 'hashed_password_1', '2023-01-15', 'ACTIVE', 'Hà Nội', '0912345678', 'nguyenvana@email.com', 'MEMBER', 'Nam', 0),
('Trần Thị B', 'hashed_password_2', '2023-02-20', 'ACTIVE', 'TP HCM', '0923456789', 'tranthib@email.com', 'MEMBER', 'Nữ', 0),
('Lê Văn C', 'hashed_password_3', '2023-03-10', 'ACTIVE', 'Đà Nẵng', '0934567890', 'levanc@email.com', 'MEMBER', 'Nam', 0),
('Phạm Thị D', 'hashed_password_4', '2023-01-05', 'ACTIVE', 'Hải Phòng', '0945678901', 'phamthid@email.com', 'LIBRARIAN', 'Nữ', 0),
('Hoàng Văn E', 'hashed_password_5', '2023-02-28', 'ACTIVE', 'Cần Thơ', '0956789012', 'hoangvane@email.com', 'ADMIN', 'Nam', 0),
('Vũ Thị F', 'hashed_password_6', '2023-04-01', 'ACTIVE', 'Nghệ An', '0967890123', 'vuthif@email.com', 'MEMBER', 'Nữ', 0),
('Đặng Văn G', 'hashed_password_7', '2023-03-15', 'BLOCKED', 'Thanh Hóa', '0978901234', 'dangvang@email.com', 'MEMBER', 'Nam', 0),
('Bùi Thị H', 'hashed_password_8', '2023-02-10', 'ACTIVE', 'Quảng Ninh', '0989012345', 'buithih@email.com', 'MEMBER', 'Nữ', 0),
('Đỗ Văn I', 'hashed_password_9', '2023-01-25', 'ACTIVE', 'Bình Dương', '0990123456', 'dovanii@email.com', 'LIBRARIAN', 'Nam', 0),
('Ngô Thị K', 'hashed_password_10', '2023-04-05', 'ACTIVE', 'Đồng Nai', '0901234567', 'ngothik@email.com', 'MEMBER', 'Nữ', 0);



-- 4. Chèn dữ liệu vào bảng BOOKS (20 cuốn sách) - ĐÃ ĐIỀU CHỈNH
INSERT INTO BOOKS (title, isbn, author_id, category_id, publish_date, total_copies, available_copies, is_reference_only, publisher, summary, price, book_status) VALUES
('Tôi thấy hoa vàng trên cỏ xanh', '978-604-2-12345-6', 1, 1, 2010, 5, 4, FALSE, 'NXB Trẻ', 'Câu chuyện về tuổi thơ ở miền quê Việt Nam', 85000, 'AVAILABLE'),
('Cho tôi xin một vé đi tuổi thơ', '978-604-1-23456-7', 1, 1, 2008, 3, 2, FALSE, 'NXB Trẻ', 'Hồi ức về tuổi thơ đầy mộng mơ', 90000, 'AVAILABLE'),
('Chí Phèo', '978-604-1-34567-8', 2, 1, 1941, 4, 3, FALSE, 'NXB Văn học', 'Tác phẩm kinh điển về người nông dân', 65000, 'AVAILABLE'),
('Rừng Na Uy', '978-604-1-45678-9', 3, 2, 1987, 2, 1, FALSE, 'NXB Hội Nhà văn', 'Tiểu thuyết về tình yêu và sự cô đơn', 120000, 'AVAILABLE'),
('Nhà giả kim', '978-604-1-56789-0', 4, 2, 1988, 6, 5, FALSE, 'NXB Văn hóa', 'Hành trình tìm kiếm ý nghĩa cuộc sống', 95000, 'AVAILABLE'),
('Lược sử thời gian', '978-604-1-67890-1', 5, 3, 1988, 3, 2, TRUE, 'NXB Khoa học', 'Khám phá vũ trụ và các lý thuyết vật lý', 150000, 'AVAILABLE'),
('Đắc nhân tâm', '978-604-1-78901-2', 6, 6, 1936, 8, 6, FALSE, 'NXB Tổng hợp', 'Nghệ thuật thu phục lòng người', 80000, 'AVAILABLE'),
('Tắt đèn', '978-604-1-89012-3', 7, 1, 1939, 4, 3, FALSE, 'NXB Văn học', 'Cuộc sống người nông dân trước cách mạng', 75000, 'AVAILABLE'),
('Dế Mèn phiêu lưu ký', '978-604-1-90123-4', 8, 1, 1941, 5, 4, FALSE, 'NXB Kim Đồng', 'Câu chuyện phiêu lưu của chú dế mèn', 60000, 'AVAILABLE'),
('Harry Potter và Hòn đá phù thủy', '978-604-1-01234-5', 9, 2, 1997, 4, 2, FALSE, 'NXB Trẻ', 'Cuộc phiêu lưu đầu tiên của Harry Potter', 110000, 'AVAILABLE'),
('Truyện Kiều', '978-604-2-11223-3', 10, 10, 1820, 3, 2, TRUE, 'NXB Văn học', 'Kiệt tác văn học dân tộc', 70000, 'AVAILABLE'),
('Góc sân và khoảng trời', '978-604-2-22334-4', 11, 10, 1968, 2, 1, FALSE, 'NXB Kim Đồng', 'Tập thơ của thần đồng thơ ca', 55000, 'AVAILABLE'),
('Cánh đồng bất tận', '978-604-2-33445-5', 12, 1, 2005, 3, 2, FALSE, 'NXB Trẻ', 'Tập truyện ngắn đương đại', 85000, 'AVAILABLE'),
('Tôi tài giỏi, bạn cũng thế', '978-604-2-44556-6', 13, 6, 1998, 5, 4, FALSE, 'NXB Phụ nữ', 'Phương pháp học tập hiệu quả', 100000, 'AVAILABLE'),
('Dạy con làm giàu tập 1', '978-604-2-55667-7', 14, 5, 1997, 4, 3, FALSE, 'NXB Trẻ', 'Kiến thức tài chính cơ bản', 90000, 'AVAILABLE'),
('Lập trình Java cơ bản', '978-604-2-66778-8', 15, 7, 2015, 3, 2, TRUE, 'NXB Khoa học kỹ thuật', 'Giáo trình lập trình Java', 120000, 'AVAILABLE'),
('1Q84', '978-604-2-77889-9', 3, 8, 2009, 2, 1, FALSE, 'NXB Hội Nhà văn', 'Tiểu thuyết giả tưởng đồ sộ', 180000, 'AVAILABLE'),
('Những người khốn khổ', '978-604-2-88990-0', 16, 2, 1862, 2, 1, TRUE, 'NXB Văn học', 'Kiệt tác văn học thế giới', 130000, 'AVAILABLE'),
('Đi tìm lẽ sống', '978-604-2-99001-1', 17, 6, 1946, 3, 2, FALSE, 'NXB Tổng hợp', 'Câu chuyện về ý nghĩa cuộc sống', 85000, 'AVAILABLE'),
('Clean Code', '978-604-3-00112-2', 18, 7, 2008, 2, 1, TRUE, 'NXB Khoa học kỹ thuật', 'Nghệ thuật viết code sạch', 160000, 'AVAILABLE');

-- 5. Chèn dữ liệu vào bảng FINE_RULES
INSERT INTO FINE_RULES (violation_type, lost_book_fine, damage_rate, overdue_rate, max_late_penalty, is_active) VALUES
('OVERDUE', 0, 0, 20000, 200000, TRUE),
('DAMAGED', 0, 0.3, 0, NULL, TRUE),
('LOST', 1.0, 0, 0, NULL, TRUE);

-- 6. Chèn dữ liệu vào bảng BORROWING_TRANSACTION - ĐÃ ĐIỀU CHỈNH
INSERT INTO BORROWING_TRANSACTION (member_id, librarian_id, borrow_date, due_date, return_date, borrower_status, renew_week_count) VALUES
(1, 4, '2024-01-10', '2024-01-24', '2024-01-23', 'RETURNED', 0),
(1, 9, '2024-02-15', '2024-03-01', NULL, 'BORROWED', 1),
(2, 4, '2024-02-20', '2024-03-05', '2024-03-10', 'OVERDUE', 0),
(3, 9, '2024-03-01', '2024-03-15', NULL, 'BORROWED', 0),
(6, 4, '2024-02-28', '2024-03-13', NULL, 'BORROWED', 0),
(8, 9, '2024-03-05', '2024-03-19', NULL, 'BORROWED', 0);

-- 7. Chèn dữ liệu vào bảng BORROWING_TRANSACTION_DETAILS - ĐÃ ĐIỀU CHỈNH
INSERT INTO BORROWING_TRANSACTION_DETAILS (transaction_id, book_id, item_status, damage_precentage, days_late) VALUES
(1, 1, 'RETURNED', 0, 0),
(1, 3, 'RETURNED', 5, 0),
(2, 5, 'BORROWED', 0, 0),
(2, 8, 'BORROWED', 0, 0),
(3, 7, 'RETURNED', 0, 5),
(4, 10, 'BORROWED', 0, 0),
(4, 12, 'BORROWED', 0, 0),
(5, 14, 'BORROWED', 0, 0),
(6, 17, 'BORROWED', 0, 0);

-- 8. Chèn dữ liệu vào bảng FINE - ĐÃ ĐIỀU CHỈNH
INSERT INTO FINE (rule_id, transaction_detail_id, fine_status, amount, paid_date) VALUES
(1, 5, 'PAID', 100000, '2024-03-11'),
(1, 1, 'UNPAID', 0, NULL),
(2, 2, 'PAID', 19500, '2024-01-24');

-- 9. Cập nhật tổng nợ phạt cho người dùng
UPDATE USERS SET totalFineDebt = 100000 WHERE user_id = 2;

-- 10. Cập nhật số bản sách có sẵn
UPDATE BOOKS b
SET available_copies = b.total_copies - COALESCE(
    (SELECT COUNT(*) 
     FROM BORROWING_TRANSACTION_DETAILS btd
     JOIN BORROWING_TRANSACTION bt ON btd.transaction_id = bt.transaction_id
     WHERE btd.book_id = b.book_id 
     AND bt.borrower_status IN ('BORROWED', 'OVERDUE')), 0);

-- ==============================================
-- TẠO INDEX ĐỂ TỐI ƯU HIỆU SUẤT
-- ==============================================

CREATE INDEX idx_users_email ON USERS(email);
CREATE INDEX idx_books_isbn ON BOOKS(isbn);
CREATE INDEX idx_books_title ON BOOKS(title);
CREATE INDEX idx_transaction_member ON BORROWING_TRANSACTION(member_id);
CREATE INDEX idx_transaction_status ON BORROWING_TRANSACTION(borrower_status);
CREATE INDEX idx_transaction_dates ON BORROWING_TRANSACTION(borrow_date, due_date);
CREATE INDEX idx_fine_status ON FINE(fine_status);
CREATE INDEX idx_fine_transaction_detail ON FINE(transaction_detail_id);
CREATE INDEX idx_transaction_details_book ON BORROWING_TRANSACTION_DETAILS(book_id);

-- ==============================================
-- TẠO VIEW ĐỂ DỄ QUẢN LÝ - ĐÃ SỬA
-- ==============================================

-- View hiển thị thông tin mượn sách chi tiết
CREATE OR REPLACE VIEW vw_borrowing_details AS
SELECT 
    bt.transaction_id,
    u.user_id as member_id,
    u.fullname as member_name,
    l.user_id as librarian_id,
    l.fullname as librarian_name,
    b.book_id,
    b.title as book_title,
    b.isbn,
    a.author_name,
    bt.borrow_date,
    bt.due_date,
    bt.return_date,
    bt.borrower_status,
    btd.item_status,
    btd.damage_precentage,
    btd.days_late,
    DATEDIFF(IFNULL(bt.return_date, CURDATE()), bt.due_date) as actual_days_late
FROM BORROWING_TRANSACTION bt
JOIN USERS u ON bt.member_id = u.user_id
LEFT JOIN USERS l ON bt.librarian_id = l.user_id
JOIN BORROWING_TRANSACTION_DETAILS btd ON bt.transaction_id = btd.transaction_id
JOIN BOOKS b ON btd.book_id = b.book_id
LEFT JOIN AUTHORS a ON b.author_id = a.author_id;

-- View hiển thị phạt tổng hợp - ĐÃ SỬA
DROP VIEW IF EXISTS vw_fine_summary;

CREATE VIEW vw_fine_summary AS
SELECT 
    f.fine_id,
    u.user_id,
    u.fullname,
    u.email,
    b.title as book_title,
    fr.violation_type,
    f.amount,
    f.fine_status,
    f.created_at,
    f.paid_date
FROM FINE f
JOIN FINE_RULES fr ON f.rule_id = fr.rule_id
JOIN BORROWING_TRANSACTION_DETAILS btd ON f.transaction_detail_id = btd.transaction_detail_id
JOIN BORROWING_TRANSACTION bt ON btd.transaction_id = bt.transaction_id
JOIN USERS u ON bt.member_id = u.user_id
JOIN BOOKS b ON btd.book_id = b.book_id;

-- ==============================================
-- TẠO STORED PROCEDURE CƠ BẢN - ĐÃ SỬA
-- ==============================================

-- Procedure tìm sách theo tiêu chí - ĐÃ SỬA
DELIMITER //
CREATE PROCEDURE sp_search_books(
    IN p_search_term VARCHAR(100),
    IN p_category_id INT,
    IN p_author_id INT
)
BEGIN
    SELECT 
        b.book_id,
        b.title,
        b.isbn,
        a.author_name,
        c.category_name,
        b.publish_date,
        b.total_copies,
        b.available_copies,
        b.price,
        b.book_status
    FROM BOOKS b
    LEFT JOIN AUTHORS a ON b.author_id = a.author_id
    LEFT JOIN CATEGORIES c ON b.category_id = c.category_id
    WHERE (p_search_term IS NULL OR 
           b.title LIKE CONCAT('%', p_search_term, '%') OR
           b.isbn LIKE CONCAT('%', p_search_term, '%') OR
           a.author_name LIKE CONCAT('%', p_search_term, '%'))
      AND (p_category_id IS NULL OR b.category_id = p_category_id)
      AND (p_author_id IS NULL OR b.author_id = p_author_id)
      AND b.book_status = 'AVAILABLE'
    ORDER BY b.title;
END //
DELIMITER ;

-- Procedure tính phạt tự động - ĐÃ SỬA
DELIMITER //
CREATE PROCEDURE sp_calculate_fine(
    IN p_transaction_detail_id INT,
    OUT p_fine_amount FLOAT
)
BEGIN
    DECLARE v_days_late INT;
    DECLARE v_damage_precentage FLOAT;
    DECLARE v_book_price FLOAT;
    DECLARE v_overdue_fine FLOAT;
    DECLARE v_damage_fine FLOAT;
    
    -- Lấy thông tin cần thiết
    SELECT btd.days_late, btd.damage_precentage, b.price
    INTO v_days_late, v_damage_precentage, v_book_price
    FROM BORROWING_TRANSACTION_DETAILS btd
    JOIN BOOKS b ON btd.book_id = b.book_id
    WHERE btd.transaction_detail_id = p_transaction_detail_id;
    
    -- Tính phạt trả muộn
    IF v_days_late > 0 THEN
        SET v_overdue_fine = LEAST(v_days_late * 20000, 200000);
    ELSE
        SET v_overdue_fine = 0;
    END IF;
    
    -- Tính phạt hư hỏng
    IF v_damage_precentage > 0 THEN
        SET v_damage_fine = v_book_price * (v_damage_precentage / 100) * 0.3;
    ELSE
        SET v_damage_fine = 0;
    END IF;
    
    -- Tổng phạt
    SET p_fine_amount = v_overdue_fine + v_damage_fine;
END //
DELIMITER ;

-- ==============================================
-- KIỂM TRA DATABASE
-- ==============================================

-- Kiểm tra số lượng sách
SELECT COUNT(*) as TotalBooks FROM BOOKS;

-- Kiểm tra người dùng
SELECT user_id, fullname, email, role_name, status, user_status, totalFineDebt FROM USERS;

-- Kiểm tra giao dịch
SELECT * FROM vw_borrowing_details;

-- Kiểm tra view phạt
SELECT * FROM vw_fine_summary;

-- Test stored procedure
CALL sp_search_books('Java', NULL, NULL);

USE LibraryDB;

-- Xem user có vấn đề
SELECT user_id, fullname, email, totalFineDebt 
FROM USERS 
WHERE user_id = 2;

-- Xem tất cả fines của user này
SELECT 
    f.fine_id,
    f.amount,
    f.fine_status,
    fr.violation_type,
    b.title
FROM FINE f
JOIN FINE_RULES fr ON f.rule_id = fr.rule_id
JOIN BORROWING_TRANSACTION_DETAILS btd ON f.transaction_detail_id = btd.transaction_detail_id
JOIN BORROWING_TRANSACTION bt ON btd.transaction_id = bt.transaction_id
JOIN BOOKS b ON btd.book_id = b.book_id
WHERE bt.member_id = 2;

-- Xem lại user 2
SELECT user_id, fullname, totalFineDebt 
FROM USERS 
WHERE user_id = 2;

-- So sánh với tính toán thực tế
SELECT 
    u.user_id,
    u.fullname,
    u.totalFineDebt as stored_debt,
    COALESCE(SUM(CASE WHEN f.fine_status = 'UNPAID' THEN f.amount ELSE 0 END), 0) as calculated_unpaid
FROM USERS u
LEFT JOIN BORROWING_TRANSACTION bt ON u.user_id = bt.member_id
LEFT JOIN BORROWING_TRANSACTION_DETAILS btd ON bt.transaction_id = btd.transaction_id
LEFT JOIN FINE f ON btd.transaction_detail_id = f.transaction_detail_id
WHERE u.user_id = 2
GROUP BY u.user_id, u.fullname, u.totalFineDebt;

-- Cập nhật totalFineDebt = tổng UNPAID fines thực tế
UPDATE USERS 
SET totalFineDebt = 90000 
WHERE user_id = 2;

-- Verify
SELECT user_id, fullname, totalFineDebt 
FROM USERS 
WHERE user_id = 2;

-- Tự động tính và update
UPDATE USERS u
SET totalFineDebt = (
    SELECT COALESCE(SUM(f.amount), 0)
    FROM FINE f
    JOIN BORROWING_TRANSACTION_DETAILS btd ON f.transaction_detail_id = btd.transaction_detail_id
    JOIN BORROWING_TRANSACTION bt ON btd.transaction_id = bt.transaction_id
    WHERE bt.member_id = u.user_id
    AND f.fine_status = 'UNPAID'
)
WHERE user_id = 2;

-- Kiểm tra tất cả transactions của user 2
SELECT 
    bt.transaction_id,
    bt.borrower_status,
    b.title,
    btd.item_status,
    f.fine_id,
    f.amount,
    f.fine_status
FROM BORROWING_TRANSACTION bt
JOIN BORROWING_TRANSACTION_DETAILS btd ON bt.transaction_id = btd.transaction_id
JOIN BOOKS b ON btd.book_id = b.book_id
LEFT JOIN FINE f ON btd.transaction_detail_id = f.transaction_detail_id
WHERE bt.member_id = 2
ORDER BY bt.transaction_id;
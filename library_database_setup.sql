-- =====================================================
-- LIBRARY MANAGEMENT SYSTEM - DATABASE SETUP
-- =====================================================

-- Tạo database
DROP DATABASE IF EXISTS LibraryDB;
CREATE DATABASE LibraryDB;
USE LibraryDB;

-- =====================================================
-- 1. BẢNG USERS (Người dùng)
-- =====================================================
CREATE TABLE USERS (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    fullname VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(100) NOT NULL,
    phone VARCHAR(20),
    address TEXT,
    role_name ENUM('GUEST', 'MEMBER', 'LIBRARIAN', 'ADMIN') DEFAULT 'MEMBER',
    user_status ENUM('ACTIVE', 'INACTIVE', 'SUSPENDED') DEFAULT 'ACTIVE',
    status ENUM('ACTIVE', 'INACTIVE') DEFAULT 'ACTIVE',
    totalFineDebt DECIMAL(10, 2) DEFAULT 0,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_email (email),
    INDEX idx_role (role_name),
    INDEX idx_status (user_status)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- =====================================================
-- 2. BẢNG BOOKS (Sách)
-- =====================================================
CREATE TABLE BOOKS (
    book_id INT AUTO_INCREMENT PRIMARY KEY,
    isbn VARCHAR(20) UNIQUE,
    title VARCHAR(200) NOT NULL,
    author VARCHAR(200) NOT NULL,
    category VARCHAR(100),
    genre VARCHAR(100),
    publisher VARCHAR(200),
    publication_year INT,
    pages INT,
    price DECIMAL(10, 2),
    total_copies INT DEFAULT 1,
    available_copies INT DEFAULT 1,
    summary TEXT,
    cover_image_url TEXT,
    book_status ENUM('AVAILABLE', 'UNAVAILABLE', 'MAINTENANCE') DEFAULT 'AVAILABLE',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_isbn (isbn),
    INDEX idx_title (title),
    INDEX idx_author (author),
    INDEX idx_category (category),
    INDEX idx_status (book_status)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- =====================================================
-- 3. BẢNG TRANSACTIONS (Giao dịch mượn/trả)
-- =====================================================
CREATE TABLE TRANSACTIONS (
    transaction_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    book_id INT NOT NULL,
    borrow_date DATE NOT NULL,
    due_date DATE NOT NULL,
    return_date DATE,
    transaction_status ENUM('BORROWED', 'RETURNED', 'OVERDUE', 'LOST') DEFAULT 'BORROWED',
    fine_amount DECIMAL(10, 2) DEFAULT 0,
    notes TEXT,
    librarian_id INT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES USERS(user_id) ON DELETE CASCADE,
    FOREIGN KEY (book_id) REFERENCES BOOKS(book_id) ON DELETE CASCADE,
    FOREIGN KEY (librarian_id) REFERENCES USERS(user_id) ON DELETE SET NULL,
    INDEX idx_user (user_id),
    INDEX idx_book (book_id),
    INDEX idx_status (transaction_status),
    INDEX idx_borrow_date (borrow_date),
    INDEX idx_due_date (due_date)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- =====================================================
-- 4. BẢNG FINES (Phạt)
-- =====================================================
CREATE TABLE FINES (
    fine_id INT AUTO_INCREMENT PRIMARY KEY,
    transaction_id INT NOT NULL,
    user_id INT NOT NULL,
    fine_amount DECIMAL(10, 2) NOT NULL,
    fine_reason VARCHAR(200),
    fine_status ENUM('UNPAID', 'PAID', 'WAIVED') DEFAULT 'UNPAID',
    paid_date DATE,
    notes TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (transaction_id) REFERENCES TRANSACTIONS(transaction_id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES USERS(user_id) ON DELETE CASCADE,
    INDEX idx_user (user_id),
    INDEX idx_transaction (transaction_id),
    INDEX idx_status (fine_status)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- =====================================================
-- 5. BẢNG RESERVATIONS (Đặt trước sách)
-- =====================================================
CREATE TABLE RESERVATIONS (
    reservation_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    book_id INT NOT NULL,
    reservation_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    reservation_status ENUM('PENDING', 'FULFILLED', 'CANCELLED', 'EXPIRED') DEFAULT 'PENDING',
    expiry_date DATE,
    notes TEXT,
    FOREIGN KEY (user_id) REFERENCES USERS(user_id) ON DELETE CASCADE,
    FOREIGN KEY (book_id) REFERENCES BOOKS(book_id) ON DELETE CASCADE,
    INDEX idx_user (user_id),
    INDEX idx_book (book_id),
    INDEX idx_status (reservation_status)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- =====================================================
-- DỮ LIỆU MẪU
-- =====================================================

-- Thêm Users mẫu
INSERT INTO USERS (fullname, email, password, phone, address, role_name, user_status, totalFineDebt) VALUES
-- Admin
('Admin User', 'admin@library.com', 'admin123', '0901234567', '123 Admin Street, HCMC', 'ADMIN', 'ACTIVE', 0),

-- Librarians
('Nguyen Van Librarian', 'librarian@library.com', 'lib123', '0912345678', '456 Librarian Ave, HCMC', 'LIBRARIAN', 'ACTIVE', 0),
('Tran Thi Librarian', 'librarian2@library.com', 'lib123', '0923456789', '789 Book Street, HCMC', 'LIBRARIAN', 'ACTIVE', 0),

-- Members
('Nguyen Van A', 'nguyenvana@email.com', 'member123', '0934567890', '111 Member Road, HCMC', 'MEMBER', 'ACTIVE', 0),
('Tran Thi B', 'tranthib@email.com', 'member123', '0945678901', '222 Reader Lane, HCMC', 'MEMBER', 'ACTIVE', 15000),
('Le Van C', 'levanc@email.com', 'member123', '0956789012', '333 Student Street, HCMC', 'MEMBER', 'ACTIVE', 0),
('Pham Thi D', 'phamthid@email.com', 'member123', '0967890123', '444 Book Lover Ave, HCMC', 'MEMBER', 'ACTIVE', 0),
('Hoang Van E', 'hoangvane@email.com', 'member123', '0978901234', '555 Knowledge Road, HCMC', 'MEMBER', 'ACTIVE', 0);

-- Thêm Books mẫu
INSERT INTO BOOKS (isbn, title, author, category, genre, publisher, publication_year, pages, price, total_copies, available_copies, summary, cover_image_url, book_status) VALUES
-- Fiction
('978-0-06-112008-4', 'To Kill a Mockingbird', 'Harper Lee', 'Fiction', 'Classic Literature', 'J.B. Lippincott & Co.', 1960, 324, 150000, 5, 3, 'A gripping tale of racial injustice and childhood innocence in the American South.', 'https://covers.openlibrary.org/b/isbn/9780061120084-L.jpg', 'AVAILABLE'),

('978-0-7432-7356-5', '1984', 'George Orwell', 'Fiction', 'Dystopian', 'Secker & Warburg', 1949, 328, 180000, 4, 2, 'A dystopian social science fiction novel and cautionary tale about totalitarianism.', 'https://covers.openlibrary.org/b/isbn/9780743273565-L.jpg', 'AVAILABLE'),

('978-0-316-76948-0', 'The Catcher in the Rye', 'J.D. Salinger', 'Fiction', 'Coming-of-age', 'Little, Brown and Company', 1951, 277, 160000, 3, 1, 'A story about teenage rebellion and alienation.', 'https://covers.openlibrary.org/b/isbn/9780316769488-L.jpg', 'AVAILABLE'),

('978-0-14-028329-5', 'Pride and Prejudice', 'Jane Austen', 'Fiction', 'Romance', 'T. Egerton', 1813, 432, 140000, 6, 4, 'A romantic novel of manners set in Georgian England.', 'https://covers.openlibrary.org/b/isbn/9780140283295-L.jpg', 'AVAILABLE'),

('978-0-553-21311-7', 'The Great Gatsby', 'F. Scott Fitzgerald', 'Fiction', 'Classic Literature', 'Charles Scribner''s Sons', 1925, 180, 170000, 4, 2, 'A tragic story of Jay Gatsby and his pursuit of the American Dream.', 'https://covers.openlibrary.org/b/isbn/9780553213119-L.jpg', 'AVAILABLE'),

-- Science & Technology
('978-0-13-110362-7', 'The C Programming Language', 'Brian Kernighan, Dennis Ritchie', 'Technology', 'Programming', 'Prentice Hall', 1988, 272, 250000, 3, 2, 'The definitive guide to C programming by its creators.', 'https://covers.openlibrary.org/b/isbn/9780131103627-L.jpg', 'AVAILABLE'),

('978-0-201-61622-4', 'The Pragmatic Programmer', 'Andrew Hunt, David Thomas', 'Technology', 'Software Engineering', 'Addison-Wesley', 1999, 352, 280000, 2, 1, 'From journeyman to master - your journey to mastery.', 'https://covers.openlibrary.org/b/isbn/9780201616224-L.jpg', 'AVAILABLE'),

('978-0-262-03384-8', 'Introduction to Algorithms', 'Thomas Cormen', 'Technology', 'Computer Science', 'MIT Press', 2009, 1312, 450000, 3, 2, 'Comprehensive introduction to algorithms and data structures.', 'https://covers.openlibrary.org/b/isbn/9780262033848-L.jpg', 'AVAILABLE'),

('978-0-13-468599-1', 'Clean Code', 'Robert C. Martin', 'Technology', 'Software Engineering', 'Prentice Hall', 2008, 464, 320000, 4, 3, 'A handbook of agile software craftsmanship.', 'https://covers.openlibrary.org/b/isbn/9780134685991-L.jpg', 'AVAILABLE'),

('978-0-321-92013-8', 'Effective Python', 'Brett Slatkin', 'Technology', 'Programming', 'Addison-Wesley', 2015, 256, 290000, 2, 1, '59 specific ways to write better Python.', 'https://covers.openlibrary.org/b/isbn/9780321920133-L.jpg', 'AVAILABLE'),

-- Business & Finance
('978-0-06-231500-7', 'Thinking, Fast and Slow', 'Daniel Kahneman', 'Business', 'Psychology', 'Farrar, Straus and Giroux', 2011, 499, 220000, 3, 2, 'A groundbreaking tour of the mind explaining the two systems that drive the way we think.', 'https://covers.openlibrary.org/b/isbn/9780062315007-L.jpg', 'AVAILABLE'),

('978-0-307-88789-4', 'Thinking in Bets', 'Annie Duke', 'Business', 'Decision Making', 'Portfolio', 2018, 288, 200000, 2, 2, 'Making smarter decisions when you don''t have all the facts.', 'https://covers.openlibrary.org/b/isbn/9780307887894-L.jpg', 'AVAILABLE'),

-- Science
('978-0-553-80370-7', 'A Brief History of Time', 'Stephen Hawking', 'Science', 'Physics', 'Bantam Books', 1988, 256, 190000, 3, 2, 'From the Big Bang to black holes.', 'https://covers.openlibrary.org/b/isbn/9780553803709-L.jpg', 'AVAILABLE'),

('978-0-385-50863-5', 'The Elegant Universe', 'Brian Greene', 'Science', 'Physics', 'W.W. Norton & Company', 1999, 448, 210000, 2, 1, 'Superstrings, hidden dimensions, and the quest for the ultimate theory.', 'https://covers.openlibrary.org/b/isbn/9780385508635-L.jpg', 'AVAILABLE'),

-- Additional popular books
('978-0-439-02348-1', 'Harry Potter and the Philosopher''s Stone', 'J.K. Rowling', 'Fiction', 'Fantasy', 'Bloomsbury', 1997, 223, 200000, 8, 5, 'The magical journey of Harry Potter begins.', 'https://covers.openlibrary.org/b/isbn/9780439023481-L.jpg', 'AVAILABLE'),

('978-0-618-00222-1', 'The Lord of the Rings', 'J.R.R. Tolkien', 'Fiction', 'Fantasy', 'George Allen & Unwin', 1954, 1178, 350000, 4, 2, 'Epic high-fantasy novel about the quest to destroy the One Ring.', 'https://covers.openlibrary.org/b/isbn/9780618002221-L.jpg', 'AVAILABLE'),

('978-0-316-01844-0', 'The Kite Runner', 'Khaled Hosseini', 'Fiction', 'Drama', 'Riverhead Books', 2003, 371, 180000, 3, 2, 'A story of friendship, betrayal, and redemption set in Afghanistan.', 'https://covers.openlibrary.org/b/isbn/9780316018449-L.jpg', 'AVAILABLE'),

('978-0-7432-4722-1', 'The Da Vinci Code', 'Dan Brown', 'Fiction', 'Mystery', 'Doubleday', 2003, 454, 195000, 5, 3, 'A thriller about secret societies and religious mysteries.', 'https://covers.openlibrary.org/b/isbn/9780743247221-L.jpg', 'AVAILABLE'),

-- Vietnamese Literature
('978-604-2-10234-5', 'Số Đỏ', 'Vũ Trọng Phụng', 'Fiction', 'Vietnamese Literature', 'Nhà Xuất Bản Văn Học', 1936, 268, 85000, 4, 3, 'Một tác phẩm hiện thực phê phán xã hội Việt Nam đầu thế kỷ 20.', 'https://via.placeholder.com/150x220/4BC1D2/FFFFFF?text=So+Do', 'AVAILABLE'),

('978-604-2-15678-9', 'Dế Mèn Phiêu Lưu Ký', 'Tô Hoài', 'Fiction', 'Children', 'Nhà Xuất Bản Kim Đồng', 1941, 156, 65000, 6, 5, 'Câu chuyện phiêu lưu của chú dế mèn dũng cảm.', 'https://via.placeholder.com/150x220/4BC1D2/FFFFFF?text=De+Men', 'AVAILABLE'),

-- Database & System Design
('978-1-4493-7454-2', 'Database System Concepts', 'Abraham Silberschatz', 'Technology', 'Database', 'McGraw-Hill', 2010, 1376, 380000, 2, 1, 'Comprehensive introduction to database management systems.', 'https://covers.openlibrary.org/b/isbn/9781449374542-L.jpg', 'AVAILABLE'),

('978-0-596-00712-6', 'Designing Data-Intensive Applications', 'Martin Kleppmann', 'Technology', 'System Design', 'O''Reilly Media', 2017, 616, 420000, 2, 1, 'The big ideas behind reliable, scalable, and maintainable systems.', 'https://covers.openlibrary.org/b/isbn/9780596007126-L.jpg', 'AVAILABLE');

-- Thêm Transactions mẫu (đã mượn và đang mượn)
INSERT INTO TRANSACTIONS (user_id, book_id, borrow_date, due_date, return_date, transaction_status, fine_amount, librarian_id) VALUES
-- Đã trả
(4, 1, '2025-12-01', '2025-12-15', '2025-12-14', 'RETURNED', 0, 2),
(5, 3, '2025-12-10', '2025-12-24', '2025-12-28', 'RETURNED', 20000, 2),
(6, 5, '2025-12-15', '2025-12-29', '2025-12-27', 'RETURNED', 0, 3),

-- Đang mượn - chưa quá hạn
(4, 2, '2026-01-01', '2026-01-16', NULL, 'BORROWED', 0, 2),
(4, 8, '2025-12-27', '2026-01-11', NULL, 'BORROWED', 0, 2),
(5, 7, '2026-01-02', '2026-01-17', NULL, 'BORROWED', 0, 3),

-- Đang mượn - quá hạn
(4, 9, '2025-12-30', '2026-01-14', NULL, 'OVERDUE', 0, 2),
(5, 11, '2025-12-26', '2026-01-10', NULL, 'OVERDUE', 0, 3),

-- Dữ liệu cho dashboard (transactions hôm nay)
(6, 15, '2026-01-28', '2026-02-12', NULL, 'BORROWED', 0, 2),
(7, 16, '2026-01-28', '2026-02-12', NULL, 'BORROWED', 0, 2),
(8, 17, '2026-01-28', '2026-02-12', NULL, 'BORROWED', 0, 3);

-- Thêm Fines mẫu
INSERT INTO FINES (transaction_id, user_id, fine_amount, fine_reason, fine_status, paid_date) VALUES
-- Phạt đã trả
(2, 5, 20000, 'Trả sách quá hạn 4 ngày (5,000 VND/ngày)', 'PAID', '2025-12-29'),

-- Phạt chưa trả
(7, 4, 70000, 'Trả sách quá hạn 14 ngày (5,000 VND/ngày)', 'UNPAID', NULL),
(8, 5, 90000, 'Trả sách quá hạn 18 ngày (5,000 VND/ngày)', 'UNPAID', NULL);

-- Thêm Reservations mẫu
INSERT INTO RESERVATIONS (user_id, book_id, reservation_date, reservation_status, expiry_date, notes) VALUES
(6, 2, '2026-01-25 10:30:00', 'PENDING', '2026-02-01', 'Waiting for book availability'),
(7, 7, '2026-01-26 14:15:00', 'PENDING', '2026-02-02', 'Requested for study'),
(8, 16, '2026-01-24 09:00:00', 'FULFILLED', '2026-01-31', 'Book became available and borrowed');

-- =====================================================
-- STORED PROCEDURES & TRIGGERS
-- =====================================================

-- Trigger: Tự động cập nhật available_copies khi mượn sách
DELIMITER //

CREATE TRIGGER after_borrow_insert
AFTER INSERT ON TRANSACTIONS
FOR EACH ROW
BEGIN
    IF NEW.transaction_status = 'BORROWED' THEN
        UPDATE BOOKS 
        SET available_copies = available_copies - 1
        WHERE book_id = NEW.book_id;
    END IF;
END//

-- Trigger: Tự động cập nhật available_copies khi trả sách
CREATE TRIGGER after_return_update
AFTER UPDATE ON TRANSACTIONS
FOR EACH ROW
BEGIN
    IF OLD.transaction_status = 'BORROWED' AND NEW.transaction_status = 'RETURNED' THEN
        UPDATE BOOKS 
        SET available_copies = available_copies + 1
        WHERE book_id = NEW.book_id;
    END IF;
END//

-- Trigger: Tự động tính phạt khi trả sách quá hạn
CREATE TRIGGER calculate_fine_on_return
AFTER UPDATE ON TRANSACTIONS
FOR EACH ROW
BEGIN
    DECLARE days_overdue INT;
    DECLARE fine_per_day DECIMAL(10,2) DEFAULT 5000; -- 5,000 VND/ngày
    DECLARE calculated_fine DECIMAL(10,2);
    
    IF OLD.transaction_status = 'BORROWED' 
       AND NEW.transaction_status = 'RETURNED' 
       AND NEW.return_date > NEW.due_date THEN
        
        SET days_overdue = DATEDIFF(NEW.return_date, NEW.due_date);
        SET calculated_fine = days_overdue * fine_per_day;
        
        -- Cập nhật fine_amount trong transaction
        UPDATE TRANSACTIONS 
        SET fine_amount = calculated_fine 
        WHERE transaction_id = NEW.transaction_id;
        
        -- Tạo bản ghi fine
        INSERT INTO FINES (transaction_id, user_id, fine_amount, fine_reason, fine_status)
        VALUES (
            NEW.transaction_id, 
            NEW.user_id, 
            calculated_fine,
            CONCAT('Trả sách quá hạn ', days_overdue, ' ngày (', fine_per_day, ' VND/ngày)'),
            'UNPAID'
        );
        
        -- Cập nhật tổng nợ của user
        UPDATE USERS 
        SET totalFineDebt = totalFineDebt + calculated_fine
        WHERE user_id = NEW.user_id;
    END IF;
END//

-- Trigger: Cập nhật tổng nợ khi thanh toán phạt
CREATE TRIGGER after_fine_paid
AFTER UPDATE ON FINES
FOR EACH ROW
BEGIN
    IF OLD.fine_status = 'UNPAID' AND NEW.fine_status = 'PAID' THEN
        UPDATE USERS 
        SET totalFineDebt = totalFineDebt - NEW.fine_amount
        WHERE user_id = NEW.user_id;
    END IF;
END//

-- Stored Procedure: Lấy thống kê dashboard
CREATE PROCEDURE GetDashboardStats(IN target_date DATE)
BEGIN
    -- Transactions today
    SELECT COUNT(*) as transactions_today
    FROM TRANSACTIONS
    WHERE DATE(created_at) = target_date;
    
    -- Books currently on loan
    SELECT COUNT(*) as books_on_loan
    FROM TRANSACTIONS
    WHERE transaction_status = 'BORROWED';
    
    -- Overdue today
    SELECT COUNT(*) as overdue_today
    FROM TRANSACTIONS
    WHERE transaction_status IN ('BORROWED', 'OVERDUE')
    AND due_date <= target_date
    AND return_date IS NULL;
    
    -- Fines processed today
    SELECT COALESCE(SUM(fine_amount), 0) as fines_today
    FROM FINES
    WHERE DATE(created_at) = target_date
    AND fine_status = 'PAID';
END//

DELIMITER ;

-- =====================================================
-- INDEXES FOR PERFORMANCE
-- =====================================================

-- Additional composite indexes for common queries
CREATE INDEX idx_transaction_status_date ON TRANSACTIONS(transaction_status, borrow_date);
CREATE INDEX idx_user_status ON USERS(user_status, role_name);
CREATE INDEX idx_book_availability ON BOOKS(book_status, available_copies);
CREATE INDEX idx_fine_status_user ON FINES(fine_status, user_id);

-- =====================================================
-- VIEWS FOR REPORTING
-- =====================================================

-- View: Thống kê sách được mượn nhiều nhất
CREATE VIEW v_popular_books AS
SELECT 
    b.book_id,
    b.title,
    b.author,
    b.category,
    COUNT(t.transaction_id) as borrow_count,
    AVG(DATEDIFF(COALESCE(t.return_date, CURDATE()), t.borrow_date)) as avg_borrow_days
FROM BOOKS b
LEFT JOIN TRANSACTIONS t ON b.book_id = t.book_id
GROUP BY b.book_id, b.title, b.author, b.category
ORDER BY borrow_count DESC;

-- View: Thành viên có nợ phạt
CREATE VIEW v_members_with_fines AS
SELECT 
    u.user_id,
    u.fullname,
    u.email,
    u.phone,
    u.totalFineDebt,
    COUNT(f.fine_id) as unpaid_fines_count,
    SUM(f.fine_amount) as total_unpaid_amount
FROM USERS u
INNER JOIN FINES f ON u.user_id = f.user_id
WHERE f.fine_status = 'UNPAID'
GROUP BY u.user_id, u.fullname, u.email, u.phone, u.totalFineDebt;

-- View: Sách quá hạn hiện tại
CREATE VIEW v_overdue_books AS
SELECT 
    t.transaction_id,
    u.user_id,
    u.fullname,
    u.email,
    u.phone,
    b.book_id,
    b.title,
    b.author,
    t.borrow_date,
    t.due_date,
    DATEDIFF(CURDATE(), t.due_date) as days_overdue,
    DATEDIFF(CURDATE(), t.due_date) * 5000 as estimated_fine
FROM TRANSACTIONS t
INNER JOIN USERS u ON t.user_id = u.user_id
INNER JOIN BOOKS b ON t.book_id = b.book_id
WHERE t.transaction_status IN ('BORROWED', 'OVERDUE')
AND t.due_date < CURDATE()
AND t.return_date IS NULL;

-- =====================================================
-- GRANT PERMISSIONS
-- =====================================================

-- Grant all privileges to root user
GRANT ALL PRIVILEGES ON LibraryDB.* TO 'root'@'localhost';
FLUSH PRIVILEGES;

-- =====================================================
-- VERIFICATION QUERIES
-- =====================================================

-- Kiểm tra số lượng records
SELECT 'USERS' as TableName, COUNT(*) as RecordCount FROM USERS
UNION ALL
SELECT 'BOOKS', COUNT(*) FROM BOOKS
UNION ALL
SELECT 'TRANSACTIONS', COUNT(*) FROM TRANSACTIONS
UNION ALL
SELECT 'FINES', COUNT(*) FROM FINES
UNION ALL
SELECT 'RESERVATIONS', COUNT(*) FROM RESERVATIONS;

-- Hiển thị thông tin users theo role
SELECT role_name, COUNT(*) as count, GROUP_CONCAT(email SEPARATOR ', ') as emails
FROM USERS
GROUP BY role_name
ORDER BY 
    CASE role_name
        WHEN 'ADMIN' THEN 1
        WHEN 'LIBRARIAN' THEN 2
        WHEN 'MEMBER' THEN 3
        ELSE 4
    END;

-- =====================================================
-- COMPLETED!
-- =====================================================
SELECT '✅ Database setup completed successfully!' as Status;
-- =====================================================
-- THÊM DỮ LIỆU MẪU BỔ SUNG
-- Chạy file này nếu bạn muốn có thêm dữ liệu test
-- =====================================================

USE LibraryDB;

-- Thêm thêm Members
INSERT INTO USERS (fullname, email, password, phone, address, role_name, user_status, totalFineDebt) VALUES
('Nguyen Thi F', 'nguyenthif@email.com', 'member123', '0989012345', '666 Reader Street, HCMC', 'MEMBER', 'ACTIVE', 0),
('Tran Van G', 'tranvang@email.com', 'member123', '0990123456', '777 Library Ave, HCMC', 'MEMBER', 'ACTIVE', 0),
('Le Thi H', 'lethih@email.com', 'member123', '0901234561', '888 Book Road, HCMC', 'MEMBER', 'ACTIVE', 0),
('Pham Van I', 'phamvani@email.com', 'member123', '0912345672', '999 Study Lane, HCMC', 'MEMBER', 'ACTIVE', 0),
('Hoang Thi J', 'hoangthij@email.com', 'member123', '0923456783', '1010 Knowledge St, HCMC', 'MEMBER', 'ACTIVE', 0);

-- Thêm sách Tiếng Việt
INSERT INTO BOOKS (isbn, title, author, category, genre, publisher, publication_year, pages, price, total_copies, available_copies, summary, cover_image_url, book_status) VALUES
('978-604-2-20345-6', 'Chí Phèo', 'Nam Cao', 'Fiction', 'Vietnamese Literature', 'NXB Văn Học', 1941, 120, 45000, 3, 3, 'Tác phẩm hiện thực phê phán về một số phận con người bi thảm.', 'https://via.placeholder.com/150x220/4BC1D2/FFFFFF?text=Chi+Pheo', 'AVAILABLE'),

('978-604-2-21456-7', 'Lão Hạc', 'Nam Cao', 'Fiction', 'Vietnamese Literature', 'NXB Văn Học', 1943, 80, 35000, 3, 3, 'Câu chuyện về tình cha con và số phận cay đắng của người nông dân.', 'https://via.placeholder.com/150x220/4BC1D2/FFFFFF?text=Lao+Hac', 'AVAILABLE'),

('978-604-2-22567-8', 'Tắt Đèn', 'Ngô Tất Tố', 'Fiction', 'Vietnamese Literature', 'NXB Văn Học', 1939, 250, 68000, 4, 4, 'Tiểu thuyết về đời sống khốn khó của nông dân Việt Nam.', 'https://via.placeholder.com/150x220/4BC1D2/FFFFFF?text=Tat+Den', 'AVAILABLE'),

('978-604-2-23678-9', 'Vợ Nhặt', 'Kim Lân', 'Fiction', 'Vietnamese Literature', 'NXB Văn Học', 1962, 45, 25000, 5, 5, 'Truyện ngắn về tình nghĩa vợ chồng trong hoàn cảnh khó khăn.', 'https://via.placeholder.com/150x220/4BC1D2/FFFFFF?text=Vo+Nhat', 'AVAILABLE'),

('978-604-2-24789-0', 'Những Ngôi Sao Xa Xôi', 'Lê Minh Khuê', 'Fiction', 'Vietnamese Literature', 'NXB Hội Nhà Văn', 1997, 180, 55000, 2, 2, 'Truyện ngắn về chiến tranh và những tổn thương của con người.', 'https://via.placeholder.com/150x220/4BC1D2/FFFFFF?text=Nhung+Ngoi+Sao', 'AVAILABLE');

-- Thêm sách Programming
INSERT INTO BOOKS (isbn, title, author, category, genre, publisher, publication_year, pages, price, total_copies, available_copies, summary, cover_image_url, book_status) VALUES
('978-0-13-468604-2', 'Design Patterns', 'Gang of Four', 'Technology', 'Software Engineering', 'Addison-Wesley', 1994, 395, 350000, 3, 3, 'Elements of Reusable Object-Oriented Software.', 'https://covers.openlibrary.org/b/isbn/9780134686042-L.jpg', 'AVAILABLE'),

('978-0-13-235088-4', 'Refactoring', 'Martin Fowler', 'Technology', 'Software Engineering', 'Addison-Wesley', 1999, 448, 380000, 2, 2, 'Improving the design of existing code.', 'https://covers.openlibrary.org/b/isbn/9780132350884-L.jpg', 'AVAILABLE'),

('978-0-596-52068-7', 'JavaScript: The Good Parts', 'Douglas Crockford', 'Technology', 'Programming', 'O''Reilly', 2008, 176, 280000, 3, 3, 'Understanding JavaScript''s best features.', 'https://covers.openlibrary.org/b/isbn/9780596520687-L.jpg', 'AVAILABLE'),

('978-1-491-91205-8', 'Learning Python', 'Mark Lutz', 'Technology', 'Programming', 'O''Reilly', 2013, 1648, 520000, 2, 2, 'Powerful object-oriented programming.', 'https://covers.openlibrary.org/b/isbn/9781491912058-L.jpg', 'AVAILABLE'),

('978-0-201-83595-3', 'Head First Design Patterns', 'Eric Freeman', 'Technology', 'Software Engineering', 'O''Reilly', 2004, 694, 420000, 2, 2, 'A brain-friendly guide to design patterns.', 'https://covers.openlibrary.org/b/isbn/9780201835953-L.jpg', 'AVAILABLE');

-- Thêm sách Self-help & Business
INSERT INTO BOOKS (isbn, title, author, category, genre, publisher, publication_year, pages, price, total_copies, available_copies, summary, cover_image_url, book_status) VALUES
('978-0-7432-3066-3', 'How to Win Friends and Influence People', 'Dale Carnegie', 'Business', 'Self-help', 'Simon & Schuster', 1936, 288, 180000, 4, 4, 'The classic guide to building relationships and influencing others.', 'https://covers.openlibrary.org/b/isbn/9780743230667-L.jpg', 'AVAILABLE'),

('978-1-59184-021-9', 'Rich Dad Poor Dad', 'Robert Kiyosaki', 'Business', 'Finance', 'Plata Publishing', 1997, 336, 220000, 5, 5, 'What the rich teach their kids about money.', 'https://covers.openlibrary.org/b/isbn/9781591840213-L.jpg', 'AVAILABLE'),

('978-0-06-231500-7', 'The 7 Habits of Highly Effective People', 'Stephen Covey', 'Business', 'Self-help', 'Free Press', 1989, 381, 240000, 3, 3, 'Powerful lessons in personal change.', 'https://covers.openlibrary.org/b/isbn/9780062315007-L.jpg', 'AVAILABLE'),

('978-1-59420-127-1', 'The Lean Startup', 'Eric Ries', 'Business', 'Entrepreneurship', 'Crown Business', 2011, 336, 280000, 2, 2, 'How today''s entrepreneurs use continuous innovation.', 'https://covers.openlibrary.org/b/isbn/9781594201271-L.jpg', 'AVAILABLE'),

('978-0-06-112008-4', 'Atomic Habits', 'James Clear', 'Business', 'Self-help', 'Avery', 2018, 320, 260000, 4, 4, 'An easy and proven way to build good habits.', 'https://covers.openlibrary.org/b/isbn/9780061120084-L.jpg', 'AVAILABLE');

-- Thêm transactions để test
INSERT INTO TRANSACTIONS (user_id, book_id, borrow_date, due_date, return_date, transaction_status, fine_amount, librarian_id) VALUES
-- User 9 mượn sách
(9, 23, '2026-01-15', '2026-01-30', NULL, 'BORROWED', 0, 2),
(9, 24, '2026-01-20', '2026-02-04', NULL, 'BORROWED', 0, 2),

-- User 10 mượn sách
(10, 25, '2026-01-18', '2026-02-02', NULL, 'BORROWED', 0, 3),
(10, 26, '2026-01-22', '2026-02-06', NULL, 'BORROWED', 0, 3),

-- User 11 mượn sách (có quá hạn)
(11, 27, '2025-12-20', '2026-01-04', NULL, 'OVERDUE', 0, 2),
(11, 28, '2026-01-10', '2026-01-25', NULL, 'BORROWED', 0, 2);

-- Thêm reservations
INSERT INTO RESERVATIONS (user_id, book_id, reservation_status, expiry_date, notes) VALUES
(9, 1, 'PENDING', '2026-02-05', 'Want to read this classic'),
(10, 15, 'PENDING', '2026-02-06', 'For school project'),
(11, 30, 'PENDING', '2026-02-07', 'Interested in this book');

-- Thống kê sau khi insert
SELECT '✅ Đã thêm dữ liệu mẫu bổ sung thành công!' as Status;

SELECT 'Tổng số Users' as Info, COUNT(*) as Count FROM USERS
UNION ALL
SELECT 'Tổng số Books', COUNT(*) FROM BOOKS
UNION ALL
SELECT 'Tổng số Transactions', COUNT(*) FROM TRANSACTIONS
UNION ALL
SELECT 'Tổng số Fines', COUNT(*) FROM FINES
UNION ALL
SELECT 'Tổng số Reservations', COUNT(*) FROM RESERVATIONS;
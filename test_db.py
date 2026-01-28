"""
TEST DATABASE CONNECTION
Chạy file này để kiểm tra kết nối database và xem dữ liệu mẫu
"""

import sys
import os

# Thêm thư mục gốc vào path để import được module
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from database.db import fetch_all, fetch_one, get_connection
    print("✅ Import database module thành công!")
except ImportError as e:
    print(f"❌ Lỗi import: {e}")
    print("Đảm bảo file database/db.py tồn tại")
    sys.exit(1)

def test_connection():
    """Test kết nối đến database"""
    print("\n" + "="*60)
    print("🔌 KIỂM TRA KẾT NỐI DATABASE")
    print("="*60)
    
    try:
        conn = get_connection()
        print("✅ Kết nối MySQL thành công!")
        print(f"   Host: localhost")
        print(f"   Database: LibraryDB")
        conn.close()
        return True
    except Exception as e:
        print(f"❌ Lỗi kết nối database: {e}")
        print("\n💡 Gợi ý:")
        print("   1. Kiểm tra MySQL service đã chạy chưa")
        print("   2. Kiểm tra password trong file database/db.py")
        print("   3. Đảm bảo database 'LibraryDB' đã được tạo")
        return False

def test_users():
    """Kiểm tra bảng USERS"""
    print("\n" + "="*60)
    print("👥 KIỂM TRA BẢNG USERS")
    print("="*60)
    
    try:
        users = fetch_all("SELECT user_id, fullname, email, role_name, user_status FROM USERS")
        
        if not users:
            print("⚠️  Không có user nào trong database")
            return False
        
        print(f"✅ Tìm thấy {len(users)} users:")
        print(f"\n{'ID':<5} {'Tên':<25} {'Email':<30} {'Role':<12} {'Status'}")
        print("-" * 90)
        
        for user in users:
            print(f"{user['user_id']:<5} {user['fullname']:<25} {user['email']:<30} {user['role_name']:<12} {user['user_status']}")
        
        # Đếm số lượng theo role
        print("\n📊 Thống kê theo role:")
        role_counts = {}
        for user in users:
            role = user['role_name']
            role_counts[role] = role_counts.get(role, 0) + 1
        
        for role, count in sorted(role_counts.items()):
            print(f"   {role}: {count}")
        
        return True
        
    except Exception as e:
        print(f"❌ Lỗi khi truy vấn USERS: {e}")
        return False

def test_books():
    """Kiểm tra bảng BOOKS"""
    print("\n" + "="*60)
    print("📚 KIỂM TRA BẢNG BOOKS")
    print("="*60)
    
    try:
        books = fetch_all("""
            SELECT book_id, title, author, category, total_copies, available_copies, book_status 
            FROM BOOKS 
            LIMIT 10
        """)
        
        if not books:
            print("⚠️  Không có sách nào trong database")
            return False
        
        total_books = fetch_one("SELECT COUNT(*) as count FROM BOOKS")
        print(f"✅ Tìm thấy {total_books['count']} sách (hiển thị 10 cuốn đầu):")
        print(f"\n{'ID':<5} {'Tiêu đề':<40} {'Tác giả':<25} {'Thể loại':<20} {'SL':<4} {'CL':<4} {'Status'}")
        print("-" * 130)
        
        for book in books:
            print(f"{book['book_id']:<5} {book['title']:<40} {book['author']:<25} {book['category']:<20} {book['total_copies']:<4} {book['available_copies']:<4} {book['book_status']}")
        
        # Thống kê theo category
        categories = fetch_all("SELECT category, COUNT(*) as count FROM BOOKS GROUP BY category")
        print("\n📊 Thống kê theo thể loại:")
        for cat in categories:
            print(f"   {cat['category']}: {cat['count']} cuốn")
        
        return True
        
    except Exception as e:
        print(f"❌ Lỗi khi truy vấn BOOKS: {e}")
        return False

def test_transactions():
    """Kiểm tra bảng TRANSACTIONS"""
    print("\n" + "="*60)
    print("📋 KIỂM TRA BẢNG TRANSACTIONS")
    print("="*60)
    
    try:
        transactions = fetch_all("""
            SELECT 
                t.transaction_id,
                u.fullname,
                b.title,
                t.borrow_date,
                t.due_date,
                t.return_date,
                t.transaction_status
            FROM TRANSACTIONS t
            JOIN USERS u ON t.user_id = u.user_id
            JOIN BOOKS b ON t.book_id = b.book_id
            ORDER BY t.transaction_id DESC
            LIMIT 10
        """)
        
        if not transactions:
            print("⚠️  Không có giao dịch nào trong database")
            return False
        
        total = fetch_one("SELECT COUNT(*) as count FROM TRANSACTIONS")
        print(f"✅ Tìm thấy {total['count']} giao dịch (hiển thị 10 giao dịch mới nhất):")
        print(f"\n{'ID':<5} {'Người mượn':<25} {'Sách':<35} {'Ngày mượn':<12} {'Hạn trả':<12} {'Ngày trả':<12} {'Status'}")
        print("-" * 140)
        
        for t in transactions:
            return_date = str(t['return_date']) if t['return_date'] else "Chưa trả"
            print(f"{t['transaction_id']:<5} {t['fullname']:<25} {t['title']:<35} {str(t['borrow_date']):<12} {str(t['due_date']):<12} {return_date:<12} {t['transaction_status']}")
        
        # Thống kê theo status
        statuses = fetch_all("SELECT transaction_status, COUNT(*) as count FROM TRANSACTIONS GROUP BY transaction_status")
        print("\n📊 Thống kê theo trạng thái:")
        for status in statuses:
            print(f"   {status['transaction_status']}: {status['count']}")
        
        return True
        
    except Exception as e:
        print(f"❌ Lỗi khi truy vấn TRANSACTIONS: {e}")
        return False

def test_fines():
    """Kiểm tra bảng FINES"""
    print("\n" + "="*60)
    print("💰 KIỂM TRA BẢNG FINES")
    print("="*60)
    
    try:
        fines = fetch_all("""
            SELECT 
                f.fine_id,
                u.fullname,
                f.fine_amount,
                f.fine_reason,
                f.fine_status
            FROM FINES f
            JOIN USERS u ON f.user_id = u.user_id
        """)
        
        if not fines:
            print("ℹ️  Không có phạt nào trong database")
            return True
        
        print(f"✅ Tìm thấy {len(fines)} khoản phạt:")
        print(f"\n{'ID':<5} {'Người bị phạt':<25} {'Số tiền':<15} {'Lý do':<50} {'Status'}")
        print("-" * 120)
        
        for f in fines:
            print(f"{f['fine_id']:<5} {f['fullname']:<25} {f['fine_amount']:>12,.0f} VND {f['fine_reason']:<50} {f['fine_status']}")
        
        # Tổng hợp
        summary = fetch_one("""
            SELECT 
                SUM(CASE WHEN fine_status = 'UNPAID' THEN fine_amount ELSE 0 END) as unpaid,
                SUM(CASE WHEN fine_status = 'PAID' THEN fine_amount ELSE 0 END) as paid,
                SUM(fine_amount) as total
            FROM FINES
        """)
        
        print("\n📊 Tổng hợp:")
        print(f"   Chưa thanh toán: {summary['unpaid']:,.0f} VND")
        print(f"   Đã thanh toán: {summary['paid']:,.0f} VND")
        print(f"   Tổng cộng: {summary['total']:,.0f} VND")
        
        return True
        
    except Exception as e:
        print(f"❌ Lỗi khi truy vấn FINES: {e}")
        return False

def test_auth():
    """Test đăng nhập với các tài khoản mẫu"""
    print("\n" + "="*60)
    print("🔐 KIỂM TRA ĐĂNG NHẬP")
    print("="*60)
    
    test_accounts = [
        ("admin@library.com", "admin123", "ADMIN"),
        ("librarian@library.com", "lib123", "LIBRARIAN"),
        ("nguyenvana@email.com", "member123", "MEMBER"),
    ]
    
    success_count = 0
    
    for email, password, expected_role in test_accounts:
        try:
            user = fetch_one(
                "SELECT * FROM USERS WHERE email=%s AND password=%s AND user_status='ACTIVE'",
                (email, password)
            )
            
            if user:
                print(f"✅ {expected_role:12} - {email:30} - Login thành công")
                success_count += 1
            else:
                print(f"❌ {expected_role:12} - {email:30} - Login thất bại")
                
        except Exception as e:
            print(f"❌ Lỗi khi test login {email}: {e}")
    
    print(f"\n📊 Kết quả: {success_count}/{len(test_accounts)} tài khoản login thành công")
    return success_count == len(test_accounts)

def main():
    """Chạy tất cả các test"""
    print("\n" + "="*60)
    print("🧪 LIBRARY DATABASE TEST SUITE")
    print("="*60)
    
    results = []
    
    # Test 1: Connection
    results.append(("Kết nối Database", test_connection()))
    
    if results[0][1]:  # Chỉ tiếp tục nếu kết nối thành công
        # Test 2: Users
        results.append(("Bảng USERS", test_users()))
        
        # Test 3: Books
        results.append(("Bảng BOOKS", test_books()))
        
        # Test 4: Transactions
        results.append(("Bảng TRANSACTIONS", test_transactions()))
        
        # Test 5: Fines
        results.append(("Bảng FINES", test_fines()))
        
        # Test 6: Authentication
        results.append(("Đăng nhập", test_auth()))
    
    # Tổng kết
    print("\n" + "="*60)
    print("📊 TỔNG KẾT")
    print("="*60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {test_name}")
    
    print(f"\n🎯 Kết quả: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 Tất cả tests đều PASS! Database hoạt động tốt.")
        print("\n💡 Bạn có thể chạy ứng dụng bằng lệnh: python main.py")
    else:
        print("\n⚠️  Có test FAIL. Vui lòng kiểm tra lại cấu hình.")
        print("\n💡 Gợi ý:")
        print("   1. Kiểm tra MySQL service đã chạy")
        print("   2. Kiểm tra password trong database/db.py")
        print("   3. Chạy lại file library_database_setup.sql")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Test bị ngắt bởi người dùng")
    except Exception as e:
        print(f"\n\n❌ Lỗi không mong đợi: {e}")
        import traceback
        traceback.print_exc()
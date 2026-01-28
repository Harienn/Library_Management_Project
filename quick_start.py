import mysql.connector
from mysql.connector import Error
import sys

# ✅ Đã cấu hình sẵn theo db.py của bạn
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'taolao',
    'database': 'LibraryDB',
    'auth_plugin': 'mysql_native_password'
}

# 🎨 URLs ảnh đẹp từ nhiều nguồn
BOOK_IMAGES = {
    # Sách Việt Nam
    'Tôi thấy hoa vàng trên cỏ xanh': 'https://images-na.ssl-images-amazon.com/images/S/compressed.photo.goodreads.com/books/1626766673i/58455775.jpg',
    'Cho tôi xin một vé đi tuổi thơ': 'https://images-na.ssl-images-amazon.com/images/S/compressed.photo.goodreads.com/books/1626766649i/58455774.jpg',
    'Chí Phèo': 'https://images-na.ssl-images-amazon.com/images/S/compressed.photo.goodreads.com/books/1348690306i/16088141.jpg',
    'Tắt đèn': 'https://images-na.ssl-images-amazon.com/images/S/compressed.photo.goodreads.com/books/1442677487i/26625036.jpg',
    'Dế Mèn phiêu lưu ký': 'https://images-na.ssl-images-amazon.com/images/S/compressed.photo.goodreads.com/books/1415937853i/23648586.jpg',
    'Truyện Kiều': 'https://images-na.ssl-images-amazon.com/images/S/compressed.photo.goodreads.com/books/1442691265i/26625159.jpg',
    'Cánh đồng bất tận': 'https://images-na.ssl-images-amazon.com/images/S/compressed.photo.goodreads.com/books/1415937819i/23648584.jpg',
    
    # Sách nước ngoài
    'Rừng Na Uy': 'https://images-na.ssl-images-amazon.com/images/S/compressed.photo.goodreads.com/books/1448742854i/11297.jpg',
    'Nhà giả kim': 'https://images-na.ssl-images-amazon.com/images/S/compressed.photo.goodreads.com/books/1654371463i/18144590.jpg',
    '1Q84': 'https://images-na.ssl-images-amazon.com/images/S/compressed.photo.goodreads.com/books/1483103331i/10357575.jpg',
    'Harry Potter và Hòn đá phù thủy': 'https://images-na.ssl-images-amazon.com/images/S/compressed.photo.goodreads.com/books/1598823299i/42844155.jpg',
    'Những người khốn khổ': 'https://images-na.ssl-images-amazon.com/images/S/compressed.photo.goodreads.com/books/1411852091i/24280.jpg',
    
    # Sách kỹ năng & khoa học
    'Lược sử thời gian': 'https://images-na.ssl-images-amazon.com/images/S/compressed.photo.goodreads.com/books/1333578746i/3869.jpg',
    'Đắc nhân tâm': 'https://images-na.ssl-images-amazon.com/images/S/compressed.photo.goodreads.com/books/1442726934i/4865.jpg',
    'Tôi tài giỏi, bạn cũng thế': 'https://images-na.ssl-images-amazon.com/images/S/compressed.photo.goodreads.com/books/1348685517i/12657835.jpg',
    'Dạy con làm giàu tập 1': 'https://images-na.ssl-images-amazon.com/images/S/compressed.photo.goodreads.com/books/1388211242i/69571.jpg',
    'Đi tìm lẽ sống': 'https://images-na.ssl-images-amazon.com/images/S/compressed.photo.goodreads.com/books/1535419394i/4069.jpg',
    
    # Sách IT
    'Lập trình Java cơ bản': 'https://images-na.ssl-images-amazon.com/images/S/compressed.photo.goodreads.com/books/1348442512i/15824.jpg',
    'Clean Code': 'https://images-na.ssl-images-amazon.com/images/S/compressed.photo.goodreads.com/books/1436202607i/3735293.jpg',
    
    # Thêm sách khác
    'Góc sân và khoảng trời': 'https://images-na.ssl-images-amazon.com/images/S/compressed.photo.goodreads.com/books/1442691179i/26625146.jpg',
}


def generate_placeholder(title, book_id):
    """Tạo placeholder gradient đẹp"""
    colors = [
        ('667eea', '764ba2'),  # Purple
        ('f093fb', 'f5576c'),  # Pink
        ('4facfe', '00f2fe'),  # Blue
        ('43e97b', '38f9d7'),  # Green
        ('fa709a', 'fee140'),  # Orange
        ('30cfd0', '330867'),  # Teal
    ]
    
    color1, color2 = colors[book_id % len(colors)]
    
    # Lấy chữ cái đầu
    words = title.split()
    if len(words) >= 2:
        text = (words[0][0] + words[1][0]).upper()
    else:
        text = title[:2].upper()
    
    import urllib.parse
    return f"https://ui-avatars.com/api/?name={urllib.parse.quote(text)}&size=400&background={color1}&color=fff&font-size=0.4&bold=true"


def quick_update():
    """Quick update - Fast & Simple"""
    try:
        print("\n" + "="*60)
        print("🚀 QUICK START - ADDING BOOK IMAGES")
        print("="*60 + "\n")
        
        # Kết nối
        print("🔗 Connecting to database...")
        connection = mysql.connector.connect(**DB_CONFIG)
        cursor = connection.cursor(dictionary=True)
        print("✅ Connected!\n")
        
        # Lấy sách
        cursor.execute("SELECT book_id, title FROM BOOKS")
        books = cursor.fetchall()
        
        print(f"📚 Found {len(books)} books\n")
        
        updated = 0
        for book in books:
            book_id = book['book_id']
            title = book['title']
            
            # Tìm ảnh
            if title in BOOK_IMAGES:
                image_url = BOOK_IMAGES[title]
                source = "✅ Real cover"
            else:
                image_url = generate_placeholder(title, book_id)
                source = "🎨 Beautiful placeholder"
            
            # Update
            cursor.execute(
                "UPDATE BOOKS SET image_url = %s WHERE book_id = %s",
                (image_url, book_id)
            )
            
            print(f"[{book_id:2d}] {title[:45]:45s} | {source}")
            updated += 1
        
        connection.commit()
        
        print("\n" + "="*60)
        print(f"✅ SUCCESS! Updated {updated} books!")
        print("="*60)
        
        # Stats
        cursor.execute("""
            SELECT 
                COUNT(*) as total,
                SUM(CASE WHEN image_url LIKE '%goodreads%' OR image_url LIKE '%amazon%' THEN 1 ELSE 0 END) as real,
                SUM(CASE WHEN image_url LIKE '%ui-avatars%' THEN 1 ELSE 0 END) as placeholder
            FROM BOOKS
        """)
        stats = cursor.fetchone()
        
        print(f"\n📊 Statistics:")
        print(f"   • Real book covers: {stats['real']}")
        print(f"   • Beautiful placeholders: {stats['placeholder']}")
        print(f"   • Total: {stats['total']}")
        
        print("\n💡 Next steps:")
        print("   1. Restart your Flet app: python main.py")
        print("   2. Go to Books page")
        print("   3. Enjoy beautiful book covers! 🎉")
        
        cursor.close()
        connection.close()
        
        return True
        
    except Error as e:
        print(f"\n❌ Database Error: {e}")
        print("\n💡 Troubleshooting:")
        print("   1. Make sure MySQL is running")
        print("   2. Check database credentials in DB_CONFIG")
        print("   3. Verify LibraryDB exists")
        return False
    
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False


def check_status():
    """Kiểm tra trạng thái nhanh"""
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        cursor = connection.cursor(dictionary=True)
        
        cursor.execute("""
            SELECT 
                COUNT(*) as total,
                SUM(CASE WHEN image_url IS NOT NULL AND image_url != '' THEN 1 ELSE 0 END) as with_images,
                SUM(CASE WHEN image_url IS NULL OR image_url = '' THEN 1 ELSE 0 END) as without_images
            FROM BOOKS
        """)
        
        stats = cursor.fetchone()
        
        print("\n" + "="*60)
        print("📊 CURRENT STATUS")
        print("="*60)
        print(f"\nTotal books: {stats['total']}")
        print(f"✅ Books with images: {stats['with_images']}")
        print(f"❌ Books without images: {stats['without_images']}")
        
        if stats['with_images'] == stats['total']:
            print("\n🎉 All books have images! Perfect!")
        elif stats['with_images'] > 0:
            percentage = (stats['with_images'] / stats['total']) * 100
            print(f"\n📈 Coverage: {percentage:.1f}%")
        else:
            print("\n⚠️  No images yet. Run 'python quick_start.py update' to add them!")
        
        print("="*60 + "\n")
        
        cursor.close()
        connection.close()
        
    except Error as e:
        print(f"\n❌ Cannot connect to database: {e}")
        print("Make sure MySQL is running and credentials are correct.\n")


if __name__ == "__main__":
    print("""
╔═══════════════════════════════════════════════════════════╗
║              📚 QUICK START - BOOK IMAGES                ║
║                  Fast & Simple Setup                      ║
╚═══════════════════════════════════════════════════════════╝
    """)
    
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        
        if command == 'update':
            success = quick_update()
            sys.exit(0 if success else 1)
        
        elif command == 'status':
            check_status()
            sys.exit(0)
        
        elif command == 'help':
            print("""
📖 USAGE:
    python quick_start.py update   - Add images to all books
    python quick_start.py status   - Check current status
    python quick_start.py help     - Show this help

✨ FEATURES:
    • Real book covers from Goodreads
    • Beautiful gradient placeholders for missing books
    • Fast execution (< 10 seconds)
    • Already configured with your database credentials
    • Safe - only updates books without images

💡 TIP: Just run 'python quick_start.py update' to get started!
            """)
            sys.exit(0)
        
        else:
            print(f"❌ Unknown command: {command}")
            print("Usage: python quick_start.py [update|status|help]")
            sys.exit(1)
    
    else:
        # Interactive mode
        print("\nWhat do you want to do?")
        print("  1. Add images to books (recommended)")
        print("  2. Check current status")
        print("  q. Quit")
        
        choice = input("\nYour choice (1/2/q): ").strip()
        
        if choice == '1':
            quick_update()
        elif choice == '2':
            check_status()
        elif choice.lower() == 'q':
            print("\n👋 Goodbye!")
        else:
            print("\n❌ Invalid choice")
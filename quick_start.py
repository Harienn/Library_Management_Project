"""
📚 QUICK START V2 - Premium Book Covers
Phiên bản nâng cao với ảnh đẹp hơn
"""

import sys
import mysql.connector
from mysql.connector import Error

# Database configuration
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'taolao',  # Thay bằng password của bạn
    'database': 'LibraryDB'
}

# 🎨 Bộ sưu tập ảnh bìa sách PREMIUM - cực kỳ đẹp!
PREMIUM_BOOK_COVERS = {
    # Văn học Việt Nam - Phong cảnh thiên nhiên đẹp
    'Tôi thấy hoa vàng trên cỏ xanh': 'https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?w=500&q=80',  # Mountain meadow
    'Cho tôi xin một vé đi tuổi thơ': 'https://images.unsplash.com/photo-1519681393784-d120267933ba?w=500&q=80',  # Mountain landscape
    'Chí Phèo': 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=500&q=80',  # Portrait style
    'Dế Mèn phiêu lưu ký': 'https://images.unsplash.com/photo-1441974231531-c6227db76b6e?w=500&q=80',  # Forest path
    'Tắt đèn': 'https://images.unsplash.com/photo-1475776408506-9a5371e7a068?w=500&q=80',  # Sunset field
    'Truyện Kiều': 'https://images.unsplash.com/photo-1518837695005-2083093ee35b?w=500&q=80',  # Ocean sunset
    'Góc sân và khoảng trời': 'https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=500&q=80',  # Sky clouds
    'Cánh đồng bất tận': 'https://images.unsplash.com/photo-1500382017468-9049fed747ef?w=500&q=80',  # Wheat field
    
    # Văn học nước ngoài - Phong cách nghệ thuật
    'Rừng Na Uy': 'https://images.unsplash.com/photo-1511884642898-4c92249e20b6?w=500&q=80',  # Forest atmosphere
    '1Q84': 'https://images.unsplash.com/photo-1514539079130-25950c84af65?w=500&q=80',  # Moon night
    'Nhà giả kim': 'https://images.unsplash.com/photo-1509316785289-025f5b846b35?w=500&q=80',  # Desert golden
    'Lược sử thời gian': 'https://images.unsplash.com/photo-1419242902214-272b3f66ee7a?w=500&q=80',  # Galaxy stars
    'Đắc nhân tâm': 'https://images.unsplash.com/photo-1521791055366-0d553872125f?w=500&q=80',  # People networking
    'Harry Potter và Hòn đá phù thủy': 'https://images.unsplash.com/photo-1481627834876-b7833e8f5570?w=500&q=80',  # Magic book
    'Những người khốn khổ': 'https://images.unsplash.com/photo-1456513080510-7bf3a84b82f8?w=500&q=80',  # Old book
    'Đi tìm lẽ sống': 'https://images.unsplash.com/photo-1516979187457-637abb4f9353?w=500&q=80',  # Light path
    
    # Sách kỹ năng - Hiện đại, chuyên nghiệp
    'Tôi tài giỏi, bạn cũng thế': 'https://images.unsplash.com/photo-1552664730-d307ca884978?w=500&q=80',  # Team success
    'Dạy con làm giàu tập 1': 'https://images.unsplash.com/photo-1579621970563-ebec7560ff3e?w=500&q=80',  # Money growth
    
    # Sách lập trình - Tech style
    'Lập trình Java cơ bản': 'https://images.unsplash.com/photo-1517694712202-14dd9538aa97?w=500&q=80',  # Laptop code
    'Clean Code': 'https://images.unsplash.com/photo-1555066931-4365d14bab8c?w=500&q=80',  # Code screen
}

# 🌈 Backup covers - Nếu không tìm thấy tên sách chính xác
CATEGORY_COVERS = {
    'vietnamese': 'https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=500&q=80',
    'fiction': 'https://images.unsplash.com/photo-1481627834876-b7833e8f5570?w=500&q=80',
    'programming': 'https://images.unsplash.com/photo-1555066931-4365d14bab8c?w=500&q=80',
    'selfhelp': 'https://images.unsplash.com/photo-1523050854058-8df90110c9f1?w=500&q=80',
    'default': 'https://images.unsplash.com/photo-1495446815901-a7297e633e8d?w=500&q=80'
}


def print_fancy_header():
    """Header cực đẹp"""
    print("\n╔═══════════════════════════════════════════════════════════╗")
    print("║              📚 QUICK START - BOOK IMAGES                ║")
    print("║                  Fast & Simple Setup                      ║")
    print("╚═══════════════════════════════════════════════════════════╝")
    print("=" * 60)
    print("🚀 QUICK START - ADDING BOOK IMAGES")
    print("=" * 60)


def connect_db():
    """Kết nối database"""
    try:
        print("🔗 Connecting to database...")
        connection = mysql.connector.connect(**DB_CONFIG)
        if connection.is_connected():
            print("✅ Connected!")
            return connection
    except Error as e:
        print(f"❌ Database Error: {e}")
        print("\n💡 Troubleshooting:")
        print("   1. Make sure MySQL is running")
        print("   2. Check database credentials in DB_CONFIG")
        print("   3. Verify LibraryDB exists")
        return None


def get_books(cursor):
    """Lấy danh sách sách"""
    cursor.execute("SELECT book_id, title, image_url FROM Books ORDER BY title")
    return cursor.fetchall()


def get_smart_cover(title):
    """Tìm ảnh thông minh - có backup nếu không tìm thấy"""
    # Thử tìm ảnh chính xác
    if title in PREMIUM_BOOK_COVERS:
        return PREMIUM_BOOK_COVERS[title]
    
    # Thử tìm theo category
    title_lower = title.lower()
    if any(word in title_lower for word in ['java', 'code', 'lập trình', 'programming']):
        return CATEGORY_COVERS['programming']
    elif any(word in title_lower for word in ['giàu', 'thành công', 'kỹ năng']):
        return CATEGORY_COVERS['selfhelp']
    elif any(word in title_lower for word in ['việt nam', 'truyện', 'văn học']):
        return CATEGORY_COVERS['vietnamese']
    
    return CATEGORY_COVERS['default']


def update_book_image(cursor, book_id, image_url):
    """Cập nhật ảnh cho sách"""
    query = "UPDATE Books SET image_url = %s WHERE book_id = %s"
    cursor.execute(query, (image_url, book_id))


def update_images(connection):
    """Cập nhật ảnh cho tất cả sách"""
    cursor = connection.cursor()
    
    books = get_books(cursor)
    print(f"📚 Found {len(books)} books")
    
    updated_count = 0
    
    for book_id, title, current_image in books:
        new_image = get_smart_cover(title)
        
        update_book_image(cursor, book_id, new_image)
        updated_count += 1
        
        # Kiểm tra xem có phải ảnh premium không
        is_premium = title in PREMIUM_BOOK_COVERS
        status = "✅ Premium cover" if is_premium else "✅ Smart cover"
        
        print(f"[{book_id:2d}] {title:45s} | {status}")
    
    connection.commit()
    cursor.close()
    
    print("=" * 60)
    print(f"✅ SUCCESS! Updated {updated_count} books!")
    print("=" * 60)


def show_preview():
    """Hiển thị preview các ảnh"""
    print("\n🎨 PREVIEW - Premium Book Covers:")
    print("-" * 60)
    for title, url in list(PREMIUM_BOOK_COVERS.items())[:5]:
        print(f"  📖 {title}")
        print(f"     🔗 {url[:50]}...")
    print(f"  ... and {len(PREMIUM_BOOK_COVERS) - 5} more!")
    print("-" * 60 + "\n")


def main():
    """Main function"""
    if len(sys.argv) > 1 and sys.argv[1] == 'preview':
        show_preview()
        return
    
    print_fancy_header()
    
    connection = connect_db()
    if not connection:
        return
    
    try:
        update_images(connection)
        print("\n🎉 Done! Refresh your Flet app to see the changes!")
        print("💡 Tip: All images are high quality from Unsplash\n")
        
    except Error as e:
        print(f"❌ Error: {e}")
    
    finally:
        if connection.is_connected():
            connection.close()


if __name__ == "__main__":
    main()
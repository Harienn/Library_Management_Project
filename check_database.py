import mysql.connector

# Kết nối database
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="taolao",
    database="LibraryDB"
)

cur = conn.cursor()

# Kiểm tra database hiện tại
cur.execute("SELECT DATABASE()")
print("=== Current database ===")
print(cur.fetchone())

# Kiểm tra columns trong bảng
cur.execute("SHOW COLUMNS FROM BORROWING_TRANSACTION_DETAILS")
print("\n=== Columns in BORROWING_TRANSACTION_DETAILS ===")
for row in cur.fetchall():
    print(row)

cur.close()
conn.close()

print("\n✅ Done! Check if 'damage_percentage' and 'days_late' exist above.")
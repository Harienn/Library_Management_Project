from database.db import fetch_all

users = fetch_all("SELECT user_id, fullname, role_name FROM USERS")
print(users)

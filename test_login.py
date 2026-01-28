from auth_service import login

user = login("nguyenvana@email.com", "hashed_password_1")

if user:
    print(user["fullname"], user["role_name"])
else:
    print("Login failed")

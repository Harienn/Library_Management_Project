# run.py
import sys
sys.dont_write_bytecode = True

import flet as ft

# Import sau khi set dont_write_bytecode
from views.home_view import HomeView
from views.books_view import BooksView
from views.book_detail_view import BookDetailView
from views.login_view import LoginView
from views.register_view import RegisterView
from views.my_borrowing_view import MyBorrowingView
from views.my_profile_view import MyProfileView
from views.instruction_view import InstructionView


class LibraryApp:
    def __init__(self, page: ft.Page):
        self.page = page
        self.page.title = "Library System"
        self.page.theme_mode = ft.ThemeMode.LIGHT
        self.page.padding = 0
        self.current_user = None
        self.page.on_route_change = self.route_change
        self.page.on_view_pop = self.view_pop
        self.navigate("/")
    
    def route_change(self, e):
        route = self.page.route
        self.page.views.clear()
        
        if route == "/":
            view = HomeView(self.page, self.current_user, self.navigate)
        elif route == "/books":
            view = BooksView(self.page, self.current_user, self.navigate)
        elif route == "/book_detail":
            view = BookDetailView(self.page, self.current_user, self.navigate)
        elif route == "/login":
            view = LoginView(self.page, self.on_login, self.navigate)
        elif route == "/register":
            view = RegisterView(self.page, self.navigate)
        elif route == "/my_borrowing":
            view = MyBorrowingView(self.page, self.current_user, self.navigate)
        elif route == "/my_profile":
            view = MyProfileView(self.page, self.current_user, self.navigate)
        elif route == "/instruction":
            view = InstructionView(self.page, self.current_user, self.navigate)
        else:
            view = HomeView(self.page, self.current_user, self.navigate)
        
        self.page.views.append(view.build())
        self.page.update()
    
    def view_pop(self, e):
        self.page.views.pop()
        top_view = self.page.views[-1]
        self.navigate(top_view.route)
    
    def navigate(self, route):
        self.page.route = route
        self.route_change(None)
    
    def on_login(self, user):
        self.current_user = user
        self.navigate("/")


def main(page: ft.Page):
    LibraryApp(page)


if __name__ == "__main__":
    ft.app(target=main)

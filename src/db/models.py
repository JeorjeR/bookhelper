from dataclasses import dataclass


@dataclass
class Book:
    table_name: str = 'books'
    book_id: int = 'book_id'
    book_name: str = 'book_name'
    pages: tuple = 'pages'
    user_id: int = 'user_id'


@dataclass
class User:
    table_name: str = 'users'
    user_id: int = 'user_id'
    user_name: str = 'user_name'


user = User()
book = Book()




from src.db.models import user, book

CREATE_USER_TABLE = f"""
CREATE TABLE {user.table_name}(
    {user.user_id} SERIAL PRIMARY KEY,
    {user.user_name} varchar(40) NOT NULL,
    UNIQUE ({user.user_name})
);
"""

CREATE_BOOK_TABLE = f"""
CREATE TABLE {book.table_name}(
    {book.book_id} SERIAL PRIMARY KEY,
    {book.book_name} varchar(255) NOT NULL,
    {book.pages} bytea[] NOT NULL,
    FOREIGN KEY ({book.user_id}) REFERENCES users ({user.user_id}) ON DELETE CASCADE,     
    UNIQUE ({book.book_name}, {user.user_id})
);   
"""

INSERT_USER = f"""
    INSERT INTO {user.table_name} VALUES($1, $2);
"""

INSERT_USER_BOOK = f"""
    INSERT INTO {book.table_name} VALUES ($1, $2, $3, $4);
"""

DELETE_USER_BOOK = f"""
    DELETE FROM {book.table_name} WHERE {book.user_id} = $1, {book.book_id} = $2;
"""

DELETE_USER = f"""
    DELETE FROM {user.table_name} WHERE {user.user_id} = $1;
"""

GET_USER_BOOK_PAGE = f"""
    SELECT {book.pages}[$3] FROM {book.table_name} WHERE {book.book_id} = $2 AND {book.user_id} = $1;
"""

GET_BOOK = f"""
    SELECT {book.pages} FROM {book.table_name} WHERE {book.book_id} = $1;
"""



CREATE_USER_TABLE = """
CREATE TABLE users(
    user_id SERIAL PRIMARY KEY,
    user_name varchar(40) NOT NULL,
    UNIQUE (user_name)
);
"""

CREATE_BOOK_TABLE = """
CREATE TABLE books(
    book_id SERIAL PRIMARY KEY,
    book_name varchar(255) NOT NULL,
    pages bytea[] NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users (user_id) ON DELETE CASCADE,     
    UNIQUE (book_name, user_id)
);   
"""

INSERT_USER = """
    INSERT INTO users VALUES($1, $2);
"""

INSERT_USER_BOOK = """
    INSERT INTO books VALUES ($1, $2, $3, $4);
"""

DELETE_USER_BOOK = """
    DELETE FROM books WHERE user_id = $1, book_id = $2;
"""

DELETE_USER = """
    DELETE FROM users WHERE user_id = $1;
"""

GET_USER_BOOK_PAGE = """
    SELECT pages[$3] FROM book WHERE book_id = $2 AND user_id = $1;
"""

GET_BOOK = """
    SELECT pages FROM books WHERE book_id = $1;
"""
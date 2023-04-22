import os
from types import MappingProxyType
import asyncpg
from asyncpg import Connection, Pool
from asyncpg.pool import PoolAcquireContext

from src.db import queries

CONNECTION_SETTINGS = MappingProxyType(dict(
        host=os.environ.get('HOST'),
        port=os.environ.get('PORT'),
        user=os.environ.get('USER'),
        password=os.environ.get('PASSWORD'),
        database=os.environ.get('DATABASE'),
))


class BookHelperAPI:
    def __init__(self, connection_pool: Pool):
        self.connection_pool: Pool = connection_pool
        book_table = 'books'
        user_table = 'users'

    #TODO посмотреть как вставлять значения asyncpg и будет готов каркас

    async def get_book_page(self, book_id: int, page_number: int):
        ...

    async def do_query(self, query, *args):
        async with self.connection_pool.acquire() as connection:
            connection: Connection
            # TODO передать сюда еще метод который к базе применяется,
            #   не всегда он будет fetchval
            await connection.fetchval(query, *args)

    async def get_book(self, book_id: int):
        return await self.do_query(queries.GET_BOOK, book_id)

    def get_user(self, user_id: int):
        ...

    def add_user_book(self, user_id):
        ...

    def add_user(self):
        ...


class BookHelperDB:
    def __init__(self, settings: dict):
        self.settings = settings

    @property
    def connection_settings(self) -> MappingProxyType:
        connection_settings: MappingProxyType = MappingProxyType({
            key: new_value if (new_value := self.connection_settings.get(key, None)) else value
            for key, value in CONNECTION_SETTINGS
        })
        return connection_settings

    async def connect(self) -> Connection:
        connection: Connection = await asyncpg.connect(self.connection_settings)
        return connection

    async def create_pool(self) -> Pool:
        return await asyncpg.create_pool(**self.connection_settings)

    # TODO Переделать через асинхронный контекстный менеджер
    #   типо создаем пул в этом классе а потом в query_api возвращаем класс контекстного менежера
    #   и по нему уже делаем соединение из пула
    #   типо
    #   db = DB(**settings)
    #   with db.query_api() as connection:
    #       await connection.get_book(...)
    #       ...

    async def query_api(self) -> BookHelperAPI:
        return BookHelperAPI(await self.create_pool())

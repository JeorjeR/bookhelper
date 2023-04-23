import os
from types import MappingProxyType
import asyncpg
from asyncpg import Connection, Pool
from src.db import queries


CONNECTION_SETTINGS = MappingProxyType(dict(
        host=os.environ.get('HOST'),
        port=os.environ.get('PORT'),
        user=os.environ.get('USER'),
        password=os.environ.get('PASSWORD'),
        database=os.environ.get('DATABASE'),
))


class Singleton:
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'):
            cls.instance = super().__new__(cls, *args, **kwargs)
        return cls.instance


class BookHelperAPI(Singleton):
    def __init__(self, connection_pool: Pool):
        self.connection_pool: Pool = connection_pool

    async def get_book_page(self, book_id: int, page_number: int):
        ...

    async def execute(self, query, *args):
        async with self.connection_pool.acquire() as connection:
            connection: Connection
            # TODO передать сюда еще метод который к базе применяется,
            #   не всегда он будет fetchval
            await connection.fetchval(query, *args)

    async def get_book(self, book_id: int):
        return await self.execute(queries.GET_BOOK, book_id)

    def get_user(self, user_id: int):
        ...

    def add_user_book(self, user_id):
        ...

    def add_user(self):
        ...


class BookHelperDB(Singleton):
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
        return await asyncpg.connect(self.connection_settings)

    async def create_pool(self) -> Pool:
        return await asyncpg.create_pool(**self.connection_settings)

    async def query_api(self) -> BookHelperAPI:
        return BookHelperAPI(await self.create_pool())

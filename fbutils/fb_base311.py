from collections import namedtuple
from typing import Any, Callable, Iterator

from firebird.driver import Connection, Cursor, DBKeyScope, connect
from firebird.driver.interfaces import (iAttachment, iBlob,
                                        iCryptKeyCallbackImpl, iDtc,
                                        iMessageMetadata, iResultSet, iService,
                                        iStatement, iTransaction)


class Fetch:
    """
    Формат получения данных из SQL запроса
    """
    class All:
        """
        Все записи
        """
        @staticmethod
        def dictfetch(cur: Cursor) -> list[dict[str, Any]]:
            columns = [col[0] for col in cur.description]
            return [dict(zip(columns, row)) for row in cur.fetchall()]

        @staticmethod
        def namedtuplefetch(cur: Cursor) -> list[namedtuple]:
            nt_result = namedtuple(
                '_', [col[0] for col in cur.description])
            return [nt_result(*row) for row in cur.fetchall()]

        @staticmethod
        def fetchall(cursor: Cursor) -> list[tuple[Any, ...]]:
            return cursor.fetchall()

    class One:
        """
        Одна запись
        """
        @staticmethod
        def namedtuplefetch(cur: Cursor, row: tuple[Any, ...]) -> list[namedtuple]:
            nt_result = namedtuple(
                '_', [col[0] for col in cur.description])
            return nt_result(*row)

        @staticmethod
        def dictfetch(cur: Cursor, row: tuple[Any, ...]) -> list[dict[str, Any]]:
            columns = [col[0] for col in cur.description]
            return dict(zip(columns, row))

        @staticmethod
        def fetchone(cursor: Cursor) -> list[Any]:
            return cursor.fetchone()


class _AutoCommit:
    """
    Реализация логики автокомита
    """

    def __init__(self, connect: Connection):
        self.connect = connect

    def __enter__(self):
        return None

    def __exit__(self, exct_type, exce_value, traceback):
        # На случай если не работает авто коммит, то коммитем в ручную
        if not self.connect.is_closed():
            self.connect.commit()

    def __repr__(self):
        return self.connect.__repr__()


class FB:
    def __init__(self, connect: Connection, *, func_fetchAll: Fetch.All = Fetch.All.fetchall, func_fetchOne: Fetch.One = lambda c, r: r):
        self.connect: Connection = connect
        self.func_fetchAll: Callable[[Cursor], Any] = func_fetchAll
        self.func_fetchOne: Callable[
            [Cursor, tuple[Any, ...]], Any] = func_fetchOne
        # Если нет ошибок то, подключение успешно
        print(self.connect)

    def connect(database: str, *, user: str = None, password: str = None, role: str = None,
                no_gc: bool = None, no_db_triggers: bool = None, dbkey_scope: DBKeyScope = None,
                crypt_callback: iCryptKeyCallbackImpl = None, charset: str = None,
                auth_plugin_list: str = None, session_time_zone: str = None) -> Connection:
        """
        Подключиться к БД
        
        :params database: URL к БД
        :params user: Имя пользователя
        :params password: Пароль пользователя
        :params role: Роль пользователя
        :params charset: Кодировка работы с БД
        """
        return connect(
            database=database,
            user=user,
            password=password,
            role=role,
            charset=charset,
        )

    def writeOne(self, sql: str, *, params: list[Any] = None) -> bool:
        """
        Команда на одной запись

        - insert into
        """
        with self.connect.cursor() as cur:
            cur: Cursor
            with _AutoCommit(self.connect):
                cur.execute(sql,params)

    def writeMany(self, sql: str, *, params: list[tuple[Any, ...]] = None) -> bool:
        """
        Команда на нескольких запись 

        - insert into
        """
        with self.connect.cursor() as cur:
            cur: Cursor
            with _AutoCommit(self.connect):
                cur.executemany(sql, params)

    def readRow(self, sql: str, params: list[tuple[Any, ...]] = None) -> Iterator[list[Any]]:
        """
        Команда на чтение, результат будет построчным итератором
        """
        with self.connect.cursor() as cur:
            cur: Cursor
            with _AutoCommit(self.connect):
                cur.execute(sql, params)
                for row in cur:
                    yield self.func_fetchOne(cur, row)

    def readAll(self, sql: readRow, params: list[tuple[Any, ...]] = None) -> list[Any]:
        """
        Команда на чтение, результат будет все строки
        """
        with self.connect.cursor() as cur:
            cur: Cursor
            with _AutoCommit(self.connect):
                cur.execute(sql, params)
                return self.func_fetchAll(cur)

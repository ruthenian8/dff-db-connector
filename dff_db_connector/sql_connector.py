"""
sql_connector
---------------------------

| Provides the sql-based version of the :py:class:`~dff_db.connector.dff_db_connector.DffDbConnector`.
| You can choose the backend option of your liking from mysql, postgresql, or sqlite.

"""
import json
import importlib

from .dff_db_connector import DffDbConnector
from df_engine.core.context import Context

try:
    from sqlalchemy import create_engine, Table, MetaData, Column, JSON, Integer, inspect, select, delete, func

    sqlalchemy_available = True
except (ImportError, ModuleNotFoundError):
    sqlalchemy_available = False

postgres_available = sqlite_available = mysql_available = False

try:
    import psycopg2

    postgres_available = True
except (ImportError, ModuleNotFoundError):
    pass

try:
    import pymysql

    mysql_available = True
except (ImportError, ModuleNotFoundError):
    pass

try:
    import sqlite3

    sqlite_available = True
except (ImportError, ModuleNotFoundError):
    pass

if not sqlalchemy_available:
    postgres_available = sqlite_available = mysql_available = False


def import_insert_for_dialect(dialect: str):
    """
    Imports the insert function into global scope depending on the chosen sqlalchemy dialect.
    """
    global insert
    insert = getattr(
        importlib.import_module(f"sqlalchemy.dialects.{dialect}"),
        "insert",
    )


class SqlConnector(DffDbConnector):
    """
    | Sql-based version of the :py:class:`~dff_db.connector.dff_db_connector.DffDbConnector`.
    | Compatible with MySQL, Postgresql, Sqlite.

    Parameters
    -----------

    path: str
        Standard sqlalchemy URI string.
        When using sqlite backend in Windows, keep in mind that you have to use double backslashes '\\'
        instead of forward slashes '/' in the file path.
    table_name: str
        The name of the table to use.
    custom_driver: bool
        If you intend to use some other database driver instead of the recommended ones,
        set this parameter to `True` to bypass the import checks.
    """

    def __init__(self, path: str, table_name: str = "contexts", custom_driver: bool = False):
        super(SqlConnector, self).__init__(path)

        self._check_availability(custom_driver)
        self.engine = create_engine(self.full_path)
        self.metadata = MetaData()
        self.table = Table(
            table_name,
            self.metadata,
            Column("id", Integer, primary_key=True),
            Column("context", JSON),  # column for storing serialized contexts
        )

        if not inspect(self.engine).has_table(self.table.name):  # create table if it does not exist
            self.table.create(self.engine)

        self.dialect: str = self.engine.dialect.name
        import_insert_for_dialect(self.dialect)

    def __setitem__(self, key: str, value: Context) -> None:
        if isinstance(value, Context):
            value = value.dict()

        if not isinstance(value, dict):
            raise TypeError(f"The saved value should be a dict or a dict-serializeable item, not {type(value)}")

        insert_stmt = insert(self.table).values(id=int(key), context=value)
        update_stmt = self._get_update_stmt(insert_stmt)

        with self.engine.connect() as conn:
            conn.execute(update_stmt)

    def __getitem__(self, key: str) -> Context:
        stmt = select(self.table.c.context).where(self.table.c.id == key)
        with self.engine.connect() as conn:
            result = conn.execute(stmt)
            row = result.fetchone()
            if row:
                return Context.cast(row[0])
        raise KeyError

    def __delitem__(self, key: str) -> None:
        stmt = delete(self.table).where(self.table.c.id == key)
        with self.engine.connect() as conn:
            conn.execute(stmt)

    def __contains__(self, key: str) -> bool:
        stmt = select(self.table.c.context).where(self.table.c.id == key)
        with self.engine.connect() as conn:
            result = conn.execute(stmt)
            return bool(result.fetchone())

    def __len__(self) -> int:
        stmt = select([func.count()]).select_from(self.table)
        with self.engine.connect() as conn:
            result = conn.execute(stmt)
            return result.fetchone()[0]

    def clear(self) -> None:
        stmt = delete(self.table).where(self.table.c.id > 0)
        with self.engine.connect() as conn:
            conn.execute(stmt)

    def _get_update_stmt(self, insert_stmt):
        if self.dialect == "mysql":
            update_stmt = insert_stmt.on_duplicate_key_update(context=insert_stmt.inserted.context)
        else:
            update_stmt = insert_stmt.on_conflict_do_update(
                index_elements=["id"], set_=dict(context=insert_stmt.excluded.context)
            )
        return update_stmt

    def _check_availability(self, custom_driver: bool) -> None:
        if not custom_driver:
            if self.full_path.startswith("postgresql") and not postgres_available:
                raise ImportError("Packages `sqlalchemy` and/or `psycopg2` are missing.")
            elif self.full_path.startswith("mysql") and not mysql_available:
                raise ImportError("Packages `sqlalchemy` and/or `pymysql` are missing.")
            elif self.full_path.startswith("sqlite") and not sqlite_available:
                raise ImportError("Package `sqlite3` is missing")

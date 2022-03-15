from .dff_db_connector import DffDbConnector
from df_engine.core.context import Context


class PostgresConnector(DffDbConnector):
    def __init__(self, path: str):
        super(PostgresConnector, self).__init__(path)

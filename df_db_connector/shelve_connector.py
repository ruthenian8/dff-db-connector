"""
shelve_connector
---------------------------
Provides the shelve-based version of the :py:class:`~df_db.connector.db_connector.DBConnector`.
"""
import os
import pickle
from shelve import DBfilenameShelf

from df_engine.core import Context

from .db_connector import DBConnector, threadsafe_method


class ShelveConnector(DBfilenameShelf, DBConnector):
    """
    Implements :py:class:`~df_db.connector.db_connector.DBConnector` with `shelve` as the driver.

    Parameters
    -----------

    path: str
        Target file URI. Example: `shelve://file.db`
    """

    def __init__(self, path: str):
        DBConnector.__init__(self, path)

        DBfilenameShelf.__init__(self, filename=self.path, protocol=pickle.HIGHEST_PROTOCOL)

    def __del__(self):
        self.close()

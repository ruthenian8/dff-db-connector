"""
shelve_connector
---------------------------
Provides the shelve-based version of the :py:class:`~df_db.connector.df_db_connector.DFDbConnector`.
"""
import os
import pickle
from shelve import DbfilenameShelf

from df_engine.core import Context

from .df_db_connector import DFDbConnector, threadsafe_method


class ShelveConnector(DbfilenameShelf, DFDbConnector):
    """
    Implements :py:class:`~df_db.connector.df_db_connector.DFDbConnector` with `shelve` as the driver.

    Parameters
    -----------

    path: str
        Target file URI. Example: `shelve://file.db`
    """

    def __init__(self, path: str):
        DFDbConnector.__init__(self, path)

        DbfilenameShelf.__init__(self, filename=self.path, protocol=pickle.HIGHEST_PROTOCOL)

    def __del__(self):
        self.close()

"""
shelve_connector
---------------------------
Provides the shelve-based version of the :py:class:`~dff_db.connector.dff_db_connector.DffDbConnector`.
"""
import os
import pickle
from shelve import DbfilenameShelf

from .dff_db_connector import DffDbConnector


class ShelveConnector(DbfilenameShelf, DffDbConnector):
    """
    Implements :py:class:`~dff_db.connector.dff_db_connector.DffDbConnector` with `shelve` as the driver.

    Parameters
    -----------

    path: str
        Target file URI. Example: `shelve://file.db`
    """

    def __init__(self, path: str):
        DffDbConnector.__init__(self, path)
        dirs = self.path.rsplit('/', maxsplit=1)[0]
        if dirs and not os.path.isdir(dirs):
            os.makedirs(dirs, exist_ok=True)

        DbfilenameShelf.__init__(self, filename=self.path, protocol=pickle.HIGHEST_PROTOCOL)

    def __del__(self):
        self.close()

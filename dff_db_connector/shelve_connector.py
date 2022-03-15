from shelve import DbfilenameShelf
import pickle

from .dff_db_connector import DffDbConnector


class ShelveConnector(DbfilenameShelf, DffDbConnector):
    def __init__(self, path: str):
        DffDbConnector.__init__(self, path)
        DbfilenameShelf.__init__(self, filename=self.path, protocol=pickle.HIGHEST_PROTOCOL)

    def __del__(self):
        self.close()

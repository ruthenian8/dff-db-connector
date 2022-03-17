import pickle
import os

from .dff_db_connector import DffDbConnector
from df_engine.core.context import Context


class PickleConnector(DffDbConnector):
    def __init__(self, path):
        DffDbConnector.__init__(self, path)
        self._load()

    def __len__(self):
        return len(self.dict)

    def __setitem__(self, key: str, item: Context) -> None:
        self.dict.__setitem__(key, item)
        self._save()

    def __getitem__(self, key: str) -> Context:
        self._load()
        return self.dict.__getitem__(key)

    def __delitem__(self, key: str) -> None:
        self.dict.__delitem__(key)
        self._save()

    def __contains__(self, key: str) -> bool:
        self._load()
        return self.dict.__contains__(key)

    def clear(self) -> None:
        self.dict.clear()

    def _save(self) -> None:
        with open(self.path, "wb+") as file:
            pickle.dump(self.dict, file)

    def _load(self) -> None:
        if not os.path.isfile(self.path) or os.stat(self.path).st_size == 0:
            self.dict = dict()
            open(self.path, "a").close()
        else:
            with open(self.path, "rb") as file:
                self.dict = pickle.load(file)

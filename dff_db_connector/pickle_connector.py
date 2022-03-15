import pickle
import os

from .dff_db_connector import DffDbConnector
from df_engine.core.context import Context


class PickleConnector(dict, DffDbConnector):
    def __new__(cls, path: str):
        obj = dict.__new__(cls)
        return obj

    def __init__(self, path: str):
        DffDbConnector.__init__(self, path)
        if not os.path.isfile(self.path):
            open(self.path, "a").close()

    def __getitem__(self, key: str) -> Context:
        self._load()
        value = dict.__getitem__(self, key)
        return Context.cast(value)

    def __setitem__(self, key: str, value: Context) -> None:
        if isinstance(value, Context):
            value_dict = value.dict()
        dict.__setitem__(self, key, value_dict)
        self._save()

    def __delitem__(self, key: str):
        dict.__delitem__(self, key)
        self._save()

    def __del__(self) -> None:
        self._save()

    def _save(self) -> None:
        with open(self.path, "wb+") as file_stream:
            pickle.dump(self, file_stream, protocol=pickle.HIGHEST_PROTOCOL)

    def __getnewargs_ex__(self):
        return ((self.full_path,), dict())

    def _load(self) -> None:
        if os.stat(self.path).st_size > 0:
            with open(self.path, "rb") as file_stream:
                saved_values = pickle.load(file_stream)
        else:
            saved_values = dict()
        self.update(saved_values)

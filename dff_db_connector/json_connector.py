"""
json_connector
---------------------------
Provides the json-based version of the :py:class:`~dff_db.connector.dff_db_connector.DffDbConnector`.
"""
import json
import os

from .dff_db_connector import DffDbConnector
from df_engine.core.context import Context


class JsonConnector(dict, DffDbConnector):
    """
    Implements :py:class:`~dff_db.connector.dff_db_connector.DffDbConnector` with `json` as the storage format.

    Parameters
    -----------

    path: str
        Target file URI. Example: 'json://file.json'
    """

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

        value_dict = value.dict() if isinstance(value, Context) else value

        if not isinstance(value_dict, dict):
            raise TypeError(f"The saved value should be a dict or a dict-serializeable item, not {type(value_dict)}")

        dict.__setitem__(self, key, value_dict)
        self._save()

    def __delitem__(self, key: str):
        dict.__delitem__(self, key)
        self._save()

    def _save(self) -> None:
        with open(self.path, "w+", encoding="utf-8") as file_stream:
            json.dump(self, file_stream, ensure_ascii=False)

    def _load(self) -> None:
        if os.stat(self.path).st_size > 0:
            with open(self.path, "r", encoding="utf-8") as file_stream:
                saved_values = json.load(file_stream)
        else:
            saved_values = dict()
        for key, value in saved_values.items():
            if key not in self:
                self[key] = value

"""Main module"""
from abc import ABC, abstractmethod
from typing import Any

from pydantic import validate_arguments
from df_engine.core import Context, Actor
from df_engine.core.types import ActorStage


class DffAbstractConnector(ABC):
    """DffDbConnector"""

    def __init__(self) -> None:
        pass

    @abstractmethod
    def __getitem__(self, key: str) -> Any:
        raise NotImplementedError

    @abstractmethod
    def __setitem__(self, key: str, value: dict) -> None:
        raise NotImplementedError

    @abstractmethod
    def __delitem__(self, key: str) -> None:
        raise NotImplementedError

    @abstractmethod
    def __contains__(self, key: str) -> bool:
        raise NotImplementedError

    @abstractmethod
    def __len__(self) -> int:
        raise NotImplementedError

    @abstractmethod
    def get(self, item) -> Any:
        raise NotImplementedError

    @abstractmethod
    def clear(self) -> None:
        raise NotImplementedError


class DffDbConnector(DffAbstractConnector):
    def __init__(self, path: str):
        prefix, _, file_path = path.partition("://")
        self.full_path = path
        self.path = file_path

    def get(self, key: str, default=None) -> Any:
        try:
            value = self.__getitem__(key)
        except KeyError:
            value = default
        return value

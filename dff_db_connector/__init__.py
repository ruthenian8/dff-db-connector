# -*- coding: utf-8 -*-

from .json_connector import JsonConnector
from .pickle_connector import PickleConnector
from .shelve_connector import ShelveConnector
from .dff_db_connector import DffDbConnector, DffAbstractConnector
from .sql_connector import SqlConnector, postgres_available, mysql_available, sqlite_available
from .redis_connector import RedisConnector, redis_available
from .mongo_connector import MongoConnector, mongo_available

__author__ = "Daniil Ignatiev"
__email__ = "ruthenian8@gmail.com"
__version__ = "0.1"

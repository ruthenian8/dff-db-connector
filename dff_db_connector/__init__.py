# -*- coding: utf-8 -*-
__author__ = "Daniil Ignatiev"
__email__ = "ruthenian8@gmail.com"
__version__ = "0.1"

import importlib


def connector_factory(path: str, **kwargs):
    """
    Use connector_factory to lazy import connector types and instantiate them.
    The function takes a database connection URI or its equivalent. It should be prefixed with database name,
    followed by the symbol triplet '://'.
    Then, you should list the connection parameters like this: user:password@host:port/database
    The whole URI will then look like this:
    postgresql://user:password@host:port/database
    For connectors that write to local files, the function expects a file path instead of connection params:
    json://file.json
    When using sqlite backend your prefix should contain three slashes if you use Windows, or four in other cases.
    sqlite:////file.db
    If you want to use additional parameters in class constructors, you can pass them to this function as kwargs.

    """
    mapping = {
        "shelve": {"module": "shelve_connector", "class": "ShelveConnector"},
        "json": {"module": "json_connector", "class": "JsonConnector"},
        "pickle": {"module": "pickle_connector", "class": "PickleConnector"},
        "redis": {"module": "redis_connector", "class": "RedisConnector"},
        "mongodb": {"module": "mongo_connector", "class": "MongoConnector"},
        "mysql": {"module": "sql_connector", "class": "SqlConnector"},
        "postgresql": {"module": "sql_connector", "class": "SqlConnector"},
        "sqlite": {"module": "sql_connector", "class": "SqlConnector"},
    }
    prefix, _, _ = path.partition("://")
    if "sql" in prefix:
        prefix = prefix.split("+")[0]  # this takes care of alternative sql drivers
    assert (
        prefix in mapping
    ), f"""
    URI path should be prefixed with one of the following:\n
    {", ".join(mapping.keys())}.\n
    For more information, see the function doc:\n{connector_factory.__doc__}
    """
    _class, module = mapping[prefix]["class"], mapping[prefix]["module"]
    target_class = getattr(importlib.import_module(f".{module}", package="dff_db_connector"), _class)
    return target_class(path, **kwargs)

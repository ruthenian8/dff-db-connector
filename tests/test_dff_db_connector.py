import pytest
import socket
import os

from df_engine.core.context import Context

from dff_db_connector import (
    DffDbConnector,
    DffAbstractConnector,
    JsonConnector,
    PickleConnector,
    ShelveConnector,
    RedisConnector,
    SqlConnector,
    MongoConnector,
    postgres_available,
    mysql_available,
    sqlite_available,
    redis_available,
    mongo_available,
)


def ping_localhost(port: int, timeout=3):
    try:
        socket.setdefaulttimeout(timeout)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(("localhost", port))
    except OSError as error:
        return False
    else:
        s.close()
        return True


MONGO_ACTIVE = ping_localhost(27017)

REDIS_ACTIVE = ping_localhost(6379)

POSTGRES_ACTIVE = ping_localhost(5432)

MYSQL_ACTIVE = ping_localhost(3307)


def test_main():
    assert issubclass(DffDbConnector, DffAbstractConnector)


def generic_test(connector_instance, testing_context, testing_telegram_id):
    assert isinstance(connector_instance, DffDbConnector)
    assert isinstance(connector_instance, DffAbstractConnector)
    # perform cleanup
    connector_instance.clear()
    assert len(connector_instance) == 0
    # test write operations
    connector_instance[testing_telegram_id] = {"foo": "bar", "baz": "qux"}
    assert testing_telegram_id in connector_instance
    assert len(connector_instance) == 1    
    connector_instance[testing_telegram_id] = testing_context  # overwriting a key
    assert len(connector_instance) == 1
    # test read operations
    new_ctx = connector_instance[testing_telegram_id]
    assert isinstance(new_ctx, Context)
    assert new_ctx.dict() == testing_context.dict()
    # test delete operations
    del connector_instance[testing_telegram_id]
    assert testing_telegram_id not in connector_instance
    # test `get` method
    assert connector_instance.get(testing_telegram_id) is None    


def test_shelve(testing_file, testing_context, testing_telegram_id):
    connector_instance = ShelveConnector(f"shelve://{testing_file}")
    generic_test(connector_instance, testing_context, testing_telegram_id)


def test_json(testing_file, testing_context, testing_telegram_id):
    connector_instance = JsonConnector(f"json://{testing_file}")
    generic_test(connector_instance, testing_context, testing_telegram_id)


def test_pickle(testing_file, testing_context, testing_telegram_id):
    connector_instance = PickleConnector(f"pickle://{testing_file}")
    generic_test(connector_instance, testing_context, testing_telegram_id)


@pytest.mark.skipif(MONGO_ACTIVE == False, reason="Mongodb server not running")
@pytest.mark.skipif(mongo_available == False, reason="Mongodb dependencies missing")
def test_mongo(testing_context, testing_telegram_id):
    connector_instance = MongoConnector(
        "mongodb://{}:{}@localhost:27017/{}".format(
            os.getenv("MONGO_INITDB_ROOT_USERNAME"),
            os.getenv("MONGO_INITDB_ROOT_PASSWORD"),
            os.getenv("MONGO_INITDB_ROOT_USERNAME")
        )
    )
    generic_test(connector_instance, testing_context, testing_telegram_id)


@pytest.mark.skipif(REDIS_ACTIVE == False, reason="Redis server not running")
@pytest.mark.skipif(redis_available == False, reason="Redis dependencies missing")
def test_redis(testing_context, testing_telegram_id):
    connector_instance = RedisConnector(
        "redis://{}:{}@localhost:6379/{}".format(
            "",
            os.getenv("REDIS_PASSWORD"),
            "0"
        )
    )
    generic_test(connector_instance, testing_context, testing_telegram_id)


@pytest.mark.skipif(POSTGRES_ACTIVE == False, reason="Postgres server not running")
@pytest.mark.skipif(postgres_available == False, reason="Postgres dependencies missing")
def test_postgres(testing_context, testing_telegram_id):
    connector_instance = SqlConnector("postgresql://{}:{}@localhost:5432/{}".format(
            os.getenv("PG_USERNAME"),
            os.getenv("PG_PASSWORD"),
            "test"
        )
    )
    generic_test(connector_instance, testing_context, testing_telegram_id)


@pytest.mark.skipif(sqlite_available == False, reason="Sqlite dependencies missing")
def test_sqlite(testing_file, testing_context, testing_telegram_id):
    connector_instance = SqlConnector(f"sqlite:////{testing_file}")
    generic_test(connector_instance, testing_context, testing_telegram_id)


@pytest.mark.skipif(MYSQL_ACTIVE == False, reason="Mysql server not running")
@pytest.mark.skipif(mysql_available == False, reason="Mysql dependencies missing")
def test_mysql(testing_context, testing_telegram_id):
    connector_instance = SqlConnector(
        "mysql+pymysql://{}:{}@localhost:3307/{}".format(
            os.getenv("MYSQL_USERNAME"),
            os.getenv("MYSQL_PASSWORD"),
            "test"
        )
    )
    generic_test(connector_instance, testing_context, testing_telegram_id)

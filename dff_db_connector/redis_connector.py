import json

try:
    from redis import Redis

    redis_available = True
except ImportError:
    redis_available = False

from .dff_db_connector import DffDbConnector
from df_engine.core.context import Context


class RedisConnector(DffDbConnector):
    def __init__(self, path: str):
        super(RedisConnector, self).__init__(path)
        if not redis_available:
            raise ImportError("`redis` package is missing")
        self._redis = Redis.from_url(self.full_path)

    def __contains__(self, key: str) -> bool:
        return self._redis.exists(key)

    def __setitem__(self, key: str, value: Context) -> None:
        if isinstance(value, Context):
            value = value.dict()

        if not isinstance(value, dict):
            raise TypeError(f"The saved value should be a dict or a dict-serializeable item, not {type(value)}")

        self._redis.set(key, json.dumps(value, ensure_ascii=False))

    def __getitem__(self, key: str) -> Context:
        result = self._redis.get(key)
        if result:
            result_dict = json.loads(result.decode("utf-8"))
            return Context.cast(result_dict)
        raise KeyError(f"No entry for key {key}.")

    def __delitem__(self, key: str) -> None:
        self._redis.delete(key)

    def __len__(self) -> int:
        return self._redis.dbsize()

    def clear(self) -> None:
        self._redis.flushdb()

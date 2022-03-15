import json

from redis import Redis

from .dff_db_connector import DffDbConnector
from df_engine.core.context import Context


class RedisConnector(DffDbConnector):
    def __init__(self, path: str):
        super(RedisConnector, self).__init__(path)
        self._redis = Redis.from_url(self.full_path)

    def __contains__(self, key: str) -> bool:
        return self._redis.exists(key)

    def __setitem__(self, key: str, value: Context) -> None:
        self._redis.set(key, json.dumps(value.dict(), ensure_ascii=False))

    def __getitem__(self, key: str) -> Context:
        result = self._redis.get(key)
        if result:
            result_dict = json.loads(result.decode("utf-8"))
            return Context.cast(result_dict)
        raise KeyError(f"No entry for key {key}.")

    def __delitem__(self, key: str) -> None:
        self._redis.delete(key)

    def __del__(self) -> None:
        self._redis.close()

    def __len__(self) -> int:
        return self._redis.dbsize()

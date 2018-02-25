import redis
from selectors import DefaultSelector, EVENT_READ, EVENT_WRITE

selector = DefaultSelector()

class RedisLoop:
    def __init__(self, msg):
        self.msg = msg
        self._pool = redis.ConnectionPool(host="127.0.0.1", port=6379, db=0, max_connections=10)

    def rpush(self):
        selector.register()

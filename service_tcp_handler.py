import re
import time
import redis
import uvloop
import asyncio

from blinker import signal
from collections import deque
from elasticsearch.helpers import bulk
from elasticsearch import Elasticsearch
from concurrent.futures import ThreadPoolExecutor

from utils import log
from config import QUEUE_MAX
from config import REDIS_HOST, REDIS_PORT, REDIS_DB


q_action = deque(maxlen=10000)
queue_signal = signal("queue_signal")
q_num = 0

p = re.compile(r'\".*\"')


@queue_signal.connect
def write_bulk_to_es(actions):

    try:
        print(actions)
        _index = "log-{0}".format(time.strftime("%Y%m%d"))
        es = Elasticsearch(["192.168.6.23:9200"])
        bulk(es, actions, index=_index, raise_on_error=True)
    except Exception as e:
        print("write_bulk_to_es", e)


async def redis_lpop(num=10):
    try:
        msg_key = "log-msg"
        bytes_data = bytes()
        pool = redis.ConnectionPool(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB, max_connections=10)
        r = redis.StrictRedis(connection_pool=pool)
        for i in range(num):
            data = r.lpop(msg_key)
            if data:
                bytes_data += data
        return bytes_data
    except Exception as e:
        print("redis_lpop", str(e))
        log('error', str(e))


async def string_to_dict(msg_string):

    """
    1. 根据\n 标记号来分包
    2. 组成dict
    3. yield 返回dict格式的日志数据或直接存于内存队列
    """
    try:
        split_n = msg_string.split("\\n")
        for i in split_n:
            tmp = p.findall(str(i))
            if tmp:
                for j in tmp:
                    split_dot = j.split(",")
                    d = {}
                    for k in split_dot:
                        split_molon = k.split(":", maxsplit=1)
                        if len(split_molon) == 2:
                            if split_molon[0] == "message":
                                d[split_molon[0]] = str(split_molon[1]).encode("utf-8")
                            else:
                                d[split_molon[0]] = str(split_molon[1])

                    if d:
                        d["_index"] = "log-{0}".format(time.strftime("%Y%m%d"))
                        d["_type"] = "log"
                        # 存于队列, 再批量写入es
                        q_action.append(d)

                        # 存进redis, 再消费进es
                        # queue_signal.send(d)
    except Exception as e:
        print("string_to_dict", "error:", e)


async def is_queue_max(list_max=QUEUE_MAX):
    try:
        if q_action.__len__() >= list_max:
            actions = [q_action.popleft() for i in range(list_max)]
            queue_signal.send(actions)
    except Exception as e:
        print("is_queue_max", e)


async def handler():
    try:
        while 1:
            bytes_data = await redis_lpop()
            if bytes_data:
                await string_to_dict(str(bytes_data))
            await is_queue_max()

    except Exception as e:
        print("handler", e)
        log('error', str(e))


if __name__ == "__main__":
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
    loop = uvloop.new_event_loop()
    asyncio.set_event_loop(loop)
    with ThreadPoolExecutor(max_workers=10) as executor:
        executor.submit(loop.run_until_complete(handler()))




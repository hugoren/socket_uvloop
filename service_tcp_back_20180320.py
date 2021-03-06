import re
import time
import redis
import uvloop
import asyncio
import socketserver

from numba import jit
from blinker import signal
from collections import deque
from elasticsearch.helpers import bulk
from elasticsearch import Elasticsearch
from concurrent.futures import ThreadPoolExecutor

from utils import log
from config import QUEUE_MAX
from config import HOST, PORT
from config import REDIS_HOST, REDIS_PORT, REDIS_DB


q = deque(maxlen=10000)
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


# @queue_signal.connect
def rpush_data_to_redis(data):
    try:
        msg_key = "log-msg"
        pool = redis.ConnectionPool(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB, max_connections=10)
        r = redis.StrictRedis(connection_pool=pool)
        r.rpush(msg_key, data)
    except Exception as e:
        log('error', str(e))


def string_to_dict(msg_string):

    """
    1. 根据\n 标记号来分包
    2. 组成dict
    3. yield 返回dict格式的日志数据
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
                            d[split_molon[0]] = str(split_molon[1])
                    if d:
                        d["_index"] = "log-{0}".format(time.strftime("%Y%m%d"))
                        d["_type"] = "log"
                        # 存于队列, 再批量写入es
                        q_action.append(d)

                        # 存进redis, 再消费进es
                        # queue_signal.send(d)
    except Exception as e:
        print("string_to_dict", e)


def is_queue_max(list_max=QUEUE_MAX):
    """
       1. 每条队列1m，大于10条，开始转格式
       2. 信号量方式调用写入redis
    """
    try:
        if q.__len__() >= list_max:

            bytes_data = bytes()
            for i in range(list_max):
                if q.__len__():
                    bytes_data += q.popleft()
            string_to_dict(str(bytes_data))

        if q_action.__len__() >= list_max:
            actions = [q_action.popleft() for i in range(list_max)]
            queue_signal.send(actions)
    except Exception as e:
        print("is_queue_max", e)


class TCPHandler(socketserver.BaseRequestHandler):
    def setup(self):
        ip = self.client_address[0].strip()
        port = self.client_address[1]
        print(ip, port)

    def handle(self):
        buff_recv = 2048
        #  keep alive
        while 1:
            data = self.request.recv(buff_recv)
            if data:
                q.appendleft(data)
                # is_queue_max()
                self.request.sendall(b"recev success!")

    def finish(self):
        print("client is disconnect")


async def handler():
    print("Socket tcp server begin.....")
    log('info', 'Socket tcp server begin.....')
    try:
        s = socketserver.ThreadingTCPServer((HOST, PORT), TCPHandler)
        s.allow_reuse_address = True
        s.serve_forever()
    except Exception as e:
        log('error', str(e))
        print("handler", e)


if __name__ == "__main__":
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
    loop = uvloop.new_event_loop()
    asyncio.set_event_loop(loop)
    with ThreadPoolExecutor(max_workers=10) as executor:
        executor.submit(loop.run_until_complete(handler()))




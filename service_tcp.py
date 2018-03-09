import asyncio
import uvloop
import socketserver
from collections import deque
from blinker import signal
from concurrent.futures import ThreadPoolExecutor
from config import REDIS_HOST, REDIS_PORT, REDIS_DB
from config import HOST, PORT
from utils import log
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
from datetime import datetime
# from utils import rpush_redis
import redis
import time

q = deque(maxlen=150000)
queue_signal = signal("queue_signal")
q_num = 0


# @queue_signal.connect
def write_to_es(actions):
    try:
        print(actions)
        _index = "log-{0}".format(time.strftime("%Y%m%d"))
        es = Elasticsearch(["192.168.6.23:9200"])
        bulk(es, actions, index=_index, raise_on_error=True)
    except Exception as e:
        print(e)
        log("error", str(e))


@queue_signal.connect
def rpush_data_to_redis(data_list):
    try:
        msg_key = "log-msg"
        pool = redis.ConnectionPool(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB, max_connections=10)
        r = redis.StrictRedis(connection_pool=pool)
        [r.rpush(msg_key, i) for i in data_list]
    except Exception as e:
        log('error', str(e))


def is_queue_max(list_max=1000):

    if q.__len__() >= list_max:
        # data_list = [q.pop() for i in range(list_max)]
        # queue_signal.send(data_list)
        _index = "log-{0}".format(time.strftime("%Y%m%d"))
        _type = "log"
        actions = [{
            "_index": _index,
            "_type": _type,

            "_source": {
                "timestamp": datetime.now(),
                "msg": str(q.pop(), "utf-8"),
            }
        } for i in range(list_max)]
        queue_signal.send(actions)

    else:
        global q_num
        if q_num == q.__len__() and q_num >=1:
            data_list = [q.pop() for i in range(q_num)]
            queue_signal.send(data_list)
        q_num = q.__len__()


class TCPHandler(socketserver.BaseRequestHandler):
    def setup(self):
        ip = self.client_address[0].strip()
        port = self.client_address[1]
        print(ip, port)

    def handle(self):
        #  keep alive
        while 1:
            buff_recv = 2048
            data = self.request.recv(buff_recv)
            if data:
                # print(data)
                q.appendleft(data)
                is_queue_max()
                self.request.sendall(b"recev success!")

    def finish(self):
        print("client is disconnect")


async def handler():
    print("Socket tcp server begin.....")
    log('info', 'Socket tcp server begin.....')
    try:
        s = socketserver.ThreadingTCPServer((HOST, PORT), TCPHandler)
        s.serve_forever()
    except Exception as e:
        log('error', str(e))
        print(e)


if __name__ == "__main__":
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
    loop = uvloop.new_event_loop()
    asyncio.set_event_loop(loop)
    with ThreadPoolExecutor(max_workers=10) as executor:
        executor.submit(loop.run_until_complete(handler()))



import asyncio
import uvloop
import socketserver
from collections import deque
from blinker import signal
from concurrent.futures import ThreadPoolExecutor
from config import REDIS_HOST, REDIS_PORT, REDIS_DB
from config import HOST, PORT
from config import QUEUE_MAX
from utils import log
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
from datetime import datetime
# from utils import rpush_redis
import redis
import time
import json

q = deque(maxlen=15000)
queue_signal = signal("queue_signal")
q_num = 0


# @queue_signal.connect
def write_to_es(actions):
    try:
        _index = "log-{0}".format(time.strftime("%Y%m%d"))
        es = Elasticsearch(["192.168.6.23:9200"])
        bulk(es, actions, index=_index, raise_on_error=True)
    except Exception as e:
        print(e)


@queue_signal.connect
def rpush_data_to_redis(data_list):
    try:
        msg_key = "log-msg"
        pool = redis.ConnectionPool(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB, max_connections=10)
        r = redis.StrictRedis(connection_pool=pool)
        [r.rpush(msg_key, i) for i in data_list]
    except Exception as e:
        log('error', str(e))


def is_queue_max(list_max=QUEUE_MAX):

    if q.__len__() >= list_max:
        data_list = [q.pop() for i in range(list_max)]
        queue_signal.send(data_list)
        # _index = "log-{0}".format(time.strftime("%Y%m%d"))
        # _type = "log"
        #
        # try:
        #     actions = [{
        #         "_index": _index,
        #         "_type": _type,
        #         "_source": eval(q.pop())
        #     } for i in range(list_max)]
        # except Exception as e:
        #     print("json to dict exception, data:{0}".format(str(e)))
        #
        # queue_signal.send(actions)



    # else:
    #     global q_num
    #     if q_num == q.__len__() and q_num >=1:
    #         data_list = [q.pop() for i in range(q_num)]
    #         # queue_signal.send(data_list)
    #     q_num = q.__len__()


class TCPHandler(socketserver.BaseRequestHandler):
    def setup(self):
        ip = self.client_address[0].strip()
        port = self.client_address[1]
        print(ip, port)

    def handle(self):
        #  keep alive
        buff_recv = 2048
        data_buffer = bytes()
        while 1:
            print(data_buffer)
            data = self.request.recv(buff_recv)
            if data:
                time.sleep(1)
                print(data)
                # if data.endswith(b"\n"):
                #     data_buffer += data
                #     q.appendleft(data)
                #     data_buffer = b""
                # else:
                #     data_buffer += data

                is_queue_max()
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
        print(e)


if __name__ == "__main__":
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
    loop = uvloop.new_event_loop()
    asyncio.set_event_loop(loop)
    with ThreadPoolExecutor(max_workers=10) as executor:
        executor.submit(loop.run_until_complete(handler()))



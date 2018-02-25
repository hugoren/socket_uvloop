import asyncio
import uvloop
import socketserver
from collections import deque
from blinker import signal
from numba import jit
from concurrent.futures import ThreadPoolExecutor
from config import HOST, PORT
from utils import log
# from utils import rpush_redis
import redis
import time

q = deque()
queue_signal = signal("queue_signal")


@queue_signal.connect
def rpush_data(data_list):
    try:
        msg_key = "log-msg"
        pool = redis.ConnectionPool(host="127.0.0.1", port=6379, db=0, max_connections=10)
        r = redis.StrictRedis(connection_pool=pool)
        [r.rpush(msg_key, i) for i in data_list]
    except Exception as e:
        log('error', str(e))


def is_list_max():
    list_max = 500
    if q.__len__() >= list_max:
        start_time = time.time()
        data_list = [q.pop() for i in range(list_max-1)]
        # rpush_data(data_list)
        queue_signal.send(data_list)
        print(time.time() - start_time)


class MyUDPHandler(socketserver.BaseRequestHandler):

    def handle(self):
        receive_bytes = 2048
        data = self.request[0][:receive_bytes]
        q.appendleft(data)
        is_list_max()


def handler():
    print("Socket udp server begin.....")
    log('info', 'Socket udp server begin.....')
    try:
        s = socketserver.ThreadingUDPServer((HOST, PORT), MyUDPHandler)
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



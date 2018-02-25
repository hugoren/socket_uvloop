import asyncio
import uvloop
import socketserver
from concurrent.futures import ThreadPoolExecutor
from config import HOST, PORT
from utils import log
# from utils import rpush_redis
import redis
import time


global data_list
data_list = []


class RedisPool:
    def __init__(self):
        self.pool = redis.ConnectionPool(host="127.0.0.1", port=6379, db=0, max_connections=10)
        self.n = 0

    @staticmethod
    def rpush_data(self):
        try:
            msg_key = "log-msg"
            # start_time = time.time()
            pool = redis.ConnectionPool(host="127.0.0.1", port=6379, db=0, max_connections=10)
            r = redis.StrictRedis(connection_pool=pool)
            [r.rpush(msg_key, i) for i in data_list]
            data_list.clear()
            # print(time.time() - start_time)
        except Exception as e:
            log('error', str(e))

    def recev_data(self, msg):
        data_list.append(msg)
        if data_list.__len__() >= 500:
            start_time = time.time()
            self.rpush_data(data_list)
            print(time.time() - start_time)


class MyUDPHandler(socketserver.BaseRequestHandler):

    def handle(self):
        receive_bytes = 2048
        data = self.request[0][:receive_bytes]
        RedisPool().recev_data(data)


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



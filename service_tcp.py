# coding=utf-8
import redis
import uvloop
import asyncio
import socketserver

from concurrent.futures import ThreadPoolExecutor

from utils import log
from config import HOST, PORT
from config import REDIS_HOST, REDIS_PORT, REDIS_DB


def rpush_data_to_redis(data):
    try:
        msg_key = "log-msg"
        pool = redis.ConnectionPool(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB, max_connections=10)
        r = redis.StrictRedis(connection_pool=pool)
        r.rpush(msg_key, data)
    except Exception as e:
        log('error', str(e))

import chardet
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
            self.request.sendall(b"recev success!")
            if data:
                rpush_data_to_redis(data)

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




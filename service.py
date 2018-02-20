import asyncio
import uvloop
import time
import socketserver
from config import HOST, PORT
from utils import log
from utils import rpush_redis


class MyUDPHandler(socketserver.BaseRequestHandler):

    def handle(self):
        receive_bytes = 2048
        start_time = time.time()
        data = self.request[0][:receive_bytes]
        rpush_redis(data)
        print(time.time() - start_time, data)


def handler():
    print("Socket udp server begin.....")
    log('info', 'Socket udp server begin.....')
    try:
        s = socketserver.ForkingUDPServer((HOST, PORT), MyUDPHandler)
        s.serve_forever()
    except Exception as e:
        log('error', str(e))
        print(e)


if __name__ == "__main__":
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
    loop = uvloop.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(handler())
    loop.run_forever()


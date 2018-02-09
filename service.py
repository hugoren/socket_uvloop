import asyncio
import uvloop
import socketserver
from config import HOST, PORT
from utils import log


class MyUDPHandler(socketserver.BaseRequestHandler):
    def handle(self):
        data = self.request[0][:2048]
        print(data)


async def handler():
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
    loop.run_until_complete(handler())

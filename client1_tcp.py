import socket

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    sock.connect(('127.0.0.1', 5454))
    while 1:
        sock.send(b'{@timestamp":"2018-03-09T16:35:09.912+08:00","@version":1,"message":">>>>>>>>>>>>>>>","logger_name":"com.oeasy.filter.LoginFilter","thread_name":"http-nio-7245-exec-13","level":"DEBUG","level_value":10000,"springAppName":"yihao01-advert-web","LOG_PORT":"5454","LOG_HOST":"192.168.0.106","X-Trace-LogId":"011031151","X-B3-TraceId":"1feec530138b9874","X-Span-Export":"true","X-B3-SpanId":"1feec530138b9874"}\\n')
        print(sock.recv(1024))


# def tcp_client():
#     s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     s.connect(('127.0.0.1', 5454))
#     while 1:
#         s.sendall(b"test66666666666")
#         s.recv(1024)
#     # s.sendall(b"fafdasfafa")
#     # print(s.recv(1024))
#
#
# if __name__ == "__main__":
#     tcp_client()
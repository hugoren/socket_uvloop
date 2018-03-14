import socket

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    sock.connect(('127.0.0.1', 5454))
    while 1:
        data = b'{"@timestamp":"2018-03-09T17:10:45.182+08:00","@version":1,"message":"Fetching config from server at: http://192.168.0.106:7998/","logger_name":"org.springframework.cloud.config.client.ConfigServicePropertySourceLocator","thread_name":"DiscoveryClient-InstanceInfoReplicator-0","level":"INFO","level_value":20000,"springAppName":"yihao01-comment","LOG_PORT":"5454","LOG_HOST":"192.168.0.106","X-Trace-LogId":"01010647"}\n'
        sock.send(data)
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
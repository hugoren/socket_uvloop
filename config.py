import os

env = os.getenv('ENV')

if env == 'test':
    HOST = '0.0.0.0'
    PORT = 5454
    TOKEN = 'b0350c8c75ddcd99738df4c9346bec48dc9c4914'
    REDIS_HOST = "192.168.6.23"
    REDIS_PORT = 6379
    REDIS_DB = 3
    QUEUE_MAX = 5



elif env == 'prod':
    HOST = '0.0.0.0'
    PORT = 5454
    TOKEN = 'b0350c8c75ddcd99738df4c9346bec48dc9c4914'
    REDIS_HOST = "127.0.0.1"
    REDIS_PORT = 6379
    REDIS_DB = 3
    QUEUE_MAX = 50


else:
    HOST = '0.0.0.0'
    PORT = 5454
    TOKEN = 'b0350c8c75ddcd99738df4c9346bec48dc9c4914'
    REDIS_HOST = "127.0.0.1"
    REDIS_PORT = 6379
    REDIS_DB = 3
    QUEUE_MAX = 1


import os

env = os.getenv('ENV')

if env == 'test':
    HOST = '192.168.0.108'
    PORT = 20000
    TOKEN = 'b0350c8c75ddcd99738df4c9346bec48dc9c4914'


elif env == 'prod':
    HOST = '192.168.0.103'
    PORT = 9200
    TOKEN = 'b0350c8c75ddcd99738df4c9346bec48dc9c4914'

else:
    HOST = '192.168.6.23'
    PORT = 9200
    TOKEN = 'b0350c8c75ddcd99738df4c9346bec48dc9c4914'

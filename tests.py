a = b'{"@timestamp\":\"2018-03-09T16:35:09.912+08:00\",\"@version\":1,\"message\":\">>>>>>>>>>>>>>>\",\"logger_name\":\"com.oeasy.filter.LoginFilter\",\"thread_name\":\"http-nio-7245-exec-13\",\"level\":\"DEBUG\",\"level_value\":10000,\"springAppName\":\"yihao01-advert-web\",\"LOG_PORT\":\"5454\",\"LOG_HOST\":\"192.168.0.106\",\"X-Trace-LogId\":\"011031151\",\"X-B3-TraceId\":\"1feec530138b9874\",\"X-Span-Export\":\"true\",\"X-B3-SpanId\":\"1feec530138b9874\"}\\\\n',
from json import JSONDecoder
import json

try:
    b = json.dumps(str(a))
    c = eval(b)
    print(c)
except Exception as e:
    print(e)


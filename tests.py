import re

dataBuffer = b'{"@timestamp":"2018-03-13T11:03:41.477+08:00","@version":1,"message":"\\u7EA2\\u5305\\u57CB\\u70B9 ----  redIds = 38b1d81b48f842e08340e231d8218804,1bbd1fa3e05a4a16a9db5ddb0c5c7787,8acf1279c52b475e895e48e6f4330b26,0cea017be90946398fc2f71ef5787072,e8f707b120fc4e8190193a2905a455dd,25367bcef24c4a21a4848e53978a3fa9,44db0883c7424a069d736dee285ff893,c1c12642a38c4a58a68df266f80e1889,bf20395be7244773a7b283f549d97e30,bc1c8fa39b924c0e826b02e8f4e010d0,","logger_name":"com.yihao01.zb.center.service.app.impl.AppAroundCouponNewServiceImpl","thread_name":"http-nio-7045-exec-4","level":"DEBUG","level_value":10000,"springAppName":"yihao01-zb","LOG_PORT":"5454","LOG_HOST":"192.168.0.106","X-B3-ParentSpanId":"b61f86ffa06d75d9","X-Trace-LogId":"01104070083","X-B3-TraceId":"37fed76a8a3df1b7","X-Span-Export":"true","X-B3-SpanId":"6e07303e74e5b8cf"}' \
             b'\n{"@timestamp":"2018-03-13T11:03:46.681+08:00","@version":1,"message":"\\u7528\\u6237\\u767B\\u5F55\\u540C\\u6B65\\u4F1A\\u5458\\u4FE1\\u606F","logger_name":"com.yihao01.zb.center.service.app.impl.AppAroundCouponNewServiceImpl","thread_name":"http-nio-7045-exec-8","level":"INFO","level_value":20000,"springAppName":"yihao01-zb","LOG_PORT":"5454","LOG_HOST":"192.168.0.106","X-B3-ParentSpanId":"6829be58bdede553","X-Trace-LogId":"01126030033","X-B3-TraceId":"34e3a3dbf5513ab2","X-Span-Export":"true","X-B3-SpanId":"40654ff7ec63ef5c"}' \
             b'\n{"@timestamp":"2018-03-13T11:03:47.884+08:00","@version":1,"message":"\\u7EA2\\u5305\\u57CB\\u70B9 ----  redIds = 58663279aa0c42a79af29b52bc8afa43,2e3a99207caf4895ba00f373ab2d6db9,6c0bc9e37d304622ae528426f0d18835,ecc8baeae4ce4e2288787a49c18564a0,a6c030e80d6348c58d4026713bcfb465,cc8b243fbad64721bda81801dac36307,db4e9a4380534b889eca423cb11585b1,ce28f47e68884edd88e7c5ba15c2189d,18739d98f0644587a817c9d9c1f58603,2803b925c29942f5a066c6e55a2268fe,","logger_name":"com.yihao01.zb.center.service.app.impl.AppAroundCouponNewServiceImpl","thread_name":"http-nio-7045-exec-5","level":"DEBUG","level_value":10000,"springAppName":"yihao01-zb","LOG_PORT":"5454","LOG_HOST":"192.168.0.106","X-B3-ParentSpanI'


def string_to_dict(msg_string):

    p = re.compile(r'\".*\"')
    msg_list = []
    s = str(msg_string)

    try:
        split_n = s.split("\\n")
        for i in split_n:
            tmp = p.findall(str(i))
            split_dot = tmp[0].split(",", maxsplit=1)
            d = {}

            for j in split_dot:
                split_molon = j.split(":", maxsplit=1)
                if len(split_molon) == 2:
                    d[split_molon[0]] = split_molon[1]
            msg_list.append(d)

        return msg_list
    except Exception as e:
            tmp += i
print(msg_list)




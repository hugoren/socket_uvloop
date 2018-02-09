import logging
import datetime
import maya
from functools import wraps
from sanic.response import json
from config import TOKEN
from logging.handlers import RotatingFileHandler


def log(level, message):

    logger = logging.getLogger('socket')

    #  这里进行判断，如果logger.handlers列表为空，则添加，否则，直接去写日志
    if not logger.handlers:
        log_name = 'app.log'
        log_count = 2
        log_format = '%(asctime)s %(levelname)s %(module)s %(funcName)s-[%(lineno)d] %(message)s'
        log_level = logging.INFO
        max_bytes = 10 * 1024 * 1024
        handler = RotatingFileHandler(log_name, mode='a', maxBytes=max_bytes, backupCount=log_count)
        handler.setFormatter(logging.Formatter(log_format))
        logger.setLevel(log_level)
        logger.addHandler(handler)

    if level == 'info':
        logger.info(message)
    if level == 'error':
        logger.error(message)


def auth(token):
    def wrapper(func):
        @wraps(func)
        async def auth_token(req, *arg, **kwargs):
            try:
                value = req.headers.get(token)
                if value and TOKEN == value:
                    r = await func(req, *arg, **kwargs)
                    return json({'retcode': 0, 'stdout': r})
                else:
                    return json({'retcode': 1, 'stderr': 'status{}'.format(403)})
            except Exception as e:
                log.error(str(e))
                return json({'retcode': 1, 'stderr': str(e)})
        return auth_token
    return wrapper


def reduction_eight_hours(iso8601):
    '''
    :param iso8601:
    :return: iso8601
    '''
    try:
        d1 = datetime.datetime.strptime(iso8601, '%Y-%m-%dT%H:%M:%SZ')
        d2 = d1 - datetime.timedelta(hours=8)
        d3 = d2.strftime("%Y-%m-%d %H:%M:%S")
        d4 = maya.when(d3).iso8601()
        return d4
    except Exception as e:
        raise Exception('转utc时区异常')


def add_eight_hours(iso8601):
    """
    :param iso8601:
    :return: date string
    """
    d1 = datetime.datetime.strptime(iso8601, '%Y-%m-%dT%H:%M:%S.%fZ')
    d2 = d1 + datetime.timedelta(hours=8)
    dt = d2.strftime("%Y-%m-%d %H:%M:%S")
    return dt

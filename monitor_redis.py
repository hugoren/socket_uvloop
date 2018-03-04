import schedule
from threading import Event


def redis_info():
    print("flushdb 0")


schedule.every(2).seconds.do(redis_info)

if __name__ == "__main__":
    while 1:
        schedule.run_pending()
        Event().wait(2)

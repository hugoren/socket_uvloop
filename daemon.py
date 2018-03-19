import os
import sys
import atexit


def daemon(pid_file=None):

    if os.path.exists("/Users/admin/devops/socket_uvloop/{0}".format(pid_file)):
        raise RuntimeError("Already running")
    pid = os.fork()

    if pid:
        sys.exit(0)

    os.chdir('/')
    # 子进程默认继承父进程的umask（文件权限掩码），重设为0（完全控制），以免影响程序读写文件
    os.umask(0)
    # 让子进程成为新的会话组长和进程组长
    os.setsid()

    _pid = os.fork()
    if _pid:
        # 退出子进程
        sys.exit(0)

    # 此时，孙子进程已经是守护进程了，接下来重定向标准输入、输出、错误的描述符(是重定向而不是关闭, 这样可以避免程序在 print 的时候出错)

    # 刷新缓冲区先，小心使得万年船
    sys.stdout.flush()
    sys.stderr.flush()

    # dup2函数原子化地关闭和复制文件描述符，重定向到/dev/nul，即丢弃所有输入输出
    with open('/dev/null') as read_null, open('/dev/null', 'w') as write_null:
        os.dup2(read_null.fileno(), sys.stdin.fileno())
        os.dup2(write_null.fileno(), sys.stdout.fileno())
        os.dup2(write_null.fileno(), sys.stderr.fileno())

    # 写入pid文件
    if pid_file:
        try:
            with open("/Users/admin/devops/socket_uvloop/{0}".format(pid_file), 'w+') as f:
                f.write(str(os.getpid()))
            # 注册退出函数，进程异常退出时移除pid文件
            atexit.register(os.remove, "/Users/admin/devops/socket_uvloop/{0}".format(pid_file))
        except Exception as e:
            print(e)


    while 1:
        print("sub process is alive")


daemon("pid_file.txt")

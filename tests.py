import time
import timeit
import numpy as np


def pySum():
    a = list(range(1000))
    b = list(range(1000))
    c = []
    for i in range(len(a)):
        c.append(a[i]**2 + b[i]**2)


def npSum():
    a = np.arange(1000)
    b = np.arange(1000)


print(np.random.randint(10))

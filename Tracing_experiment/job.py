import random
import sys
import time
from _thread import start_new_thread

import numpy as np


# fibonacci function using recursion
def fib(n):
    if n <= 1:
        return n
    return fib(n - 1) + fib(n - 2)


def sqrrt(n):
    for _ in range(n):
        x = random.random()
        y = x ** 0.5


def ops(n):
    a = np.random.rand(n, n)
    b = np.random.rand(n, n)
    c = np.dot(a, b)


# multiple threads
def server_workload(T, n):
    for _ in range(T):
        start_new_thread(sqrrt, (n,))


# Driver Program
if __name__ == "__main__":
    args = sys.argv[1:]  # job number and depth
    start_time = time.time()
    name = args[0]  # name of the job
    T = int(args[1])  # number of threads
    n = int(args[2])  # depth of fib job
    server_workload(T, n)  # run fib job

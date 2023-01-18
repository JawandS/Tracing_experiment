import sys
import time
from _thread import start_new_thread


# fibonacci function using recursion
def fib(n):
    if n <= 1:
        return n
    return fib(n - 1) + fib(n - 2)


# multiple fibonacci threads
def server_workload(numThreads, depth):
    for counter in range(numThreads):
        if counter % 2 == 0: # double depth every other thread
            depth *= 2
        start_new_thread(fib, (depth,))


# Driver Program
if __name__ == "__main__":
    args = sys.argv[1:]  # job number and depth
    start_time = time.time()
    name = args[0]  # name of the job
    numThreads = int(args[1])  # number of threads
    depth = int(args[2])  # depth of fib job
    isVariable = bool(int(args[3]))  # is the workload variable
    server_workload(numThreads, depth)  # run fib job

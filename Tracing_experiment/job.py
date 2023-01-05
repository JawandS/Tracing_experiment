import time, sys, os, signal


# fibonacci function using recursion
def fib(n):
    if n <= 1:
        return n
    return fib(n - 1) + fib(n - 2)


# Driver Program
if __name__ == "__main__":
    args = sys.argv[1:]  # job number and depth
    start_time = time.time()
    n = int(args[1])  # depth of fib job
    fib(n) # run fib job
    print(f"job {args[0]}, depth {n}, {round(time.time() - start_time, 3)}s") # output job info

import time, sys, os, signal

# fibonacci function using recursion
def fib(n):
    if n <= 1:
        return n
    return fib(n-1) + fib(n-2)

# Driver Program
if __name__ == "__main__":
    start_time = time.time()
    n = 35
    fib(n)

    # check for auto kill needed
    args = sys.argv
    if args[1] == "tracing":
        name = "auto_kill.py"
        for line in os.popen("ps ax | grep " + name + " | grep -v grep"):
            fields = line.split()
            # extracting Process ID from the output
            pid = fields[0]
            # kill process
            os.kill(int(pid), signal.SIGUSR1)  # send user signal
        if len(args) > 1:
            print(args[2], round(time.time() - start_time, 3))
        else:
            print(-1, round(time.time() - start_time, 3))

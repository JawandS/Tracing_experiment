import time, os, signal

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

    # signal auto kill
    name = "auto_kill.py"
    for line in os.popen("ps ax | grep " + name + " | grep -v grep"):
        fields = line.split()
        # extracting Process ID from the output
        pid = fields[0]
        # kill process
        os.kill(int(pid), signal.SIGUSR1)  # send user signal

import subprocess, sys, signal


def handler(sig, frame):
    global counter
    counter += 1
    # print("Caught signal", counter)

    if counter >= THREADS:
        subprocess.call("kill $(ps aux | grep '[b]pftrace' | awk '{print $2}')")
        # end auto kill
        exit(0)


if __name__ == "__main__":
    THREADS = int(sys.argv[1])  # number of threads
    counter = 0
    while 1:
        signal.signal(signal.SIGUSR1, handler)

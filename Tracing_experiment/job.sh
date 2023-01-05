for counter in {1...5} # numer of fib jobs
do
  python3 job.py "$counter" 30 & sleep 0.015
done
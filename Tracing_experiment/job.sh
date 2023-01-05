for ((i = 1; i <= 5; i++)) # numer of fib jobs
do
  python3 job.py $i 30 & sleep 0.015
done

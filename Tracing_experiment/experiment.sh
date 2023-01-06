#!/bin/bash
truncate -s 0 file.txt; killall python3; killall bpftrace # clear output file and kill processes
for _ in {1..15} # number of iterations
do
  # first set - with tracing
  tracing_counter=0 # number of fib jobs completed
  sudo bpftrace context_switch_probe.bt >> raw.txt & # being tracing
  end=$((SECONDS+20)) # 10 seconds
  while [ $SECONDS -lt $end ]; do # continue for 10 seconds
      python3 job.py $tracing_counter 15 30 >> /dev/null &&
      tracing_counter=$((tracing_counter+1)) # run job and increment counter
  done
  # killall python3 && echo "kill python"
  echo $tracing_counter >> Logs/log_"$1".txt && echo "tracing set got through $tracing_counter" # output to log
  killall bpftrace && echo "kill bpftrace" # end tracing
  # second set - without tracing
  simple_counter=0 # number of fib jobs completed
  end=$((SECONDS+20)) # 10 seconds
  while [ $SECONDS -lt $end ]; do # continue for 10 seconds
      python3 job.py $simple_counter 15 30 >> /dev/null &&
      simple_counter=$((simple_counter+1)) # run job and increment counter
  done
  # killall python3 && echo "kill python"
  echo $simple_counter >> Logs/log_"$1".txt && echo "standard produced $simple_counter" # output to log
done
python3 processing.py "$1" 15 20s 15 30 # run number, iterations, time, threads, depth
git add .; git commit -m "add and process overhead experiment $1"; git push # add to git

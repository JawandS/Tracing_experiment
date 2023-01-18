#!/bin/bash
# start overhead
git pull
echo powersave | sudo tee /sys/devices/system/cpu/cpu*/cpufreq/scaling_governor # powersave or performance
increment=10
threads=20
depth=30
# define experiment
experiment() {
  # setup
  truncate -s 0 raw.txt
  killall -q python3
  killall -q bpftrace
  sleep 1   # wait for 1 second
  counter=0 # number of fib jobs completed
  # run tracing if necessary
  if $2 != ""; then
    # shellcheck disable=SC2024
    sudo bpftrace Script/"$2".bt >>raw.txt & # being tracing
  fi
  # run the jobs and count how many get done
  end=$((SECONDS + increment))    # 10 seconds
  while [ $SECONDS -lt $end ]; do # continue for 10 seconds
    python3 job.py counter $threads $depth >>/dev/null &&
      counter=$((counter + 1)) # run job and increment counter
  done
  # add jobs completed and output size to log
  echo $counter >>Logs/log_"$1".txt # add jobs done to log
  echo "Completed: $counter for $2"        # output to console
  if $2 != ""; then
    wc -l raw.txt >>Logs/log_"$1".txt
  else
    echo 0 >>Logs/log_"$1".txt # add size of log
  fi
  killall -q bpftrace # end tracing
}
# run experiment
iterationCounter=0
for _ in {1..20}; do # number of iterations
  iterationCounter=$((iterationCounter + 1)) && printf "\t---------Run %s---------\n" "$iterationCounter"
  experiment "$1" "" # base run
  experiment "$1" A  # context switch
  experiment "$1" B  # context switch + rcu
  experiment "$1" C  # rcu
done
python3 process.py "$1" 20 $increment $threads $depth "$2" # run number, iterations, time, threads, depth, governor
git add .
git commit -m "add and process overhead experiment $1"
git push # add to git

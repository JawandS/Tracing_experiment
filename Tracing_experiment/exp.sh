#!/bin/bash
# start overhead
git pull
echo "$2" | sudo tee /sys/devices/system/cpu/cpu*/cpufreq/scaling_governor # powersave or performance
increment=10
threads=20
depth=30
iterations=5
# define experiment
experiment() {
  # setup
  killall -q python3
  killall -q bpftrace
  truncate -s 0 raw.txt
  sleep 1   # wait for 1 second
  counter=0 # number of fib jobs completed
  # run tracing if necessary
  if [ "$2" != "N" ]; then
    # shellcheck disable=SC2024
    sudo bpftrace Script/"$2".bt >>raw.txt & # being tracing
  fi
  # run the jobs and count how many get done
  end=$((SECONDS + increment))    # 10 seconds
  while [ $SECONDS -lt $end ]; do # continue for 10 seconds
    python3 job.py counter $threads $depth >>/dev/null &&
      counter=$((counter + 1)) # run job and increment counter
  done
  # end tracing
  killall -q bpftrace
  # update logs
  echo $counter >>Logs/log_"$1".txt # add jobs done to log
  outputSize=$(wc -l raw.txt)
  echo "$outputSize" >>Logs/log_"$1".txt               # add output size to log
  echo "Completed: $counter for $2 with $outputSize events" # output to console
}
# run experiment
iterationCounter=0
for _ in {1..5}; do # number of iterations
  iterationCounter=$((iterationCounter + 1)) && printf "\t---------Run %s---------\n" "$iterationCounter"
  experiment "$1" N # base run
  experiment "$1" A  # context switch
  experiment "$1" B  # context switch + rcu
  experiment "$1" C  # rcu
  experiment "$1" D  # blank
  experiment "$1" E  # rcu + enter sleep
done
python3 process.py "$1" $iterations $increment $threads $depth "$2" # run number, iterations, time, threads, depth, governor
git add .
git commit -m "add and process overhead experiment $1"
git push # add to git

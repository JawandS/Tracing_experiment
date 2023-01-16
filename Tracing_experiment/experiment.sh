#!/bin/bash
echo "$2" | sudo tee /sys/devices/system/cpu/cpu*/cpufreq/scaling_governor # powersave or performance
iterationCounter=0
increment=20
threads=30
depth=54
# run experiment
for _ in {1..20}; do # number of iterations
  iterationCounter=$((iterationCounter + 1)) && printf "\t---------Run %s---------\n" "$iterationCounter"
  # clear output file and kill processes
  truncate -s 0 raw.txt
  truncate -s 0 rawTwo.txt
  killall -q python3
  killall -q bpftrace
  # first set - with two probes tracing
  sleep 1       # wait for 1 second
  two_counter=0 # number of fib jobs completed
  # shellcheck disable=SC2024
  sudo bpftrace two_probes.bt >>rawTwo.txt & # being tracing
  end=$((SECONDS + increment))               # 10 seconds
  while [ $SECONDS -lt $end ]; do            # continue for 10 seconds
    python3 job.py two_counter $threads $depth >>/dev/null &&
      two_counter=$((two_counter + 1)) # run job and increment counter
  done
  echo $two_counter >>Logs/log_"$1".txt && echo "Two probes: $two_counter" # output to log
  killall bpftrace                                                         # end tracing
  # second set - with tracing
  sleep 1           # wait for 1 second
  tracing_counter=0 # number of fib jobs completed
  # shellcheck disable=SC2024
  sudo bpftrace context_switch_probe.bt >>raw.txt & # begin tracing
  end=$((SECONDS + increment))                      # 10 seconds
  while [ $SECONDS -lt $end ]; do                   # continue for 10 seconds
    python3 job.py $tracing_counter $threads $depth >>/dev/null &&
      tracing_counter=$((tracing_counter + 1)) # run job and increment counter
  done
  echo $tracing_counter >>Logs/log_"$1".txt && echo "Tracing: $tracing_counter" # output to log
  killall bpftrace                                                              # end tracing
  # third set - without tracing
  sleep 1                         # wait for 1 second
  simple_counter=0                # number of fib jobs completed
  end=$((SECONDS + increment))    # 10 seconds
  while [ $SECONDS -lt $end ]; do # continue for 10 seconds
    python3 job.py $simple_counter $threads $depth >>/dev/null &&
      simple_counter=$((simple_counter + 1)) # run job and increment counter
  done
  # killall python3 && echo "kill python"
  echo $simple_counter >>Logs/log_"$1".txt && echo "Standard: $simple_counter" # output to log
  wc -l rawTwo.txt >>Logs/log_"$1".txt
  wc -l raw.txt >>Logs/log_"$1".txt
  echo ""
done
#echo "info: run number, iterations, time, threads, depth" >>Logs/log_"$1".txt
#echo "      $1          20          30s   15       27" >>Logs/log_"$1".txt
# add line numbers to info file
python3 processing.py "$1" 20 $increment $threads $depth "$2" # run number, iterations, time, threads, depth, governor
python3 visualizer.py "$1"                                    # add visual
git add .
git commit -m "add and process overhead experiment $1"
git push # add to git

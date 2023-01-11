#!/bin/bash
# run experiment
for _ in {1..20}; do # number of iterations
  # clear output file and kill processes
  truncate -s 0 raw.txt
  truncate -s 0 rawTwo.txt
  killall python3 >>/dev/null
  killall bpftrace >>/dev/null
  # first set - with two probes tracing
  sleep 1       # wait for 1 second
  two_counter=0 # number of fib jobs completed
  # shellcheck disable=SC2024
  sudo bpftrace two_probes.bt >>rawTwo.txt & # being tracing
  end=$((SECONDS + 30))                      # 10 seconds
  while [ $SECONDS -lt $end ]; do            # continue for 10 seconds
    python3 job.py two_counter 15 27 >>/dev/null &&
      two_counter=$((two_counter + 1)) # run job and increment counter
  done
  echo $two_counter >>Logs/log_"$1".txt && echo "two probes $two_counter" # output to log
  killall bpftrace && echo "kill bpftrace"                                # end tracing
  # second set - with tracing
  sleep 1           # wait for 1 second
  tracing_counter=0 # number of fib jobs completed
  # shellcheck disable=SC2024
  sudo bpftrace context_switch_probe.bt >>raw.txt & # being tracing
  end=$((SECONDS + 30))                             # 10 seconds
  while [ $SECONDS -lt $end ]; do                   # continue for 10 seconds
    python3 job.py $tracing_counter 15 27 >>/dev/null &&
      tracing_counter=$((tracing_counter + 1)) # run job and increment counter
  done
  echo $tracing_counter >>Logs/log_"$1".txt && echo "tracing set got through $tracing_counter" # output to log
  killall bpftrace && echo "kill bpftrace"                                                     # end tracing
  # third set - without tracing
  sleep 1                         # wait for 1 second
  simple_counter=0                # number of fib jobs completed
  end=$((SECONDS + 30))           # 10 seconds
  while [ $SECONDS -lt $end ]; do # continue for 10 seconds
    python3 job.py $simple_counter 15 27 >>/dev/null &&
      simple_counter=$((simple_counter + 1)) # run job and increment counter
  done
  # killall python3 && echo "kill python"
  echo $simple_counter >>Logs/log_"$1".txt && echo "standard produced $simple_counter" # output to log
  echo wc -l rawTwo.txt >>Logs/log_"$1".txt
  echo wc -l raw.txt >>Logs/log_"$1".txt
done
#echo "info: run number, iterations, time, threads, depth" >>Logs/log_"$1".txt
#echo "      $1          20          30s   15       27" >>Logs/log_"$1".txt
 # add line numbers to info file
python3 processing.py "$1" 20 30s 15 27 # run number, iterations, time, threads, depth
git add .
git commit -m "add and process overhead experiment $1"
git push # add to git

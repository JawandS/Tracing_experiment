#!/bin/bash
for _ in {1..3} # number of iterations
do
  # first set - with tracing
  tracing_counter=0 # number of fib jobs completed
  sudo bpftrace context_switch_probe.bt >> raw.txt & # being tracing
  end=$((SECONDS+10)) # 10 seconds
  while [ $SECONDS -lt $end ]; do # continue for 10 seconds
      ./job.sh &&
      tracing_counter=$((tracing_counter+1)) && echo $tracing_counter # run job and increment counter
  done
  echo $tracing_counter >> Logs/log_"$1".txt # output to log
  kill "$(ps aux | grep 'bpftrace' | awk '{print $2}')" # end tracing
  # second set - without tracing
  simple_counter=0 # number of fib jobs completed
  end=$((SECONDS+10)) # 10 seconds
  while [ $SECONDS -lt $end ]; do # continue for 10 seconds
      ./job.sh &&
      simple_counter=$((simple_counter+1)) && echo $simple_counter # run job and increment counter
  done
  echo $tracing_counter >> Logs/log_"$1".txt # output to log
done
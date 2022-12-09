#!/bin/bash
for run_num in {1..20}
do
  echo time +%N >> Logs/four_fib_"$1".txt
  # first job - with tracing
  for a_var in 1 2 3 4
  do
    python3 job.py tracing &
  done
  sudo python3 auto_kill.py & sudo bpftrace context_switch_probe.bt >> raw.txt
  echo time +%N >> Logs/four_fib_"$1".txt
  # second job - without tracing
  for b_var in 1 2 3 4
  do
    python3 job.py tracing &
  done
  sudo python3 auto_kill.py && echo time +%N >> Logs/four_fib_"$1".txt
  echo "$run_num"
done
sudo python3 processing.py "$1"
find . -size +98M | cat >> .gitignore
git commit -m "update .gitignore"
git add .
git commit -m "add and process probe experiment $1"
git push

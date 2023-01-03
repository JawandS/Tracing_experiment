#!/bin/bash
for run_num in {1..3} # number of total iterations
do
  echo date +"%T.%N" >> Logs/four_fib_"$1".txt # starting time for tracing set
  # first job - with tracing
  sudo bpftrace context_switch_probe.bt >> raw.txt & sudo python3 auto_kill.py &
  for a_var in {1...20}
  do
    python3 job.py $a_var 25 &
    sleep 0.015
  done
  echo date +"%T.%N" >> Logs/log_"$1".txt # end tracing, start non tracing
  # second job - without tracing
  for b_var in {1...20}
  do
    python3 job.py $b_var 25 &
    sleep 0.015
  done
  echo date +"%T.%N" >> Logs/four_fib_"$1".txt # end non tracing
done
sudo python3 processing.py "$1"
find . -size +98M | cat >> .gitignore
git commit -m "update .gitignore"
git add .
git commit -m "add and process probe experiment $1"
git push

#!/bin/bash
for run_num in {1..3} # number of total iterations
do
  echo date +"%T.%N" >> Logs/log_"$1".txt # starting time for tracing set
  counter=0
  # first set - with tracing
  sudo bpftrace context_switch_probe.bt >> raw.txt & while inotifywait -e close_write tracking.txt; do ((counter=counter+1)) && if [ $counter -ge 5 ]; then kill $(ps aux | grep '[b]pftrace' | awk '{print $2}'); fi; done &
  for a_var in {1...20}
  do
    python3 job.py $a_var 25 >> tracking.txt &
    sleep 0.015
  done
  echo date +"%T.%N" >> Logs/log_"$1".txt # end tracing, start non tracing
  # second set - without tracing
  for b_var in {1...20}
  do
    python3 job.py $b_var 25 &
    sleep 0.015
  done
  echo date +"%T.%N" >> Logs/log_"$1".txt # end non tracing
done
#sudo python3 processing.py "$1"
#find . -size +98M | cat >> .gitignore
#git commit -m "update .gitignore"
#git add .
#git commit -m "add and process probe experiment $1"
#git push

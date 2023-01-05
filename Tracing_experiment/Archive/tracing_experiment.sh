#!/bin/bash
for _ in {1..3} # number of iterations
do
  echo date +"%T.%N" >> Logs/log_"$1".txt # starting time for tracing set
  counter=0
  # first set - with tracing
  sudo bpftrace context_switch_probe.bt >> raw.txt & while inotifywait -q -q -e modify tracking.txt; do ((counter=counter+1)) && echo "$counter" && if [ "$counter" -ge 20 ]; then kill "$(ps aux | grep '[b]pftrace' | awk '{print $2}')" && echo "killing jobs"; fi; done &
  for a_var in {1...20}
  do
    python3 job.py "$a_var" 30 >> tracking.txt & sleep 0.015
  done
  echo date +"%T.%N" >> Logs/log_"$1".txt # end tracing, start non tracing
  # second set - without tracing
#  for b_var in {1...20}
#  do
#    python3 job.py "$b_var" 30 & sleep 0.015
#  done
#  echo date +"%T.%N" >> Logs/log_"$1".txt # end non tracing
done
#sudo python3 processing.py "$1"
#find . -size +98M | cat >> .gitignore
#git commit -m "update .gitignore"
#git add .
#git commit -m "add and process probe experiment $1"
#git push

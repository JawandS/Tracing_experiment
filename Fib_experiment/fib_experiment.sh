#!/bin/bash
for counter in 1 2 3 4 5 6 7
do
  python3 job.py $counter &
done
sudo bpftrace -e 'tracepoint:sched:sched_switch { printf("%s %lu %d %lu\n", comm, pid, cpu, nsecs); }' >> Logs/log_"$1".txt &
sudo python3 auto_kill.py && sudo python3 processing.py "$1"
find . -size +99M | cat >> ../.gitignore
git commit -m "update .gitignore"
git add .
git commit -m "add and process $1"
git push

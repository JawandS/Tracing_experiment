#!/bin/bash
# setup
git pull
echo performance | sudo tee /sys/devices/system/cpu/cpu*/cpufreq/scaling_governor # powersave or performance
increment=15
threads=20
depth=30
# clear previous jobs
killall -q python3
killall -q bpftrace
# begin tracing
sudo bpftrace context_switch_probe.bt >>Logs/log_"$1".txt &
# start workload
counter=0
end=$((SECONDS + increment))
while [ $SECONDS -lt $end ]; do                                                   # continue for 10 seconds
  python3 job.py $counter $threads $depth >>/dev/null && counter=$((counter + 1)) # run job and increment counter
done
# clear previous jobs
killall -q python3
killall -q bpftrace
# process results
echo "length: $increment | threads: $threads | depth: $depth | jobs: $counter" >>Results/results.txt # output to log
sudo python3 processing.py "$1"
# add to git
find . -size +99M | cat >>../.gitignore
git commit -m -q "update .gitignore"
git add .
git commit -m "add and process $1"
git push

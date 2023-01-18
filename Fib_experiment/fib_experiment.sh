#!/bin/bash
# setup
git pull -q
sudo echo performance >>/sys/devices/system/cpu/cpu*/cpufreq/scaling_governor # powersave or performance
increment=15
threads=20
depth=30
isVariable="$2"
# clear previous jobs
killall -q python3
killall -q bpftrace
# begin tracing
sudo bpftrace context_switch_probe.bt >>Logs/log_"$1".txt &
# start workload
counter=0
end=$((SECONDS + increment))
while [ $SECONDS -lt $end ]; do
  python3 job.py $counter $threads $depth "$isVariable" >>/dev/null && counter=$((counter + 1)) # run job and increment counter
done
# clear previous jobs
killall -q python3
killall -q bpftrace
# process results
result="job: $1 | length: $increment | threads: $threads | depth: $depth | jobs: $counter | isVariable: $isVariable"
echo "$result"
echo "$result" >>Results/results.txt # output to log
#sudo python3 processing.py "$1"
# add to git
git add -q .
git commit -q -m "add and process $1"
git push -q

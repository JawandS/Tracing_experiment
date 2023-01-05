#!/bin/bash
counter=0
sudo bpftrace context_switch_probe.bt >> /dev/null &
while inotifywait -e modify tracking.txt; do counter=$((counter+1)) && if [ $counter -ge 5 ]; then kill $(ps aux | grep '[b]pftrace' | awk '{print $2}'); kill $(ps aux | grep '[i]notifywait' | awk '{print $2}'); fi; done
#sudo when-changed tracking.txt 'echo $counter && counter=$((counter+1)) && echo "second print " && echo $counter';
echo $counter

#!/bin/bash
sudo bpftrace context_switch_probe.bt >> raw.txt &
sudo python3 auto_kill.py 100 &
for job_num in {1..100}
do
  #              id         depth
  sudo python3 job.py "$job_num" 30 &
done
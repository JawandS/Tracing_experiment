#!/bin/bash
start = $(date +%s)
sudo bpftrace context_switch_probe.bt >> raw.txt
for job_num in {1..100}
do
  #              id         depth
  python3 job.py "$job_num" 30 &
done
end = $(date +%s)
echo $end - $start
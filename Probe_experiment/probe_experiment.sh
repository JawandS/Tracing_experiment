#!/bin/bash
for counter in {1..20}
do
    date +%N >> Logs/run"$1".txt
    sudo bpftrace context_switch_probe.bt >> /dev/null
    sudo kill pidof bpftrace
    date +%N >> Logs/run"$1".txt
done
sudo python3 processing.py "$1"
find . -size +99M | cat >> ./.gitignore
git commit -m "update .gitignore"
git add .
git commit -m "add and process probe experiment $1"
git push

#!/bin/bash
for counter in {1..20}
do
    sudo python3 model.py -1 quiet >> Logs/run"$1".txt & sudo bpftrace two_probes.bt >> /dev/null
    sudo python3 model.py -1 quiet >> Logs/run"$1".txt
    echo $counter
done
sudo python3 processing.py "$1"
find . -size +99M | cat >> ./.gitignore
git commit -m "update .gitignore"
git add .
git commit -m "add and process probe experiment $1"
git push

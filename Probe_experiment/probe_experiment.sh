#!/bin/bash
for counter in {1..20}
do
    sudo python3 model.py -1 quiet >> Results/run"$1".txt & sudo bpftrace two_probes.bt >> junk.txt
    sudo python3 model.py -1 quiet >> Results/run"$1".txt
    echo $counter
done
find . -size +99M | cat >> ../.gitignore
git commit -m "update .gitignore"
git add .
git commit -m "$1"
git push

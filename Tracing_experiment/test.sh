#!/bin/bash
counter=0
sudo when-changed tracking.txt 'echo $counter && counter=$((counter+1)) && echo $counter';
echo $counter

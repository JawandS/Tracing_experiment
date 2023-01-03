#!/bin/bash
counter=0
counter=((counter+1))
while inotifywait -e close_write tracking.txt; do "echo $counter; echo $counter"; done
#sudo when-changed tracking.txt 'echo $counter && counter=$((counter+1)) && echo "second print " && echo $counter';
echo $counter
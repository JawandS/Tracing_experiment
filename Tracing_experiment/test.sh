#!/bin/bash
counter=0
sudo when-changed tracking.txt tracking.txt counter=$counter+1; cat $counter &

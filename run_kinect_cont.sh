#!/bin/bash
runtime="300 minute"
endtime=$(date -ud "$runtime" +%s)
while [ $(date -u +%s) -le $endtime ];
do
    echo "Time Now: `date +%H:%M:%S`"
    time=`date +%s`
    python3 kinect_save.py "$time"
    echo "done capturing with kinect and realsense"
    echo "Sleeping for 10 seconds"
    sleep 10
done
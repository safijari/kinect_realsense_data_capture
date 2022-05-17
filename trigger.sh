#!/bin/bash
time=`date +%s`
python3 realsense_save.py "$time" $1
python3 kinect_save.py "$time"

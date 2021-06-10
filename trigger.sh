#!/bin/bash
time=`date +%s`
python3 realsense_save.py "$time"
python3 kinect_save.py "$time"
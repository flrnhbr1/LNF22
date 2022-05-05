#!/bin/bash

cd
source /opt/ros/noetic/setup.bash
source crazyswarm/ros_ws/devel/setup.bash
cd crazyswarm/ros_ws/src/crazyswarm/scripts
python3 chooser.py
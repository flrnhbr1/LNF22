#!/usr/bin/env python

import numpy as np
from pycrazyswarm import *

RefHeight = 0.75
swarm = Crazyswarm()
timeHelper = swarm.timeHelper
cf = swarm.allcfs.crazyflies[0]
wand = swarm.allcfs.crazyflies[1]

def landInOrigin():
    # function that makes the cf fly back to (0,0,RefHeigth+0.5) and land there
    cf.goTo([0, 0, RefHeight+0.5], yaw=0, duration=5)   
    timeHelper.sleep(5)
    cf.land(targetHeight=RefHeight+0.02, duration=2)
    timeHelper.sleep(2)


def followTheWand():
    offset = np.array([1.0, 0.0, 0.0])  # offset in which the drone should follow the wand
    cf.takeoff(targetHeight=RefHeight+0.5, duration=2)
    timeHelper.sleep(2)

    # Wait until key is pressed before following the wand
    print("press button to continue\n\n\n")
    swarm.input.waitUntilButtonPressed()

    i = 0
    while i <= 100:
        cf.cmdPosition(wand.position() + offset, yaw=0.0)
        timeHelper.sleep(0.1)
        i = i+1

    cf.notifySetpointsStop(remainValidMillisecs=100)    # Needed for change of low-lvl commander to high-lvl commander (cmdPosition -> goTo)
    landInOrigin()


def followTheWaypoints():
    waypoints = np.array([
        (0.0, 0.0, 0.0),
        (0.0, 0.0, 0.0),
        (0.0, 0.0, 0.0),
        (0.0, 0.0, 0.0),
    ])

    print("Press button to set first waypoint\n\n\n")
    swarm.input.waitUntilButtonPressed()
    waypoints[0] = wand.position()

    print("Press button to set second waypoint\n\n\n")
    swarm.input.waitUntilButtonPressed()
    waypoints[1] = wand.position()

    print("Press button to set third waypoint\n\n\n")
    swarm.input.waitUntilButtonPressed()
    waypoints[2] = wand.position()

    print("Press button to set fourth waypoint\n\n\n")
    swarm.input.waitUntilButtonPressed()
    waypoints[3] = wand.position()


    print("Press button to start flying")
    swarm.input.waitUntilButtonPressed()

    print(waypoints)  

    cf.takeoff(targetHeight=1, duration=2)
    timeHelper.sleep(3)

    for p in waypoints:
        cf.goTo(p, yaw=0.0, duration=3)
        timeHelper.sleep(4)

    landInOrigin()


def followThePath():
    n = 100     # amount of samples

    # Sample wand path    
    print("\n\n\n\n------------------------------ Wand Sampling ------------------------------\n\n\n")
    n = 10 * input('Enter the amount of time for sampling the path [sec]:\n\n\n') # make ~10 samples / second
    print("Press a button to start the trajectory sampling process!\n\n\n\n")
    
    samples = np.zeros((n, 3))
    swarm.input.waitUntilButtonPressed()
    
    for i in range(0,n):
        samples[i,:] = wand.position()
        timeHelper.sleep(0.1)


    # Fly the path
    print("\n\n--------------------Press a button to fly the path!--------------------")
    swarm.input.waitUntilButtonPressed()

    cf.takeoff(targetHeight=1.0, duration=2.0)
    timeHelper.sleep(2.1)

    cf.goTo(samples[0,:], yaw=0.0, duration=2)  # fly to first sample point (in high-lvl commander)
    timeHelper.sleep(3)

    for p in samples:
        cf.cmdPosition(p, yaw=0.0)
        timeHelper.sleep(0.1)

    cf.notifySetpointsStop(remainValidMillisecs=100)    # Needed for change of low-lvl commander to high-lvl commander (cmdPosition -> goTo)

    landInOrigin()


def main():
    progCode = input('Enter programcode to execute:\nFollow the wand --> 0\nFollow the Waypoints --> 1\nFollow the path --> 2\n\n\n')
    if progCode == 0:
        followTheWand()
    elif progCode == 1:
        followTheWaypoints()
    elif progCode == 2:
        followThePathl()
    else:
        print("Programcode invalid!")


if __name__ == "__main__":
    main()
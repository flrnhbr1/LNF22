#!/usr/bin/env python

import numpy as np
from pycrazyswarm import *
import uav_trajectory


def landInOrigin(cf, RefHeight, timeHelper):
    #
    # function that makes the cf fly back to the origin (0,0,RefHeigth+0.5) and land there
    #

    cf.goTo([0, 0, RefHeight+0.5], yaw=0, duration=5)   
    timeHelper.sleep(5)
    cf.land(targetHeight=RefHeight+0.02, duration=2)
    timeHelper.sleep(2)


def figure8(cf, RefHeight, timeHelper):
    #
    # fly a 8 figure forwards and backwards
    #

    traj1 = uav_trajectory.Trajectory()
    traj1.loadcsv("figure8.csv")

    TRIALS = 1
    TIMESCALE = 1.0
    for i in range(TRIALS):
        cf.uploadTrajectory(0, 0, traj1)

        cf.takeoff(targetHeight=RefHeight+0.5, duration=2.0)
        timeHelper.sleep(2.5)
        

        cf.startTrajectory(0, timescale=TIMESCALE)
        timeHelper.sleep(traj1.duration * TIMESCALE + 2.0)
        cf.startTrajectory(0, timescale=TIMESCALE, reverse=True)
        timeHelper.sleep(traj1.duration * TIMESCALE + 2.0)

        cf.land(targetHeight=RefHeight+0.02, duration=2.0)
        timeHelper.sleep(3.0)


def followTheWand(cf, wand, sampleAmount, RefHeight, swarm, timeHelper):
    #
    # Follow the wand with a given distance
    #

    offset = np.array([1.0, 0.0, 0.0])  # offset in which the drone should follow the wand
    cf.takeoff(targetHeight=RefHeight+0.5, duration=2)
    timeHelper.sleep(2)

    # Wait until key is pressed before following the wand
    print("press button to start following the wand\n\n\n")
    swarm.input.waitUntilButtonPressed()

    i = 0
    while i <= sampleAmount:
        cf.cmdPosition(wand.position() + offset, yaw=0.0)
        timeHelper.sleep(0.1)
        i = i+1

    cf.notifySetpointsStop(remainValidMillisecs=100)    # Needed for change of low-lvl commander to high-lvl commander (cmdPosition -> goTo)
    landInOrigin(cf, RefHeight, timeHelper)


def followTheWaypoints(cf, wand, RefHeight, swarm, timeHelper):
    #
    # Set 4 waypoints and fly straight lines between those points
    #

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
        cf.goTo(p, yaw=0.0, duration=4)
        timeHelper.sleep(4)

    landInOrigin(cf, RefHeight, timeHelper)


def followThePath(cf, wand, sampleAmount, RefHeight, swarm, timeHelper):
    #
    # Draw a path in the capture volume and fly through this path afterwards
    #

    # Sample wand path    
    print("\n\n\n\n------------------------------ Wand Sampling ------------------------------\n\n\n")
    print("Press a button to start the trajectory sampling process!\n\n\n\n")
    
    samples = np.zeros((sampleAmount, 3))
    swarm.input.waitUntilButtonPressed()
    
    for i in range(0,sampleAmount):
        samples[i,:] = wand.position()
        timeHelper.sleep(0.1)


    # Fly the path
    print("\n\n--------------------Press a button to fly the path!--------------------")
    swarm.input.waitUntilButtonPressed()

    cf.takeoff(targetHeight=1.0, duration=2.0)
    timeHelper.sleep(2.1)

    cf.goTo(samples[0,:], yaw=0.0, duration=2)  # fly to first sample point (in high-lvl commander)
    timeHelper.sleep(3)

    for n in samples:
        cf.cmdPosition(n, yaw=0.0)
        timeHelper.sleep(0.1)

    cf.notifySetpointsStop(remainValidMillisecs=100)    # Needed for change of low-lvl commander to high-lvl commander (cmdPosition -> goTo)

    landInOrigin(cf, RefHeight, timeHelper)


def main():
    RefHeight = 0.75
    swarm = Crazyswarm()
    timeHelper = swarm.timeHelper
    cf = swarm.allcfs.crazyflies[0]
    wand = swarm.allcfs.crazyflies[1]
    sampleAmount = 0

    progCode = int(input('Enter programcode to execute:\n\nFly a 8: --> 1\n\nFollow the wand --> 2\n\nFollow the Waypoints --> 3\n\nFollow the path --> 4\n\n\n'))

    if progCode == 1:
        figure8(cf, RefHeight, timeHelper)

    elif progCode == 2:
        sampleAmount = (10*int(input('Enter time the cf should follow the wand[s]: ')))     # ~10 samples per second are taken
        followTheWand(cf, wand, sampleAmount, RefHeight, swarm, timeHelper)

    elif progCode == 3:
        followTheWaypoints(cf, wand, RefHeight, swarm, timeHelper)

    elif progCode == 4:
        sampleAmount = (10*int(input('Enter time the path should be stored[s]: ')))     # ~10 samples per second are taken
        followThePath(cf, wand, sampleAmount, RefHeight, swarm, timeHelper)
        
    else:
        print("Programcode invalid!")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3

import numpy as np
from colorama import init
from termcolor import colored
from pycrazyswarm import *
import uav_trajectory


def landInOrigin(cf, RefHeigth,timeHelper):
    #
    # function that makes the cf fly back to the origin (0,0,RefHeigth+0.5) and land there
    #

    cf.goTo([0, 0, RefHeigth+0.5], yaw=0, duration=5)
    timeHelper.sleep(5)
    cf.land(targetHeight=RefHeigth+0.05, duration=2)
    timeHelper.sleep(2)


def hoverTest(cf, RefHeigth, FlightHeigth, timeHelper):
    #
    # takeoff, hover for 5 seconds than land 
    #
    
    cf.takeoff(targetHeight=FlightHeigth, duration=2)
    timeHelper.sleep(2 + 5)
    cf.land(targetHeight=RefHeigth+0.05, duration=2)
    timeHelper.sleep(2)


def figure8(cf, RefHeigth, FlightHeigth, timeHelper):
    #
    # fly a predefined figure (in this script a 8 shaped figure) forwards and backwards
    #

    traj1 = uav_trajectory.Trajectory()
    traj1.loadcsv("figure8.csv")

    TRIALS = 1
    TIMESCALE = 1

    for i in range(TRIALS):
        cf.uploadTrajectory(0, 0, traj1)
        cf.takeoff(targetHeight=FlightHeigth, duration=2)
        timeHelper.sleep(2)

        # Fly the trajectory forwards
        cf.startTrajectory(0, timescale=TIMESCALE)
        timeHelper.sleep(traj1.duration * TIMESCALE+2)

        # Fly the trajectory backwards
        cf.startTrajectory(0, timescale=TIMESCALE, reverse=True)
        timeHelper.sleep(traj1.duration * TIMESCALE + 2)

        cf.land(targetHeight=RefHeigth+0.05, duration=3)
        timeHelper.sleep(3)


def followTheWand(cf, wand, sampleAmount, RefHeigth, FlightHeigth, swarm, timeHelper):
    #
    # Follow the wand with a given distance
    #

    offset = np.array([0.7, 0.0, 0.0])  # offset in which the drone should follow the wand
    cf.takeoff(targetHeight=FlightHeigth, duration=2)
    timeHelper.sleep(2)

    # Wait until key is pressed before following the wand
    print("press key to start following the wand\n\n\n")
    swarm.input.waitUntilButtonPressed()

    # Following process
    i = 0
    while i <= sampleAmount:
        cf.cmdPosition(wand.position() + offset, yaw=0.0)
        timeHelper.sleep(0.1)
        i = i+1

    cf.notifySetpointsStop(remainValidMillisecs=100)    # Needed for change of low-lvl commander to high-lvl commander (cmdPosition -> goTo)
    landInOrigin(cf, RefHeigth, timeHelper)


def followTheWaypoints(cf, wand, RefHeigth, FlightHeigth, swarm, timeHelper):
    #
    # Set 4 waypoints and fly straight lines between those points
    #

    waypoints = np.array([
        (0.0, 0.0, 0.0),
        (0.0, 0.0, 0.0),
        (0.0, 0.0, 0.0),
        (0.0, 0.0, 0.0),
    ])

    print("\n\n\nPress key to set 1 waypoint\n\n\n")
    swarm.input.waitUntilButtonPressed()
    waypoints[0] = wand.position()

    print("Press key to set 2 waypoint\n\n\n")
    swarm.input.waitUntilButtonPressed()
    waypoints[1] = wand.position()

    print("Press key to set 3 waypoint\n\n\n")
    swarm.input.waitUntilButtonPressed()
    waypoints[2] = wand.position()

    print("Press key to set 4 waypoint\n\n\n")
    swarm.input.waitUntilButtonPressed()
    waypoints[3] = wand.position()


    print("Press key to start flying\n\n\n")
    swarm.input.waitUntilButtonPressed()

    # Printing the initialized waypoints
    print(waypoints)  

    cf.takeoff(targetHeight=FlightHeigth, duration=2)
    timeHelper.sleep(3)

    # Fly to all waypoints
    for p in waypoints:
        cf.goTo(p, yaw=0, duration=3)
        timeHelper.sleep(3)

    landInOrigin(cf, RefHeigth, timeHelper)


def followThePath(cf, wand, sampleAmount, RefHeigth, FlightHeigth, swarm, timeHelper):
    #
    # Draw a path in the capture volume and fly through this path afterwards
    #

    # Sample wand path    
    print("\n\n\n\nPress a key to start the trajectory sampling process\n\n\n")
    
    samples = np.zeros((sampleAmount, 3))
    swarm.input.waitUntilButtonPressed()
    
    for i in range(0,sampleAmount):
        samples[i,:] = wand.position()
        timeHelper.sleep(0.1)


    # Fly the path
    print("Press a key to fly the path\n\n\n")
    swarm.input.waitUntilButtonPressed()

    cf.takeoff(targetHeight=FlightHeigth, duration=2)
    timeHelper.sleep(2)

    cf.goTo(samples[0,:], yaw=0, duration=2)  # fly to first sample point (in high-lvl commander)
    timeHelper.sleep(2)

    for n in samples:
        cf.cmdPosition(n, yaw=0)
        timeHelper.sleep(0.1)

    cf.notifySetpointsStop(remainValidMillisecs=100)    # Needed for change of low-lvl commander to high-lvl commander (cmdPosition -> goTo)

    landInOrigin(cf, RefHeigth, timeHelper)


def main():
    RefHeigth = 0   # Height of starting point
    FlightHeigth = RefHeigth + 1.5
    swarm = Crazyswarm()
    timeHelper = swarm.timeHelper
    cf = swarm.allcfs.crazyflies[0]
    wand = swarm.allcfs.crazyflies[1]
    sampleAmount = 0

    # Progcode:
    #   0  -->  hoverTest           ...  Fly straigth up, hover 5 seconds and land again.
    #   1  -->  figure8             ...  Fly a trajectory two times, that looks like the number 8.
    #   2  -->  followTheWand       ...  The drone follows the wand for a given amount of time in a specific distance.
    #   3  -->  followTheWaypoints  ...  With the help of the wand, waypoints inside the capture volume can be set, after all are set the drone can fly along these waypoints.
    #   4  -->  followThePath       ...  With the help of the wand, a path can be drawn inside the capture volume, for a specific time.
    #                                    After the path is drwan, the drone will fly along this path and land again.

    progCode = int(input('Enter programcode to execute:\n\nHover test: --> 0\n\nFly a 8: --> 1\n\nFollow the wand --> 2\n\nFollow the Waypoints --> 3\n\nFollow the path --> 4\n\n\n'))
    print("\n\n")
    init()  # for printing in color
    if progCode == 0:
        print(colored('--- Hover Test --- ', 'white', 'on_blue'))
        hoverTest(cf ,RefHeigth, FlightHeigth, timeHelper)

    elif progCode == 1:
        print(colored('--- Figure 8 --- ', 'white', 'on_blue'))
        figure8(cf, RefHeigth, FlightHeigth, timeHelper)

    elif progCode == 2:
        print(colored('--- Follow the wand --- ', 'white', 'on_blue'))
        sampleAmount = (10*int(input('Enter time the cf should follow the wand[s]: ')))     # ~10 samples per second are taken
        followTheWand(cf, wand, sampleAmount, RefHeigth, FlightHeigth, swarm, timeHelper)

    elif progCode == 3:
        print(colored('--- Follow the waypoints --- ', 'white', 'on_blue'))
        followTheWaypoints(cf, wand, RefHeigth, FlightHeigth, swarm, timeHelper)

    elif progCode == 4:
        print(colored('--- Follow the path --- ', 'white', 'on_blue'))
        sampleAmount = (10*int(input('Enter time the path should be stored[s]: ')))     # ~10 samples per second are taken
        followThePath(cf, wand, sampleAmount, RefHeigth, FlightHeigth, swarm, timeHelper)
        
    else:
        print("Programcode invalid!")


if __name__ == "__main__":
    main()
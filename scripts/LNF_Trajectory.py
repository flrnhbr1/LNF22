#!/usr/bin/env python

import numpy as np
from pycrazyswarm import *

REF = 0.75
Z = REF + 0.5

if __name__ == "__main__":
    swarm = Crazyswarm()
    timeHelper = swarm.timeHelper
    cf = swarm.allcfs.crazyflies[0]
    wand = swarm.allcfs.crazyflies[1]
    n = 100     # amount of samples

    # Sample wand trajectory
    print("\n\n\n\n------------------------------ Wand Sampling ------------------------------ ")
    print("Draw a trajectory with the wand, which the drone should fly")
    print("Press a button to start the trajectory sampling process!\n\n\n\n")
    
    samples = np.zeros((n, 3))
    swarm.input.waitUntilButtonPressed()
    
    for i in range(0,n):
        samples[i,:] = wand.position()
        timeHelper.sleep(0.1)
    # print(samples)
    # print("--")
    # print(samples[0,:])

    # Fly the trajectory
    print("\n\n--------------------Press a button to fly the trajectory!--------------------")
    swarm.input.waitUntilButtonPressed()

    cf.takeoff(targetHeight=1.0, duration=2.0)
    timeHelper.sleep(2.1)

    cf.goTo(samples[0,:], yaw=0.0, duration=2)  # fly to first sample point (in high-lvl commander)
    timeHelper.sleep(3)

    for p in samples:
        cf.cmdPosition(p, yaw=0.0)
        timeHelper.sleep(0.1)

    cf.notifySetpointsStop(remainValidMillisecs=100)    # Needed for change of low-lvl commander to high-lvl commander (cmdPosition -> goTo)

    cf.goTo([0, 0, 1], yaw=0, duration=5)   # fly back to the origin
    timeHelper.sleep(5)
    cf.land(targetHeight=REF + 0.02, duration=2)
    timeHelper.sleep(2)



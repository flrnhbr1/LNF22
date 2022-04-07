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
    offset = np.array([1.0, 0.0, 0.0])  # offset in which the drone should follow the wand

    cf.takeoff(targetHeight=Z, duration=1.0+Z)
    timeHelper.sleep(1.5+Z)

    # Wait until key is pressed before following the wand
    print("press button to continue...")
    swarm.input.waitUntilButtonPressed()

    i = 0
    while i <= 100:
        cf.cmdPosition(wand.position() + offset, yaw=0.0)
        timeHelper.sleep(0.1)
        i = i+1

    cf.notifySetpointsStop(remainValidMillisecs=100)    # Needed for change of low-lvl commander to high-lvl commander (cmdPosition -> goTo)

    cf.goTo([0, 0, 1], yaw=0, duration=5)   # fly back to the origin
    timeHelper.sleep(5)
    cf.land(targetHeight=REF + 0.02, duration=1.0+Z)
    timeHelper.sleep(1.0+Z)



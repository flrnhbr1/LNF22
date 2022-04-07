#!/usr/bin/env python

import numpy as np

from pycrazyswarm import *
import uav_trajectory

if __name__ == "__main__":

    Ref = 0.75
    Z = Ref+0.5

    swarm = Crazyswarm()
    timeHelper = swarm.timeHelper
    cf = swarm.allcfs.crazyflies[0]

    traj1 = uav_trajectory.Trajectory()
    traj1.loadcsv("figure8.csv")

    TRIALS = 1
    TIMESCALE = 1.0
    for i in range(TRIALS):
        #for cf in cf.crazyflies:
        cf.uploadTrajectory(0, 0, traj1)

        cf.takeoff(targetHeight=Z, duration=2.0)
        timeHelper.sleep(2.5)
        

        cf.startTrajectory(0, timescale=TIMESCALE)
        timeHelper.sleep(traj1.duration * TIMESCALE + 2.0)
#        allcfs.startTrajectory(0, timescale=TIMESCALE, reverse=True)
#       timeHelper.sleep(traj1.duration * TIMESCALE + 2.0)

        cf.land(targetHeight=Ref+0.02, duration=2.0)
        timeHelper.sleep(3.0)

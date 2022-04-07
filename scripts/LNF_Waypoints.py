#!/usr/bin/env python

import numpy as np

from pycrazyswarm import Crazyswarm

REF = 0.75
Z = REF + 0.5

if __name__ == "__main__":
    swarm = Crazyswarm()
    timeHelper = swarm.timeHelper
    cf = swarm.allcfs.crazyflies[0]
    wand = swarm.allcfs.crazyflies[1]
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

    # print(waypoints)    


    cf.takeoff(targetHeight=1, duration=2)
    timeHelper.sleep(3)

    for p in waypoints:
        cf.goTo(p, yaw=0.0, duration=3)
        timeHelper.sleep(4)

    cf.goTo([0, 0, 1], yaw=0, duration=5)
    timeHelper.sleep(5)
    cf.land(targetHeight=REF + 0.02, duration=2)
    timeHelper.sleep(2)
    



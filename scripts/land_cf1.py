#!/usr/bin/env python3

from pycrazyswarm import Crazyswarm

#
# Land cf1 
#

def main():
    swarm = Crazyswarm()
    timeHelper = swarm.timeHelper
    cf = swarm.allcfs.crazyflies[0]
    timeHelper.sleep(0.5)
    cf.land(targetHeight=0.75+0.02, duration=3)
    timeHelper.sleep(3)


if __name__ == "__main__":
    main()

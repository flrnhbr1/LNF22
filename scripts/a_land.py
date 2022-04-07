import numpy as np

from pycrazyswarm import Crazyswarm


def main():
    swarm = Crazyswarm()
    timeHelper = swarm.timeHelper
    cf = swarm.allcfs.crazyflies[0]
    timeHelper.sleep(0.5)
#    cf.takeoff(targetHeight=Z, duration=TAKEOFF_DURATION)
    timeHelper.sleep(3 + 1.0)

    cf.land(targetHeight=0.75+0.02, duration=3)
    timeHelper.sleep(3 + 1.0)


if __name__ == "__main__":
    main()

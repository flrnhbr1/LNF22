import math
from pycrazyswarm import Crazyswarm


TAKEOFF_DURATION = 2.5
HOVER_DURATION = 1.0
GOTO_DURATION = 0.01

CIRCLE = 2 * math.pi
STEPS = 100
ROTATIONS = 10
MAX_HEIGTH = 3


def main():
    swarm = Crazyswarm()
    timeHelper = swarm.timeHelper
    cf1 = swarm.allcfs.crazyflies[0]
    cf2 = swarm.allcfs.crazyflies[1]

    #takeoff drone 1
    cf1.takeoff(targetHeight=0.1, duration=TAKEOFF_DURATION)
    timeHelper.sleep(TAKEOFF_DURATION + HOVER_DURATION)

    #flight drone 1
    cf1.goTo([1,0,0], 0, 2, True)
    timeHelper.sleep(GOTO_DURATION)

    angle = 0
    xPos = 0
    yPos = 0
    zPos = 0.1

    while zPos <= MAX_HEIGTH:
        angle += (CIRCLE / STEPS)
        xPos = math.cos(angle)
        yPos = math.sin(angle)
        zPos += 1/STEPS

        cf1.goTo([xPos,yPos,zPos], 0, 0.01)
        timeHelper.sleep(GOTO_DURATION)

    #land drone 1
    cf1.land(targetHeight=0.04, duration=2.5)
    timeHelper.sleep(TAKEOFF_DURATION)


if __name__ == "__main__":
    main()

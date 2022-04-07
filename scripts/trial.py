

from pycrazyswarm import Crazyswarm


TAKEOFF_DURATION = 0.75
HOVER_DURATION = 0.25


def main():
	swarm = Crazyswarm()
	timeHelper = swarm.timeHelper
	cf = swarm.allcfs.crazyflies[0] 
	cf.takeoff(targetHeight=1.0, duration=TAKEOFF_DURATION)
	timeHelper.sleep(TAKEOFF_DURATION + HOVER_DURATION)
	i = 0
   
	while i <= 10:
		#define position array
		cf_pos = cf.position().copy()
		#increment x coord. by 1cm
		cf_pos[0] = cf_pos[0]+0.01
		#fly
		#cmdPosition(cf_pos, yaw=0)
		cf.goTo(cf_pos, 0, 1, False)
		i = i+1
		timeHelper.sleep(1)
	
	cf.land(targetHeight=0.04, duration=0.25)
	timeHelper.sleep(TAKEOFF_DURATION)


if __name__ == "__main__":
    main()

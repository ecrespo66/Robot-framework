import sys
import traceback
from iBott import RobotFlow, RobotBaseException, System
from robot.robot import Robot


if __name__ == "__main__":
    try:
        args = System.get_args(sys.argv)
        robot = Robot(args)
        RobotFlow.run_robot(robot)
    except:
        raise RobotBaseException(robot)




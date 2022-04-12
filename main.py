import sys
from iBott.robot_activities.flow import RobotFlow
from iBott.robot_activities.exceptions import RobotBaseException
from iBott.robot_activities.server import OrchestratorAPI
from robot.robot import Robot


if __name__ == "__main__":
    try:
        kwargs = OrchestratorAPI.get_args(sys.argv)
        robot = Robot(**kwargs)
        RobotFlow.run_robot(robot)
    except:
        raise RobotBaseException(robot)




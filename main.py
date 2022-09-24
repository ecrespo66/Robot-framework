import sys
from robot_manager.flow import RobotFlow
from robot_manager.server import OrchestratorAPI
from robot.robot import Robot


if __name__ == "__main__":
    try:
        kwargs = OrchestratorAPI.get_args(sys.argv)
        robot = Robot(**kwargs)
        RobotFlow.run_robot(robot)
    except Exception as e:
        raise Exception(e)




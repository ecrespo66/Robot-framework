import sys
import json
import robot

if __name__ == "__main__":
    args = json.loads(str(sys.argv[1]))
    robot.Main(args).runRobot()

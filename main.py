import sys
import json
import traceback

import robot

if __name__ == "__main__":
    args = json.loads(str(sys.argv[1]))
    try:
        Robot = robot.Main(args)
        Robot.runRobot()
    except Exception as e:

        Robot.Log.systemException(str(e))
        Robot.Log.systemException(str(traceback.print_exception()))


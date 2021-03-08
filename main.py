import sys
import traceback
from robot import robot
import json
if __name__ == "__main__":
    args = eval(sys.argv[1].replace("'", '"'))
    try:
        Robot = robot.Main(args)
        Robot.cleanup()
        Robot.init()
        Robot.run()
        Robot.end()
    except:
        for line in traceback.format_exc().splitlines():
            Robot.Log.systemException(str(line))
        Robot.Log.systemException("[Execution Failed]")

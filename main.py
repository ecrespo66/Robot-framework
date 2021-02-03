import sys
import json
import traceback
from .robot import Main

if __name__ == "__main__":
    args = json.loads(str(sys.argv[1]))
    try:
        Robot = Main(args)
        Robot.runRobot()
    except:
        for line in traceback.format_exc().splitlines():
            Robot.Log.systemException(str(line))
        Robot.Log.systemException("[Execution Failed]")

import sys
import traceback
from robot import robot

if __name__ == "__main__":
    if len(sys.argv) > 1:
        args = eval(sys.argv[1].replace("'", '"'))
    else:
        args = None
    try:
        Robot = robot.Main(args)
        for method in Robot.methods:
            method()
        Robot.finishExecution()

    except:
        if len(sys.argv) > 1:
            for line in traceback.format_exc().splitlines():
                Robot.Log.systemException(str(line))
            Robot.Log.systemException("[Execution Failed]")
        else:
            raise Exception

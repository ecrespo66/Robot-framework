import sys
import json
import robot

if __name__ == "__main__":
    args = json.loads(str(sys.argv[1]))
    try:
        robot.Main(args).runRobot()
    except Exception as e:
        for line in e.stripLines():
            raise robot.systemException(line)


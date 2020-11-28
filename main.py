import sys
import json
import robot


if __name__ == "__main__":
   args = json.loads(json.dumps(sys.argv[1:][0]))
   robot.Main(args).runRobot()
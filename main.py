import sys
import json
import robot


if __name__ == "__main__":
   print(sys.argv[1:][0])
   print(json.loads(json.dumps(sys.argv[1:][0])))
   #robot.Main(sys.argv[1][0]).runRobot()
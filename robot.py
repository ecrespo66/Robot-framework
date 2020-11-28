from iBot import Robot
import json


class Main(Robot):
    def __init__(self, args):
        self.params = args
        super().__init__(self.params['RobotId'], self.params['url'], self.params['ip'], self.params['port'],
                         self.params['params'], self.params['username'], self.params['password'])

    def runRobot(self):
        self.queue = self.createQueue("pollon")


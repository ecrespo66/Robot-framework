from iBot import Robot
import json


class main(Robot):
    def __init__(self, args):
        self.params = json.parse(args)
        print(self.params)
        super().__init__(self.params['RobotId'], self.params['url'], self.params['ip'], self.params['port'],
                         self.params['params'], self.params['username'], self.params['password'])

        self.queue = self.createQueue("pollon")

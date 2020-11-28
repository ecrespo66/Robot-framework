from iBot import Robot
import json


class Main(Robot):
    def __init__(self, args):

        self.params = args
        super().__init__(robotId=self.params['RobotId'], ExecutionId= self.params['ExecutionId'],url= self.params['url'],
                         ip=self.params['ip'], port=self.params['port'], username= self.params['username'],
                         password=self.params['password'],params =self.params['params'])
    def runRobot(self):
        self.queue = self.createQueue("pollon")
        self.Log.info("Info")
        self.Log.systemException("System Exception")
        self.Log.businessException("Business Exception")
        self.Log.log("Log")




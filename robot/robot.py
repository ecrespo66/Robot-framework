import time
from iBot import Robot


class Main(Robot):
    def __init__(self, args):
        self.robotId = args['RobotId']
        self.ExecutionId = args['ExecutionId']
        self.url = args['url']
        self.username = args['username']
        self.password = args['password']
        self.robotParameters = args['params']

        super().__init__(robotId=self.robotId, ExecutionId=self.ExecutionId, url=self.url,
                         username=self.username, password=self.password,
                         params=self.robotParameters)

    def runRobot(self):
        self.queue = self.createQueue("pollon")
        for i in range(0, 60):
            time.sleep(1)
            self.Log.info("Item" + str(i))

import time
from iBot import Robot
import json


class Main(Robot):
    def __init__(self, args):
        self.params = args
        super().__init__(robotId=self.params['RobotId'], ExecutionId=self.params['ExecutionId'], url=self.params['url'],
                         ip=self.params['ip'], port=self.params['port'], username=self.params['username'],
                         password=self.params['password'], params=self.params['params'])

    def runRobot(self):
        self.queue = self.createQueue("pollon")

        for i in range(0, 60):
            time.sleep(1)
            self.Log.info("Item" + str(i))


class systemException(Main):
    def __init__(self, exception):
        self.exception = exception
        await self.systemException()

    async def sendExecution(self):
        await self.systemException(self.exception)

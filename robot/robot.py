import time
from iBot import Robot
from iBot.browser_activities import ChromeBrowser
import robot.settings as settings


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

    def cleanup(self):
        '''Clean system before executing the robot'''
        pass

    def init(self):
        '''Init variables, instance objects and start the applications you are going to work with'''
        pass

    def run(self):
        '''Run robot process'''

        browser = ChromeBrowser()
        browser.open()
        self.Log.log("Chrome Browser Oppen")
        browser.get("http://google.com")

    def end(self):
        '''Finish robot execution, cleanup enviroment, close applications and send reports'''

        self.finishExecution()


class BusinessException(Main, Exception):
    '''Manage Exceptions Caused by business errors'''

    def init(self, message, action):
        self.action = action
        self.message = message
        self.processException()

    def processException(self):
        self.Log.businessException(self.message)
        pass


class SystemException(Main, Exception):
    '''Manage Exceptions Caused by system errors'''

    def init(self, message, action):
        self.action = action
        self.message = message
        self.processException()

    def processException(self):
        self.Log.systemException(self.message)
        pass

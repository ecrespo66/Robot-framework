from iBott.robot_activities import Robot, RobotException, Robotmethod, get_all_Methods
from iBott.browser_activities import ChromeBrowser


class Main(Robot):
    def __init__(self, args):
        self.methods = get_all_Methods(self)
        if args is not None:
            self.robotId = args['RobotId']
            self.ExecutionId = args['ExecutionId']
            self.url = args['url']
            self.username = args['username']
            self.password = args['password']
            self.robotParameters = args['params']
            super().__init__(robotId=self.robotId, ExecutionId=self.ExecutionId, url=self.url,
                             username=self.username, password=self.password,
                             params=self.robotParameters)
        else:
            super().__init__()

    @Robotmethod
    def cleanup(self):
        """Clean system before executing the robot"""

        pass

    @Robotmethod
    def start(self):
        """Init variables, instance objects and start the applications you are going to work with"""

        self.browser = ChromeBrowser()
        self.browser.open()
        pass

    @Robotmethod
    def process(self):
        """Run robot process"""

        self.Log.log("Chrome Browser Oppen")
        self.browser.get("http://google.com")

    @Robotmethod
    def end(self):
        """Finish robot execution, cleanup environment, close applications and send reports"""
        self.browser.close()
        self.finishExecution()


class BusinessException(Main, RobotException):
    """Manage Exceptions Caused by business errors"""

    def __init__(self, message, action):
        self.action = action
        self.message = message
        self.processException()

    def processException(self):
        self.Log.businessException(self.message)
        pass


class SystemException(Main, RobotException):
    """Manage Exceptions Caused by system errors"""

    def __init__(self, message, action):
        self.message = message
        self.processException()

    def processException(self):
        self.Log.systemException(self.message)
        pass

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
        self.browser.get("https://google.com")
        element = "/html/body/div[1]/div[3]/form/div[2]/div[1]/div[1]/div/div[2]/input"
        texto = "gatitos"

        self.browser.switch_to.frame(self.browser.find_element_by_tag_name("iframe"))

        if self.browser.element_exists("Xpath", "//*[contains(text(),'Acepto')]"):
            acceptButton = self.browser.find_element_by_xpath("//*[contains(text(),'Acepto')]")
            acceptButton.click()
        self.browser.switch_to.default_content()

        elemento_buscador = self.browser.find_element_by_xpath(element)
        # hacemos click sobre el elemento e introducimos el texto
        elemento_buscador.click()
        elemento_buscador.send_keys(texto)
        #pulsamos el boton Enter
        self.browser.enter(elemento_buscador)

    @Robotmethod
    def end(self):
        """Finish robot execution, cleanup environment, close applications and send reports"""
        self.browser.close()
        self.finishExecution()


class BusinessException(RobotException):
    '''Manage Exceptions Caused by business errors'''

    def _init__(self,  message, action):
        super().__init__(get_instances(Main), action)
        self.action = action
        self.message = message
        self.processException()

    def processException(self):
        self.Log.businessException(self.message)


class SystemException(RobotException):
    '''Manage Exceptions Caused by system errors'''

    def __init__(self, message, action):
        super().__init__(get_instances(Main), action)
        self.retry_times = 1
        self.action = action
        self.message = message
        self.processException()

    def processException(self):
        """
        self.Log.systemException(self.message)
        


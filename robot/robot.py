from iBott import RobotFlow
from iBott.browser_activities.firefox import FirefoxBrowser
from iBott.robot_activities.base import Bot
from robot.flow import Nodes


class Robot(Bot):
    """
    Robot class:
    ----------------
    Robot class - Inherits from Bot class.
    ** Describe the process **
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.browser = None
        self.element_list = None

    @RobotFlow(Nodes.StartNode)
    def start(self):
        """
        start method
        ======================
        Start method is the first method to be executed.
        Use this method to execute the robot's initialization.
        Example usage:
            1. Initialize the robot's variables.
            2. Clean up the environment.
            3. Get the robot's data.
            4. Open Applications
        """
        self.log.trace("start Method")
        self.element_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        self.browser = FirefoxBrowser(undetectable=True)
        self.browser.ignore_popups()
        self.browser.open()
        self.browser.get("https://google.com/")
        self.browser.save_cookies()

    @RobotFlow(Nodes.ConditionNode, parents=["process_data"], condition=lambda x: True if x else False)
    def get_transaction_data(self, *args):
        """
        Get transaction data method
        ===========================
        Get transaction data method is the method that gets the data from the source.
        Use this method to get each transactional item and send it to the next method to be processed.
        Example usage:
            1. Get the data from the source.
            2. Send the data to the next method.
        """
        self.log.trace("get_transaction_data method")
        element = next(iter(self.element_list), None)
        return element

    @RobotFlow(Nodes.OnTrue, parents=["get_transaction_data"])
    def process_data(self, *args):
        """
        Process data Method
        ======================
        Process data method is the method that processes the data gathered from the previous method.
        Use this method to process the data.
        Arguments:
            1. *args: Receives data from the previous method.
        Example usage:
            1. Process the data.
        """

        data = args[0]
        self.log.trace(f"Start process_transaction_data Method for element: {data}")
        self.element_list.remove(data)
        return data

    @RobotFlow(Nodes.OnFalse, parents=["get_transaction_data"])
    def end(self, *args):
        """
        End method
        ======================
        End method is the last method to be executed.
        Use this method to execute the robot's finalization.
        Example usage:
            1. Close the applications.
            2. Clean up the environment.
        """
        self.log.trace("end Method")
        return

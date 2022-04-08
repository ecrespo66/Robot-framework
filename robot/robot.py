"""
Robot class:
----------------
Robot class - Inherits from Bot class.
It contains the nodes and functions of the robot.

Arguments:
======================
args: Receives data from the main function to initialize Bot class
    1. robotId: The robot's ID.
    2. ExecutionId: The execution ID.
    3. url: The url of the iBott API.
    4. username: The username of the iBott account.
    5. password: The password of the iBott account.
    6. orchestrator_parameters: Additional parameters sent from iBott Orchestrator.

RobotFlow:
-----------------------
@RobotFlow is a decorator class that creates the flow nodes of the bot.
It grabs the decorated functions from the class and creates the flow nodes of the bot.
Read More in robot/flow.py

Arguments:
======================
To instance Nodes classes and register them in the flow.
    1. Nodes: Nodes class that contains the nodes of the flow
    2. parents: *optional - Defines the ancestors of the current node in the flow
    3. condition: *optional - Defines the condition of the current node for conditional nodes


BusinessException & SystemException
--------------------------------------
Default exception classes for the robot.
You must define your own process_exception method in file robot/exceptions.py if you want to use them
    1. BusinessException: Exception rised when the robot fails due to a Business error like input errors, data validation etc.
    2. SystemException: Exception raised when the robot fails due to a System error like connection errors, etc.
Arguments
----------
    1. Robot: Robot class
    2. Message: Exception message
    4. next_action: method from robot class to be executed after the exception occurs. like retry, restart, skip, etc.

"""
from iBott import RobotFlow
from iBott.robot_activities import Bot
from robot.exceptions import BusinessException, SystemException
from robot.flow import Nodes


class Robot(Bot):
    """
    Robot class:
    ----------------
    Robot class - Inherits from Bot class.
    ** Describe what the robot does **

    """

    def __init__(self, args=None):
        super().__init__(args)
        self.element_list = None

    @RobotFlow(Nodes.StartNode)
    def start(self, *args, **kwargs):
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
        return

    @RobotFlow(Nodes.ConditionNode, parents=["process_data"], condition=lambda x: True if x else False)
    def get_transaction_data(self, *args, **kwargs):
        """Get transaction data"""
        self.log.trace("get_transaction_data method")
        for element in self.element_list:
            self.element_list.remove(element)
            return element
        return None

    @RobotFlow(Nodes.OnTrue, parents=["get_transaction_data"])
    def process_data(self, *args, **kwargs):
        """Run robot process"""
        data = args[0]
        self.log.trace(f"Start process_transaction_data Method for element: {data}")

        return data


    @RobotFlow(Nodes.OnFalse, parents=["get_transaction_data"])
    def end(self, *args, **kwargs):
        """Finish robot execution, cleanup environment, close applications and send reports
        """
        print("Start end Method")
        return

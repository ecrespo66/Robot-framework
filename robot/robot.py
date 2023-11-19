from robot_manager.base import Bot
from robot_manager.flow import RobotFlow
from .flow import *
from .exceptions import *


class Robot(Bot):
    """
    Robot class:
    ----------------
    Robot class - Inherits from Bot class.
    This Framework is design to test the Robot Funcionality
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs, disabled=False)

    @RobotFlow(Nodes.StartNode)
    def start(self):
        """
        start method
        ======================
        Start method is the first method to be executed.
        Use this method to execute the robot's initialization.
        Example:
            1. Initialize the robot's variables.
            2. Clean up the environment.
            3. Get the robot's data.
            4. Open Applications
        """
        # Transaction data example
        self.data = [1, 2, 3, 4, 5]
        self.log.trace("start")

    @RobotFlow(Nodes.ConditionNode, parents=["process_data"], condition=Conditions.has_data)
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
        self.log.trace("get_transaction_data")

        return self.data

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
        # Get first available item of array
        item = args[0][0]

        # TODO: Create process

        # Remove Processed Item
        self.data.pop(0)
        self.log.trace(f"process_transaction_data for element {item}")

    @RobotFlow(node=Nodes.OnFalse, parents=["get_transaction_data"])
    def finish_process(self, *args):
        """
        Finish the workflow.
        Saves final changes to the Excel file.
        Sends output to user
        """
        self.log.trace(f"finish_process")

    @RobotFlow(node=Nodes.EndNode, parents=["finish_process"])
    def end(self, *args):
        """
        Ends the workflow. Closes any open resources like the web browser
        """
        self.log.trace(f"end")

from robot_manager.base import Bot
from robot_manager.flow import RobotFlow
from .flow import Nodes


class Robot(Bot):
    """
    Robot class:
    ----------------
    Robot class - Inherits from Bot class.
    This Framework is design to test the Robot Funcionality
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

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


        return

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
        self.log.trace(f"Start process_transaction_data Method for element")
        return

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

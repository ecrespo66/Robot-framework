from robot_manager.flow import RobotFlow
from .flow import Nodes
from robot_manager.base import Bot
import random  # Assuming random is used for demonstration

class Robot(Bot):
    @RobotFlow(node=Nodes.StartNode)
    def Init(self, *args):
        print("Initializing the transactional workflow")

    @RobotFlow(node=Nodes.ConditionNode, parents=["Init", "process_transaction"], condition=lambda x: x is not None)
    def get_transaction_data(self, *args):
        """
        Fetches transaction data and checks if there is more data to process.
        Returns transaction data if available, None otherwise.
        This method is executed after 'Init' and after each 'process_transaction'.
        """
        # Simulation of data fetching process
        has_data = random.choice([True, False])  # Randomly simulates data availability
        data = "Transaction Data" if has_data else None
        print(f"Fetching transaction data: {'Data available' if has_data else 'No data available'}")
        return data

    @RobotFlow(node=Nodes.OnTrue, parents=["get_transaction_data"])
    def process_transaction(self, *args):
        print("Processing transaction data")

    @RobotFlow(node=Nodes.OnFalse, parents=["get_transaction_data"])
    def end(self, *args):
        print("No more data to process, ending the workflow")


if __name__ == "__main__":
    try:
        # Get arguments from the orchestrator
        kwargs = OrchestratorAPI.get_args(sys.argv)
        # Instantiate the Robot with these arguments
        robot = Robot(**kwargs)
        # Run the robot using RobotFlow's run_robot method
        RobotFlow.run_robot(robot)
    except Exception as e:
        # Handle exceptions appropriately
        raise Exception(e)

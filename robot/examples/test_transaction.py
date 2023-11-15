from robot_manager.base import Bot
from robot_manager.flow import RobotFlow
from flow import Nodes, Conditions
from robot_manager.server import OrchestratorAPI
import sys
#import pandas as pd  # for Excel operations
#from selenium import webdriver  # for web automation

#Robot class should call super() class at the beginning
#Methods will only receive *Args as argument
#At  the end of each iteration go to a previous node to get more data
#There should be


class Robot(Bot):
    """
    This Robot automates the process of performing Google searches based on keywords
    read from an Excel file. It extracts the first 10 search results for each keyword,
    creates a new sheet in the Excel file named after the keyword, and appends the
    search results to this sheet.
    """

    @RobotFlow(node=Nodes.StartNode)
    def init(self, *args):
        """
        Initializes the workflow by setting up necessary resources like opening
        a web browser and reading the Excel file with keywords.
        """
        # Implementation code to open browser and read Excel file


    @RobotFlow(node=Nodes.ConditionNode, parents=["process_results"], condition=Conditions.has_data)
    def get_next_keyword(self, *args):
        """
        Checks if a keyword is available for processing.
        Returns True if a keyword is present, False otherwise.
        Retrieves the next keyword from the list for searching.
        If no more keywords are left, it returns None to indicate completion.
        """

        return 1

    @RobotFlow(node=Nodes.OnTrue, parents=["has_keyword"])
    def search_keyword(self, *args):
        """
        Searches the given keyword in Google using the provided browser instance.
        Extracts the first 10 results (name and URL).
        """
        # Implementation to perform Google search and extract results

    @RobotFlow(node=Nodes.OperationNode, parents=["search_keyword"])
    def process_results(self, *args):
        """
        Processes the search results: creates a new sheet in the Excel file with
        the keyword's name and appends the search results to this sheet.
        """
        # Implementation to process and store search results in Excel

    @RobotFlow(node=Nodes.OnFalse, parents=["get_next_keyword"])
    def finish_process(self, *args):
        """
        Finish the workflow.
        Saves final changes to the Excel file.
        Sends output to user
        """
        # Implementation to close browser and save Excel file

    @RobotFlow(node=Nodes.EndNode, parents=["finish_process"])
    def end(self, *args):
        """
        Ends the workflow. Closes any open resources like the web browser
        """



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

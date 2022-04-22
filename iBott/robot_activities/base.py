import base64
import os
import requests
import asyncio
from pathlib import Path
from iBott import OrchestratorConnectionError
from iBott.robot_activities.assets import Asset
from iBott.robot_activities.flow import RobotFlow
from iBott.files_activities import Folder
from iBott.robot_activities.logs import Log
from iBott.robot_activities.queues import Queue
from iBott.robot_activities.server import OrchestratorAPI


class Bot(object):
    """
    This class is used to interact with the iBott Orchestrator API.
    Arguments:
        kwargs: dictionary of arguments to be passed to the API.
    """
    def __init__(self, **kwargs):
        self.kwargs = kwargs
        self.connection = OrchestratorAPI(**self.kwargs)
        self.robot_id = kwargs.get('RobotId', None)
        self.execution_id = kwargs.get('ExecutionId', None)
        self.log = Log(self.connection)
        self.queue = None
        RobotFlow.connect_nodes()

    def create_queue(self, queue_name: str):
        """
        This method is used to create a queue.
        Arguments:
            queue_name: The name of the queue.
        Returns:
            queue object.
        """
        queue = Queue(connection=self.connection, robot_id=self.robot_id, queue_name=queue_name)
        return queue

    def find_queue_by_id(self, queue_id: str):
        """
        This method is used to find a queue by its ID.
        Arguments:
            queue_id: The ID of the queue.
        Returns:
            Queue object: The Queue where items are stored in

        """
        queue = Queue(self.connection, robot_id=self.robot_id, queue_id=queue_id)
        return queue

    def find_queues_by_name(self, queue_name: str):
        """
        This method is used to find queues by their name.
        Arguments:
             queue_name:  The name of the queue.
        Returns:
            list: A list of Queue objects.
        """
        queue_list = []
        end_point = f'{self.connection.http_protocol}{self.connection.url}/api/queues/QueueName={queue_name}/'
        try:
            queues = requests.get(end_point, headers=self.connection.headers)
        except:
            raise OrchestratorConnectionError("Orchestrator is not connected")
        for queue_data in queues.json():
            queue = Queue(connection=self.connection, queue_id=queue_data['QueueId'])
            queue_list.append(queue)
        return queue_list

    def get_asset_by_name(self, asset_name: str):
        """
        This method is used to find an asset by its name.
        Arguments:
            asset_name: The name of the asset.
        Returns:
            Asset object: The Asset object.
        """
        return Asset(connection=self.connection, asset_name=asset_name)

    def get_asset_by_id(self, asset_id: str):
        """
        This method is used to find an asset by its ID.
        Arguments:
            asset_id: The ID of the asset.
        Returns:
            Asset object: The Asset object.
        """
        return Asset(connection=self.connection, asset_id=asset_id)

    @staticmethod
    def save_file_from_orchestrator(string, folder=None):
        """
        This method is used to save a file sent to the robot execution from the orchestrator console.
        Arguments:
            string: The string  in base64 format to save.
            folder: The folder where to save the file.
        Returns:
            file_path: The path of the saved file.
        """
        if folder is None:
            folder = Folder(Path(os.path.dirname(os.path.realpath(__file__))).parent)
        base = string.split(",")[-1]
        filename = string.split(",")[0]
        file = base64.b64decode(base)
        f = open(os.path.join(folder.path, filename), "wb")
        f.write(file)
        f.close()
        return os.path.join(folder.path, filename)

    def finish_execution(self):
        """
        This method is used to finish the execution of the robot.
        Returns:
            None
        """
        try:
            asyncio.run(self.connection.send_message("[Execution Over]"))
        except:
            raise OrchestratorConnectionError("Orchestrator is not connected")









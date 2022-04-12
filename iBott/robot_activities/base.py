import base64
import os
import requests
import asyncio
import warnings
from pathlib import Path
from iBott import OrchestratorConnectionError
from iBott.robot_activities.assets import Asset
from iBott.robot_activities.flow import RobotFlow
from iBott.files_activities import Folder
from iBott.robot_activities.logs import Log
from iBott.robot_activities.queues import Queue
from iBott.robot_activities.server import OrchestratorAPI


class Bot(OrchestratorAPI):
    """
    This class is used to interact with the iBott Orchestrator API.
    Arguments:
        kwargs: dictionary of arguments to be passed to the API.
    """
    def __init__(self, **kwargs):
        self.kwargs = kwargs
        super().__init__(**self.kwargs)
        self.log = Log(self)
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
        self.kwargs['queue_name'] = queue_name
        queue = Queue(**self.kwargs)
        return queue

    def find_queue_by_id(self, queue_id: str):
        """
        This method is used to find a queue by its ID.
        Arguments:
            queue_id: The ID of the queue.
        Returns:
            Queue object: The Queue where items are stored in

        """
        kwargs = self.kwargs
        kwargs['queue_id'] = queue_id
        queue = Queue(**kwargs)
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
        kwargs = self.kwargs
        end_point = f'{self.http_protocol}{self.url}/api/queues/QueueName={queue_name}/'
        try:
            queues = requests.get(end_point, headers=self.headers)
        except:
            raise OrchestratorConnectionError("Orchestrator is not connected")
        for queue_data in queues.json():
            kwargs['queue_id'] = queue_data['QueueId']
            queue = Queue(**kwargs)
            queue_list.append(queue)
        return queue_list

    def get_asset_by_name(self, assets_name):
        endpoint = f"{self.http_protocol}{self.url}/api/assets/credential_name = {assets_name}"
        response = requests.get(endpoint, headers=self.headers)
        asset = response.json()
        kwargs = self.kwargs
        kwargs["credential_id"] = asset['credential_id']
        kwargs["credential_name"] = asset['credential_name']
        kwargs["credential_type"] = asset['credential_type']
        if asset['credential_type'] == "Credential":
            kwargs["username"] = asset['data_1']
            kwargs["password"] = asset['data_2']
        else:
            kwargs["data"] = asset['data_1']
        return Asset(**kwargs)

        return

    def get_asset_by_id(self, assets_id):
        endpoint = f"{self.http_protocol}{self.url}/api/assets/credential_id = {assets_id}"
        try:
            response = requests.get(endpoint, headers=self.headers)
            asset = response.json()
            kwargs = self.kwargs
            kwargs["credential_id"] = asset['credential_id']
            kwargs["credential_name"] = asset['credential_name']
            kwargs["credential_type"] = asset['credential_type']
            if asset['credential_type'] == "Credential":
                kwargs["username"] = asset['data_1']
                kwargs["password"] = asset['data_2']
            else:
                kwargs["data"] = asset['data_1']
            return Asset(**kwargs)
        except Exception as e:
            raise


        return
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
            asyncio.run(self.__send_message("[Execution Over]"))
        except:
            raise OrchestratorConnectionError("Orchestrator is not connected")









import asyncio
import json
import os
import warnings
from pathlib import Path
import requests
import websockets
from iBott.robot_activities.exceptions import OrchestratorConnectionError


class OrchestratorAPI:
    """
    Class that handles the communication with the orchestrator.

    """

    def __init__(self, **kwargs):
        self.url = kwargs.get('url', None)
        self.username = kwargs.get('username', None)
        self.password = kwargs.get('password', None)
        self.parameters = kwargs.get('params', None)
        self.debug = False
        self.debug_data = None
        self.___connection = self.__check_connection()
        self.http_protocol = self.__get_protocol()
        self.ws_protocol = self.__get_ws_protocol()
        self.url = self.__get_url()
        self.token = self.__get_token()
        self.headers = {'Authorization': f'Token {self.token}'}

    def __check_connection(self):
        """
        This method is used to check if the connection with the orchestrator is working.
        Returns:
             True if the connection is working, False otherwise.
        """
        if self.username is None:
            self.debug = True
            folder = Path(os.path.dirname(os.path.realpath(__file__))).parent.parent
            debug_file = os.path.join(folder, 'debug.json')
            try:
                with open(debug_file, 'r') as f:
                    self.debug_data = json.load(f)

                self.username = self.debug_data["IBOTT_USERNAME"]
                self.password = self.debug_data["IBOTT_PASSWORD"]
                self.url = self.debug_data['URL']
                self.robot_id = self.debug_data['ROBOT_ID']
                warnings.warn(f"Using debug file:{debug_file} to connect to the orchestrator, please check the variables in debug.json ")
            except:
                warnings.warn("No username or password provided.Please Set them in debug.json")
                return False
        return True

    def __get_token(self):
        """
        This method is used to get the token of iBott Ochestrator API. It is used to authenticate the user.
        Returns:
            token: str
        """
        endpoint = f"{self.http_protocol}{self.url}/api-token-auth/"
        user_data = {'username': self.username, 'password': self.password}
        try:
            response = requests.post(endpoint, user_data)
            return response.json()['token']
        except:
            raise OrchestratorConnectionError(f"Error while trying to connect to {self.url}")

    def __get_protocol(self):
        """
        This method is used to get the protocol of the iBott API.
        Returns:
            http_protocol: str
        """
        if "https://" in self.url:
            return "https://"
        return "http://"

    def __get_ws_protocol(self):
        """
        This method is used to get the websocket protocol of the iBott API.
        Returns:
             websocket protocol
        """
        if "https://" in self.url:
            return "wss://"
        return "ws://"

    def __get_url(self):
        """
        This method is used to get the url of the iBott API.
        Returns:
            url: str
        """
        if "https://" in self.url:
            return self.url.replace("https://", "")
        return self.url.replace("http://", "")

    async def send_message(self, message, log_type='log'):
        """
        Async method used to send a message to the orchestrator.
        Arguments:
            message: str
            log_type: str
        Returns:
            response: dict
        """
        await asyncio.sleep(0.01)
        uri = f"{self.ws_protocol}{self.url}/ws/execution/{self.executionId}/"
        message = json.dumps({"message": {"type": log_type, "data": message, "executionId": self.executionId}})

        async with websockets.connect(uri) as websocket:
            await websocket.send(str(message))
            try:
                await asyncio.wait_for(websocket.recv(), timeout=10)
            except asyncio.TimeoutError:
                await self.send_message(message, log_type)
            await websocket.close()

    @classmethod
    def get_args(cls, args):
        """
        Get arguments from command line
        Arguments:
            args: list
        Returns:
            args: dict
            """
        if len(args) > 1:
            args = eval(args[1].replace("'", '"'))
        else:
            args = {
                'RobotId': None,
                'ExecutionId': None,
                'url': None,
                'username': None,
                'password': None,
                'params': None
            }
        return args



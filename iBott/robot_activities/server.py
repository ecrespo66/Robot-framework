import datetime
import json
import os
import string
import warnings
from pathlib import Path
import random
import requests


class OrchestratorAPI:
    """
    Class that handles the communication with the orchestrator.

    """

    def __init__(self, **kwargs):
        self.url = kwargs.get('url', None)

        self.token = kwargs.get('token', None)
        self.parameters = kwargs.get('params', None)
        self.execution_id = kwargs.get("ExecutionId", None)
        self.debug = False
        self.debug_data = None
        self.___connection = self.__check_connection()
        self.http_protocol = self.__get_protocol()
        self.url = self.__get_url()
        self.headers = {'Authorization': f'Token {self.token}'}

    def __check_connection(self):
        """
        This method is used to check if the connection with the orchestrator is working.
        Returns:
             True if the connection is working, False otherwise.
        """
        if self.token is None:
            #self.debug = True
            folder = Path(os.path.dirname(os.path.realpath(__file__))).parent.parent
            debug_file = os.path.join(folder, 'debug.json')
            try:
                with open(debug_file, 'r') as f:
                    self.debug_data = json.load(f)
                self.token = self.debug_data["IBOTT_TOKEN"]
                self.url = self.debug_data['URL']
                self.robot_id = self.debug_data['ROBOT_ID']
                warnings.warn(f"Using debug file:{debug_file} to connect to the orchestrator, please check the variables in debug.json ")
            except:
                warnings.warn("Incorrect Data. Please Set Robot Console Data in debug.json")
                return False
        return True

    def __get_protocol(self):
        """
        This method is used to get the protocol of the iBott API.
        Returns:
            http_protocol: str
        """
        if "https://" in self.url:
            return "https://"
        return "http://"


    def __get_url(self):
        """
        This method is used to get the url of the iBott API.
        Returns:
            url: str
        """
        if "https://" in self.url:
            return self.url.replace("https://", "")
        else:
            return self.url.replace("http://", "")

    def send_message(self, message, log_type='log'):
        """
        method used to send a message to the orchestrator.
        Arguments:
            message: str
            log_type: str
        Returns:
            response: dict
        """
        """
        send log to robot manage console
        Arguments:
            message {string} -- message to send
            log_type {string} -- type of the log
        """

        endpoint = f'{self.http_protocol}{self.url}/api/logs/'
        log_data = {
            "LogType": log_type,
            "LogData": message,
            "ExecutionId": self.execution_id,
            "LogId":  ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(64)),
            "DateTime": datetime.datetime.now()
        }
        try:
            requests.post(endpoint, log_data, headers=self.headers)
        except Exception as e:
            print(e)



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
                'token': None,
                'params': None
            }
        return args



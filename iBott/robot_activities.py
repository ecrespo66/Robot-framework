from pathlib import Path
from .robot_flow import RobotFlow
from .robot_excepcions import OrchestratorConnectionError
from .files_activities import Folder
from .system_activities import System
from datetime import datetime
import base64
import os
import requests
import asyncio
import json
import websockets
import warnings


class Bot:
    """
    This class is used to interact with the iBott Orchestrator API.
    :param robotId: The robot's ID.
    :param ExecutionId: The execution ID.
    :param url: The url of the iBott API.
    :param username: The username of the iBott account.
    :param password: The password of the iBott account.
    :param orchestrator_parameters: Additional parameters sent from iBott Orchestrator.
    """
    warn_message = """"You must provide the robot's ID, execution ID, url, username and password to use Orquestrator features
                set enviroment varibales for the connection with the following command:
                python manage.py --add_credentials
                """

    def __init__(self, args=None):
        if args:
            self.robot_id = args['RobotId']
            self.executionId = args['ExecutionId']
            self.url = args['url']
            self.username = args['username']
            self.password = args['password']
            self.orchestrator_parameters = args['params']
            self.http_protocol = self.get_httpprotocol()
            self.ws_protocol = self.__get_ws_protocol()
            self.url = self.__get_url()
            self.token = self.__get_token()
            self.__headers = {'Authorization': f'Token {self.token}'}
        else:
            self.debug = True
            warnings.warn(Bot.warn_message)

        self.queue = None
        self.log = Log(self)
        RobotFlow.connect_nodes()

    def __get_token(self):
        """
        This method is used to get the token of iBott Ochestrator API. It is used to authenticate the user.
        :return: token
        :rtype: str
        """
        try:
            response = requests.post(f"{self.http_protocol}{self.url}/api-token-auth/",
                                     {'username': self.username, 'password': self.password})
            return response.json()['token']
        except:
            Raise = OrchestratorConnectionError(f"Error while trying to connect to {self.url}")

    def __get_protocol(self):
        """
        This method is used to get the protocol of the iBott API.
        :return: http_protocol
        """
        if "https://" in self.url:
            return "https://"
        return "http://"

    def __get_ws_protocol(self):
        """
        This method is used to get the websocket protocol of the iBott API.
        :return: websocket protocol
        """
        if "https://" in self.url:
            return "wss://"
        return "ws://"

    def __get_url(self):
        """
        This method is used to get the url of the iBott API.
        :return: url
        """
        if "https://" in self.url:
            return self.url.replace("https://", "")
        return self.url.replace("http://", "")

    async def __send_message(self, message, log_type='log'):
        """
        Async method used to send a message to the orchestrator.
        :param message:
        :type message: str

        :param log_type:
        :type log_type: str
        :return:
        """
        await asyncio.sleep(0.01)
        uri = f"{self.ws_protocol}{self.url}/ws/execution/{self.executionId}/"
        message = json.dumps({"message": {"type": log_type, "data": message, "executionId": self.executionId}})

        async with websockets.connect(uri) as websocket:
            await websocket.send(str(message))
            try:
                await asyncio.wait_for(websocket.recv(), timeout=10)
            except asyncio.TimeoutError:
                await self.__send_message(message, log_type)
            await websocket.close()

    def create_queue(self, queue_name):
        """
        This method is used to create a queue.
        :param queue_name: The name of the queue.
        :type queue_name: str

        :return: queue
        :rtype: Queue object
        """
        queue = Queue(robot_id=self.robot_id, url=self.url, token=self.token, queueName=queue_name)
        return queue

    def find_queue_by_id(self, queueId):
        """
        This method is used to find a queue by its ID.

        :param queueId: The ID of the queue.
        :type queueId: str

        :return: queue
        :rtype: Queue object
        """

        queue = Queue(robot_id=self.robot_id, url=self.url, token=self.token, queueId=queueId)
        return queue

    def find_queues_by_name(self, queue_name):
        """
        This method is used to find queues by their name.

        :param queue_name: The name of the queue.
        :type queue_name: str

        :return: queue_list
        :rtype: list
        """

        queue_list = []
        end_point = f'{self.http_protocol}{self.url}/api/queues/QueueName={queue_name}/'
        queues = requests.get(end_point, headers=self.__headers)

        for queue_data in queues.json():
            queue = Queue(robot_id=self.robot_id, url=self.url, token=self.token, queueId=queue_data['QueueId'])
            queue_list.append(queue)
        return queue_list

    @staticmethod
    def save_file_from_orchestrator(string, folder=None):
        """
        This method is used to save a file sent to the robot executionfrom the orchestrator console.
        :param string:
        :param folder:
        :return:
        """
        if folder is None:
            folder = Folder(Path(os.path.dirname(os.path.realpath(__file__))).parent)
        base = string.split(",")[-1]
        filename = string.split(",")[0]
        file = base64.b64decode(base)
        f = open(os.path.join(folder.path, filename), "wb")
        f.write(file)
        f.close()

    def finish_execution(self):
        """
        This method is used to finish the execution of the robot.
        :return:
        """
        try:
            asyncio.run(self.__send_message("[Execution Over]"))
        except:
            raise OrchestratorConnectionError("Orchestrator is not connected")


class Log:
    """
    This class is used to log messages in the Orchestrator console.
    :param args: same arguments as Bot Class
    :type args: list
    """

    def __init__(self, robot):
        self.robot = robot

    def debug(self, log: str):
        """
        Send debug trace to ochestrator
        :param log: Message to send to ochestrator
        :type log: str
        :return:
        """
        log_type = 'debug'
        asyncio.run(self.send(log, log_type=log_type))

    def trace(self, log: str):
        """
        Send trace to ochestrator
        :param log: Message to send to ochestrator
        :type log: str
        :return:
        """
        log_type = 'log'
        asyncio.run(self.send(log, log_type=log_type))

    def info(self, log: str):
        """Send info trace to orchestrator"""
        log_type = 'info'
        asyncio.run(self.send(log, log_type=log_type))

    def system_exception(self, error: str):
        """Send systemException trace to orchestrator"""
        log_type = 'systemException'
        asyncio.run(self.send(error, log_type=log_type))

    def business_exception(self, error: str):
        """Send businessException trace to orchestrator"""
        log_type = 'businessException'
        asyncio.run(self.send(error, log_type=log_type))

    async def send(self, log: str, log_type: str):
        if not self.robot.debug:
            try:
                await self.robot.__send_message(log, log_type=log_type)
            except:
                raise OrchestratorConnectionError("Orchestrator is not connected")
        else:
            print(f'{log_type}: {log}')


class Queue:
    def __init__(self, *args, **kwargs):
        """
        Class to manage queues in Orchestrator.
        With this class you can create, update and get queues from Orchestrator.
        :param args:
        :param kwargs:
        """
        self.token = kwargs.get("token")
        self.robotId = kwargs.get("robot_id")
        self.url = kwargs.get("url")
        self.queueId = kwargs.get("queueId", None)
        self.queueName = kwargs.get("queueName", None)

        self.http_protocol = self.__get_protocol()
        self.ws_protocol = self.__get_ws_protocol()
        self.url = self.__get_url()
        self.__headers = {'Authorization': f'Token {self.token}'}
        self.__get_queue()
        self.__retryTimes = 1

    def __get_queue(self):
        if self.queueId is None:
            self.queueId = System.id_generator(16)
            end_point = f'{self.http_protocol}{self.url}/api/queues/'
            data = {
                'RobotId': self.robotId,
                'QueueId': self.queueId,
                'QueueName': self.queueName
            }
            requests.post(end_point, data, headers=self.__headers)

        else:
            end_point = f'{self.http_protocol}{self.url}/api/queues/QueueId={self.queueId}/'
            response = requests.get(end_point, headers=self.__headers)
            self.queueName = response.json()['QueueName']

    def __getItem(self):
        """Get all items from Queue"""
        queueItems = requests.get(f'{self.http_protocol}{self.url}/api/items/QueueId={self.queueId}',
                                  headers={'Authorization': f'Token {self.token}'}).json()

        for Qitem in queueItems:
            item = Item(self.queueId, self.url, self.token, itemId=Qitem['ItemId'])

            if item.status == 'Fail' and item.itemExecutions < self.__retryTimes:
                item.setItemExecution()
                item.setItemAsPending()
            if item.status == 'Pending':
                item.setItemAsWorking()
                yield item

    def __get_protocol(self):
        if "https://" in self.url:
            return "https://"
        return "http://"

    def __get_ws_protocol(self):
        if "https://" in self.url:
            return "wss://"
        return "ws://"

    def __get_url(self):
        if "https://" in self.url:
            return self.url.replace("https://", "")
        return self.url.replace("http://", "")

    def createItem(self, value):
        """Create New Item in The Orchestrator"""
        return Item(self.queueId, self.url, self.token, value=value)

    def getNextItem(self):
        """Get Next Pending item from Orchestrator"""
        try:
            item = next(self.__getItem())
        except:
            item = None
        return item

    def setRetryTimes(self, times):
        """Set number of retry times for each item"""
        self.__retryTimes = times


class Item(Queue):
    def __init__(self, queueId, url, token, itemId=None, value=None):
        """Item constructor"""

        self.QueueId = queueId
        self.url = url
        if self.url is not None:
            if "https://" in self.url:
                self.httpprotocol = "https://"
                self.wsprotocol = "wss://"
                self.url = self.url.replace("https://", "")
            else:
                self.httpprotocol = "http://"
                self.wsprotocol = "ws://"
                self.url = self.url.replace("http://", "")
        else:
            pass
        self.token = token
        self.itemExecutions = 0
        self.startDate = None
        self.endDate = None
        if itemId is None:
            self.itemId = System.id_generator(24)
            if type(value) is dict:
                self.value = str(value)
                self.status = 'Pending'
                itemData = {
                    'QueueId': self.QueueId,
                    'ItemId': self.itemId,
                    'Value': str(value),
                    'Status': self.status,
                    'CreationTime': datetime.now()
                }
                try:
                    requests.post(f'{self.httpprotocol}{self.url}/api/items/', itemData,
                                  headers={'Authorization': f'Token {self.token}'})
                except:
                    pass
            else:
                raise ValueError("Item data must be a dictionary")
        else:
            self.itemId = itemId
            try:
                item = requests.get(f'{self.httpprotocol}{self.url}/api/items/ItemId={self.itemId}',
                                    headers={'Authorization': f'Token {self.token}'}).json()

                self.value = eval(item['Value'])
                self.status = item['Status']
            except:
                pass

    def set_item_status(self):
        try:
            data = {"ItemId": self.itemId,
                    "Status": self.status,
                    'ResolutionTime': datetime.now()}
            requests.put(f'{self.httpprotocol}{self.url}/api/items/{self.itemId}/',
                         data,
                         headers={'Authorization': f'Token {self.token}'}
                         )
        except Exception as e:
            raise OrchestratorConnectionError(e)

    def setItemAsWorking(self):
        """Block current item """
        self.status = 'Working'
        self.set_item_status()

    def setItemAsOk(self):
        """Set Item status as OK"""
        self.status = 'OK'
        self.set_item_status()

    def setItemAsFail(self):
        """Set Item status as Fail"""
        self.status = 'Fail'
        self.set_item_status()

    def setItemAsWarn(self):
        """Set Item status as Warn"""
        self.status = 'Warn'
        self.set_item_status()

    def setItemAsPending(self):
        """Set Item status as Pending"""
        self.status = 'Pending'
        self.set_item_status()

    def setItemExecution(self):
        """Set number of executrions"""
        self.itemExecutions += 1

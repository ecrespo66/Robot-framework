import warnings
import gc
from .system_activities import id_generator
from datetime import datetime
import requests
import asyncio
import json
import websockets


class Robot:
    def __init__(self, robotId=None, ExecutionId=None, url=None, username=None, password=None, params=None):
        self.robotId = robotId
        self.ExecutionId = ExecutionId
        self.url = url
        self.username = username
        self.password = password
        self.params = params
        if self.url is not None:
            if "https://" in self.url:
                self.httpprotocol = "https://"
                self.wsprotocol = "wss://"
                self.url = self.url.replace("https://", "")
            else:
                self.httpprotocol = "http://"
                self.wsprotocol = "ws://"
                self.url = self.url.replace("http://", "")
        self.Log = self.Log(self)

        try:
            response = requests.post(f"{self.httpprotocol}{self.url}/api-token-auth/",
                                     {'username': self.username, 'password': self.password})
            self.token = response.json()['token']
        except:
            warnings.warn('Robot Data Not set')
        self.queue = None

    def createQueue(self, queueName):
        try:
            queue = Queue(self.robotId, self.url, self.token, queueName=queueName)
        except:
            warnings.warn('Method createQueue fail -> Robot Data Not set')
        return queue

    def findQueueById(self, queueId):
        try:
            queue = Queue(self.robotId, self.url, self.token, queueId=queueId)
        except:
            warnings.warn('Method findQueueById fail -> Robot Data Not set')
        return queue

    def findQueuesByName(self, queueName):
        Queues = []
        try:
            queues = requests.get(f'{self.httpprotocol}{self.url}/api/queues/QueueName={queueName}/',
                                  headers={'Authorization': f'Token {self.token}'}).json()
            for queue in queues:
                Queues.append(Queue(self.robotId, self.url, self.token, queueId=queue['QueueId']))
        except:
            warnings.warn('Method findQueuesByName fail -> Robot Data Not set')
        return Queues

    def finishExecution(self):
        try:
            asyncio.run(self.sendExecution("[Execution Over]"))
        except:
            warnings.warn('Method finishExecution fail -> Robot Data Not set')

    async def sendExecution(self, message, type='log'):
        await asyncio.sleep(0.01)
        uri = f"{self.wsprotocol}{self.url}/ws/execution/{self.ExecutionId}/"
        message = json.dumps({"message": {"type": type, "data": message, "executionId": self.ExecutionId}})
        async with websockets.connect(uri) as websocket:
            await websocket.send(str(message))
            try:
                await asyncio.wait_for(websocket.recv(), timeout=10)
            except asyncio.TimeoutError:
                await self.sendExecution(message, type)
            await websocket.close()

    class Log:
        def __init__(self, robot):
            self.robot = robot

        async def send(self, log, type):
            try:
                await self.robot.sendExecution(log, type=type)
            except:
                warnings.warn('Method send fail -> Robot Data Not set')

        def debug(self, log):
            '''Send debug trace to ochestrator'''
            try:
                asyncio.run(self.send(log, type='debug'))
            except:
                warnings.warn('Method debug fail -> Robot Data Not set')

        def log(self, log):
            '''Send log trace to ochestrator'''

            try:
                asyncio.run(self.send(log, type='log'))
            except:
                warnings.warn('Method log fail -> Robot Data Not set')

        def info(self, log):
            '''send info trace to orchestrator'''

            try:
                asyncio.run(self.send(log, type='info'))
            except:
                warnings.warn('Method info fail -> Robot Data Not set')

        def systemException(self, error):
            '''send systemException trace to orchestrator'''

            try:
                asyncio.run(self.send(error, type="systemException"))
            except:
                warnings.warn('Method systemException fail -> Robot Data Not set')

        def businessException(self, error):
            '''send businessException trace to orchestrator'''

            try:
                asyncio.run(self.send(error, type="businesException"))
            except:
                warnings.warn('Method businessException fail -> Robot Data Not set')


class Queue:
    def __init__(self, robotId, url, token, queueName=None, queueId=None):
        """Queue constructor"""

        self.token = token
        self.robotId = robotId
        self.url = url
        self.__retryTimes = 1
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
            warnings.warn('Robot Data Not set')

        if queueId is None:
            self.queueId = id_generator(16)
            self.queueName = queueName
            try:
                requests.post(f'{self.httpprotocol}{self.url}/api/queues/',
                              {'RobotId': self.robotId, 'QueueId': self.queueId, 'QueueName': self.queueName},
                              headers={'Authorization': f'Token {self.token}'})
            except:
                warnings.warn('Robot Data Not set')

        else:
            self.queueId = queueId
            try:
                response = requests.get(f'{self.httpprotocol}{self.url}/api/queues/QueueId={self.queueId}/',
                                        headers={'Authorization': f'Token {self.token}'})
                self.queueName = response.json()['QueueName']
            except:
                warnings.warn('Robot Data Not set')

    def __getItem(self):
        """Get all items from Queue"""
        queueItems = requests.get(f'{self.httpprotocol}{self.url}/api/items/QueueId={self.queueId}',
                                  headers={'Authorization': f'Token {self.token}'}).json()

        for Qitem in queueItems:
            item = Item(self.queueId, self.url, self.token, itemId=Qitem['ItemId'])

            if item.status == 'Fail' and item.itemExecutions < self.__retryTimes:
                item.setItemExecution()
                item.setItemAsPending()
            if item.status == 'Pending':
                item.setItemAsWorking()
                yield item

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
            warnings.warn('Robot Data Not set')
        self.token = token
        self.itemExecutions = 0
        self.startDate = None
        self.endDate = None
        if itemId is None:
            self.itemId = id_generator(24)
            if type(value) is dict:
                self.value = str(value)
                self.status = 'Pending'
                itemData = {'QueueId': self.QueueId, 'ItemId': self.itemId, 'Value': str(value),
                            'Status': self.status, 'CreationTime': datetime.now()}
                try:
                    requests.post(f'{self.httpprotocol}{self.url}/api/items/', itemData,
                                  headers={'Authorization': f'Token {self.token}'})
                except:
                    warnings.warn('Robot Data Not set')
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
                warnings.warn('Robot Data Not set')

    def setItemAsWorking(self):
        """Block current item """
        self.status = 'Working'
        data = {"ItemId": self.itemId, "Status": self.status, 'ResolutionTime': datetime.now()}
        try:
            requests.put(f'{self.httpprotocol}{self.url}/api/items/{self.itemId}/', data,
                         headers={'Authorization': f'Token {self.token}'})
        except:
            warnings.warn('Robot Data Not set')

    def setItemAsOk(self):
        """Set Item status as OK"""

        self.status = 'OK'
        data = {"ItemId": self.itemId, "Status": self.status, 'ResolutionTime': datetime.now()}
        try:
            requests.put(f'{self.httpprotocol}{self.url}/api/items/{self.itemId}/', data,
                         headers={'Authorization': f'Token {self.token}'})
        except:
            warnings.warn('Robot Data Not set')

    def setItemAsFail(self):
        """Set Item status as Fail"""
        self.status = 'Fail'
        data = {"ItemId": self.itemId, "Status": self.status, 'ResolutionTime': datetime.now()}
        try:
            requests.put(f'{self.httpprotocol}{self.url}/api/items/{self.itemId}/', data,
                         headers={'Authorization': f'Token {self.token}'})
        except:
            warnings.warn('Robot Data Not set')

    def setItemAsWarn(self):
        """Set Item status as Warn"""
        self.status = 'Warn'
        data = {"ItemId": self.itemId, "Status": self.status, 'ResolutionTime': datetime.now()}
        try:
            requests.put(f'{self.httpprotocol}{self.url}/api/items/{self.itemId}/', data,
                         headers={'Authorization': f'Token {self.token}'})
        except:
            warnings.warn('Robot Data Not set')

    def setItemAsPending(self):
        """Set Item status as Pending"""
        self.status = 'Pending'
        data = {"ItemId": self.itemId, "Status": self.status}
        try:
            requests.put(f'{self.httpprotocol}{self.url}/api/items/{self.itemId}/', data,
                         headers={'Authorization': f'Token {self.token}'})
        except:
            warnings.warn('Robot Data Not set')

    def setItemExecution(self):
        """Set number of executrions"""

        self.itemExecutions += 1


def get_all_Methods(module):
    funcs = sorted((func for func in (getattr(module, name) for name in dir(module))
                    if callable(func) and hasattr(func, "_order")), key=lambda func: func._order)
    return funcs


class RobotException(Exception):
    def __init__(self, cls, action):
        self.cls = cls
        self.action = action
        self.methods = cls.methods

    def find_index_method(self):
        methodsName = []
        for method in self.methods:
            methodsName.append(method.__name__)
        return methodsName.index(self.action)

    def retry(self, retry_times):
        index = self.find_index_method()
        if self.count_retry_times() <= retry_times:
            for i in range(index, len(self.methods) - 1):
                self.methods[i]()
        else:
            raise Exception("Max retry times reached")

    def jump_to_method(self, method, retry_times):
        self.action = method
        index = self.find_index_method()
        if self.count_retry_times() <= retry_times:
            for i in range(index, len(self.methods) - 1):
                self.methods[i]()
        else:
            raise Exception("Max retry times reached")

    def restart(self, retry_times):
        if self.count_retry_times() <= retry_times:
            for method in self.methods:
                method()
            else:
                raise Exception("Max retry times reached")

    @staticmethod
    def count_retry_times(counter=[0]):
        counter[0] += 1
        return counter[0]


def Robotmethod(func, counter=[0]):
    func._order = counter[0]
    counter[0] += 1
    return func


def get_instances(cls):
    for obj in gc.get_objects():
        if isinstance(obj, cls):
            return obj

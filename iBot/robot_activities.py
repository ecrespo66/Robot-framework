from .dataBase_activities import *
from .system_activities import id_generator
from datetime import datetime
import os
import requests
import asyncio
import json
import websockets


class Robot:
    def __init__(self, robotId, ExecutionId, url, username, password, params):
        self.robotId = robotId
        self.ExecutionId = ExecutionId
        self.url = url
        self.username = username
        self.password = password
        self.params = params

        if "https://" in self.url:
            self.httpprotocol = "https://"
            self.wsprotocol = "wss://"
        else:
            self.httpprotocol = "http://"
            self.wsprotocol = "ws://"

        response = requests.post(f"{self.httpprotocol}{self.url}/api-token-auth/", {'username': self.username, 'password': self.password})
        self.token = response.json()['token']
        self.Log = self.Log(self)
        self.queue = None

    def createQueue(self, queueName):
        queue = Queue(self.robotId, self.url, self.token, queueName=queueName)
        return queue

    def findQueueById(self, queueId):
        queue = Queue(self.robotId, self.url, self.token, queueId=queueId)
        return queue

    def findQueuesByName(self, queueName):
        Queues = []
        queues = requests.get(f'{self.httpprotocol}{self.url}/api/queues/QueueName={queueName}/',
                              headers={'Authorization': f'Token {self.token}'}).json()

        for queue in queues:
            Queues.append(Queue(self.robotId, self.url, self.token, queueId=queue['QueueId']))
        return Queues

    async def sendExecution(self, message, type='log'):
        await asyncio.sleep(0.01)
        uri = f"{self.wsprotocol}{self.url}/ws/execution/{self.ExecutionId}/"
        message = json.dumps({"message": {"type": type, "data": message, "executionId": self.ExecutionId}})
        async with websockets.connect(uri) as websocket:
            await websocket.send(str(message))

    class Log:
        def __init__(self, robot):
            self.robot = robot

        async def send(self, log, type):
            await self.robot.sendExecution(log, type=type)

        def log(self, log):
            asyncio.run(self.send(log, type='log'))

        def info(self, log):
            asyncio.run(self.send(log, type='info'))

        def systemException(self, error):
            asyncio.run(self.send(error, type="systemException"))

        def businessException(self, error):
            asyncio.run(self.send(error, type="businesException"))


class Queue:
    def __init__(self, robotId, url, token, queueName=None, queueId=None):
        self.token = token
        self.url = url
        self.robotId = robotId
        self.__retryTimes = 1
        if "https://" in self.url:
            self.httpprotocol = "https://"
            self.wsprotocol = "wss://"
        else:
            self.httpprotocol = "http://"
            self.wsprotocol = "ws://"

        if queueId is None:
            self.queueId = id_generator(16)
            self.queueName = queueName
            requests.post(f'{self.httpprotocol}{self.url}/api/queues/',
                          {'RobotId': self.robotId, 'QueueId': self.queueId, 'QueueName': self.queueName},
                          headers={'Authorization': f'Token {self.token}'})
        else:
            self.queueId = queueId
            response = requests.get(f'{self.httpprotocol}{self.url}/api/queues/QueueId={self.queueId}/',
                                    headers={'Authorization': f'Token {self.token}'})
            self.queueName = response.json()['QueueName']

    def __getItem(self):
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
        return Item(self.queueId, self.url, self.token, value=value)

    def getNextItem(self):
        try:
            item = next(self.__getItem())
        except:
            item = None
        return item

    def setRetryTimes(self, times):
        self.__retryTimes = times

    def clearQueue(self):
        self.__DataBase.Query("Delete from Items where QueueId = '{}'".format(self.queueId))


class Item(Queue):
    def __init__(self, queueId, url, token, itemId=None, value=None):

        self.QueueId = queueId
        self.url = url
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
                requests.post(f'{self.httpprotocol}{self.url}/api/items/', itemData,
                              headers={'Authorization': f'Token {self.token}'})
            else:
                raise ValueError("Item data must be a dictionary")
        else:
            self.itemId = itemId
            item = requests.get(f'{self.httpprotocol}{self.url}/api/items/ItemId={self.itemId}',
                                headers={'Authorization': f'Token {self.token}'}).json()

            self.value = item['Value']
            self.status = item['Status']

    def setItemAsWorking(self):
        self.status = 'Working'
        data = {"ItemId": self.itemId, "Status": self.status, 'ResolutionTime': datetime.now()}
        requests.put(f'{self.httpprotocol}{self.url}/api/items/{self.itemId}/', data,
                     headers={'Authorization': f'Token {self.token}'})

    def setItemAsOk(self):
        self.status = 'OK'
        data = {"ItemId": self.itemId, "Status": self.status, 'ResolutionTime': datetime.now()}
        requests.put(f'{self.httpprotocol}{self.url}/api/items/{self.itemId}/', data,
                     headers={'Authorization': f'Token {self.token}'})

    def setItemAsFail(self):
        self.status = 'Fail'
        data = {"ItemId": self.itemId, "Status": self.status, 'ResolutionTime': datetime.now()}
        requests.put(f'{self.httpprotocol}{self.url}/api/items/{self.itemId}/', data,
                     headers={'Authorization': f'Token {self.token}'})

    def setItemAsWarn(self):
        self.status = 'Warn'
        data = {"ItemId": self.itemId, "Status": self.status, 'ResolutionTime': datetime.now()}
        requests.put(f'{self.httpprotocol}{self.url}/api/items/{self.itemId}/', data,
                     headers={'Authorization': f'Token {self.token}'})

    def setItemAsPending(self):
        self.status = 'Pending'
        data = {"ItemId": self.itemId, "Status": self.status}
        requests.put(f'{self.httpprotocol}{self.url}/api/items/{self.itemId}/', data,
                     headers={'Authorization': f'Token {self.token}'})

    def setItemExecution(self):
        self.itemExecutions += 1

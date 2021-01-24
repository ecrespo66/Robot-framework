from .dataBase_activities import *
from .system_activities import id_generator
from datetime import datetime
import os


class Robot:

    def __init__(self, robotName, path):
        Dbpath = os.path.abspath(os.path.join(os.path.dirname(__file__), ".")) + "/Robots.sqlite"
        self.__DataBase = Sqlite(Dbpath)
        self.robotName = robotName
        self.path = path
        self.__DataBase.createTable('Robots', {'id': "NULL", 'name': "NULL", 'path': "NULL"})
        self.__DataBase.createTable("Queues", {'RobotId': "NULL", 'QueueId': "NULL", 'QueueName': "NULL"})
        robotid = self.__DataBase.Query("SELECT id FROM Robots where name = '{}' ".format(self.robotName))

        if len(robotid) < 1:
            self.robotid = id_generator(6)
            self.__DataBase.Insert("Robots", {'id': self.robotid, 'name': self.robotName, 'path': self.path})
        else:
            self.robotid = robotid[0][0]

    def robotQuery(self, robot):
        query = "SELECT id FROM Robots where id = '{}' ".format(robot)
        robotquery = self.__DataBase.Query(query)
        if len(robotquery) > 0:
            return True
        else:
            return False

    def createQueue(self, queueName):
        queue = Queue(self.robotid, queueName=queueName)
        return queue

    def findQueueById(self, queueId):
        queue = Queue(self.robotid, queueId=queueId)
        return queue

    def findQueuesByName(self, queueName):
        Queues = []
        queues = self.__DataBase.Query(f"Select QueueId from Queues where QueueName = '{queueName}'")
        for queue in queues:
            Queues.append(Queue(self.robotid, queueId=queue[0]))
        return Queues

    def deleteQueue(self, queueId):
        queue = Queue(queueId)
        queue.clearQueue()
        query = f"DELETE from Queues WHERE RobotId = '{self.robotid}' and  QueueId = '{queueId}'"
        self.__DataBase.Query(query)


class Queue:
    def __init__(self, robotId, queueName=None, queueId=None):
        Dbpath = os.path.abspath(os.path.join(os.path.dirname(__file__), ".")) + "/Robots.sqlite"
        self.__DataBase = Sqlite(Dbpath)
        self.__retryTimes = 1
        if queueId is None:
            self.queueId = id_generator(16)
            self.queueName = queueName
            queuedata = {'RobotId': robotId, 'QueueId': self.queueId, 'QueueName': self.queueName}
            self.__DataBase.Insert("Queues", queuedata)

        else:
            self.queueId = queueId
            queueName = self.__DataBase.Query(f"select QueueName from Queues where QueueId = '{self.queueId}'")
            self.queueName = queueName[0][0]

    def __getItem(self):
        queueItems = self.__DataBase.Query(f"Select ItemId from Items where QueueId ='{self.queueId}'")
        for itemId in queueItems:
            item = Item(self.queueId, itemId=itemId[0])
            if item.status == 'Fail' and item.itemExecutions < self.__retryTimes:
                item.setItemExecution()
                item.setItemAsPending()
            if item.status == 'Pending':
                item.setItemAsWorking()
                yield item

    def createItem(self, item):
        Item(self.queueId, value=item)

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
    def __init__(self, queueId, itemId=None, value=None):
        Dbpath = os.path.abspath(os.path.join(os.path.dirname(__file__), ".")) + "/Robots.sqlite"
        self.__DataBase = Sqlite(Dbpath)
        self.QueueId = queueId
        self.itemExecutions = 0
        self.startDate = None
        self.endDate = None
        if itemId is None:
            self.itemId = id_generator(24)
            self.value = value
            self.status = 'Pending'
            itemData = {'QueueId': self.QueueId, 'ItemId': self.itemId, 'Value': value, 'Status': self.status,
                        'StartTime': 'NULL', 'EndTime': 'NULL'}
            self.__DataBase.Insert("Items", itemData)

        else:
            self.itemId = itemId
            query = self.__DataBase.Query(
                "Select Value, Status from Items where ItemId ='{}'".format(self.itemId))
            self.value = query[0][0]
            self.status = query[0][1]

    def setItemAsWorking(self):
        self.status = 'Working'
        self.startDate = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        query = "update Items SET Status = 'Working',StartTime = '{}' where ItemId = '{}'".format(self.startDate,
                                                                                                  self.itemId)
        self.__DataBase.Query(query)

    def setItemAsOk(self):
        self.status = 'OK'
        self.endDate = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        query = "update Items SET Status= 'OK', EndTime = '{}' where ItemId = '{}'".format(self.endDate,
                                                                                           self.itemId)
        self.__DataBase.Query(query)

    def setItemAsFail(self):
        self.status = 'Fail'
        self.endDate = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        query = "update Items SET Status= 'Fail', EndTime = '{}' where ItemId = '{}'".format(self.itemId,
                                                                                             self.itemId)
        self.__DataBase.Query(query)

    def setItemAsWarn(self):
        self.status = 'Warn'
        self.endDate = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        query = "update Items SET Status= 'Warn' , EndTime = '{}' where ItemId = '{}'".format(self.itemId,
                                                                                              self.itemId)
        self.__DataBase.Query(query)

    def setItemAsPending(self):
        self.status = 'Pending'
        self.startDate = 'NULL'
        self.endDate = 'NULL'
        query = "update Items SET Status= 'Pending' ,StartTime = '{}', EndTime='{}' where ItemId = '{}'".format(
            self.startDate, self.endDate, self.itemId)

        self.__DataBase.Query(query)

    def setItemExecution(self):
        self.itemExecutions += 1


class Logger:
    def __init__(self, robotId):
        Dbpath = os.path.abspath(os.path.join(os.path.dirname(__file__), ".")) + "/Robots.sqlite"
        self.__DataBase = Sqlite(Dbpath)
        self.robot = robotId
        self.time = None

    def log(self, log):
        self.time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        data = {"RobotId": self.robot, "LogType": "Log", "LogData": log, "DateTime": self.time}
        self.__DataBase.Insert("Logger", data)

    def systemException(self, error):
        self.time = datetime.today()
        data = {"RobotId": self.robot, "QueueId": self.queue, "ItemId": self.item, "LogType": "System Exception",
                "LogData": error, "DateTime": self.time}
        self.__DataBase.Insert("Logger", data)

    def businessException(self, error):
        self.time = datetime.today()
        data = {"RobotId": self.robot, "QueueId": self.queue, "ItemId": self.item, "LogType": "Business Exception",
                "LogData": error, "DateTime": self.time}
        self.__DataBase.Insert("Logger", data)

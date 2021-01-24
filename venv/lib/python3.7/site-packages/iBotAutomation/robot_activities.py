from .dataBase_activities import *
from .system_activities import id_generator
from datetime import datetime
import os


class Robot:

    def __init__(self, robotid=None):

        self._DataBase = os.path.abspath(__file__) + "Robots.sqlite"

        if robotid is None:
            robotId = id_generator(6)

        if not self.robotQuery(robotid):
            print("Robot {} doesn't exists".format(robotid))
        else:
            print("Robot {} successfully match".format(robotid))
            self.robotid = robotid
            self.robotName = \
                Sqlite.Query(self._DataBase, "SELECT name FROM Robots where id = '{}' ".format(self.robotid))[0][0]
            self.RobotPath = \
                Sqlite.Query(self._DataBase, "SELECT path FROM Robots where id = '{}' ".format(self.robotid))[0][0]

    def robotQuery(self, robot):

        query = "SELECT id FROM Robots where id = '{}' ".format(robot)
        robotquery = Sqlite.Query(self._DataBase, query)
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
        queues = Sqlite.Query(self._DataBase, "Select QueueId from Queues where QueueName = '{}'".format(queueName))
        for queue in queues:
            Queues.append(Queue(self.robotid, queueId=queue[0]))
        return Queues

    def deleteQueue(self, queueId):
        query = "DELETE from Queues WHERE RobotId = '{}' and  QueueId = '{}' ".format(self.robotid, queueId)
        Sqlite.Query(self._DataBase, query)


class Queue:
    def __init__(self, robotId, queueName=None, queueId=None):

        self._DataBase = os.path.abspath(__file__ + '/../../../../..') + "/Kivyapp/Robots.sqlite"
        self.items = []
        self.retryTimes = 1
        if queueId is None:
            self.queueId = id_generator(16)
            self.queueName = queueName
            queuedata = {'RobotId': robotId, 'QueueId': self.queueId, 'QueueName': self.queueName}
            Sqlite.Insert(self._DataBase, "Queues", queuedata)

        else:
            self.queueId = queueId
            self.queueName = Sqlite.Query(self._DataBase,
                                          "select QueueName from Queues where QueueId = '{}'".format(self.queueId))[0][
                0]
            self._getItems()

    def _getItems(self):
        self.items = []
        queueItems = Sqlite.Query(self._DataBase, "Select ItemId from Items where QueueId ='{}'".format(self.queueId))
        for itemId in queueItems:
            self.items.append(Item(self.queueId, itemId=itemId[0]))

    def createItem(self, item):
        item = Item(self.queueId, value=item)
        self.items.append(item)

    def getNextItem(self):
        for item in self.items:

            if item.status == 'Fail' and item.itemExecutions < self.retryTimes:
                self.items.append(self.items.pop(self.items.index(item)))
                item.setItemExecution()
                item.setItemAsPending()
            if item.status == 'Pending':
                item.setItemAsWorking()
                return item

    def setRetryTimes(self, times):
        self.retryTimes = times

    def clearQueue(self):
        Sqlite.Query("Delete from Items where QueueId = '{}'".format(self.queueId))


class Item:
    def __init__(self, queueId, itemId=None, value=None):
        self._DataBase = os.path.abspath(__file__ + '/../../../../..') + "/Kivyapp/Robots.sqlite"
        self.QueueId = queueId
        self.itemExecutions = 0
        self.startDate = None
        self.endDate = None
        if itemId is None:
            self.itemId = id_generator(24)
            self.value = value
            self.status = 'Pending'
            itemData = {'QueueId': self.QueueId, 'ItemId': self.itemId, 'Value': value, 'Status': self.status}
            Sqlite.Insert(self._DataBase, "Items", itemData)

        else:
            self.itemId = itemId
            query = Sqlite.Query(self._DataBase,
                                 "Select Value, Status from Items where ItemId ='{}'".format(self.itemId))
            self.value = query[0][0]
            self.status = query[0][1]

    def setItemAsWorking(self):
        self.status = 'Working'
        self.startDate = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        query = "update Items SET Status = 'Working',StartTime = '{}' where ItemId = '{}'".format(self.startDate,
                                                                                                  self.itemId)
        Sqlite.Query(self._DataBase, query)

    def setItemAsOk(self):
        self.status = 'OK'
        self.endDate = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        query = "update Items SET Status= 'OK', EndTime = '{}' where ItemId = '{}'".format(self.endDate,
                                                                                           self.itemId)
        sqlQuery(self._DataBase, query)

    def setItemAsFail(self):
        self.status = 'Fail'
        self.endDate = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        query = "update Items SET Status= 'Fail', EndTime = '{}' where ItemId = '{}'".format(self.itemId,
                                                                                             self.itemId)
        Sqlite.Query(self._DataBase, query)

    def setItemAsWarn(self):
        self.status = 'Warn'
        self.endDate = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        query = "update Items SET Status= 'Warn' , EndTime = '{}' where ItemId = '{}'".format(self.itemId,
                                                                                              self.itemId)
        Sqlite.Query(self._DataBase, query)

    def setItemAsPending(self):
        self.status = 'Pending'
        self.startDate = 'NULL'
        self.endDate = 'NULL'
        query = "update Items SET Status= 'Pending' ,StartTime = '{}', EndTime='{}' where ItemId = '{}'".format(
            self.startDate, self.endDate, self.itemId)

        Sqlite.Query(self._DataBase, query)

    def setItemExecution(self):
        self.itemExecutions += 1


class Logger:
    def __init__(self, robotId):
        self._DataBase = os.path.abspath(__file__ + '/../../../../..') + "/Kivyapp/Robots.sqlite"
        self.robot = robotId
        self.time = None

    def log(self, log):
        self.time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        data = {"RobotId": self.robot, "LogType": "Log", "LogData": log, "DateTime": self.time}
        Sqlite.Insert(self._DataBase, "Logger", data)

    def systemException(self, error):
        self.time = datetime.today()
        data = {"RobotId": self.robot, "QueueId": self.queue, "ItemId": self.item, "LogType": "System Exception",
                "LogData": error, "DateTime": self.time}
        Sqlite.Insert(self._DataBase, "Logger", data)

    def businessException(self, error):
        self.time = datetime.today()
        data = {"RobotId": self.robot, "QueueId": self.queue, "ItemId": self.item, "LogType": "Business Exception",
                "LogData": error, "DateTime": self.time}
        Sqlite.Insert(self._DataBase, "Logger", data)

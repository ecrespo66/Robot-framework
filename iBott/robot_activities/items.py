import requests
from datetime import datetime


class Item(object):
    """
    Class to handle Queue items from the robot manager console.
    Arguments:
        connection (object): Connection object to the robot manager console.
        queue_id (int): Queue ID to get items from.
        start_date (str): Start date to get items from.
        end_date (str): End date to get items from.
        item_id (int): Item ID to get items from.
        item_data (dict): Item data to get items from.
    Attributes:
        connection (object): Connection object to the robot manager console.
        queue_id (int): Queue ID to get items from.
        start_date (str): Start date to get items from.
        end_date (str): End date to get items from.
        item_id (int): Item ID to get items from.
        item_data (dict): Item data to get items from.
        item_executions (int): List of item executions.
        value (str): Item value.
        status (str): Item status.
    Methods:
        set_item_as_working(self): Set item as working.
        set_item_as_ok(self): Set item as ok.
        set_item_as_fail(self): Set item as failed.
        set_item_as_warn(self): Set item as warning.
        set_item_as_pending(self): Set item as pending.
        set_item_executions(self): increment item execution counter

    """
    def __init__(self, **kwargs):
        """Item constructor"""
        self.connection = kwargs.get('connection')
        self.queue_id = kwargs.get('queue_id', None)
        self.start_date = kwargs.get('start_date', None)
        self.end_date = kwargs.get('end_date', None)
        self.item_id = kwargs.get('item_id', None)
        self.item_data = kwargs.get('item_data', None)
        self.item_executions = 0
        self.value = None
        self.status = None
        self.__check_item()

    def __set_item_status(self):
        """Set item status"""
        endpoint = f'{self.connection.ws_protocol}{self.connection.url}/api/items/{self.item_id}/'
        data = {"ItemId": self.item_id,
                "Status": self.status,
                'ResolutionTime': datetime.now()}
        try:
            requests.put(endpoint, data, headers=self.connection.headers)
        except Exception as exception_message:
            raise Exception(exception_message)

    def set_item_as_working(self):
        """Block current item"""
        self.status = 'Working'
        self.__set_item_status()

    def set_item_as_ok(self):
        """Set Item status as OK"""
        self.status = 'OK'
        self.__set_item_status()

    def set_item_as_fail(self):
        """Set Item status as Fail"""
        self.status = 'Fail'
        self.__set_item_status()

    def set_item_as_warn(self):
        """Set Item status as Warn"""
        self.status = 'Warn'
        self.__set_item_status()

    def set_item_as_pending(self):
        """Set Item status as Pending"""
        self.status = 'Pending'
        self.__set_item_status()

    def set_item_executions(self):
        """Set number of executions"""
        self.item_executions += 1

    def __check_item(self):
        """Check if item data is correct"""
        if self.item_id is None:
            self.__post_item()
        elif self.item_data is not None:
            if type(self.item_data) is not dict:
                raise ValueError("Item data must be a dictionary")
            self.__get_item()
        else:
            raise ValueError('Invalid item data')

    def __post_item(self):
        """Post new item"""
        self.status = 'Pending'
        endpoint = f'{self.connection.ws_protocol}{self.connection.url}/api/items/'
        item = {'QueueId': self.queue_id,
                'ItemId': self.item_id,
                'Value': str(self.item_data),
                'Status': self.status,
                'CreationTime': datetime.now()}
        try:
            requests.post(endpoint, item, headers=self.connection.headers)
        except Exception as exception_message:
            raise Exception(exception_message)

    def __get_item(self):
        """Get item data"""
        try:
            endpoint = f'{self.connection.ws_protocol}{self.connection.url}/api/items/ItemId={self.item_id}'
            item = requests.get(endpoint, headers=self.connection.headers).json()
            self.value = eval(item['Value'])
            self.status = item['Status']
        except Exception as exception_message:
            raise Exception(exception_message)


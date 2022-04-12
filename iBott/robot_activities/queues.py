import requests
from iBott import System, OrchestratorConnectionError
from iBott.robot_activities.items import Item
from iBott.robot_activities.server import OrchestratorAPI


class Queue(OrchestratorAPI):
    """
    Class to manage queues in Orchestrator.
    With this class you can create, update and get queues from Orchestrator.
    Arguments:
        robot: The robot object.
    """

    def __init__(self, **kwargs):
        self.kwargs = kwargs
        super().__init__(**self.kwargs)
        self.queue_id = self.kwargs.get('queue_id', None)
        self.queue_name = self.kwargs.get('queue_name', None)
        self.__get_queue()
        self.__retry_times = 1

    def __get_queue(self):
        """
        Get Queue from Orchestrator
        Returns:
            Queue: queue object.
        """
        if self.queue_id is None:
            self.queue_id = System.id_generator(size=16)
            end_point = f'{self.http_protocol}{self.url}/api/queues/'
            data = {
                'RobotId': self.robot_id,
                'QueueId': self.queue_id,
                'QueueName': self.queue_name
            }
            requests.post(end_point, data, headers=self.headers)

        else:
            end_point = f'{self.http_protocol}{self.url}/api/queues/QueueId={self.queue_id}/'
            response = requests.get(end_point, headers=self.headers)
            self.queue_name = response.json()['QueueName']

    def __getItem(self):
        """
        Get all items from Queue
        Return:
            Item: Yields pending items from Queue.
        """

        endpoint = f'{self.http_protocol}{self.url}/api/items/QueueId={self.queue_id}'

        try:
            queue_items = requests.get(endpoint, headers=self.headers).json()
        except Exception as exception_message:
            raise OrchestratorConnectionError(exception_message)

        for qitem in queue_items:
            self.kwargs['item_id'] = qitem['ItemId']
            self.kwargs['queue_id'] = self.queue_id
            item = Item(self.kwargs)

            if item.status == 'Fail' and item.item_executions < self.__retry_times:
                item.set_item_executions()
                item.set_item_as_pending()
            if item.status == 'Pending':
                item.set_item_as_working()
                yield item

    def create_item(self, item_data: dict):
        """
        Create New Item in The Orchestrator
        Arguments:
            item_data: Dictionary with the item data.
        """
        self.kwargs['item_data'] = item_data
        item = Item(self.kwargs)
        return item

    def get_next_item(self):
        """
        Get Next Pending item from Orchestrator
        Returns:
            Item: The next item from the queue.
        """
        try:
            item = next(self.__getItem())
        except:
            item = None
        return item

    def set_retry_times(self, times: int):
        """
        Set number of retry times for each item
        Arguments:
            times: Number of retry times.
        """
        self.__retry_times = times


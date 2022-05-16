from iBott.robot_activities.flow import RobotFlow
import inspect
import traceback


class RobotBaseException(Exception):
    def __init__(self, robot):
        self.robot = robot
        self.traceback = traceback.format_exc()
        self.send_exception()

    def send_exception(self):
        """send exception to orchestrator"""
        for line in self.traceback.splitlines():
            self.robot.log.system_exception(str(line))
        self.robot.log.system_exception("[Execution Failed]")


class RobotException(Exception):
    exceptions = []

    def __init__(self, *args, **kwargs):
        self.__class__.exceptions.append(self)
        curframe = inspect.currentframe()
        current_method_name = inspect.getouterframes(curframe, 2)[1][3]  # get the name of the caller method
        self.node = RobotFlow.get_node(current_method_name)
        self.nodes = RobotFlow.nodes
        self.robot = args[0]  # kwargs.get("robot")
        self.message = kwargs.get("message", None)
        self.next_action = kwargs.get("next_action", None)
        Exception.__init__(self, self.message)
        self.process_exception()

    def process_exception(self):
        return

    def get_next_node(self, next_method: str):
        """
        get next node from the flow based on the next_method name (string)
        Arguments:
            next_method {string} -- name of the next method
        """
        for node in self.nodes:
            if node.name == next_method:
                return node

    def retry(self, max_retry_times):
        """
        retry the current node
        Arguments:
            max_retry_times {int} -- max retry times
        """
        retry_times = self.count_retry_times()
        if retry_times <= max_retry_times:
            self.node.run(self.robot)
        else:
            raise RecursionError(f"Max retry times reached for node: {self.node.name}")

    def go_to_node(self, next_node, max_retry_times):
        """
        go to the next node
        Arguments:
            next_node {function} -- method to be executed when Exception is raised
            max_retry_times {int} -- max retry times

        """
        next_node = self.get_next_node(next_node)
        retry_times = self.count_retry_times()
        if retry_times <= max_retry_times:
            next_node.run(self.robot)
        else:
            raise RecursionError(f"Max retry times reached for node: {self.node.name}")

    def restart(self, max_retry_times):
        """
        Restart process from the beginning of the flow
        Arguments:
            max_retry_times {int} -- max retry times
        """
        retry_times = self.count_retry_times()
        if retry_times <= max_retry_times:
            self.nodes[0].run(self.robot)
        else:
            raise RecursionError(f"Max retry times reached for node: {self.node.name}")

    def skip(self):
        """
        skip the current node
        """
        self.node.next_node.run(self.robot)

    def stop(self):
        """
        stop the current node
        """
        self.nodes[-1].run(self.robot)

    @staticmethod
    def count_retry_times(counter=[0]):
        """
        count the retry times of the current node
        Arguments:
            counter {list} -- counter list
        """
        counter[0] += 1
        return counter[0]




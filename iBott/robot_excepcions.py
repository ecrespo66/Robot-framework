from iBott.robot_flow import RobotFlow
import inspect
import traceback


class RobotBaseException(Exception):
    def __init__(self, robot):
        self.robot = robot
        self.traceback = traceback.format_exc()
        self.send_exception()

    def send_exception(self):
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
        self.message = kwargs.get("message")
        self.next_action = kwargs.get("next_action")
        Exception.__init__(self, self.message)
        self.process_exception()

    @classmethod
    def get_exceptions(cls):
        return cls.exceptions

    def process_exception(self):
        return

    def get_next_node(self, next_method):
        for node in self.nodes:
            if node.name == next_method.name:
                return node

    def retry(self, max_retry_times):
        retry_times = self.count_retry_times()
        if retry_times <= max_retry_times:
            print(max_retry_times, retry_times)
            self.node.run(self.robot)
        else:
            raise RecursionError(f"Max retry times reached for node: {self.node.name}")

    def go_to_node(self, next_node, max_retry_times):
        next_node = self.get_next_node(next_node)
        retry_times = self.count_retry_times()
        if retry_times <= max_retry_times:
            next_node.run(self.robot)
        else:
            raise RecursionError(f"Max retry times reached for node: {self.node.name}")

    def restart(self, max_retry_times):
        retry_times = self.count_retry_times()
        if retry_times <= max_retry_times:
            print(retry_times, retry_times)
            self.nodes[0].run(self.robot)
        else:
            raise RecursionError(f"Max retry times reached for node: {self.node.name}")

    @staticmethod
    def count_retry_times(counter=[0]):
        counter[0] += 1
        return counter[0]


class OrchestratorConnectionError(Exception):
    pass

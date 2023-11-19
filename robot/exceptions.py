from robot_manager.exceptions import RobotException


class BusinessException(RobotException):
    """Inherits from RobotException class.
    BusinessException is raised when the robot is doing something wrong.

    Arguments:
        robot: Robot instance
        message: Message sent to the user.
        next_action:  Next action when the exception is raised.
    """

    def __init__(self, *args, **kwargs):
        super.__init__(*args, **kwargs)

    def process_exception(self):
        """
        Overwrite the process_exception method from RobotException class.
        Write action when a Business exception occurs
        :param: None
        :return: None
        """
        # send log to robot manager console.
        self.robot.Log.business_exception(self.message)
        # Process exception
        if self.next_action == "retry":
            self.retry(3)
        elif self.next_action == "restart":
            self.restart(3)
        elif self.next_action == "go_to_node":
            self.go_to_node("end", 3)
        elif self.next_action == "skip":
            self.skip()
        elif self.next_action == "stop":
            self.stop()
        else:
            raise Exception("Invalid next_action")


class SystemException(RobotException):
    """Inherits from RobotException class.
    SystemException is raised when the robot is doing something wrong.

    Arguments:
        robot: Robot instance
        message: Message sent to the user.
        next_action:  Next action when the exception is raised.
    """
    def __init__(self, *args, **kwargs):
        super.__init__(*args, **kwargs)

    def process_exception(self):
        """Overwrite the process_exception method from RobotException class.
        Write action when a Business exception occurs
        :param: None
        :return: None"""
        self.robot.Log.system_exception(self.message)
        # send log to robot manager console.
        # Process exception
        if self.next_action == "retry":
            self.retry(3)
        elif self.next_action == "restart":
            self.restart(3)
        elif self.next_action == "go_to_node":
            self.go_to_node("end", 3)
        elif self.next_action == "skip":
            self.skip()
        elif self.next_action == "stop":
            self.stop()
        else:
            raise Exception("Invalid next_action")


from iBott.robot_activities.exceptions import RobotException


class BusinessException(RobotException):
    """Inherits from RobotException class.
    BusinessException is raised when the robot is doing something wrong.

    Arguments:
        robot: Robot instance
        message: Message sent to the user.
        next_action:  Next action when the exception is raised.
    """

    def _init__(self, *args, **kwargs):
        super.__init__(*args, **kwargs)

    def process_exception(self):
        """
        Overwrite the process_exception method from RobotException class.
        Write action when a Business exception occurs
        :param: None
        :return: None
        """
        self.robot.Log.business_exception(self.message)
        self.go_to_node(self.next_action, 3)


class SystemException(RobotException):
    """Inherits from RobotException class.
    SystemException is raised when the robot is doing something wrong.

    Arguments:
        robot: Robot instance
        message: Message sent to the user.
        next_action:  Next action when the exception is raised.
    """
    def _init__(self, *args, **kwargs):
        super.__init__(*args, **kwargs)

    def process_exception(self):
        """Overwrite the process_exception method from RobotException class.
        Write action when a Business exception occurs
        :param: None
        :return: None"""
        self.robot.Log.system_exception(self.message)

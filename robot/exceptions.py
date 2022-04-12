from iBott.robot_activities.exceptions import RobotException


class BusinessException(RobotException):
    """Inherits from RobotException class.
    BusinessException is raised when the robot is doing something wrong.

    Arguments:
        :param robot: The robot that is doing something wrong.
        :type robot: Robot

        :param message: The message that is being sent to the user.
        :type message: str

        :param next_action: The next action that the robot should do.
        :type next_action: function"""

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
        :param robot: The robot that is doing something wrong.
        :type robot: Robot

        :param message: The message that is being sent to the user.
        :type message: str

        :param next_action: The next action that the robot should do.
        :type next_action: function"""

    def _init__(self, *args, **kwargs):
        super.__init__(*args, **kwargs)

    def process_exception(self):
        """Overwrite the process_exception method from RobotException class.
        Write action when a Business exception occurs
        :param: None
        :return: None"""
        self.robot.Log.system_exception(self.message)

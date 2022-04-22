class RobotNode:
    """
    This class is used to create a node for the robot.
    :param method: method from the robot class
    :param parent: Parents node
    :param position: Position of the node

    """
    def __init__(self, **kwargs):
        self.method = kwargs.get("method")
        self.position = kwargs.get("position")
        self.parent_nodes = kwargs.get("parents", None)
        self.node_type = "OperationNode"
        self.name = self.method.__name__
        self.exception_type = None
        self.on_exception_node = None
        self.next_node = None
        self.doc = self.method.__doc__
        self.node_flows = []
        self.data = None

    def connect(self, next_node, pathName=None):
        """
        This method is used to connect the current node to the next node.
        receives the next node and the path name.
        :param next_node:
        :param pathName:
        :return:
        """
        self.next_node = next_node
        if pathName:
            flow_path = f"{str(self.position)}-->|{pathName}|{str(next_node.position)}"
        else:
            flow_path = f"{str(self.position)}-->{str(next_node.position)}"
        self.node_flows.append(flow_path)

    def run(self, robot, *args):
        """
        This method is used to run the node.
        """
        self.data = self.method(robot, *args)
        if self.next_node:
            self.next_node.run(robot, self.data)


class StartClass(RobotNode):
    """
    This class is used to create a start node.
    :param **kwargs:
    :type **kwargs:
    """
    def __init__(self, **kwargs):
        """Initialize Node Class """
        super().__init__(**kwargs)
        self.node_type = "StartNode"

        self.node_object = f"{str(self.position)}(({self.name}))"
        if self.position > 0:
            raise ValueError("Start Node must be in first position of the flow")


class EndClass(RobotNode):
    """
    This class is used to create an end node.
    Heritates from RobotNode Class
    :param **kwargs:
    :type **kwargs:
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.node_type = "EndNode"
        self.node_object = f"{str(self.position)}([{self.name}])"

    def connect(self, **kwargs):
        """
        This method is used to connect the current node to the next node.
        :param kwargs:

        raises ValueError if the node is not in the last position of the flow
        """
        raise ValueError("EndNode Must be at the end of the flow")

    def run(self, robot, *args):
        self.method(robot, *args)
        robot.finish_execution()


class OperationClass(RobotNode):
    """
    This class is used to create an operation node.
    Heritates from RobotNode Class
    :param **kwargs:
    :type **kwargs:
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.node_type = "OperationNode"
        self.node_object = f"{str(self.position)}[{self.name}]"


class OnTrueClass(RobotNode):
    """
    This class is used to create an onTrue node.
    Heritates from RobotNode Class
    :param **kwargs:
    :type **kwargs:
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.node_type = "OnTrueNode"
        self.node_object = f"{str(self.position)}[{self.name}]"


class OnFalseClass(RobotNode):
    """
    This class is used to create an onFalse node.
    Heritates from RobotNode Class
    :param **kwargs:
    :type **kwargs:
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.node_type = "OnFalseNode"
        self.node_object = f"{str(self.position)}[[{self.name}]]"


class ConditionClass(RobotNode):
    """
    ConditionClass is used to create a condition node.
    Heritates from RobotNode Class.

    Arguments:
    =========
    To instance Conditional classes.
        1. function: Function to be used as condition.
        2. parents: *optional - Defines the ancestors of the current node in the flow
        3. condition: *optional - Defines the condition of the current node for conditional nodes

    Methods:
    ========
    Custom methods: override the default implementation of RobotNode class.
        1. Connect: Creates a double connection for node (OnTrueNode/OnFalseNode).
        2. Run: This method is used to run conditional nodes.
           Evaluates function and executes next node (OnTrueNode/OnFalseNode) depending on the result.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.node_type = "ConditionNode"
        self.node_object = str(self.position) + "{" + self.name + "}"
        self.condition = kwargs.get("function")
        self.on_true_node = None
        self.on_false_node = None

    def connect(self, module):
        """
        This method is used to connect the current node to the next nodes.
        Evaluating node_types and setting the corresponding onTrueNode and onFalseNode and the flow_path attribute.

        Arguments:
        module: type RobotNode -> module to be connected to the current node.
        """
        if module.node_type == "OnTrueNode":
            self.on_true_node = module
            flow_path = f"{str(self.position)}-->|True|{str(self.on_true_node.position)}"
        elif module.node_type == "OnFalseNode":
            self.on_false_node = module
            flow_path = f"{str(self.position)}-->|False|{str(self.on_false_node.position)}"
        else:
            raise ValueError("Wrong module connection for ConditionClass")
        self.node_flows.append(flow_path)

    def run(self, robot, *args):
        """
        This method is used to run the conditional nodes.
        Evaluates function and execute the next node (OnTrueNode/OnFalseNode) depending on the result.
        Arguments:
        robot: type Robot -> robot object.
        *args: *optional - Defines the arguments of the current node.
        """
        self.data = self.method(robot, *args)
        if self.condition(self.data):
            self.on_true_node.run(robot, self.data)
        else:
            self.on_false_node.run(robot, self.data)

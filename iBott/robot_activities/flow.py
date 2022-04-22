class RobotFlow(object):
    """
    RobotFlow is a class that allows you to define the flow of you process
    it is used as decorator for the methods of the robot class.
        Arguments:
            method: the method that will be decorated by the flow
            node: the node that will be used to execute the method
            counter: autoincrement counter for the methods of robot classmethods
            parents (optional): list of parent nodes
            condition (optional): conditional function to execute the method
        Returns:
            List of nodes that will be executed
    """

    nodes = []

    def __init__(self, node: object, counter: object = [0], **kwargs: object) -> object:
        self.nodeclass = node
        self.counter = counter
        self.parent_methods = kwargs.get("parents", None)
        self.eval_func = kwargs.get("condition", None)

    def __call__(self, method):
        self.method = method
        self.position = self.counter[0]
        self.counter[0] += 1
        self.node = self.nodeclass.value(method=self.method,
                                         position=self.position,
                                         parents=self.parent_methods,
                                         function=self.eval_func)
        self.__class__.nodes.append(self.node)
        return self.node

    @classmethod
    def get_nodes(cls):
        return cls.nodes

    @classmethod
    def get_node(cls, node_name):
        for node in cls.nodes:
            if node.name == node_name:
                return node

    @classmethod
    def get_children(cls, node):
        childNodes = []
        for childNode in cls.nodes:
            if childNode.parent_nodes:
                for childMethod in childNode.parent_nodes:
                    if node.name == childMethod:
                        childNodes.append(childNode)
        return childNodes

    @classmethod
    def order_nodes(cls):
        return sorted(cls.nodes, key=lambda x: x.position, reverse=False)

    @classmethod
    def run_robot(cls, robot):
        cls.nodes[0].run(robot)

    @classmethod
    def connect_nodes(cls):
        cls.nodes = cls.order_nodes()
        for node in cls.nodes:
            if node.node_type == "StartNode":
                childNodes = cls.get_children(node)
                if childNodes:
                    for child in childNodes:
                        node.connect(child)
                else:
                    next_node = cls.nodes[node.position + 1]
                    node.connect(next_node)

            elif node.node_type == "EndNodeNode":
                childNodes = cls.get_children(node)
                if len(childNodes) > 0:
                    for child in childNodes:
                        node.connect(child)
                else:
                    pass
            elif node.node_type == "OnTrueNode":
                childNodes = cls.get_children(node)
                if len(childNodes) > 0:
                    for child in childNodes:
                        node.connect(child)
                else:
                    pass
            elif node.node_type == "OnFalseNode":
                childNodes = cls.get_children(node)
                if len(childNodes) > 0:
                    for child in childNodes:
                        node.connect(child)
                else:
                    pass
            elif node.node_type == "OperationNode":
                childNodes = cls.get_children(node)
                if len(childNodes) > 0:
                    for child in childNodes:
                        node.connect(child)
                else:
                    next_node = cls.nodes[node.position + 1]
                    node.connect(next_node)

            elif node.node_type == "ConditionNode":
                childNodes = cls.get_children(node)
                if len(childNodes) > 0:
                    for child in childNodes:
                        node.connect(child)
                else:
                    raise Exception("No child nodes found for condition node")

    @classmethod
    def generate_documentation(cls):
        flow_str = "\n# FLOW CHART\n```mermaid\nflowchart LR"
        for node in cls.nodes:
            flow_str += "\n" + node.node_object
        for node in cls.nodes:
            for c in node.node_flows:
                flow_str += "\n" + c
        flow_str += "\n```"
        flow_str += "\n# FLOW NODES"
        for node in cls.nodes:
            flow_str += f"\n## NODE: {node.name}"
            if node.doc:
                flow_str += f"\n {node.doc}"
        return flow_str


from inspect import getclosurevars, getsource
from collections import ChainMap
from textwrap import dedent
import ast


class RobotFlow:
    """
    RobotFlow is a class that allows you to define a flow of the robot
    it is used as decorator for the methods of the robot class.
        arguments
            :param node: the node of the flow
            :type object: Node class

            :param counter autoRegister position of the method in the flow
            :type int

            :param method get the method decorated with @RobotFlow
            :type function
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

    @staticmethod
    def get_exceptions(func, ids=set()):
        try:
            vars = ChainMap(*getclosurevars(func)[:3])
            source = dedent(getsource(func))
        except TypeError:
            return

        class _visitor(ast.NodeTransformer):
            def __init__(self):
                self.nodes = []
                self.other = []

            def visit_Raise(self, n):
                self.nodes.append(n.exc)

            def visit_Expr(self, n):
                if not isinstance(n.value, ast.Call):
                    return
                c, ob = n.value.func, None
                if isinstance(c, ast.Attribute):
                    parts = []
                    while getattr(c, 'value', None):
                        parts.append(c.attr)
                        c = c.value
                    if c.id in vars:
                        ob = vars[c.id]
                        for name in reversed(parts):
                            ob = getattr(ob, name)

                elif isinstance(c, ast.Name):
                    if c.id in vars:
                        ob = vars[c.id]

                if ob is not None and id(ob) not in ids:
                    self.other.append(ob)
                    ids.add(id(ob))

        v = _visitor()
        v.visit(ast.parse(source))
        for n in v.nodes:
            if isinstance(n, (ast.Call, ast.Name)):
                name = n.id if isinstance(n, ast.Name) else n.func.id
                if name in vars:
                    print(name)

                    yield vars[name]

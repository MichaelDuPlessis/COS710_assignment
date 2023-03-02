from abc import ABC, abstractmethod

# interface to for two children nodes
class Node(ABC):
    # used to calulate the value of the tree
    @abstractmethod
    def calculate(self) -> float:
        pass

# represents a terminal node (so just a single value)
class TerminalNode(Node):
    def __init__(self, val: float) -> None:
        self.val = val

    def calculate(self) -> float:
        return self.val

# reprsents a function node which takes a variable amount of paramters an a function list
class FunctionNode(Node):
    def __init__(self, func: function, children: list[Node]) -> None:
        self.function = func # the function that performs some operation
        self.children = children

    def calculate(self) -> float:
        return self.function([child.calculate() for child in self.children])

# this is the tree
class Chromosome:
    def __init__(self) -> None:
        self.root = None

    def calculate(self) -> float:
        self.root.calculate()
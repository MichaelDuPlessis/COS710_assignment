from abc import ABC, abstractmethod
from typing import Dict, Callable, List, Iterable, get_origin, get_args

# interface to for two children nodes
class Node(ABC):
    # used to calulate the value of the tree
    # params is a dictionarry of the passed in paramters which is used by a child node
    @abstractmethod
    def calculate(self, params: Dict[str, float]) -> float:
        pass

# represents a terminal node (so just a single value) specifically a number
class NumberNode(Node):
    def __init__(self, val: float):
        self._val = val

    # implements base class
    def calculate(self, _: Dict[str, float]) -> float:
        return self._val
    
# represents a terminal node (so just a single value) specifically a paramter
class ParamNode(Node):
    def __init__(self, param: str):
        self._param = param

    # implements base class
    def calculate(self, params: Dict[str, float]) -> float:
        return params[self._param]

# reprsents a function node which takes a variable amount of paramters an a function list
class FunctionNode(Node):
    def __init__(self, func: Callable[..., float], children: List[Node] = []):
        self._function = func # the function that performs some operation
        self._children = children

    # implements base class
    def calculate(self, params: Dict[str, float]) -> float:
        return self._function(*[child.calculate(params) for child in self._children])
    
    # adds a child/childs to the children list
    def add_children(self, n: Node | Iterable[Node]):
        # this is weird shit
        if get_origin(Iterable) and isinstance(n, get_origin(Iterable)) and get_args(Iterable) == (Node,):
            self._children.extend(n)
        else:
            self._children.append(n)
    
# this is the tree
class Program:
    def __init__(self, root: Node = None) -> None:
        self._root = root

    def calculate(self) -> float:
        self._root.calculate()
from abc import ABC, abstractmethod
from typing import Dict, Callable, List, Iterable, get_origin, get_args

# interface to for two children nodes
class Node(ABC):
    # used to calulate the value of the tree
    # params is a dictionarry of the passed in paramters which is used by a child node
    @abstractmethod
    def calculate(self, params: Dict[str, float]) -> float:
        pass

    # to give string representation
    @abstractmethod
    def node_str(self, depth: int) -> str:
        pass

# represents a terminal node (so just a single value) specifically a number
class NumberNode(Node):
    def __init__(self, val: float):
        self._val = val

    # implements base class
    def calculate(self, _: Dict[str, float]) -> float:
        return self._val
    
    def node_str(self, depth: int) -> str:
        return f'{"=" * depth}{self._val}\n'
    
    def __str__(self) -> str:
        return f'{self._val}\n'
    
# represents a terminal node (so just a single value) specifically a paramter
class ParamNode(Node):
    def __init__(self, param: str):
        self._param = param

    # implements base class
    def calculate(self, params: Dict[str, float]) -> float:
        return params[self._param]
    
    def node_str(self, depth: int) -> str:
        return f'{"=" * depth}{self._param}\n'
    
    def __str__(self) -> str:
        return f'{self._param}\n'

# reprsents a function node which takes a variable amount of paramters an a function list
class FunctionNode(Node):
    def __init__(self, func: Callable[..., float]):
        self._function = func # the function that performs some operation
        self._children = []

    # implements base class
    def calculate(self, params: Dict[str, float]) -> float:
        return self._function(*[child.calculate(params) for child in self._children])
    
    # adds a child/childs to the children list
    def add_children(self, n: Node | Iterable[Node]):        
        if isinstance(n, Node):
            self._children.append(n)
        else:
            self._children.extend(n)

    def node_str(self, depth: int) -> str:
        return f'{"=" * depth}{self._function}\n{"".join([child.node_str(depth + 1) for child in self._children])}'
    
    def __str__(self) -> str:
        return f'{self._function}\n{"".join([child.node_str(1) for child in self._children])}'
    
# this is the tree
class Program:
    def __init__(self, root: Node) -> None:
        self._root = root

    def calculate(self, params: Dict[str, float]) -> float:
        return self._root.calculate(params)

    def tree_str(self) -> str:
        return self._root.node_str(0)
    
    def __str__(self) -> str:
        return self.tree_str()
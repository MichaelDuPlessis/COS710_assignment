from abc import ABC, abstractmethod
from typing import Dict, Callable, Iterable, List
import random
from random_module.rand import rand_node, function_id, param_id
from collections import deque

# interface to for three children nodes
class Node(ABC):
    def __init__(self, depth: int, parent: 'Node' = None):
        self.depth = depth # the depth that the current node is at
        self.parent = parent

    # used to calulate the value of the tree
    # params is a dictionarry of the passed in paramters which is used by a child node
    @abstractmethod
    def calculate(self, params: Dict[str, float]) -> float:
        pass

    # to give string representation
    @abstractmethod
    def node_str(self, depth: int) -> str:
        pass

    # to serialize a tree into a string
    @abstractmethod
    def serialize(self) -> str:
        pass

    # updates the nodes depth and is recursive for function node
    def update_depth(self, new_depth: int, max_depth: int):
        self.depth = new_depth

    def choose_random_node(self) -> 'Node':
        nodes = []
        self._linearize(nodes)
        return random.choice(nodes)

    # used for linearizing the tree
    def _linearize(self, node_list: List['Node']):
        node_list.append(self)

    def choose_random_node(self, depth: int) -> 'Node':
        nodes = []
        self._linearize(nodes, depth)
        return random.choice(nodes)

    # used for linearizing the tree
    def _linearize(self, node_list: List['Node'], depth: int):
        if self.depth > depth:
            node_list.append(self)

    # overloading equals operator
    def __eq__(self, other: object) -> bool:
        return isinstance(other, self.__class__)

# represents a terminal node (so just a single value) specifically a number
class NumberNode(Node):
    def __init__(self, val: float, depth: int, parent: Node = None):
        super(NumberNode, self).__init__(depth, parent)
        self._val = val

    # implements base class
    def calculate(self, _: Dict[str, float]) -> float:
        return self._val
    
    def serialize(self) -> str:
        return f'{self._val}'
    
    def node_str(self, depth: int) -> str:
        return f'{"=" * depth}{self._val}\n'
    
    def __str__(self) -> str:
        return f'{self._val}\n'
    
    def __eq__(self, other: object) -> bool:
        return super().__eq__(other) and self._val == other._val
    
# represents a terminal node (so just a single value) specifically a paramter
class ParamNode(Node):
    def __init__(self, param: str, depth: int, parent: Node = None):
        super(ParamNode, self).__init__(depth, parent)
        self._param = param

    # implements base class
    def calculate(self, params: Dict[str, float]) -> float:
        return float(params[self._param])
    
    def serialize(self) -> str:
        return f'{self._param}'
    
    def node_str(self, depth: int) -> str:
        return f'{"=" * depth}{self._param}\n'
    
    def __str__(self) -> str:
        return f'{self._param}\n'
    
    def __eq__(self, other: object) -> bool:
        return super().__eq__(other) and self._param == other._param

# reprsents a function node which takes a variable amount of paramters an a function list
class FunctionNode(Node):
    def __init__(self, func: Callable[..., float], depth: int, parent: Node = None):
        super(FunctionNode, self).__init__(depth, parent)
        self._function = func # the function that performs some operation
        self._children = []

    # implements base class
    def calculate(self, params: Dict[str, float]) -> float:
        return self._function(*[child.calculate(params) for child in self._children])
    
    # adds a child/childs to the children list
    def add_children(self, n: Node | Iterable[Node]):        
        if isinstance(n, Node):
            n.parent = self
            self._children.append(n)
        else:
            for node in n:
                node.parent = self
            self._children.extend(n)

    def _linearize(self, node_list: List[Node]):
        node_list.append(self)
        for child in self._children:
            child._linearize(node_list)

    def _linearize(self, node_list: List[Node], depth: int):
        if self.depth > depth:
            node_list.append(self)
            
        for child in self._children:
            child._linearize(node_list)

    def serialize(self) -> str:
        return f'{self._function.__name__}({" ".join([child.serialize() for child in self._children])})'

    # must update depth of children
    def update_depth(self, new_depth: int, max_depth: int):
        self.depth = new_depth

        # cannot be function node must update
        if self.depth == max_depth:
            # choose new node
            node = rand_node([1, 2], self.depth)

            # update parent
            children = [child if child != self else node for child in self.parent._children]
            self.parent._children = children
        else:
            for child in self._children:
                child.update_depth(new_depth + 1, max_depth)

    def node_str(self, depth: int) -> str:
        return f'{"=" * depth}{self._function.__name__}\n{"".join([child.node_str(depth + 1) for child in self._children])}'
    
    def __str__(self) -> str:
        return f'{self._function.__name__}\n{"".join([child.node_str(1) for child in self._children])}'
    
    def __eq__(self, other: object) -> bool:
        return super().__eq__(other) and self._function == other._function
    
    # used for structure based gp to get teh structure as a byte array/list to compare
    # only goes to depth specified
    # it does this by bfs
    def to_structure_list(self, depth: int) -> List[int]:
        queue = deque([self])
        nodes_vals = []

        while len(queue) > 0:
            cur_node = queue.pop(0)

            if cur_node.depth > depth:
                return nodes_vals
            
            if type(cur_node) is FunctionNode:
                nodes_vals.append(function_id(cur_node._function))

                for child in cur_node._children:
                    queue.append(child)
            elif type(cur_node) is ParamNode:
                nodes_vals.append(param_id(cur_node._param))
            else:
                nodes_vals.append(-1)

import random
from population_module.functions import FUNCTIONS
from typing import Callable, Tuple, List
from population_module.program import FunctionNode, ParamNode, NumberNode

# list of all kinds of params that can be used
# maybe move later
PARAMS = [
    'Distance',
    'PLong',
    'PLatd',
    'DLong',
    'DLatd',
    'Haversine',
    'Pmonth',
    'Pday',
    'Phour',
    'Pmin',
    'PDweek',
    'Dmonth',
    'Dday',
    'Dhour',
    'Dmin',
    'DDweek',
    'Temp',
    'Precip',
    'Wind',
    'Humid',
    'Solar',
    'Snow',
    'GroundTemp',
    'Dust'
]

# must be called 
def set_seed(seed: int):
    random.seed(seed)

# returns a random function
def rand_func() -> Tuple[int, Callable[..., float]]:
    return random.choice(FUNCTIONS)

# give a random input paramter
def rand_param() -> str:
    return random.choice(PARAMS)

# takes list of numbers (max number of node types(3)) and returns one
# [0, 1, 2] means all nodes
# [1, 2] means only param or num node
def rand_node(options: List[int], depth: int) -> Node | Tuple[int, Node]:
    # deciding what to generate
    # 0 = func
    # 1 = param
    # 2 = number
    gen_node = random.choice(options)

    if gen_node == 0:
        arg_count, func = rand_func()
        return [arg_count, FunctionNode(func, depth)]
    elif gen_node == 1:
        node = ParamNode(rand_param(), depth)
    else:
        node = NumberNode(rand_num(), depth)

    return node


# generates a random numebr between two ranges
def rand_num(min: float = -100, max: float = 100) -> float:
    return random.uniform(min, max)
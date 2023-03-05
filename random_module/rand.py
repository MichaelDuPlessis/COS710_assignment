import random
from population_module.functions import FUNCTIONS
from typing import Callable, Tuple

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

# generates a random numebr between two ranges
def rand_num(min: float = -100, max: float = 100) -> float:
    random.uniform(min, max)
import random
from population_module.functions import FUNCTIONS

# must be called 
def set_seed(seed: int):
    random.seed(seed)

# returns a random function
def rand_func() -> function:
    return random.choice(FUNCTIONS)

# generates a random numebr between two ranges
def rand_num(min: float = -100, max: float = 100) -> float:
    random.uniform(min, max)
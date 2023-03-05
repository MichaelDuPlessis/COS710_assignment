from program import Program
from typing import List

# generate a single tree of the population
def _generate_tree(depth: int) -> Program:
    pass

# create initial population of certain size with certain depth
def generate_initial_pop(pop_size: int, depth: int) -> List[Program]:
    return [_generate_tree(depth) for _ in range(pop_size)]
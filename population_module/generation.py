from .program import Program
from typing import List

# generate a single tree of the population
def _generate_tree(current_depth: int, min_depth: int, max_depth: int) -> Program:
    pass

# create initial population of certain size with certain depth
def generate_initial_pop(pop_size: int, min_depth: int, max_depth: int) -> List[Program]:
    return [_generate_tree(0, min_depth, max_depth) for _ in range(pop_size)]
# contains all the logic related to calculating the fitness

from typing import Dict, List
from population_module.program import Node
from multiprocessing import Pool

# cache = {} # used to cache tress so that they don't need to be recalculated

class Please:
    def __init__(self, program):
        self.program = program
    def __call__(self, data):
        return abs(self.program.calculate(data) - data['Duration'])

# calulates the raw fitness for a singular progra and some test data
def raw_fitness(program: Node, test_data: List[Dict[str, float]]) -> float:
    # program_str = program.serialize()
    # if program_str in cache:
    #     return cache[program_str]
    
    with Pool() as pool:
        fitness = sum(pool.map(Please(program), test_data))
        # cache[program_str] = fitness
        return fitness
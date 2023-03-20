# contains all the logic related to calculating the fitness

import multiprocessing
from typing import Dict, List
from population_module.program import Node
# from pathos.multiprocessing import ProcessingPool as Pool
from multiprocessing import Pool

class Please:
    def __init__(self, program):
        self.program = program
    def __call__(self, data):
        return abs(self.program.calculate(data) - data['Duration'])

# calulates the raw fitness for a singular progra and some test data
def raw_fitness(program: Node, test_data: List[Dict[str, float]]) -> float:
    # return sum([abs(program.calculate(data) - data['Duration']) for data in test_data])
    with Pool() as pool:
        return sum(pool.map(Please(program), test_data))
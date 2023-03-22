# contains all the logic related to calculating the fitness

from typing import Dict, Iterable, List
from population_module.program import Node
from multiprocessing import Pool

class Please:
    def __init__(self, program):
        self.program = program
    def __call__(self, data):
        return abs(self.program.calculate(data) - float(data['Duration']))

# calulates the raw fitness for a singular progra and some test data
def raw_fitness(program: Node, test_data: Iterable) -> float:
    with Pool() as pool:
        fitness = sum(pool.map(Please(program), test_data))
        return fitness
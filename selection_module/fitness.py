# contains all the logic related to calculating the fitness

from typing import Dict, Iterable, List
from population_module.program import Node
from multiprocessing import Pool

# this class is needed as an intermediary as pool.map cannot accept lambdas
class RunProgram:
    def __init__(self, program):
        self.program = program
    def __call__(self, data):
        return abs(self.program.calculate(data) - float(data['Duration']))

# calulates the raw fitness for a singular progra and some test data
def raw_fitness(program: Node, test_data: Iterable, multithreading: int = None) -> float:
    if multithreading:
        with Pool(multithreading) as pool:
            fitness = sum(pool.map(RunProgram(program), test_data))
            return fitness
        
    return sum([abs(program.calculate(data) - float(data['Duration'])) for data in test_data])
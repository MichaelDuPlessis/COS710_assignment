# contains all the logic related to calculating the fitness

from typing import Dict, List
from population_module.program import Program

# calulates the raw fitness for a singular progra and some test data
def raw_fitness(program: Program, test_data: List[Dict[str, float]]) -> float:
    return sum([abs(program.calculate(data) - test_data['Duration']) for data in test_data])
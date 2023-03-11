# this file is used for producing the next generation

from typing import Tuple
from population_module.program import Program
import copy

# programs are cloned in crossover
def crossover(program1: Program, program2: Program) -> Tuple[Program, Program]:
    program1, program2 = copy.deepcopy(program1), copy.deepcopy(program2)

    return program1, program2

# programs are cloned in mutate
def mutate(program: Program) -> Program:
    program = copy.deepcopy(program)

    return program
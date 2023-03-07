# this file contains the logic for selcting part of the population

from population_module.program import Program
from selection_module.fitness import raw_fitness
from typing import List
import random

def tournament(programs: List[Program], tournament_size: int = 4) -> Program:
    assert tournament_size < len(programs), "Tournament size must be less than population size"
    assert tournament_size >= 0, "Tournament size must be >= 0"

    participants = [random.choice(programs) for _ in range(tournament_size)]

    return max(participants, key=raw_fitness)
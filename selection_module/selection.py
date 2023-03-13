# this file contains the logic for selcting part of the population

from population_module.program import Node
from selection_module.fitness import raw_fitness
from typing import List, Dict
import random

def tournament(programs: List[Node], test_data: List[Dict[str, float]], tournament_size: int = 4) -> Node:
    assert tournament_size < len(programs), 'Tournament size must be less than population size'
    assert tournament_size >= 0, 'Tournament size must be >= 0'

    participants = [random.choice(programs) for _ in range(tournament_size)]

    return max(participants, key=lambda participants: raw_fitness(participants, test_data))
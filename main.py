#!/usr/bin/env python

import datetime
import random
import sys
from selection_module.fitness import raw_fitness
from population_module.generation import generate_initial_pop
from population_module.genetic_operators import crossover, mutate
from random_module import rand
from typing import List, Dict

# save is whether the output should be saved to a file or just outputted and runs is the number of runs that must be completed
# max_generations is the number of generations and the function ends either when desrid fitness is met or max_generations is met
def run(pop_size: int, max_depth: int, max_generations: int, desired_fitness: float, test_data: List[Dict[str, float]], runs: int = 1, save: bool = False):
    if save:
        now = datetime.now()
        dt_string = now.strftime("./runs/%d/%m/%Y-%H:%M:%S")
        file = open(dt_string, 'w')

    # data for all runs which will be outputted
    runs_data = {
        'pop_size': pop_size,
        'max_depth': max_depth,
        'max_generations': max_generations,
        'desired_fitness': desired_fitness,
        'runs': []
    }

    for id in range(runs):
        # seed
        seed = random.randrange(sys.maxsize)
        print(f'The see for the run is {seed}')
        rand.set_seed(seed)

        # data for specific run
        run_data = {
            'seed': seed,
            'generations': [] # list of all the generations as the best of each generation
        }

        population = generate_initial_pop(pop_size, max_depth)
        sorted(population, key=raw_fitness)

        run_data['generations'].append(population[0])

        

        runs_data['runs'].append(runs_data)


    if save:
        file.close()

if __name__ == '__main__':
    pass
#!/usr/bin/env python

import datetime
import random
import sys
from selection_module.fitness import raw_fitness
from population_module.generation import generate_initial_pop, generate_next_populateion
from random_module import rand
from typing import List, Dict

# save is whether the output should be saved to a file or just outputted and runs is the number of runs that must be completed
# max_generations is the number of generations and the function ends either when desrid fitness is met or max_generations is met
# cross_per + mut_per + repro_per = 1 must be true
def run(pop_size: int, max_depth: int, max_generations: int, desired_fitness: float, test_data: List[Dict[str, float]], tournament_size: int = 4, runs: int = 1, save: bool = False, cross_per: float = 0.5, mut_per: float = 0.5, repro_per: float = 0):
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

    for _ in range(runs):
        # seed
        seed = random.randrange(sys.maxsize)
        print(f'The see for the run is {seed}')
        rand.set_seed(seed)

        # data for specific run
        run_data = {
            'seed': seed,
            'desired_found': False, # whether we stopped because we found the desired fitness or the generations
            'generations': [] # list of all the generations as the best of each generation
        }

        population = generate_initial_pop(pop_size, max_depth)
        population_fitness = [(raw_fitness(p, test_data), p) for p in population] # fitness first as max looks at first element in tuple
        best = max(population_fitness)

        run_data['generations'].append({
            'generation': 0,
            'best_score': best
        })

        if best >= desired_fitness:
            run_data['desired_found'] = True
        else:
            for g in range(1, max_generations):
                population = generate_next_populateion(population, max_depth, max_generations * cross_per, max_generations * mut_per, max_generations * repro_per, tournament_size)
                population_fitness = [(raw_fitness(p, test_data), p) for p in population] # fitness first as max looks at first element in tuple
                best = max(population_fitness)

                run_data['generations'].append({
                    'generation': g,
                    'best_score': best
                })

                if best >= desired_fitness:
                    run_data['desired_found'] = True
                    break

        runs_data['runs'].append(runs_data)

    if save:
        file.close()

if __name__ == '__main__':
    pass
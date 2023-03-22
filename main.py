#!/usr/bin/env python

from datetime import datetime
import math
import random
import sys
import time
from performance_module.measures import run_all_measures
from selection_module.fitness import raw_fitness
from population_module.generation import generate_initial_pop, generate_next_populateion
from random_module import rand
from typing import List, Dict
import json
from input_module.file_reader import read_csv
import argparse
import os
import math

# save is whether the output should be saved to a file or just outputted and runs is the number of runs that must be completed
# max_generations is the number of generations and the function ends either when desrid fitness is met or max_generations is met
# cross_per + mut_per + repro_per = 1 must be true
def run(pop_size: int, max_depth: int, max_generations: int, desired_fitness: float, train_data: List[Dict[str, float]],
        test_data: List[Dict[str, float]], tournament_size: int = 4, runs: int = 1, save: bool = False, cross_per: float = 0.5,
        mut_per: float = 0.5, repro_per: float = 0, seed: int = None , seed_set: bool = False):
    
    training_data_size = len(train_data)

    if save:
        now = datetime.now()
        dt_string = now.strftime("%d-%m-%Y_%H#%M#%S")
        folder = os.sep.join(['.', 'runs', f'{dt_string}'])
        os.mkdir(folder)

    for r in range(runs):
        # run number
        print(f'Starting run: {r}')

        # seed
        if not seed_set:
            seed = random.randrange(sys.maxsize)
        print(f'The seed for the run is {seed}')
        rand.set_seed(seed)

        # data for specific run
        run_data = {
            'pop_size': pop_size,
            'max_depth': max_depth,
            'max_generations': max_generations,
            'desired_fitness': desired_fitness,
            'run': r,
            'data_set_size': {
                'training': training_data_size,
                'testing': len(test_data) 
            },
            'tournament_size': tournament_size,
            'weights': [
                cross_per,
                mut_per,
                repro_per
            ],
            'seed': seed,
            'desired_found': False, # whether we stopped because we found the desired fitness or the generations
            'generations': [] # list of all the generations as the best of each generation
        }

        start = time.time()
        population = generate_initial_pop(pop_size, max_depth)
        population_fitness = [(raw_fitness(p, train_data), p) for p in population] # fitness first as max looks at first element in tuple
        best = min(population_fitness, key=lambda p: p[0])

        run_data['generations'].append({
            'generation': 0,
            'best_score': best[0],
            'best_tree': best[1].serialize()
        })

        if best[0] / training_data_size <= desired_fitness: # taking average for fitness
            run_data['desired_found'] = True
        else:
            for g in range(1, max_generations):
                population = generate_next_populateion(population_fitness, max_depth, pop_size * cross_per,
                                                       pop_size * mut_per, pop_size * repro_per, tournament_size)

                population[random.randint(0, len(population) - 1)] = best[1]
                population_fitness = [(raw_fitness(p, train_data), p) for p in population] # fitness first as max looks at first element in tuple
                best = min(population_fitness, key=lambda p: p[0])

                # only printing every 10th generation should make command line parameter
                if (g + 1) % 10 == 0:
                    print(f'Generation {g} best score: {best[0] / training_data_size}')
                    run_data['generations'].append({
                        'generation': g,
                        'best_score': best[0],
                        'best_tree': best[1].serialize()
                    })

                if best[0] / training_data_size <= desired_fitness: # taking average for fitness
                    run_data['desired_found'] = True
                    print('Desered fitness found stopping')
                    break

        run_data['time'] = time.time() - start

        run_data['best'] = best[0] / training_data_size
        run_data['best_tree'] = best[1].serialize()
        run_data['generations_completed'] = g

        rmse, r_squared, median_absolute_error, mean_absolute_error = run_all_measures(best[1], train_data)
        run_data['measures'] = {
            'training': {
                'rmse': rmse,
                'r_squared': r_squared,
                'median_absolute_error' : median_absolute_error,
                'mean_absolute_error': mean_absolute_error
            }
        }

        rmse, r_squared, median_absolute_error, mean_absolute_error = run_all_measures(best[1], train_data)
        run_data['measures']['testing'] = {
                'rmse': rmse,
                'r_squared': r_squared,
                'median_absolute_error' : median_absolute_error,
                'mean_absolute_error': mean_absolute_error
            }

        print()

        if save:
            file = open(os.sep.join(['.', folder, f'{r}.json']), 'w')
            json.dump(run_data, file)
            file.close()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--save', help='Whether the output of the runs should be saved to a file', action='store_true')
    parser.add_argument('-p', '--pop', help='The size of the population. default 10', default=10, type=int)
    parser.add_argument('-e', '--seed', help='The seed to be used in every run', type=int)
    parser.add_argument('-r', '--runs', help='The number of runs to perform. default 3', default=3, type=int)
    parser.add_argument('-d', '--depth', help='The max depth of each run. default 5', default=5, type=int)
    parser.add_argument('-g', '--generations', help='The max number of generations of each run. default 20', default=20, type=int)
    parser.add_argument('-f', '--fitness', help='The desired fitness to reach (lower is better). default 5.0', default=5.0, type=float)
    parser.add_argument('-t', '--tournament', help='The size of the tournament for tournament selection. default 4', default=4, type=int)
    parser.add_argument('-w', '--weights', help='The crossover, mutation and reproduction chances as a comma seperated list e.g. 0.4,0.3,0.3. default "0.5,0.5,0"', default='0.5,0.5,0')
    parser.add_argument('-i', '--train', help='The amount from the data set to be trained on. default 100000', default=100_000, type=int)
    parser.add_argument('-j', '--test', help='The amount from the data set to be tested on. default 50000', default=50_000, type=int)
    default_path = os.sep.join(['.', 'data', 'For_modeling.csv'])
    parser.add_argument('-P', '--path', help=f'The path to the data set. default {default_path}', default=default_path, type=str)
    args = parser.parse_args()

    weights = [float(w) for w in args.weights.split(',')]

    data = read_csv(args.path, args.train + args.test)

    print(f'Start: {time.time()}')
    run(args.pop, args.depth, args.generations, args.fitness, data[:args.train], data[args.train:],
        save=args.save, runs=args.runs, tournament_size=args.tournament,
        seed=args.seed, seed_set=not not args.seed, cross_per=weights[0], mut_per=weights[1], repro_per=weights[2],
    )
    print(f'End: {time.time()}')
    
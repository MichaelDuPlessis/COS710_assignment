from datetime import datetime
import random
import sys
import time
from performance_module.measures import run_all_measures
from selection_module.fitness import raw_fitness
from population_module.generation import generate_initial_pop, generate_next_populateion, generate_pop_with_initial_structure
from random_module import rand
from typing import List, Dict
import json
import os

# this is for running a traditional GP
# save is whether the output should be saved to a file or just outputted and runs is the number of runs that must be completed
# max_generations is the number of generations and the function ends either when desrid fitness is met or max_generations is met
# cross_per + mut_per + repro_per = 1 must be true
def run_gp(pop_size: int, max_depth: int, max_generations: int, desired_fitness: float, train_data: List[Dict[str, float]],
        test_data: List[Dict[str, float]], tournament_size: int = 4, runs: int = 1, save: bool = False, cross_per: float = 0.5,
        mut_per: float = 0.5, repro_per: float = 0, seed: int = None , seed_set: bool = False, multithreading: int = None):
    
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
            'kind': 'Classical',
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
        population_fitness = [(raw_fitness(p, train_data, multithreading=multithreading), p) for p in population] # fitness first as max looks at first element in tuple
        best = min(population_fitness, key=lambda p: p[0])

        run_data['generations'].append({
            'generation': 0,
            'best_score': best[0],
            'best_tree': best[1].serialize()
        })

        g = 0 # incase loop is never entered
        if best[0] / training_data_size <= desired_fitness: # taking average for fitness
            run_data['desired_found'] = True
            print('Desered fitness found stopping')
        else:
            for g in range(1, max_generations):
                population = generate_next_populateion(population_fitness, max_depth, pop_size * cross_per,
                                                       pop_size * mut_per, pop_size * repro_per, tournament_size)

                population[random.randint(0, len(population) - 1)] = best[1]
                population_fitness = [(raw_fitness(p, train_data, multithreading=multithreading), p) for p in population] # fitness first as max looks at first element in tuple
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

        rmse, r_squared, median_absolute_error, mean_absolute_error = run_all_measures(best[1], train_data, multithreading=multithreading)
        run_data['measures'] = {
            'training': {
                'rmse': rmse,
                'r_squared': r_squared,
                'median_absolute_error' : median_absolute_error,
                'mean_absolute_error': mean_absolute_error
            }
        }

        rmse, r_squared, median_absolute_error, mean_absolute_error = run_all_measures(best[1], test_data)
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

# this is for running a structure GP
# save is whether the output should be saved to a file or just outputted and runs is the number of runs that must be completed
# max_generations is the number of generations and the function ends either when desrid fitness is met or max_generations is met
# cross_per + mut_per + repro_per = 1 must be true, structure depth is the depth at which a trees structure can be compared,
# comparison_len the number of generations between structure comparisons, change_wanted is the amount of change required not to change the structure
def run_sgp(pop_size: int, max_depth: int, max_generations: int, desired_fitness: float, train_data: List[Dict[str, float]],
        test_data: List[Dict[str, float]], tournament_size: int = 4, runs: int = 1, save: bool = False, cross_per: float = 0.5,
        mut_per: float = 0.5, repro_per: float = 0, seed: int = None , seed_set: bool = False, multithreading: int = None,
        structure_depth: int  = 1, comparison_len: int = 10, change_wanted: float = 5.0):
    
    training_data_size = len(train_data)

    if save:
        now = datetime.now()
        dt_string = now.strftime("%d-%m-%Y_%H#%M#%S")
        folder = os.sep.join(['.', 'runs', f'{dt_string}'])
        os.mkdir(folder)

    # the structures we have already generated and want to avoid it can be thought of as a global index
    gsim = set()

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
            'kind': 'Structure',
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
        population = generate_initial_pop(pop_size, max_depth, gsim)
        population_fitness = [(raw_fitness(p, train_data, multithreading=multithreading), p) for p in population] # fitness first as max looks at first element in tuple
        best = min(population_fitness, key=lambda p: p[0])

        # the structure that we want to keep generating
        structures = [best[1].to_structure_list(structure_depth)]
        # what we will compare to when we decide if we want to change the structure or not
        change_start = best[0]
        # the strucutre that we are mainting to search for
        structure_want = None

        run_data['generations'].append({
            'generation': 0,
            'best_score': best[0],
            'best_tree': best[1].serialize()
        })

        g = 0 # incase loop is never entered
        if best[0] / training_data_size <= desired_fitness: # taking average for fitness
            run_data['desired_found'] = True
            print('Desered fitness found stopping')
        else:
            for g in range(1, max_generations):
                population = generate_next_populateion(population_fitness, max_depth, pop_size * cross_per,
                                                       pop_size * mut_per, pop_size * repro_per, tournament_size)

                population_fitness = [(raw_fitness(p, train_data, multithreading=multithreading), p) for p in population] # fitness first as max looks at first element in tuple
                best = min(population_fitness, key=lambda p: p[0])

                structures.append(best[1].to_structure_list(structure_depth))

                # only printing every 10th generation should make command line parameter
                if (g + 1) % comparison_len == 0:
                    print(f'Generation {g} best score: {best[0] / training_data_size}')

                    # checking if we want to generate a new structure
                    if structure_want and best[0] > change_start - change_wanted:
                        # if the current structure appears at least 70% than add to avoid
                        if structures.count(structures[-1]) / len(structures) > 0.7:
                            print("Local optimum found adding to index")
                            gsim.add(structures[-1])
                            structure_want = structures[-1]
                            population = generate_pop_with_initial_structure(pop_size, max_depth, structure_want, structure_depth)
                            population_fitness = [(raw_fitness(p, train_data, multithreading=multithreading), p) for p in population] # fitness first as max looks at first element in tuple
                        
                        structures = []
                        change_start = best[0]

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

        rmse, r_squared, median_absolute_error, mean_absolute_error = run_all_measures(best[1], train_data, multithreading=multithreading)
        run_data['measures'] = {
            'training': {
                'rmse': rmse,
                'r_squared': r_squared,
                'median_absolute_error' : median_absolute_error,
                'mean_absolute_error': mean_absolute_error
            }
        }

        rmse, r_squared, median_absolute_error, mean_absolute_error = run_all_measures(best[1], test_data)
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
#!/usr/bin/env python

import time
from input_module.file_reader import read_csv
import argparse
import os

from training_module.train import run_gp

if __name__ == '__main__':
    # creating command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--save', help='Whether the output of the runs should be saved to a file. default true', action='store_true')
    parser.add_argument('-p', '--pop', help='The size of the population. default 10', default=10, type=int)
    parser.add_argument('-e', '--seed', help='The seed to be used in every run', type=int)
    parser.add_argument('-r', '--runs', help='The number of runs to perform. default 3', default=3, type=int)
    parser.add_argument('-d', '--depth', help='The max depth of each run. default 5', default=5, type=int)
    parser.add_argument('-g', '--generations', help='The max number of generations of each run. default 20', default=20, type=int)
    parser.add_argument('-f', '--fitness', help='The desired fitness to reach (lower is better). default 5.0', default=5.0, type=float)
    parser.add_argument('-t', '--tournament', help='The size of the tournament for tournament selection. default 4', default=4, type=int)
    parser.add_argument('-w', '--weights', help='The crossover, mutation and reproduction chances as a comma seperated list e.g. 0.4,0.3,0.3. default "0.5,0.5,0"', default='0.5,0.5,0')
    parser.add_argument('-i', '--train', help='The amount from the data set to be trained on. default 100000', default=100_000, type=int)
    parser.add_argument('-j', '--test', help='The amount from the data set to be tested on. default 25000', default=25_000, type=int)
    default_path = os.sep.join(['.', 'data', 'For_modeling.csv'])
    parser.add_argument('-P', '--path', help=f'The path to the data set. default {default_path}', default=default_path, type=str)
    parser.add_argument('-m', '--multithreading', help=f'Whether multithreading should be used and number of cores to use. default off', type=int)
    parser.add_argument('-k', '-kind', help=f'What kind of AI to use, gp, sgp, ge. default gp', default='gp', type=str)
    args = parser.parse_args()

    weights = [float(w) for w in args.weights.split(',')]

    data = read_csv(args.path, args.train + args.test)

    # running gp
    start = time.time()
    print(f'Start: {start}')
    
    match args.kind:
        case 'gp':
            run_gp(args.pop, args.depth, args.generations, args.fitness, data[:args.train], data[args.train:],
                save=args.save, runs=args.runs, tournament_size=args.tournament, multithreading=args.multithreading,
                seed=args.seed, seed_set=not not args.seed, cross_per=weights[0], mut_per=weights[1], repro_per=weights[2],
            )
        case 'sgp':
            print('not yet implemented')
        case 'ge':
            print('not yet implemented')

    end = time.time()
    print(f'End: {end}')
    print(f'Total time: {end - start}')
    
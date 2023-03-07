#!/usr/bin/env python

from population_module.generation import generate_initial_pop
from random_module import rand
from input_module import file_reader

if __name__ == '__main__':
    rand.set_seed(1)
    x = file_reader.read_csv('./data/test.csv')[0]
    print(generate_initial_pop(10, 5)[0].calculate(x))
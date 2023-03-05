#!/usr/bin/env python

from population_module.generation import generate_initial_pop
from random_module import rand

if __name__ == '__main__':
    rand.set_seed(1)
    print(generate_initial_pop(10, 5))
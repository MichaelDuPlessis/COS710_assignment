#!/usr/bin/env python

from population_module.generation import generate_initial_pop
from random_module import rand
from input_module import file_reader
import copy
from population_module.program import NumberNode

if __name__ == '__main__':
    rand.set_seed(1)
    x = generate_initial_pop(10, 5)

    print(x[0]._root._children[0].parent == x[0]._root)
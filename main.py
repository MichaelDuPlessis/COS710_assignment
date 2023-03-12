#!/usr/bin/env python

import random
import sys
from population_module.generation import generate_initial_pop
from population_module.reproduction import crossover, mutate
from random_module import rand
import copy

if __name__ == '__main__':
    seed = random.randrange(sys.maxsize)
    print(seed)
    print()
    rand.set_seed(5535402362016755500)
    # 6512001792335970851
    x = generate_initial_pop(10, 5)

    print(x[0])
    # print(x[1])

    print(mutate(x[0], 5))
    # print(mutate(x[1], 5))

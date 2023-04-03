from population_module.program import FunctionNode, NumberNode, ParamNode, Node
from typing import List, Dict, Tuple, Set
from random_module import rand
from random import randint # not using my rand module because it was more confusing when generating the numbers
from population_module.genetic_operators import crossover, mutate
from selection_module.selection import tournament
import math
import copy

# generate a single tree of the population
def generate_tree(current_depth: int, max_depth: int) -> Node:
    # if this is the first node we are generating make sure it is a function node
    if current_depth == 0:
        arg_count, func = rand.rand_func()
        node = FunctionNode(func, current_depth)

        node.add_children([generate_tree(current_depth + 1, max_depth) for _ in range(arg_count)])
        
        return node
    
    # chceking if allowed to generate function
    # deciding what to generate
    # 0 = func
    # 1 = param
    # 2 = number
    if current_depth < max_depth:
        gen_node = randint(0, 2)
    else:
        gen_node = randint(1, 2)

    if gen_node == 0:
        arg_count, func = rand.rand_func()
        node = FunctionNode(func, current_depth)

        node.add_children([generate_tree(current_depth + 1, max_depth) for _ in range(arg_count)])
    elif gen_node == 1:
        node = ParamNode(rand.rand_param(), current_depth)
    else:
        node = NumberNode(rand.rand_num(), current_depth)

    return node

# create initial population of certain size with certain depth
def generate_initial_pop(pop_size: int, max_depth: int) -> List[Node]:
    assert max_depth > 0, 'Max depth must be > 0'

    return [generate_tree(0, max_depth) for _ in range(pop_size)]

# create initial population of certain size with certain depth
def generate_initial_pop(pop_size: int, max_depth: int, gsim: Set[List[int]]) -> List[Node]:
    assert max_depth > 0, 'Max depth must be > 0'

    population = []
    while len(population) < pop_size:
        tree = generate_tree(0, max_depth)
        if tree not in gsim:
            population.append(tree)

    return population

# create the next population based of a previous generation
# takes in the amount which should be created from crossover, mutation and reproduction as well as tournament size
# crossover should not be halved as it is in the function
# can pass in the best node to ensure that it stays for next generation
def generate_next_populateion(prev_population: List[Node], test_data: List[Dict[str, float]], max_depth: int, cross_amount: int, mut_amount: int, repro_amount: int, tournament_size: int = 4) -> List[Node]:    
    # maybe change this to be mulithreaded based on pop_size

    # crossover
    population = [program for program in crossover(tournament(prev_population, test_data, tournament_size), tournament(prev_population, test_data, tournament_size), max_depth) for _ in range(math.trunc(cross_amount / 2))]

    # mutation
    population.extend(mutate(tournament(prev_population, test_data, tournament_size), max_depth) for _ in range(math.trunc(mut_amount)))

    # reproduction
    population.extend(copy.deepcopy(tournament(prev_population, test_data, tournament_size)) for _ in range(math.trunc(repro_amount)))

    # using reproduction to fill remaining spots
    population.extend(copy.deepcopy(tournament(prev_population, test_data, tournament_size)) for _ in range(len(prev_population) - len(population)))

    return population

# create the next population based of a previous generation
# takes in the amount which should be created from crossover, mutation and reproduction as well as tournament size
# crossover should not be halved as it is in the function
# can pass in the best node to ensure that it stays for next generation
def generate_next_populateion(prev_population_score: List[Tuple[float, Node]], max_depth: int, cross_amount: int, mut_amount: int, repro_amount: int, tournament_size: int = 4) -> List[Node]:    
    # maybe change this to be mulithreaded based on pop_size

    # crossover
    population = [program for program in crossover(tournament(prev_population_score, tournament_size), tournament(prev_population_score, tournament_size), max_depth) for _ in range(math.trunc(cross_amount / 2))]

    # mutation
    population.extend(mutate(tournament(prev_population_score, tournament_size), max_depth) for _ in range(math.trunc(mut_amount)))

    # reproduction
    population.extend(copy.deepcopy(tournament(prev_population_score, tournament_size)) for _ in range(math.trunc(repro_amount)))

    # using reproduction to fill remaining spots
    population.extend(copy.deepcopy(tournament(prev_population_score, tournament_size)) for _ in range(len(prev_population_score) - len(population)))

    return population
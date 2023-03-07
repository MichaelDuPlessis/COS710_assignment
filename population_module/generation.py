from population_module.program import Program, FunctionNode, NumberNode, ParamNode, Node
from typing import List
from random_module import rand
from random import randint # not using my rand module because it was more confusing when generating the numbers

# generate a single tree of the population
def _generate_tree(current_depth: int, max_depth: int) -> Node:
    # if this is the first node we are generating make sure it is a function node
    if current_depth == 0:
        arg_count, func = rand.rand_func()
        node = FunctionNode(func)

        node.add_children([_generate_tree(current_depth + 1, max_depth) for _ in range(arg_count)])
        
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
        node = FunctionNode(func)

        node.add_children([_generate_tree(current_depth + 1, max_depth) for _ in range(arg_count)])
    elif gen_node == 1:
        node = ParamNode(rand.rand_param())
    else:
        node = NumberNode(rand.rand_num()) 

    return node

# create initial population of certain size with certain depth
def generate_initial_pop(pop_size: int, max_depth: int) -> List[Program]:
    return [Program(_generate_tree(0, max_depth)) for _ in range(pop_size)]
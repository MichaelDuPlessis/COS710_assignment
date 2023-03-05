from population_module.program import Program, FunctionNode, NumberNode, ParamNode
from typing import List
from random_module import rand

# generate a single tree of the population
def _generate_tree(current_depth: int, max_depth: int) -> Program:
    # if this is the first node we are generating make sure it is a function node
    if current_depth == 0:
        arg_count, func = rand.rand_func()
        node = FunctionNode(func=func)

        node.add_children([_generate_tree(current_depth + 1, max_depth) for _ in range(arg_count)])
        
        return node
    
    # chceking if allowed to generate function
    if current_depth == max_depth:
        # deciding what to generate
        gen_func = rand.rand_bool()
        if gen_func:
            arg_count, func = rand.rand_func()
            node = FunctionNode(func=func)

            node.add_children([_generate_tree(current_depth + 1, max_depth) for _ in range(arg_count)])
            
            return node
    
    # whether a paramter or random number should be used
    gen_param = rand.rand_bool()
    if gen_param:
        return ParamNode(rand.rand_param())

    return NumberNode(rand.rand_num())    


# create initial population of certain size with certain depth
def generate_initial_pop(pop_size: int, max_depth: int) -> List[Program]:
    return [_generate_tree(0, max_depth) for _ in range(pop_size)]
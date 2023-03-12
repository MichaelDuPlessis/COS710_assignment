# this file is used for producing the next generation

from typing import Tuple
from population_module.program import Node, ParamNode, NumberNode
from population_module.generation import generate_tree
from random_module import rand
import random
import copy

# programs are cloned in crossover
def crossover(program1: Node, program2: Node) -> Tuple[Node, Node]:
    program1, program2 = copy.deepcopy(program1), copy.deepcopy(program2)

    return program1, program2

# programs are cloned in mutate
# max depth is used when generating subtrees
def mutate(program: Node, max_depth: int) -> Node:
    program = copy.deepcopy(program)

    chosen_node = program.choose_random_node()
    chosen_parent = chosen_node.parent

    # if parent is none than at root node so may as well generate a new tree
    if chosen_parent == None:
        return generate_tree(0, max_depth)
    
    # if we are at a node that is at the max depth than can only generate terminals
    if chosen_node.depth == max_depth:
        # deciding what to generate
        # 0 = param
        # 1 = number
        gen_node = random.randint(0, 1)

        if gen_node == 0:
            new_node = ParamNode(rand.rand_param(), chosen_node.depth)
        else:
            new_node = NumberNode(rand.rand_num(), chosen_node.depth)

        children = [child if child != chosen_node else new_node for child in chosen_parent.children]
        chosen_parent._children = children

        return program

    # else generate tree where subtree cannot go lower than max depth
    new_subtree = generate_tree(program.depth, max_depth)
    children = [child if child != chosen_node else new_subtree for child in chosen_parent.children]
    chosen_parent._children = children

    return program
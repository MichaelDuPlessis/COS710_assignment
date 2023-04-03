# this file is used for producing the next generation

from typing import Tuple, List, Set
from population_module.program import Node
from random_module import rand
import copy

# programs are cloned in crossover
def crossover(program1: Node, program2: Node, max_depth: int) -> Tuple[Node, Node]:
    program1, program2 = copy.deepcopy(program1), copy.deepcopy(program2)

    # does not make sense swapping the root of the node
    node1 = program1.choose_random_node()
    while node1.parent == None:
        node1 = program1.choose_random_node()

    node2 = program2.choose_random_node()
    while node2.parent == None:
        node2 = program2.choose_random_node()
    
    parent1 = node1.parent
    depth1 = node1.depth
    parent2 = node2.parent
    depth2 = node2.depth

    children = [child if child != node1 else node2 for child in parent1._children]
    parent1._children = children

    children = [child if child != node2 else node1 for child in parent2._children]
    parent2._children = children

    node1.parent = parent2
    node2.parent = parent1

    node1.update_depth(depth2, max_depth)
    node2.update_depth(depth1, max_depth)

    return program1, program2

# programs are cloned in mutate
# max depth is used when generating subtrees
def mutate(program: Node, max_depth: int) -> Node:
    from population_module.generation import generate_tree
    
    program = copy.deepcopy(program)

    chosen_node = program.choose_random_node()
    chosen_parent = chosen_node.parent

    # if parent is none than at root node so may as well generate a new tree
    if chosen_parent == None:
        return generate_tree(0, max_depth)
    
    # if we are at a node that is at the max depth than can only generate terminals
    if chosen_node.depth == max_depth:
        new_node = rand.rand_node([1, 2], chosen_node.depth)

        children = [child if child != chosen_node else new_node for child in chosen_parent._children]
        chosen_parent._children = children

        return program

    # else generate tree where subtree cannot go lower than max depth
    new_subtree = generate_tree(chosen_node.depth, max_depth)
    new_subtree.parent = chosen_parent
    children = [child if child != chosen_node else new_subtree for child in chosen_parent._children]

    chosen_parent._children = children

    return program

# programs are cloned in crossover
# this version is used in structure based gp
def crossover(program1: Node, program2: Node, max_depth: int, structure_depth: int) -> Tuple[Node, Node]:
    program1, program2 = copy.deepcopy(program1), copy.deepcopy(program2)

    # does not make sense swapping the root of the node
    node1 = program1.choose_random_node(structure_depth)
    while node1.parent == None:
        node1 = program1.choose_random_node(structure_depth)

    node2 = program2.choose_random_node(structure_depth)
    while node2.parent == None:
        node2 = program2.choose_random_node(structure_depth)
    
    parent1 = node1.parent
    depth1 = node1.depth
    parent2 = node2.parent
    depth2 = node2.depth

    children = [child if child != node1 else node2 for child in parent1._children]
    parent1._children = children

    children = [child if child != node2 else node1 for child in parent2._children]
    parent2._children = children

    node1.parent = parent2
    node2.parent = parent1

    node1.update_depth(depth2, max_depth)
    node2.update_depth(depth1, max_depth)

    return program1, program2

# programs are cloned in mutate
# max depth is used when generating subtrees
# this version is used in structure based gp
def mutate(program: Node, max_depth: int, structure_depth: int) -> Node:
    from population_module.generation import generate_tree
    
    program = copy.deepcopy(program)

    chosen_node = program.choose_random_node(structure_depth)
    chosen_parent = chosen_node.parent

    # if parent is none than at root node so may as well generate a new tree
    if chosen_parent == None:
        return generate_tree(0, max_depth)
    
    # if we are at a node that is at the max depth than can only generate terminals
    if chosen_node.depth == max_depth:
        new_node = rand.rand_node([1, 2], chosen_node.depth)

        children = [child if child != chosen_node else new_node for child in chosen_parent._children]
        chosen_parent._children = children

        return program

    # else generate tree where subtree cannot go lower than max depth
    new_subtree = generate_tree(chosen_node.depth, max_depth)
    new_subtree.parent = chosen_parent
    children = [child if child != chosen_node else new_subtree for child in chosen_parent._children]

    chosen_parent._children = children

    return program
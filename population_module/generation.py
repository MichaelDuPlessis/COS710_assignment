from organism import Organism

# generate a single tree of the population
def generate_tree(depth: int) -> Organism:
    pass

# create initial population of certain size with certain depth
def generate_initial_pop(pop_size: int, depth: int) -> list:
    return [generate_tree(depth) for _ in range(pop_size)]
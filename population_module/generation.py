from chromosome import Chromosome

def generate_tree(depth: int) -> Chromosome:
    pass

# create initial population

def generate_initial_pop(pop_size: int) -> list:
    return [generate_tree() for _ in range(pop_size)]
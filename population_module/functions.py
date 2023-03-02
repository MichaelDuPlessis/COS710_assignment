# this module contains all fucntions to be used in the genetic tree and contains a list of them

def add(x: float, y: float) -> float:
    return x + y

def multiply(x: float, y: float) -> float:
    return x * y

# the functions that are in use (num_args, func)
# this is because we need to know how many children nodes to generates
FUNCTIONS = [
    (2, add),
    (2, multiply),
]
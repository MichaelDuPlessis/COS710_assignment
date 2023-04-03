# this module contains all fucntions to be used in the genetic tree and contains a list of them

import math

class Add:
    def __call__(x: float, y: float) -> float:
        return x + y
    
class Mul:
    def __call__(x: float, y: float) -> float:
        return x * y
    
class Sub:
    def __call__(x: float, y: float) -> float:
        return x - y
    
class Div:
    def __call__(x: float, y: float) -> float:
        if y == 0:
            return 0
        return x / y

def add(x: float, y: float) -> float:
    return x + y

def mul(x: float, y: float) -> float:
    return x * y

def sub(x: float, y: float) -> float:
    return x - y

def div(x: float, y: float) -> float:
    if y == 0:
        return 0
    return x / y

def sqrt(x: float) -> float:
    if x < 0:
        return 0
    return math.sqrt(x)

# the functions that are in use (num_args, func)
# this is because we need to know how many children nodes to generates
FUNCTIONS = [
    (2, add),
    (2, mul),
    (2, sub),
    (2, div),
    # (1, sqrt),
]
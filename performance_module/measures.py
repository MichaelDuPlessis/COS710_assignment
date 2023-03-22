# this module is used to determine how could a tree is

import numpy as np
from typing import List, Dict, Tuple
from population_module.program import Node
from multiprocessing import Pool

from selection_module.fitness import RunProgram

def rmse(predictions: List[float], targets: List[float]) -> float:
    predictions = np.array(predictions)
    targets = np.array(targets)
    mse = np.mean((predictions - targets)**2)
    rmse = np.sqrt(mse)
    
    return rmse

def r_squared(predictions: List[float], targets: List[float]) -> float:
    predictions = np.array(predictions)
    targets = np.array(targets)
    ss_residual = np.sum((targets - predictions)**2)
    ss_total = np.sum((targets - np.mean(targets))**2)
    r2 = 1 - (ss_residual / ss_total)

    return r2


def median_absolute_error(predictions: List[float], targets: List[float]) -> float:
    predictions = np.array(predictions)
    targets = np.array(targets)
    mae = np.median(np.abs(predictions - targets))

    return mae

def mean_absolute_error(predictions: List[float], targets: List[float]) -> float:
    predictions = np.array(predictions)
    targets = np.array(targets)
    mae = np.mean(np.abs(predictions - targets))
    
    return mae

# runs all the performance measures for a given tree and data set
# frequires the tree/program and data set
def run_all_measures(program: Node, data: List[Dict[str, float]]) -> Tuple[float, float, float, float]:
    with Pool() as pool:
        # prediction_target = [(program.calculate(d), d['Duration']) for d in data]
        prediction_target = pool.map(RunProgram(program), data)
        predictions, targets = zip(*prediction_target)

        return rmse(predictions, targets), r_squared(predictions, targets), median_absolute_error(predictions, targets), mean_absolute_error(predictions, targets)
import numpy as np
from typing import List

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

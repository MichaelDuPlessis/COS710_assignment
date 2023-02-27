import numpy as np

def rmse(predictions, targets):
    predictions = np.array(predictions)
    targets = np.array(targets)
    mse = np.mean((predictions - targets)**2)
    rmse = np.sqrt(mse)
    
    return rmse
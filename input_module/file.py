from dask import dataframe as dd
from typing import Dict

def read_csv_parallel(filename: str) -> Dict[str, float]:
    df = dd.read_csv(filename)
    data = df.compute().to_dict('records')
    return data
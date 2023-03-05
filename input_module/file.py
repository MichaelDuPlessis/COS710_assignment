from dask import dataframe as dd
from typing import Dict, List

def read_csv_parallel(filename: str) -> List[Dict[str, float]]:
    df = dd.read_csv(filename)
    data = df.compute().to_dict('records')
    return data
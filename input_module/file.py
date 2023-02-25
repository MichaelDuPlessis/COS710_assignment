from dask import dataframe as dd

def read_csv_parallel(filename):
    df = dd.read_csv(filename)
    data = df.compute().to_dict('records')
    return data
import input_module.file as im
import time

if __name__ == '__main__':
    start = time.time()
    im.read_csv_parallel('./data/For_modeling.csv')
    end = time.time()
    print("Read csv with dask: ",(end-start),"sec")
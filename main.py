import input_module.file as im
import time
from performance_module.measures import rmse 

if __name__ == '__main__':
    # start = time.time()
    # im.read_csv_parallel('./data/For_modeling.csv')
    # end = time.time()
    # print("Read csv with dask: ",(end-start),"sec")

    predictions = [1, 2, 3, 4, 5]
    targets = [1.5, 2.5, 3.5, 4.5, 5.5]
    print(rmse(predictions, targets))  # Output: 0.7071067811865476

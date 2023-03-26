# About
This is an genetic program to calculate the duration of a bike trip in Seoul according to a number of paramters.

The dataset reading as well as fitness calculations can be done in parallel.

# Structure
- Requirments.txt holds all the package requirments to run the program, use "pip install -r requirements.txt"
- The data folder holds the data set which can be found at https://data.mendeley.com/datasets/gtfh9z865f/1. The data set is not pushed to github as it is too large
- The runs folder holds all the saved runs as well as aggregate information on runs if one exists
- All other folders contain source code

# Run Data
Run data is saved in runs as a json file. Each set of runs get their own folder which is named with a timestamp being the current date and time.

If there is aggregate information about all the runs it is saved in a json file in the runs directory and has the same name as the folder.

## Structure of n.json file
- pop_size = size of population
- max_depth = maximum allowed depth of tree
- max_generations = maximum number of generations that a run can take
- desired_fitness = the desired bound to achieve
- run = the run number in a set of runs
- data_set_size = json object with size of training and testing data
- tournament_size = the size of a tournament used in tournament selection
- weights = and array representing the weight of crossover, mutation and reproduction respectively
- seed = the seed of the run
- desired_found = whether the bound was met before the max_generations was hit
generations = an array containing a json object of the generation number, the best score achieved in that generation and a postfix representation of the tree that achieved that fitness
- time = the time in seconds that the run took not including calculating the performance measures
- best = the best score achieved in the end
- best_tree = a postfix representation of the tree that achieved the best fitness
- generations_completed = the number of generations completed before the bound was achieved or max_generations was hit
- measures = an object containing the preformance measures for both the training and testing set for RMSE, R squared, MAE and MedAE

# Usage
The following paramters can be specified as command line inputs:
- The number of generations.
- The number used in the tournament selection.
- The population size.
- The bound (lower is better).
- The seed.
- The number of runs to perform (each with a different seed unless seed is specified).
- The maximum depth of every tree.
- The weights to be used as a comma seperated list e.g. 0.7,0.2,0.1 where the order is crossover,mutation,reproduction.
- Whether you want to save the run or not.
- The path to the data set
- The size of the training and testing set
- The number of cores to be used

Type "python main.py -h" for help and all paramters have default values
# About
This is an genetic program to calculate the duration of a bike trip in Seoul according to a number of paramters.

The dataset reading as well as fitness calculations are done in parallel.

# Structure
- Requirments.txt holds all the package requirments to run the program, use "pip install -r requirements.txt"
- The data folder holds the data set which can be found at . The data set is not pushed to github as it is too large
- The runs folder holds all the saved runs
- All other folders contain source code 

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

Type python main.py -h for help and all paramters have default values
**Job Shop Scheduling Problem (JSSP) Optimization Using Genetic Algorithm and Tabu Search**

This repository contains an implementation of the Job Shop Scheduling Problem (JSSP) solution using Genetic Algorithm (GA) with the option of further refining the solution using Tabu Search. The goal is to optimize the distribution of tasks across machines to minimize the total computational time (makespan).

**Project Overview**

**The project consists of the following major components:**
Genetic Algorithm (GA): Used to find the optimal task scheduling that minimizes makespan.
Tabu Search: A local search technique used to refine the solution obtained by the GA.
Multiple Datasets: The code is tested on various datasets representing different problem sizes (3-5 machines, ~10 machines, and 15+ machines).
Visualizations: Includes Gantt charts to visualize task scheduling and fitness evolution over generations.

**Files in this Repository:**
JSSP.py: Main script for running the genetic algorithm and experimenting with different parameter combinations.
tabu_search.py: Contains the implementation of the Tabu Search method used to refine the solution.
chromosome.py: Contains functions related to chromosome representation and population initialization.
operators.py: Implements crossover and mutation techniques used in the GA.
elitism.py: Contains the elitism operator to preserve the best individuals in the population.
experiment_results.csv: Stores the results from the experiments with various parameter combinations for each dataset.
Gantt Chart and Fitness Evolution: Graphs and plots of the results, including the Gantt chart visualization for task scheduling and the fitness evolution for each algorithm step.

**Requirements:**
Python 3.8 or higher
deap library (for genetic algorithms)
matplotlib (for plotting graphs)
numpy (for numerical operations)
You can install the required dependencies using:

bash
Copy
pip install deap matplotlib numpy
How to Run
Dataset: Place the datasets in the directory where the script is located or modify the dataset paths in the JSSP.py file.
Run the Script: Run the main script JSSP.py to start the genetic algorithm and optionally refine the solution using Tabu Search.

**Example command:**
bash
Copy
python JSSP.py
This will prompt you to select a dataset and experiment with different parameter combinations.
View Results: The results of the experiments will be saved in a CSV file (experiment_results.csv), and fitness evolution plots will be generated as images.

**Datasets:**
The datasets used in this project represent different problem sizes:
fisher_thompson_6x6: A small dataset with 6 jobs and 6 machines.
fisher_thompson_10x10: A medium-sized dataset with 10 jobs and 10 machines.
adams_balas_and_zawack_15x20: A large dataset with 15 jobs and 20 machines.

**Results:**
The results are saved in experiment_results.csv and contain the following columns:
Population Size: The number of individuals in each generation.
Crossover Probability: The probability of crossover between two parents.
Mutation Probability: The probability of mutation for an individual.
Generations: The number of generations for which the algorithm runs.
Makespan: The total computational time (fitness of the solution).
Runtime: The time taken to run the experiment.

**Example Results Format:**
Population Size	Crossover Probability	Mutation Probability	Generations	Makespan	Runtime
50	0.6	0.1	100	52.0	0.64s
50	0.7	0.2	100	55.0	1.24s

**Key Observations:**
**GA Performance:** The genetic algorithm was able to find solutions with significantly reduced makespan over generations.
**Tabu Search:** Applying Tabu Search showed improvement in the makespan for most experiments, especially with larger datasets.
**Parameter Tuning:** The optimal parameter combination varied depending on the dataset, but larger population sizes generally led to better solutions.

**Conclusion:** This project demonstrates the application of a genetic algorithm for solving the Job Shop Scheduling Problem and uses Tabu Search for solution refinement. The method was evaluated on datasets of varying sizes, and the results show that the GA performs well in finding optimized schedules with the potential for further improvement using Tabu Search.

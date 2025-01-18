import random
from deap import base, creator, tools
import matplotlib.pyplot as plt
import time
import os
import csv
import chromosome  # Import the chromosome module
from operators import uniform_crossover, single_point_crossover, swap_mutation, scramble_mutation
from elitism import apply_elitism
from tabu_search import tabu_search  # Importing Tabu Search


# Define Fitness and Individual classes globally to prevent re-creation
creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
creator.create("Individual", list, fitness=creator.FitnessMin)

def plot_gantt_chart(task_schedule, num_machines):
    """
    Plot the Gantt chart for the schedule of tasks.

    Parameters:
    - task_schedule: A list of tuples (job_id, task_id, machine, start_time, end_time).
    - num_machines: The number of machines in the system.
    """
    fig, ax = plt.subplots(figsize=(10, 6))
    colors = plt.cm.tab20.colors  # A set of colors for jobs
    for task in task_schedule:
        job_id, task_id, machine, start_time, end_time = task
        ax.barh(machine, end_time - start_time, left=start_time, color=colors[job_id % len(colors)], edgecolor="black")
        ax.text((start_time + end_time) / 2, machine, f"J{job_id}-T{task_id}", ha='center', va='center', fontsize=8)

    ax.set_xlabel("Time")
    ax.set_ylabel("Machine")
    ax.set_title("Task Schedule (Gantt Chart)")
    ax.invert_yaxis()
    plt.show()

# Parse the dataset
def parse_dataset(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    num_jobs, num_machines = map(int, lines[0].split())
    jobs_data = []

    for line in lines[1:]:
        try:
            data = list(map(int, line.split()))
            job = []
            for i in range(0, len(data), 2):
                machine = data[i]
                duration = data[i + 1]
                job.append((machine, duration))
            jobs_data.append(job)
        except ValueError:
            continue

    return num_jobs, num_machines, jobs_data

# Fitness evaluation function
def evaluate(individual, jobs_data):
    job_end_times = {job_id: 0 for job_id in range(len(jobs_data))}
    machine_end_times = {}
    current_time = 0
    task_schedule = []

    for job_id, task_id in individual:
        machine, duration = jobs_data[job_id][task_id]
        start_time = max(job_end_times[job_id], machine_end_times.get(machine, 0))
        end_time = start_time + duration
        job_end_times[job_id] = end_time
        machine_end_times[machine] = end_time
        task_schedule.append((job_id, task_id, machine, start_time, end_time))
        current_time = max(current_time, end_time)

    return current_time, task_schedule

# Custom crossover function
def uniform_crossover(parent1, parent2):
    size = len(parent1)
    child1 = []
    child2 = []
    for i in range(size):
        if random.random() < 0.5:
            child1.append(parent1[i])
            child2.append(parent2[i])
        else:
            child1.append(parent2[i])
            child2.append(parent1[i])
    
    return child1, child2

# Mutation function
def swap_mutation(individual):
    size = len(individual)
    idx1, idx2 = random.sample(range(size), 2)
    individual[idx1], individual[idx2] = individual[idx2], individual[idx1]
    return individual

# Tournament selection function
def tournament_selection(population, tournament_size=3):
    selected = []
    for _ in range(len(population)):
        tournament = random.sample(population, tournament_size)
        winner = min(tournament, key=lambda ind: ind.fitness.values[0])
        selected.append(winner)
    return selected

# Run GA with specific parameters
def run_ga(file_path, population_size, cxpb, mutpb, ngen, elitism_size=1):
    num_jobs, num_machines, jobs_data = parse_dataset(file_path)

    # Define tasks
    tasks = [(job_id, task_id) for job_id, job in enumerate(jobs_data) for task_id in range(len(job))]
    
    # Initialize population and evaluate fitness
    population = chromosome.initialize_population(population_size, tasks, lambda ind: evaluate(ind, jobs_data))

    # Initialize the toolbox with the appropriate GA functions
    toolbox = base.Toolbox()
    toolbox.register("individual", tools.initIterate, creator.Individual, lambda: random.choice(population))
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)

    toolbox.register("evaluate", lambda ind: evaluate(ind, jobs_data)[0])  # Fitness function (makespan)
    
    # Randomly choose between two crossover methods
    toolbox.register("mate", random.choice([uniform_crossover, single_point_crossover]))
    toolbox.register("mutate", random.choice([swap_mutation, scramble_mutation]))  # Randomly choose mutation method
    toolbox.register("select", tools.selTournament, tournsize=3)  # Selection function

    fitness_evolution = []

    # Main GA loop
    for gen in range(ngen):
        # Apply elitism: preserve the best individuals
        elites = apply_elitism(population, elitism_size)

        # Create offspring by selecting the rest of the population
        offspring = toolbox.select(population, len(population) - elitism_size)
        offspring = list(map(toolbox.clone, offspring))

        for child1, child2 in zip(offspring[::2], offspring[1::2]):
            if random.random() < cxpb:
                toolbox.mate(child1, child2)
                del child1.fitness.values
                del child2.fitness.values

        for mutant in offspring:
            if random.random() < mutpb:
                toolbox.mutate(mutant)
                del mutant.fitness.values

        # Evaluate the fitness of the offspring
        invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
        fitnesses = map(toolbox.evaluate, invalid_ind)
        for ind, fit in zip(invalid_ind, fitnesses):
            ind.fitness.values = (fit,)  # Ensure fitness is a tuple

        # The next generation is the combination of elites and offspring
        population[:] = elites + offspring
        fitness_evolution.append(min(ind.fitness.values[0] for ind in population))

    best_ind = tools.selBest(population, 1)[0]
    best_makespan, best_task_schedule = evaluate(best_ind, jobs_data)

    # Add Gantt Chart Visualization for this experiment
    plot_gantt_chart(best_task_schedule, num_machines)

    # Now applying Tabu Search to refine the best solution
    print("Applying Tabu Search to refine the solution...")
    refined_solution, refined_makespan = tabu_search(best_task_schedule, jobs_data, evaluate)
    print(f"Refined Makespan after Tabu Search: {refined_makespan}")
    
    return fitness_evolution, best_makespan, refined_solution, refined_makespan

def save_results_to_csv(results, filename="experiment_results.csv"):
    # Specify the full path where you want to save the file
    folder_path = r"C:\Users\Arif Bhuiyan\Desktop\google\Result"
    
    # Create the folder if it doesn't exist
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    file_path = os.path.join(folder_path, filename)
    
    # Open the CSV file and write the results
    with open(file_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        # Write the header row
        writer.writerow(["Population Size", "Crossover Probability", "Mutation Probability", "Generations", "Makespan", "Refined Makespan", "Runtime"])
        
        # Write the results of each experiment
        for result in results:
            writer.writerow(result)

# Main function for parameter tuning and visualization
def main():
    datasets = {
        "fisher_thompson_6x6": r"C:\Users\Arif Bhuiyan\Desktop\google\fisher_thompson_6x6.txt",
        "fisher_thompson_10x10": r"C:\Users\Arif Bhuiyan\Desktop\google\fisher_thompson_10x10.txt",
        "adams_balas_and_zawack_15x20": r"C:\Users\Arif Bhuiyan\Desktop\google\adams_balas_and_zawack_15x20.txt",
    }

    # Select dataset
    dataset_name = input(f"Select dataset {list(datasets.keys())}: ")
    if dataset_name not in datasets:
        print("Invalid dataset name!")
        return

    file_path = datasets[dataset_name]

    # Parameter combinations
    parameters = [
        {"population_size": 50, "cxpb": 0.6, "mutpb": 0.1, "ngen": 100},
        {"population_size": 50, "cxpb": 0.7, "mutpb": 0.2, "ngen": 100},
        {"population_size": 100, "cxpb": 0.8, "mutpb": 0.1, "ngen": 100},
        {"population_size": 100, "cxpb": 0.7, "mutpb": 0.2, "ngen": 150},
        {"population_size": 200, "cxpb": 0.7, "mutpb": 0.2, "ngen": 100},
        {"population_size": 200, "cxpb": 0.8, "mutpb": 0.3, "ngen": 150},
    ]

    # Store results
    results = []
    all_fitness_evolution = []  # List to store fitness evolution data for each experiment

    # Loop through each set of parameters and run the experiment
    for i, param in enumerate(parameters):
        print(f"Running experiment {i+1} with parameters: {param}")
        start_time = time.time()
        fitness_evolution, makespan, refined_solution, refined_makespan = run_ga(file_path, **param)
        runtime = time.time() - start_time

        # Store the results
        results.append([param["population_size"], param["cxpb"], param["mutpb"], param["ngen"], makespan, refined_makespan, runtime])
        all_fitness_evolution.append(fitness_evolution)  # Append fitness evolution data for this experiment

        print(f"Experiment {i+1} results: Makespan = {makespan}, Refined Makespan = {refined_makespan}, Runtime = {runtime:.2f}s")

    # Save the results to CSV
    save_results_to_csv(results)

    # Plot combined fitness evolution for all experiments
    plt.figure(figsize=(10, 6))
    for i, fitness_evolution in enumerate(all_fitness_evolution):
        plt.plot(fitness_evolution, label=f"Experiment {i+1}")
    plt.xlabel("Generation")
    plt.ylabel("Best Fitness (Makespan)")
    plt.title(f"Combined Fitness Evolution for {dataset_name}")
    plt.legend()
    plt.show()

if __name__ == "__main__":
    main()

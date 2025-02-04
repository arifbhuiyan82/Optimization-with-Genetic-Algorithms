import random
from deap import base, creator, tools
from copy import deepcopy
import matplotlib.pyplot as plt
import time
import os
import csv
from chromosome import initialize_population
from crossover import single_point_crossover, uniform_crossover
from mutation import scramble_mutation
from elitism import apply_elitism
from tabu_search import tabu_search

# Check if 'FitnessMin' is already defined before creating it
if not hasattr(creator, "FitnessMin"):
    creator.create("FitnessMin", base.Fitness, weights=(-1.0,))

# Check if 'Individual' is already defined before creating it
if not hasattr(creator, "Individual"):
    creator.create("Individual", list, fitness=creator.FitnessMin)

# Parse dataset function
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
    task_schedule = []
    current_time = 0

    for job_id, task_id in individual:
        machine, duration = jobs_data[job_id][task_id]
        start_time = max(job_end_times[job_id], machine_end_times.get(machine, 0))
        end_time = start_time + duration
        job_end_times[job_id] = end_time
        machine_end_times[machine] = end_time
        task_schedule.append((job_id, task_id, machine, start_time, end_time))
        current_time = max(current_time, end_time)

    return current_time, task_schedule

# Define Gantt Chart plotting function
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

# Run GA with specific parameters
def run_ga(file_path, population_size, cxpb, mutpb, ngen, elitism_size=1):
    # Parse dataset
    num_jobs, num_machines, jobs_data = parse_dataset(file_path)

    # Define tasks (flatten jobs into a single list of tasks)
    tasks = [(job_id, task_id) for job_id, job in enumerate(jobs_data) for task_id in range(len(job))]

    # Initialize population
    population = initialize_population(population_size, tasks, lambda ind: evaluate(ind, jobs_data))


    # Initialize DEAP toolbox
    toolbox = base.Toolbox()
    toolbox.register("individual", tools.initIterate, creator.Individual, lambda: random.choice(population))
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)
    toolbox.register("evaluate", lambda ind: evaluate(ind, jobs_data)[0])  # Fitness function
    toolbox.register("mate", random.choice([single_point_crossover, uniform_crossover]))
    toolbox.register("mutate", lambda ind: scramble_mutation(ind, jobs_data))
    toolbox.register("select", tools.selTournament, tournsize=3)

    fitness_evolution = []

    # Main GA loop
    for gen in range(ngen):
        print(f"Generation {gen+1}/{ngen}")

        # Apply elitism
        elites = apply_elitism(population, elitism_size)
        if not elites:
            print("⚠️ No valid elites found! Re-evaluating population...")
        elites = tools.selBest(population, elitism_size)  # Use best available solutions


        # Select offspring and clone
        offspring = toolbox.select(population, len(population) - elitism_size)
        offspring = list(map(toolbox.clone, offspring))

        # Apply crossover
        for child1, child2 in zip(offspring[::2], offspring[1::2]):
            if random.random() < cxpb:
                toolbox.mate(child1, child2)
                del child1.fitness.values
                del child2.fitness.values

        # Apply mutation
        for mutant in offspring:
            if random.random() < mutpb:
                toolbox.mutate(mutant)
                del mutant.fitness.values

        # Evaluate invalid individuals
        invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
        fitnesses = map(toolbox.evaluate, invalid_ind)
        for ind, fit in zip(invalid_ind, fitnesses):
            ind.fitness.values = (fit,)

        # Replace population with elites and offspring
        population[:] = elites + offspring

        # Track best fitness value for this generation
        fitness_evolution.append(min(ind.fitness.values[0] for ind in population))

    # Extract the best individual
    best_ind = tools.selBest(population, 1)[0]
    best_makespan, best_task_schedule = evaluate(best_ind, jobs_data)

    # **Check if task order is respected for each job**
    print("\nValidating Task Order for Each Job:")
    job_task_order = {}

    for task in best_task_schedule:
        job_id, task_id, machine, start_time, end_time = task
        if job_id not in job_task_order:
            job_task_order[job_id] = []
        job_task_order[job_id].append((task_id, start_time))

    # Sort and check order violations
    for job_id, tasks in job_task_order.items():
        sorted_tasks = sorted(tasks, key=lambda x: x[1])  # Sort by start time
        sorted_task_ids = [t[0] for t in sorted_tasks]

        if sorted_task_ids != sorted(sorted_task_ids):  # Check if task order is sequential
            print(f"⚠️ Task order violation in Job {job_id}: {sorted_task_ids}")
        else:
            print(f"✅ Job {job_id} task order is correct: {sorted_task_ids}")

    # Add Gantt Chart Visualization for this experiment
    plot_gantt_chart(best_task_schedule, num_machines)

    # Now applying Tabu Search to refine the best solution
    print("Applying Tabu Search to refine the solution...")

    # Extract only job-task pairs from the best solution
    best_solution_tabu = [(job_id, task_id) for job_id, task_id, _, _, _ in best_task_schedule]

    # Run Tabu Search with a deepcopy of best_solution_tabu
    refined_solution, refined_makespan = tabu_search(best_solution_tabu, jobs_data, evaluate)

    # Re-evaluate refined solution
    _, refined_task_schedule = evaluate(refined_solution, jobs_data)

    print(f"Refined Makespan after Tabu Search: {refined_makespan}")

    # Plot Gantt chart for Tabu Search refined solution
    print("Plotting refined schedule (Tabu Search)...")
    plot_gantt_chart(refined_task_schedule, num_machines)

    return fitness_evolution, refined_makespan, refined_task_schedule


def save_results_to_csv(results, filename="experiment_results.csv"):
    # Specify the full path where you want to save the file
    folder_path = r"C:\Users\Arif Bhuiyan\Desktop\A2\Result"
    
    # Create the folder if it doesn't exist
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    file_path = os.path.join(folder_path, filename)
    
    # Open the CSV file and write the results
    with open(file_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        # Write the header row
        writer.writerow(["Population Size", "Crossover Probability", "Mutation Probability", "Generations", "Makespan", "Runtime"])
        
        # Write the results of each experiment
        for result in results:
            writer.writerow(result)
            
def main():
    datasets = {
        "fisher_thompson_6x6": r"C:\Users\Arif Bhuiyan\Desktop\A2\fisher_thompson_6x6.txt",
        "fisher_thompson_10x10": r"C:\Users\Arif Bhuiyan\Desktop\A2\fisher_thompson_10x10.txt",
        "adams_balas_and_zawack_15x20": r"C:\Users\Arif Bhuiyan\Desktop\A2\adams_balas_and_zawack_15x20.txt",
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
    all_fitness_evolution = []  # Store fitness evolution data for all experiments

    # Run each experiment
    for i, param in enumerate(parameters):
        print(f"Running Experiment {i+1} with parameters: {param}")
        start_time = time.time()
        fitness_evolution, makespan, best_task_schedule = run_ga(file_path, **param)
        runtime = time.time() - start_time

        # Store results
        results.append([param["population_size"], param["cxpb"], param["mutpb"], param["ngen"], makespan, runtime])
        all_fitness_evolution.append(fitness_evolution)

        print(f"Experiment {i+1}: Makespan = {makespan}, Runtime = {runtime:.2f} seconds")

    # Save results to CSV
    save_results_to_csv(results)

    # Plot combined fitness evolution for all experiments
    plt.figure(figsize=(10, 6))
    for i, fitness_evolution in enumerate(all_fitness_evolution):
        plt.plot(
            fitness_evolution,
            label=f"Experiment {i+1}",
            linestyle='-',  # Solid line
            marker='o',     # Circle markers
            markersize=4    # Marker size
        )

    # Add gridlines
    plt.grid(visible=True, linestyle='--', alpha=0.7)

    # Add labels and title
    plt.xlabel("Generation", fontsize=12)
    plt.ylabel("Best Fitness (Makespan)", fontsize=12)
    plt.title(f"Combined Fitness Evolution for {dataset_name}", fontsize=14)

    # Highlight best fitness for each experiment
    for i, fitness_evolution in enumerate(all_fitness_evolution):
        best_fitness = min(fitness_evolution)
        plt.annotate(
            f"{best_fitness:.2f}",
            xy=(len(fitness_evolution) - 1, best_fitness),
            xytext=(len(fitness_evolution) - 1, best_fitness + 5),
            arrowprops=dict(arrowstyle="->", color='gray', lw=1),
            fontsize=10,
            color='blue'
        )

    # Add legend
    plt.legend(fontsize=10)

    # Save the plot as an image
    output_folder = r"C:\Users\Arif Bhuiyan\Desktop\A2\Result"
    os.makedirs(output_folder, exist_ok=True)
    plot_path = os.path.join(output_folder, f"fitness_evolution_{dataset_name}.png")
    plt.savefig(plot_path, dpi=300, bbox_inches='tight')

    # Show the plot
    plt.show()


if __name__ == "__main__":
    main()


    



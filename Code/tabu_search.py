import random
import numpy as np
from copy import deepcopy
from JSSP import evaluate

def tabu_search(current_solution, jobs_data, evaluate, max_iter=100, tabu_tenure=5, neighborhood_size=10):
    # Evaluate the current solution
    best_solution = deepcopy(current_solution)  # Best solution found
    best_solution = [(task[0], task[1]) for task in best_solution]  # Ensure job-task pair structure
    best_makespan, _ = evaluate(best_solution, jobs_data)

    # Tabu list (used to store recent moves)
    tabu_list = []

    # **Early Stopping Variables**
    stagnation_limit = 10  # Stop if no improvement in 10 iterations
    stagnation_counter = 0  # Counts iterations with no improvement

    # Tabu Search main loop
    for iteration in range(max_iter):
        neighborhood = generate_neighborhood(current_solution, neighborhood_size, jobs_data)  # Generate neighborhood
        best_neighbor = None
        best_neighbor_makespan = float('inf')

        for neighbor in neighborhood:
            neighbor = [(task[0], task[1]) for task in neighbor]  # Ensure job-task pair structure
            neighbor_makespan, _ = evaluate(neighbor, jobs_data)

            # If the neighbor is not in the Tabu list or it improves the solution, consider it
            if neighbor_makespan < best_makespan or (neighbor not in tabu_list):  # Aspiration criteria
                if neighbor_makespan < best_neighbor_makespan:
                    best_neighbor = neighbor
                    best_neighbor_makespan = neighbor_makespan

        # **Ensure we do not update with an invalid solution**
        if best_neighbor is not None:
            current_solution = best_neighbor
            if best_neighbor_makespan < best_makespan:
                best_solution = best_neighbor
                best_makespan = best_neighbor_makespan
                stagnation_counter = 0  # **Reset stagnation counter on improvement**
            else:
                stagnation_counter += 1  # **Increase counter if no improvement**
        else:
            print(f"⚠️ No valid neighbor found at iteration {iteration + 1}, stopping early.")
            break  # **Avoid infinite loop**

        # Add the current solution to the tabu list with a tenure (to avoid revisiting)
        tabu_list.append(current_solution)
        if len(tabu_list) > tabu_tenure:
            tabu_list.pop(0)  # Remove the oldest tabu if the list exceeds the tenure

        # **Early stopping condition**
        if stagnation_counter >= stagnation_limit:
            print(f"⚠️ Early stopping at iteration {iteration + 1} due to no improvement.")
            break

        # Optionally: Print the iteration and current best makespan
        print(f"Iteration {iteration + 1}/{max_iter}: Best Makespan = {best_makespan}")

    # Return the best solution found
    return best_solution, best_makespan

def generate_neighborhood(solution, neighborhood_size, jobs_data):
    """
    Generate a neighborhood by swapping tasks while maintaining task precedence.
    Ensures at least one valid neighbor is generated.
    """
    neighborhood = []

    while len(neighborhood) < max(1, neighborhood_size):  # Ensure at least one neighbor
        neighbor = deepcopy(solution)
        idx1, idx2 = random.sample(range(len(solution)), 2)

        job1, task1 = neighbor[idx1]
        job2, task2 = neighbor[idx2]

        # Ensure task precedence is maintained
        if (task1 < task2 and jobs_data[job1][task1][0] == jobs_data[job2][task2][0]) or (job1 != job2):
            neighbor[idx1], neighbor[idx2] = neighbor[idx2], neighbor[idx1]  # Swap only valid tasks
            neighborhood.append(neighbor)

    return neighborhood

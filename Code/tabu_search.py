import random
import numpy as np
from copy import deepcopy
from JSSP import evaluate

# In the tabu_search function
def tabu_search(current_solution, jobs_data, evaluate, max_iter=100, tabu_tenure=5, neighborhood_size=10):
    # Evaluate the current solution
    best_solution = deepcopy(current_solution)  # Best solution found
    best_solution = [(task[0], task[1]) for task in best_solution]  # Ensure job-task pair structure
    best_makespan, _ = evaluate(best_solution, jobs_data)
    
    # Tabu list (used to store recent moves)
    tabu_list = []

    # Tabu Search main loop
    for iteration in range(max_iter):
        neighborhood = generate_neighborhood(current_solution, neighborhood_size)  # Generate neighborhood
        best_neighbor = None
        best_neighbor_makespan = float('inf')

        for neighbor in neighborhood:
            neighbor = [(task[0], task[1]) for task in neighbor]  # Ensure job-task pair structure
            neighbor_makespan, _ = evaluate(neighbor, jobs_data)
            
            # If the neighbor is not in the Tabu list or it improves the solution, consider it
            if neighbor not in tabu_list or neighbor_makespan < best_makespan:
                if neighbor_makespan < best_neighbor_makespan:
                    best_neighbor = neighbor
                    best_neighbor_makespan = neighbor_makespan

        # Update the current solution with the best neighbor found
        if best_neighbor:
            current_solution = best_neighbor
            if best_neighbor_makespan < best_makespan:
                best_solution = best_neighbor
                best_makespan = best_neighbor_makespan

        # Add the current solution to the tabu list with a tenure (to avoid revisiting)
        tabu_list.append(current_solution)
        if len(tabu_list) > tabu_tenure:
            tabu_list.pop(0)  # Remove the oldest tabu if the list exceeds the tenure
        
        # Optionally: Print the iteration and current best makespan
        print(f"Iteration {iteration + 1}/{max_iter}: Best Makespan = {best_makespan}")

    # Return the best solution found
    return best_solution, best_makespan

def generate_neighborhood(solution, neighborhood_size):
    """
    Generate a neighborhood by randomly mutating the current solution.
    In this case, we perform random swaps in the solution.
    """
    neighborhood = []
    
    for _ in range(neighborhood_size):
        neighbor = deepcopy(solution)
        idx1, idx2 = random.sample(range(len(solution)), 2)
        neighbor[idx1], neighbor[idx2] = neighbor[idx2], neighbor[idx1]  # Swap two tasks
        neighborhood.append(neighbor)
    
    return neighborhood


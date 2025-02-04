def apply_elitism(population, elitism_size):
    """
    Preserve the best individuals (elites) from the current population to the next generation.
    Ensures that only valid schedules are preserved.

    Parameters:
    - population (list): The current population (list of individuals).
    - elitism_size (int): The number of elites to preserve.

    Returns:
    - elites (list): The best `elitism_size` valid individuals.
    """
    # Sort population by fitness (ascending order)
    population.sort(key=lambda ind: ind.fitness.values[0])

    # Filter only valid individuals before selecting elites
    valid_elites = [ind for ind in population if validate_task_order(ind)]

    # Select the top `elitism_size` valid individuals
    elites = valid_elites[:elitism_size] if len(valid_elites) >= elitism_size else valid_elites

    return elites

def validate_task_order(individual):
    """
    Check if an individual's task order is valid (task precedence is maintained).
    Returns True if valid, False if order is incorrect.
    """
    job_task_order = {}

    for job_id, task_id in individual:
        if job_id not in job_task_order:
            job_task_order[job_id] = []
        job_task_order[job_id].append(task_id)

    # Check if tasks are in the correct order
    for job_id, task_list in job_task_order.items():
        if task_list != sorted(task_list):  # Should be in increasing order
            return False

    return True

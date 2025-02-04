import random
from deap import creator

def create_chromosome(tasks):
    """
    Create a chromosome while maintaining task precedence within jobs.
    Jobs are shuffled, but tasks within a job remain in order.
    """
    job_tasks = {}  # Group tasks by job
    for job_id, task_id in tasks:
        if job_id not in job_tasks:
            job_tasks[job_id] = []
        job_tasks[job_id].append(task_id)

    # Shuffle jobs but keep tasks in order
    shuffled_jobs = list(job_tasks.keys())
    random.shuffle(shuffled_jobs)  # Shuffle job order
    
    # Construct a valid chromosome
    chromosome = []
    for job_id in shuffled_jobs:
        for task_id in job_tasks[job_id]:  # Maintain task order
            chromosome.append((job_id, task_id))

    return chromosome

def initialize_population(population_size, tasks, evaluate):
    """
    Initialize a population while ensuring task precedence is maintained.
    """
    population = []
    for _ in range(population_size):
        chromosome = create_chromosome(tasks)  # Uses updated function
        individual = creator.Individual(chromosome)
        
        # Evaluate the fitness of the individual
        individual.fitness.values = (evaluate(individual)[0],)  # Ensure fitness is a tuple

        population.append(individual)
    return population

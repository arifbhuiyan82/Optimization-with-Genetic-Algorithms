import random
from deap import creator

def create_chromosome(tasks):
    """
    Create a chromosome by randomly shuffling the order of tasks.
    Each task is represented by a tuple (job_id, task_id).
    The tasks are randomly ordered to represent a schedule.
    """
    return random.sample(tasks, len(tasks))

def initialize_population(population_size, tasks, evaluate):
    """
    Initialize a population of chromosomes (solutions) randomly.
    Each chromosome is a list of job-task pairs.
    After initialization, evaluate the fitness of each individual.
    """
    population = []
    for _ in range(population_size):
        chromosome = create_chromosome(tasks)
        individual = creator.Individual(chromosome)
        
        # Evaluate the fitness of the individual
        individual.fitness.values = evaluate(individual)[0],  # Ensure fitness is a tuple

        population.append(individual)
    return population

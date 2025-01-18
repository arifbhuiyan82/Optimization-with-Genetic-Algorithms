import random

# Crossover Techniques
def single_point_crossover(parent1, parent2):
    """
    Perform single-point crossover between two parents.
    """
    size = len(parent1)
    cxpoint = random.randint(1, size - 1)  # Random crossover point
    child1 = parent1[:cxpoint] + parent2[cxpoint:]
    child2 = parent2[:cxpoint] + parent1[cxpoint:]
    return child1, child2

def uniform_crossover(parent1, parent2):
    """
    Perform uniform crossover between two parents.
    """
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

# Mutation Techniques
def swap_mutation(individual):
    """
    Perform swap mutation by randomly swapping two tasks in the chromosome.
    """
    size = len(individual)
    idx1, idx2 = random.sample(range(size), 2)
    individual[idx1], individual[idx2] = individual[idx2], individual[idx1]
    return individual

def scramble_mutation(individual):
    """
    Perform scramble mutation by randomly scrambling a subset of tasks in the chromosome.
    """
    size = len(individual)
    start, end = sorted(random.sample(range(size), 2))  # Random segment to scramble
    individual[start:end] = random.sample(individual[start:end], len(individual[start:end]))
    return individual

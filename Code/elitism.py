def apply_elitism(population, elitism_size):
    """
    Preserve the best individuals (elites) from the current population to the next generation.
    
    Parameters:
    - population (list): The current population (list of individuals).
    - elitism_size (int): The number of elites to preserve.

    Returns:
    - elites (list): The best `elitism_size` individuals in the population.
    """
    # Sort population by fitness (ascending order)
    population.sort(key=lambda ind: ind.fitness.values[0])

    # Select the top `elitism_size` individuals (elites)
    elites = population[:elitism_size]

    return elites

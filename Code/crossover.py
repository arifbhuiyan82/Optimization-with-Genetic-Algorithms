import random

def single_point_crossover(parent1, parent2):
    """
    Perform single-point crossover while preserving task order within jobs.
    """
    size = len(parent1)
    cxpoint = random.randint(1, size - 1)  # Random crossover point

    # Perform crossover
    child1 = parent1[:cxpoint] + parent2[cxpoint:]
    child2 = parent2[:cxpoint] + parent1[cxpoint:]

    # Repair invalid chromosomes
    child1 = repair_chromosome(child1, parent1)
    child2 = repair_chromosome(child2, parent2)

    return child1, child2


def repair_chromosome(child, parent):
    """
    Repair a child chromosome by ensuring that task precedence is maintained.
    """
    job_task_order = {}

    # Build job task precedence order from the parent (correct order reference)
    for job_id, task_id in parent:
        if job_id not in job_task_order:
            job_task_order[job_id] = []
        job_task_order[job_id].append(task_id)

    # Ensure tasks appear in the correct order
    seen_tasks = {job_id: [] for job_id in job_task_order}
    fixed_child = []

    for job_id, task_id in child:
        if task_id in job_task_order[job_id] and task_id not in seen_tasks[job_id]:
            fixed_child.append((job_id, task_id))
            seen_tasks[job_id].append(task_id)

    return fixed_child


def uniform_crossover(parent1, parent2):
    """
    Perform uniform crossover while preserving task order within jobs.
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

    # Repair invalid chromosomes
    child1 = repair_chromosome(child1, parent1)
    child2 = repair_chromosome(child2, parent2)

    return child1, child2

import random

def scramble_mutation(individual, jobs_data):
    """
    Perform scramble mutation while preserving task order within jobs.
    """
    size = len(individual)
    start, end = sorted(random.sample(range(size), 2))  # Random segment to scramble

    # Extract segment
    segment = individual[start:end]

    # Group tasks by jobs
    job_tasks = {job_id: [] for job_id in range(len(jobs_data))}
    for job_id, task_id in segment:
        job_tasks[job_id].append(task_id)

    # Preserve order
    scrambled_segment = []
    for job_id, task_list in job_tasks.items():
        scrambled_segment.extend([(job_id, task) for task in sorted(task_list)])  # Sort to maintain order

    individual[start:end] = scrambled_segment
    return individual

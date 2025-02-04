Job Shop Scheduling Problem (JSSP) Optimization Using Genetic Algorithm and Tabu Search

This repository contains an implementation of the Job Shop Scheduling Problem (JSSP) using a Genetic Algorithm (GA) combined with Tabu Search (TS) for refining the best solution. The objective is to optimize task scheduling across machines to minimize the total computational time (makespan).

---

 📌 Project Overview

This project consists of the following major components:

✅ Genetic Algorithm (GA)

- Used to find an optimal or near-optimal task scheduling that minimizes makespan.
- Implements selection, crossover, mutation, and elitism techniques to improve solutions over generations.

✅ Tabu Search (TS)

- A local search technique that refines the best GA-generated schedule, avoiding local optima traps.
- Uses tabu tenure, aspiration criteria, and stagnation limits to guide search efficiency.

✅ Multiple Datasets

- The algorithm is tested on three datasets representing different problem complexities:
  - Small-scale: fisher_thompson_6x6 (6 jobs × 6 machines)
  - Medium-scale: fisher_thompson_10x10 (10 jobs × 10 machines)
  - Large-scale: adams_balas_and_zawack_15x20 (15 jobs × 20 machines)

✅ Visualizations

- Gantt charts to visualize task scheduling.
- Fitness evolution plots to track solution improvement across generations.

---

 📂 Files in This Repository

| File                 | Description                                                                                            |
| ------------------------ | ---------------------------------------------------------------------------------------------------------- |
| JSSP.py                | Main script for running the Genetic Algorithm and experimenting with different parameter settings. |
| JSSP_Tabu.py           | Modified version of JSSP.py that integrates Tabu Search for post-processing solution refinement.     |
| tabu_search.py         | Implements Tabu Search algorithm to further optimize the best GA-found solution.                       |
| chromosome.py          | Defines chromosome structure, population initialization, and task precedence handling.         |
| crossover.py           | Implements single-point crossover and uniform crossover.                                           |
| mutation.py            | Implements scramble mutation for diversity maintenance.                                            |
| elitism.py             | Ensures top-performing individuals are preserved across generations.                                   |

---

 📌 Requirements

- Python 3.8 or higher
- deap (for Genetic Algorithm implementation)
- matplotlib (for Gantt chart visualization)
- numpy (for numerical operations)

Install dependencies using:

pip install deap matplotlib numpy


---

 🚀 How to Run the Code

1️. Prepare the dataset: Place datasets in the project directory or update file paths in JSSP.py.\
2️. Run the script to execute the Genetic Algorithm and optionally apply Tabu Search:


python JSSP.py

or (to include Tabu Search refinement)

python JSSP_Tabu.py


3. Select a dataset when prompted.\
4. View and analyze results in the CSV output files and visualization plots.

---

 📊 Parameter Settings Used

| Experiment No. | Population Size | Crossover Probability (Cxpb) | Mutation Probability (Mutpb) | Generations (Ngen) |
| ------------------ | ------------------- | -------------------------------- | -------------------------------- | ---------------------- |
| 1                  | 50                  | 0.6                              | 0.1                              | 100                    |
| 2                  | 50                  | 0.7                              | 0.2                              | 100                    |
| 3                  | 100                 | 0.8                              | 0.1                              | 100                    |
| 4                  | 100                 | 0.7                              | 0.2                              | 150                    |
| 5                  | 200                 | 0.7                              | 0.2                              | 100                    |
| 6                  | 200                 | 0.8                              | 0.3                              | 150                    |

---

 📈 Results: GA vs. GA+Tabu Search

| Dataset                     | Best Makespan (GA Only) | Best Makespan (GA+TS) | Improvement            |
| ------------------------------- | --------------------------- | ------------------------- | -------------------------- |
| Fisher & Thompson 6×6       | 76                      | 75                    | ✅ 1 unit improvement   |
| Fisher & Thompson 10×10     | 1612                    | 1590                  | ✅ 22 units improvement |
| Adams, Balas & Zawack 15×20 | 462                     | 641                   | ❌ No improvement       |

---

 📌 Key Observations

✔ GA Performance:

- The Genetic Algorithm alone achieved strong results, reducing makespan across all datasets.
- Larger populations (100-200) and higher crossover rates (0.7-0.8) generally improved solution quality.

✔ Tabu Search Effectiveness:

- TS helped refine solutions, especially in Fisher & Thompson datasets.
- However, it was not always beneficial, as seen in Adams 15×20, where GA performed better.

✔ Mutation Rate Impact:

- Low mutation (0.1): Converged too early.
- High mutation (0.3): Disrupted good solutions.
- Balanced mutation (0.2) worked best.

✔ Runtime Considerations:

- Tabu Search added computational overhead but provided meaningful refinements in most cases.

---

 📌 Conclusion

✅ Genetic Algorithm is an effective approach for JSSP, and it works well with proper parameter tuning.\
✅ Tabu Search serves as a useful refinement tool, but its impact depends on the dataset complexity.\
✅ Future Directions:

- Hybrid GA-TS Integration: Instead of applying TS after GA, integrate it within the GA evolution process.
- Larger-scale JSSP problems: Test on 20×20+ configurations to assess scalability.
- Comparing other metaheuristics (Simulated Annealing, Particle Swarm Optimization) to GA+TS.

---

 📌 Final Takeaways

- Genetic Algorithm alone performed well, but Tabu Search provided additional refinements in most cases.
- For complex datasets (15×20), GA alone performed better.
- Further tuning and hybridization of GA+TS can yield even better results in future research.


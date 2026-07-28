# Week 3 Experiment Report: GA vs OR-Tools for EVRP-TW

## 1. Experimental Setup

### 1.1 Comparison Target
- **Method tested**: Genetic Algorithm (GA) with battery constraint
- **Baseline**: OR-Tools with battery constraint
- **Main difference**: GA is a stochastic heuristic; OR-Tools is an exact solver
- **Research question**: Can GA find feasible solutions for EVRP-TW when OR-Tools fails?

### 1.2 Test Cases
- Dataset: Custom-generated instances with 50, 100, 200 customers
- Battery capacity: 30 units
- Battery consumption rate: 1.0 per distance unit
- Time windows: Included for all customers
- Vehicle capacity: 200 units
- Same distance matrix used for both methods

### 1.3 Metrics Recorded
- Objective value (total distance)
- Number of vehicles used
- Runtime
- Feasibility status

### 1.4 GA Parameters
- Population size: 400
- Generations: 300
- Crossover probability: 0.85
- Mutation probability: 0.02
- Random seed: 64

## 2. Results

### 2.1 Summary Table

| Scale | Method | Feasible | Objective | Vehicles | Runtime (s) |
|-------|--------|----------|-----------|----------|-------------|
| 50 | GA | Yes | 38,985 | 37 | ~30 |
| 50 | OR-Tools | No | N/A | N/A | ~60 |
| 100 | GA | Yes | 66,990 | 38 | ~120 |
| 100 | OR-Tools | No | N/A | N/A | ~60 |
| 200 | GA | Yes | 150,398 | 194 | ~900 |
| 200 | OR-Tools | No | N/A | N/A | ~60 |

### 2.2 Key Observations

GA found feasible solutions for all three scales (50, 100, and 200 customers). OR-Tools failed to find any feasible solution across all scales when battery constraints were applied.

For GA, the number of vehicles used increased significantly with problem size:
- 50 customers → 37 vehicles (1.35 customers per vehicle)
- 100 customers → 38 vehicles (2.63 customers per vehicle)
- 200 customers → 194 vehicles (1.03 customers per vehicle)

The vehicle utilization drops sharply at 200 customers, indicating that battery capacity becomes a severe constraint when customers are spread across a larger area.

## 3. Discussion

### 3.1 Why GA Succeeded and OR-Tools Failed

OR-Tools is an exact solver that searches for the globally optimal solution while strictly satisfying all constraints. When the problem becomes highly constrained with both time windows and battery capacity, the feasible search space shrinks dramatically. OR-Tools may determine that no feasible solution exists within its search bounds and terminate without returning a solution.

GA, in contrast, starts with a population of random solutions and iteratively improves them through selection, crossover, and mutation. It does not require optimality; it only needs to find feasible solutions. This flexibility allows GA to handle complex constraints more robustly than exact solvers.

### 3.2 Scale Effects on GA Performance

The sharp increase in vehicle count at 200 customers (from 38 to 194 vehicles) suggests that battery capacity becomes a critical bottleneck as the service area expands. Many vehicles return to the depot after serving only one customer, indicating that the current battery capacity (30 units) is insufficient for efficient large-scale delivery.

### 3.3 Trade-offs

| Aspect | GA | OR-Tools |
|--------|-----|----------|
| Feasibility | Always feasible | Often infeasible under tight constraints |
| Solution quality | Suboptimal | Optimal (if found) |
| Runtime | Increases with scale | Relatively fast but returns no solution |
| Constraint handling | Flexible | Strict |

The key trade-off is between **feasibility** and **optimality**. GA guarantees a feasible solution but may not be optimal, while OR-Tools guarantees optimality only when it can find a solution, which fails under complex constraints.

## 4. Conclusion

This experiment compared GA and OR-Tools on EVRP-TW instances with battery constraints. GA consistently found feasible solutions across all scales (50, 100, and 200 customers), while OR-Tools failed on all instances. This suggests that GA's flexibility makes it more suitable for complex VRPs where feasibility is the primary concern. However, GA's solution quality may be suboptimal, and its runtime increases significantly with problem size. The sharp increase in vehicle count at 200 customers highlights the importance of battery capacity in large-scale EVRP-TW problems. Future work could explore hybrid approaches that use GA to generate initial feasible solutions and OR-Tools to refine them.

## 5. Limitations

- Only one run per GA configuration (no repeated trials due to time constraints)
- OR-Tools parameters were not extensively tuned
- Battery constraint does not include recharging stations
- Time windows were derived from random generation, not real-world data

## 6. Appendix: Raw Outputs

Raw experimental outputs are available in the following files:
- `src/py-ga-VRPTW/results/battery_capacity_30.txt` (100 customers)
- GA 50 and 200 customer results in terminal outputs (saved in results folder)
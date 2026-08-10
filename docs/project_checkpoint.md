# Project Checkpoint — FURP 2026

## 1. Current Project Status

**Problem**: EVRP-TW (Electric Vehicle Routing Problem with Time Windows) with battery constraints and time windows.

**Method**: Genetic Algorithm (GA) with battery constraint, implemented via py-ga-VRPTW.

**What works:**
- GA runs successfully on 50, 100, and 200 customer instances
- Battery constraint (capacity=30) is enforced
- Time windows are enforced
- Results are saved to CSV files

**What is not finished:**
- POMO method not implemented
- Truck-drone variant not explored
- Only one random seed per configuration (no repeated trials)

## 2. Evidence of Progress

### Experiment Results

| Scale | Method | Feasible | Objective | Vehicles | Runtime |
|-------|--------|----------|-----------|----------|---------|
| 50 | GA (with battery) | Yes | 38,985 | 37 | ~30s |
| 100 | GA (with battery) | Yes | 66,990 | 38 | ~120s |
| 200 | GA (with battery) | Yes | 150,398 | 194 | ~900s |
| 50 | OR-Tools (with battery) | No | N/A | N/A | ~60s |
| 100 | OR-Tools (with battery) | No | N/A | N/A | ~60s |
| 200 | OR-Tools (with battery) | No | N/A | N/A | ~60s |

### Key Observations
- GA finds feasible solutions for all scales
- OR-Tools fails to find feasible solutions with battery constraints
- Vehicle utilization drops sharply at 200 customers (194 vehicles for 200 customers)

### 2-opt Experiment
- 2-opt increased total cost from 66,990 to 91,714 (+36.9%)
- Vehicle count increased from 38 to 91 (+53 vehicles)
- Conclusion: 2-opt is not suitable for this problem due to battery constraints

## 3. Problems and Limitations

**Main difficulties:**
1. OR-Tools cannot find feasible solutions under battery constraints
2. No repeated trials for GA (only one run per configuration)
3. POMO method not implemented
4. Battery constraint does not include recharging stations
5. Time windows are randomly generated, not based on real-world data

**What needs improvement:**
- Add multiple runs with different random seeds
- Test different battery capacities (10, 20, 50)
- Improve the README for reproducibility

## 4. Next Steps

1. Run GA with different random seeds (3 runs per configuration) to verify stability
2. Test different battery capacities to analyze sensitivity
3. If time permits, explore POMO method
4. Clean up repository structure and improve documentation

## 5. Repository Structure

# Week 6 Lab: Integrate Methods and Explore Learning-Based Extensions

## 1. Current Stage

**Track B: Combine Existing Methods Into One Workflow**

I already have two working methods:
- GA with battery constraints (baseline)
- OR-Tools with battery constraints (fails on all instances)

This track fits my progress because I have runnable code and experimental results, and I want to combine them into a more unified workflow.

## 2. Method Design

### Workflow Pipeline
Input Instance (50/100/200 customers)
↓
GA Initial Solution (with battery constraints)
↓
Feasibility Check (capacity, time windows, battery)
↓
OR-Tools Refinement (if initial solution is feasible)
↓
Feasibility Check
↓
Final Solution
↓
Evaluation Table

text

### Why This Order?

1. **GA generates a feasible initial solution** first because it can handle complex constraints flexibly
2. **OR-Tools refines the solution** because it can find better routes if given a good starting point
3. **Feasibility check after each step** ensures no constraint violations are introduced

### What Baseline to Compare Against?

- Baseline: GA alone (already tested on 50/100/200 customers)
- Proposed: GA + OR-Tools refinement

### Expected Improvement

- OR-Tools should improve the objective value without breaking feasibility
- Runtime may increase slightly, but objective should improve

## 3. Experiment Plan

### Instances

- 50, 100, 200 customers (same as previous experiments)
- Battery capacity: 30 units
- Time windows: included
- 3 runs per configuration (different random seeds)

### Metrics

- Objective value (total distance)
- Number of vehicles used
- Runtime
- Feasibility status

### Success Criteria

- Proposed method achieves lower objective value than GA alone
- Feasibility rate remains 100%
- Runtime increase is acceptable (< 2x baseline)

### Expected Failure Case

- OR-Tools may fail to refine the solution if the initial solution is too far from optimal
- If this happens, we will use GA only

## 4. Preliminary Result or Implementation Progress

### Current Results (Baseline GA)

| Scale | Feasible | Objective | Vehicles | Runtime |
|-------|----------|-----------|----------|---------|
| 50 | Yes | 38,985 | 37 | ~30s |
| 100 | Yes | 66,990 | 38 | ~120s |
| 200 | Yes | 150,398 | 194 | ~900s |

### Implementation Status

- GA baseline code is working and tested
- OR-Tools code is working but fails to find feasible solutions independently
- Integration is in progress
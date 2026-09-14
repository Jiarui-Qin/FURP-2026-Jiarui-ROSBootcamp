FURP 2026 Project Report: Electric Vehicle Routing Problem with Time Windows (EVRP-TW)
Author: Jiarui Qin
Student ID: 20809602
Supervising Faculty: 
Project Period: FURP 2026
Repository: FURP-2026-Jiarui-ROSBootcamp

Abstract
This project investigates the Electric Vehicle Routing Problem with Time Windows (EVRP-TW). We reproduced and extended the open-source py-ga-VRPTW project by adding battery capacity constraints, and compared a Genetic Algorithm (GA) against Google OR-Tools on instances with 50, 100, and 200 customers. The results show that GA consistently finds feasible solutions across all scales, while OR-Tools fails to find any feasible solution under battery and time window constraints. Battery capacity significantly affects vehicle count and total cost. A 2-opt local search was also tested but increased total cost by 36.9% because shorter routes reduced vehicle utilization under the battery constraint. Based on these findings, we selected Track B: a combined workflow using GA to generate an initial feasible solution and OR-Tools to refine it.

1. Introduction
The Electric Vehicle Routing Problem (EVRP) is a variant of the classic Vehicle Routing Problem (VRP) that must simultaneously consider vehicle capacity, time windows, and battery range. As logistics fleets electrify, EVRP-TW has become an important topic in operations research. This project aims to:

Reproduce a GA baseline and add battery constraints;

Compare GA with OR-Tools under complex constraints;

Explore the effect of a local search operator (2-opt);

Design a combined method that balances feasibility and solution quality.

2. Methodology
2.1 Problem Definition: EVRP-TW
Customers: 50 / 100 / 200, each with randomly generated time windows;

Vehicles: capacity 200 units;

Battery: adjustable capacity (10, 30, 50, 100 in experiments), consumption rate 1.0 per distance unit;

Depot: a single depot; all vehicles start from and return to it;

Objective: minimize total travel distance (or total cost, including fixed vehicle cost init_cost = 100).

2.2 Genetic Algorithm (GA) Implementation
Based on the py-ga-VRPTW project. Core functions include:

ind2route: decodes an individual into routes and adds battery check logic;

eval_vrptw: fitness evaluation with time window and battery penalty;

cx_partially_matched: partially matched crossover;

mut_inverse_indexes: inversion mutation.

GA parameters: population 400, 300 generations, crossover probability 0.85, mutation probability 0.02, random seed 64 (single run).

2.3 Battery Constraint
Inside ind2route, travel distance is accumulated. If it exceeds battery_capacity, the route is marked infeasible and a penalty is applied. New parameters battery_capacity and battery_consumption_rate were added to the data file.

2.4 OR-Tools Attempt
We built a VRP model using OR-Tools RoutingModel and added battery constraints via dimension constraints or callbacks. However, OR-Tools failed to find feasible solutions under the combined battery and time window constraints.

2.5 2-opt Local Search
After GA decoding, 2-opt was applied to each route to reverse segments and shorten travel distance. Cost was then re-evaluated.

2.6 Combined Method (Track B)
Designed workflow: GA → Feasibility Check → OR-Tools Refinement → Final Solution. The integration note is complete, but the implementation has not yet been coded.

3. Experimental Setup
Item	Setting
Dataset	Custom-generated instances, 50 / 100 / 200 customers
Battery capacity	30 (comparison); 10/30/50/100 (sensitivity analysis)
Battery consumption rate	1.0 per distance unit
Vehicle capacity	200
Time windows	Randomly generated
GA parameters	Population 400, 300 generations, crossover 0.85, mutation 0.02, seed 64
OR-Tools	Default parameters, timeout about 60 s
4. Results
4.1 GA Baseline Reproduction (Week 2)
With 100 customers and battery capacity 100, GA reproduced the baseline: 12 vehicles, total cost 63,333.99, battery constraint not activated.

Battery capacity sensitivity analysis (100 customers):

Battery capacity	Vehicles	Total cost	Note
100	12	63,333.99	Constraint not activated
50	69	81,285.61	Constraint begins to take effect
30	38	66,990.85	Better balance
10	101	96,066.39	Constraint too tight
A comparison chart comparison_chart.png was generated.

4.2 GA vs OR-Tools (Week 3)
Scale	Method	Feasible	Objective	Vehicles	Runtime
50	GA	Yes	38,985	37	~30 s
50	OR-Tools	No	N/A	N/A	~60 s
100	GA	Yes	66,990	38	~120 s
100	OR-Tools	No	N/A	N/A	~60 s
200	GA	Yes	150,398	194	~900 s
200	OR-Tools	No	N/A	N/A	~60 s
Key observations:

GA found feasible solutions at all scales; OR-Tools failed in every case.

At 200 customers, vehicle count jumped to 194, meaning each vehicle served only about one customer on average. Battery capacity became a severe bottleneck.

4.3 2-opt Local Search Experiment (Week 4)
With 100 customers and battery capacity 30:

Metric	Baseline GA	GA + 2-opt	Change
Total cost	66,990.85	91,714.45	+36.9%
Vehicles used	38	91	+53
Analysis: 2-opt shortened individual route distances, reducing battery consumption per route. Vehicles returned to the depot earlier, so more vehicles were needed to cover all customers. The fixed vehicle cost (100 per vehicle) caused total cost to rise sharply.

4.4 Project Checkpoint (Week 5)
Weeks 2–4 were summarized into project_checkpoint.md, including:

Current status: GA feasible, OR-Tools infeasible, 2-opt unsuccessful;

Limitations: single run, no repeated trials, POMO not implemented, no recharging stations;

Next steps: multiple random seeds, battery capacity sensitivity, improved documentation.

4.5 Track B Selection (Week 6)
A combined method was chosen: GA generates an initial feasible solution → OR-Tools refines it. An integration note week6_integration.md was written, but implementation has not started.

5. Discussion
5.1 Feasibility vs Optimality
OR-Tools is an exact solver. Under tight constraints, the feasible search space shrinks dramatically, and it may terminate without a solution. GA is a stochastic heuristic; it does not require optimality and only needs to find feasible solutions, making it more robust under complex constraints. However, GA solution quality may be suboptimal, and runtime grows significantly with scale.

5.2 Impact of Battery Constraints
Battery capacity directly determines how many customers a vehicle can serve. With capacity 30, 100 customers require 38 vehicles; 200 customers require 194 vehicles, resulting in very low vehicle utilization. Future work should consider recharging stations or dynamic battery management.

5.3 Why 2-opt Failed
The local search optimized a local objective (single-route distance) but worsened the global objective (total vehicles × fixed cost). Under battery constraints, shortening routes actually reduced vehicle utilization. This suggests that EVRP-TW optimization must consider both distance and vehicle count simultaneously.

6. Conclusion
GA shows strong feasibility-search ability for EVRP-TW and is suitable as a base solver.

OR-Tools cannot find feasible solutions under combined battery and time window constraints; constraint modeling or hybrid methods are needed.

Battery capacity is a key parameter affecting vehicle count and total cost.

2-opt is not suitable for this problem because it conflicts with the battery constraint.

A combined method (GA + OR-Tools refinement) is a promising direction.

7. Limitations
Only one GA run per configuration; no repeated trials with multiple random seeds;

OR-Tools parameters were not extensively tuned;

Battery model does not include recharging stations;

Time windows were randomly generated, not based on real-world data;

POMO method was not implemented.

8. Next Steps
Run GA with multiple random seeds (3 runs per configuration) to verify stability;

Test more battery capacities (10, 20, 50) for sensitivity analysis;

Implement the Track B combined workflow and test on 50/100/200 customer instances;

If time permits, explore the POMO method;

Improve repository documentation and reproducibility;

Prepare the final poster FURP_Showcase.pdf.

9. References and Links
Google OR-Tools documentation: https://developers.google.com/optimization

py-ga-VRPTW project: https://github.com/CluFei/py-ga-VRPTW

Project repository: https://github.com/Jiarui-Qin/FURP-2026-Jiarui-ROSBootcamp

Experimental data and charts: src/py-ga-VRPTW/results/

Weekly logs and checkpoints: docs/00_weekly.md, docs/project_checkpoint.md, docs/week2_report.md, docs/week2_reflection.md, docs/week6_integration.md
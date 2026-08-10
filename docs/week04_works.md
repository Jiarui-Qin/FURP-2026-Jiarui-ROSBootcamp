# Week 4 Lab: GA + 2-opt Local Search

## 1. Experimental Setup

### 1.1 Comparison Target
- **Method tested**: GA with 2-opt local search
- **Baseline**: Original GA (hard constraints)
- **Research question**: Can 2-opt local search improve solution quality for EVRP-TW?

### 1.2 Implementation
2-opt is a local search operator that reverses segments of a route to reduce total travel distance. It was applied to each route after decoding and before cost evaluation.

### 1.3 Test Cases
- Dataset: Custom-generated instance with 100 customers
- Battery capacity: 30 units
- Time windows: Included
- Vehicle capacity: 200 units
- Same settings used for both baseline and improved GA

### 1.4 Metrics Recorded
- Total cost
- Number of vehicles used

## 2. Results

### 2.1 Comparison Table

| Metric | Baseline GA | GA + 2-opt | Change |
|--------|-------------|------------|--------|
| Total Cost | 66,990.85 | 91,714.45 | +36.9% |
| Vehicles Used | 38 | 91 | +53 |

### 2.2 Route Analysis
The baseline GA used 38 vehicles to serve 100 customers. After adding 2-opt, the number of vehicles increased to 91, meaning most vehicles served only one customer. This suggests that 2-opt optimization made individual routes shorter, reducing battery usage per route, but requiring more vehicles to cover all customers.

## 3. Discussion

2-opt improved individual route distances but failed to improve the overall solution. The root cause is the battery constraint (capacity=30). When 2-opt shortened each route, vehicles consumed less battery per trip and returned to depot earlier. As a result, fewer customers were assigned to each vehicle, and more vehicles were needed to serve all customers. The fixed cost per vehicle (init_cost=100) then caused the total cost to increase.

This result highlights a limitation of local search operators: they optimize local objectives (route distance) but may worsen global objectives (total vehicles × fixed cost), especially under tight battery constraints.

## 4. Conclusion

2-opt local search was implemented and tested on the EVRP-TW problem. The result shows that 2-opt increased total cost by 36.9% and vehicle count by 53 vehicles. The improvement failed because shorter routes led to lower vehicle utilization under the battery constraint. This suggests that for EVRP-TW, global optimization should consider both distance and vehicle count simultaneously. Future work could explore hybrid approaches that optimize vehicle count first and then refine routes.
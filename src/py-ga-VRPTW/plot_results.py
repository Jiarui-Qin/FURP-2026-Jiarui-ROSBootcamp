import matplotlib.pyplot as plt

battery_capacities = [10, 30, 50, 100]
total_costs = [96066.39, 91714.45, 81285.61, 66990.85]
vehicle_counts = [101, 91, 69, 38]

battery_capacities_sorted = sorted(battery_capacities, reverse=True)
total_costs_sorted = [total_costs[battery_capacities.index(x)] for x in battery_capacities_sorted]
vehicle_counts_sorted = [vehicle_counts[battery_capacities.index(x)] for x in battery_capacities_sorted]

fig, ax1 = plt.subplots(figsize=(8, 5))

color = 'tab:red'
ax1.set_xlabel('Battery Capacity')
ax1.set_ylabel('Total Cost', color=color)
ax1.plot(battery_capacities_sorted, total_costs_sorted, 'o-', color=color, linewidth=2, markersize=8)
ax1.tick_params(axis='y', labelcolor=color)
for i, (x, y) in enumerate(zip(battery_capacities_sorted, total_costs_sorted)):
    ax1.annotate(f'{y:,.2f}', (x, y), textcoords="offset points", xytext=(0,10), ha='center')

ax2 = ax1.twinx()
color = 'tab:blue'
ax2.set_ylabel('Number of Vehicles', color=color)
ax2.plot(battery_capacities_sorted, vehicle_counts_sorted, 's-', color=color, linewidth=2, markersize=8)
ax2.tick_params(axis='y', labelcolor=color)
for i, (x, y) in enumerate(zip(battery_capacities_sorted, vehicle_counts_sorted)):
    ax2.annotate(f'{y}', (x, y), textcoords="offset points", xytext=(0,-15), ha='center')

plt.title('Impact of Battery Capacity on Cost and Vehicle Count', fontsize=14)
plt.grid(True, linestyle='--', alpha=0.7)
plt.savefig('results/comparison_chart.png', dpi=300, bbox_inches='tight')
plt.show()

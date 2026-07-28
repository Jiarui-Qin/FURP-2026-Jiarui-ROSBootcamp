from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp
import json
import time

def load_data_from_json(scale):
    if scale == 50 or scale == 100:
        file_path = 'data/json_customize/Customized_Data.json'
    elif scale == 200:
        file_path = 'data/json_customize/Customized_Data_200.json'
    else:
        raise ValueError("Scale must be 50, 100, or 200")
    
    with open(file_path, 'r') as f:
        raw = json.load(f)
    
    n = scale
    dist_matrix = raw['distance_matrix'][:n+1]
    dist_matrix = [row[:n+1] for row in dist_matrix]
    
    time_windows = []
    for i in range(n + 1):
        if i == 0:
            time_windows.append((0, 1236))
        else:
            customer = raw[f'customer_{i}']
            time_windows.append((int(customer['ready_time']), int(customer['due_time'])))
    
    demands = [0] + [int(raw[f'customer_{i}']['demand']) for i in range(1, n + 1)]
    service_times = [0] + [int(raw[f'customer_{i}']['service_time']) for i in range(1, n + 1)]
    
    return {
        'distance_matrix': dist_matrix,
        'time_windows': time_windows,
        'demands': demands,
        'service_times': service_times,
        'vehicle_capacity': int(raw['vehicle_capacity']),
        'battery_capacity': int(raw['battery_capacity']),
        'battery_rate': raw['battery_consumption_rate'],
        'num_vehicles': min(n, 50)
    }

def solve_ortools(scale):
    data = load_data_from_json(scale)
    
    dist_matrix = data['distance_matrix']
    time_windows = data['time_windows']
    demands = data['demands']
    service_times = data['service_times']
    vehicle_capacity = data['vehicle_capacity']
    battery_capacity = data['battery_capacity']
    battery_rate = data['battery_rate']
    num_vehicles = data['num_vehicles']
    n = len(dist_matrix)
    depot = 0
    
    manager = pywrapcp.RoutingIndexManager(n, num_vehicles, depot)
    routing = pywrapcp.RoutingModel(manager)
    
    def distance_callback(from_index, to_index):
        from_node = manager.IndexToNode(from_index)
        to_node = manager.IndexToNode(to_index)
        return int(dist_matrix[from_node][to_node] * 10)
    
    transit_callback_index = routing.RegisterTransitCallback(distance_callback)
    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)
    
    battery_dimension_name = 'Battery'
    def battery_callback(from_index, to_index):
        from_node = manager.IndexToNode(from_index)
        to_node = manager.IndexToNode(to_index)
        return int(dist_matrix[from_node][to_node] * 10 * battery_rate)
    
    battery_callback_index = routing.RegisterTransitCallback(battery_callback)
    routing.AddDimension(
        battery_callback_index,
        0,
        int(battery_capacity * 10),
        True,
        battery_dimension_name
    )
    battery_dimension = routing.GetDimensionOrDie(battery_dimension_name)
    
    def demand_callback(from_index):
        from_node = manager.IndexToNode(from_index)
        return demands[from_node]
    
    demand_callback_index = routing.RegisterUnaryTransitCallback(demand_callback)
    routing.AddDimensionWithVehicleCapacity(
        demand_callback_index,
        0,
        [vehicle_capacity] * num_vehicles,
        True,
        'Capacity'
    )
    
    def time_callback(from_index, to_index):
        from_node = manager.IndexToNode(from_index)
        to_node = manager.IndexToNode(to_index)
        return int(dist_matrix[from_node][to_node] * 10) + service_times[from_node]
    
    time_callback_index = routing.RegisterTransitCallback(time_callback)
    routing.AddDimension(
        time_callback_index,
        3000,
        30000,
        False,
        'Time'
    )
    time_dimension = routing.GetDimensionOrDie('Time')
    
    for location_idx in range(n):
        if location_idx == depot:
            continue
        index = manager.NodeToIndex(location_idx)
        time_dimension.CumulVar(index).SetRange(
            time_windows[location_idx][0] * 10,
            time_windows[location_idx][1] * 10
        )
    
    for vehicle_id in range(num_vehicles):
        index = routing.Start(vehicle_id)
        time_dimension.CumulVar(index).SetRange(0, 1236 * 10)
        battery_dimension.CumulVar(index).SetRange(0, int(battery_capacity * 10))
    
    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.first_solution_strategy = (
        routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC
    )
    search_parameters.local_search_metaheuristic = (
        routing_enums_pb2.LocalSearchMetaheuristic.GUIDED_LOCAL_SEARCH
    )
    search_parameters.time_limit.seconds = 120
    
    start_time = time.time()
    solution = routing.SolveWithParameters(search_parameters)
    elapsed = time.time() - start_time
    
    if solution:
        vehicles_used = 0
        total_distance = 0
        for vehicle_id in range(num_vehicles):
            index = routing.Start(vehicle_id)
            if routing.IsEnd(solution.Value(routing.NextVar(index))):
                continue
            vehicles_used += 1
            route_distance = 0
            while not routing.IsEnd(index):
                next_index = solution.Value(routing.NextVar(index))
                route_distance += dist_matrix[manager.IndexToNode(index)][manager.IndexToNode(next_index)]
                index = next_index
            total_distance += route_distance
        
        return {
            'feasible': True,
            'objective': total_distance,
            'vehicles': vehicles_used,
            'runtime': elapsed
        }
    else:
        return {
            'feasible': False,
            'objective': None,
            'vehicles': None,
            'runtime': elapsed
        }

if __name__ == '__main__':
    print("=" * 60)
    print("OR-Tools Comparison Experiment (with Battery Constraint)")
    print("=" * 60)
    
    results = {}
    for scale in [50, 100, 200]:
        print(f"\n--- Running OR-Tools on {scale} customers ---")
        result = solve_ortools(scale)
        results[scale] = result
        if result['feasible']:
            print(f"  Feasible: Yes")
            print(f"  Objective (total distance): {result['objective']:.2f}")
            print(f"  Vehicles used: {result['vehicles']}")
            print(f"  Runtime: {result['runtime']:.2f} seconds")
        else:
            print(f"  Feasible: No solution found")
    
    print("\n" + "=" * 60)
    print("Summary Table")
    print("=" * 60)
    print(f"{'Scale':<10} {'Feasible':<10} {'Objective':<15} {'Vehicles':<10} {'Runtime (s)':<12}")
    print("-" * 60)
    for scale in [50, 100, 200]:
        r = results[scale]
        if r['feasible']:
            print(f"{scale:<10} {'Yes':<10} {r['objective']:<15.2f} {r['vehicles']:<10} {r['runtime']:<12.2f}")
        else:
            print(f"{scale:<10} {'No':<10} {'N/A':<15} {'N/A':<10} {r['runtime']:<12.2f}")
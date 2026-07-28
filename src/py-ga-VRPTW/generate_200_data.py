
import json
import random
import os

def generate_customized_data(num_customers):
    random.seed(64)
    data = {}
    data['instance_name'] = 'Customized_Data_200'
    data['vehicle_capacity'] = 200.0
    data['max_vehicle_number'] = 25
    data['battery_capacity'] = 30
    data['battery_consumption_rate'] = 1.0
    data['depart'] = {
        "coordinates": {"x": 40.0, "y": 50.0},
        "demand": 0.0,
        "due_time": 1236.0,
        "ready_time": 0.0,
        "service_time": 0.0
    }

    coords = [(random.randint(0, 100), random.randint(0, 100)) for _ in range(num_customers + 1)]
    coords[0] = (40, 50)

    data['distance_matrix'] = []
    for i in range(num_customers + 1):
        row = []
        for j in range(num_customers + 1):
            dist = ((coords[i][0] - coords[j][0])**2 + (coords[i][1] - coords[j][1])**2)**0.5
            row.append(round(dist, 2))
        data['distance_matrix'].append(row)

    for i in range(1, num_customers + 1):
        data[f'customer_{i}'] = {
            "coordinates": {"x": float(coords[i][0]), "y": float(coords[i][1])},
            "demand": float(random.randint(1, 50)),
            "due_time": float(random.randint(50, 1200)),
            "ready_time": float(random.randint(0, 100)),
            "service_time": 90.0
        }

    return data

if __name__ == '__main__':
    data = generate_customized_data(200)
    os.makedirs('data/json_customize', exist_ok=True)
    file_path = 'data/json_customize/Customized_Data_200.json'
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=2)
    print(f'Generated 200-customer data: {file_path}')
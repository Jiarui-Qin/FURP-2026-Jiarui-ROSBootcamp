# -*- coding: utf-8 -*-

'''gavrptw/core.py'''

import os
import io
import random
from csv import DictWriter
from deap import base, creator, tools
from . import BASE_DIR
from .utils import make_dirs_for_file, exist, load_instance, merge_rules


def ind2route(individual, instance):
    print("=== USING NEW ind2route ===")
    return [individual[:]]

def print_route(route, merge=False):
    '''gavrptw.core.print_route(route, merge=False)'''
    route_str = '0'
    sub_route_count = 0
    for sub_route in route:
        sub_route_count += 1
        sub_route_str = '0'
        for customer_id in sub_route:
            sub_route_str = f'{sub_route_str} - {customer_id}'
            route_str = f'{route_str} - {customer_id}'
        sub_route_str = f'{sub_route_str} - 0'
        if not merge:
            print(f'  Vehicle {sub_route_count}\'s route: {sub_route_str}')
        route_str = f'{route_str} - 0'
    if merge:
        print(route_str)


def eval_vrptw(individual, instance, unit_cost=1.0, init_cost=0, wait_cost=0, delay_cost=0, 
               ev_penalty=500.0, tw_penalty=500.0):
    '''gavrptw.core.eval_vrptw with penalty for EV and TW violations'''
    route = ind2route(individual, instance)
    print(f"eval_vrptw: route has {len(route)} sub-routes")

    total_cost = 0
    total_ev_penalty = 0
    total_tw_penalty = 0
    
    battery_capacity = instance.get('battery_capacity', 100)
    battery_rate = instance.get('battery_consumption_rate', 1.0)
    dist_matrix = instance['distance_matrix']
    
    for sub_route in route:
        sub_route_time_cost = 0
        sub_route_distance = 0
        elapsed_time = 0
        last_customer_id = 0
        current_battery = battery_capacity
        
        for customer_id in sub_route:
            distance = dist_matrix[last_customer_id][customer_id]
            sub_route_distance = sub_route_distance + distance
            
            # Battery constraint with penalty
            battery_needed = distance * battery_rate
            if current_battery - battery_needed < 0:
                shortage = abs(current_battery - battery_needed)
                total_ev_penalty += shortage * ev_penalty
                current_battery = 0
            else:
                current_battery -= battery_needed
            
            # Time window with penalty
            arrival_time = elapsed_time + distance
            ready_time = instance[f'customer_{customer_id}']['ready_time']
            due_time = instance[f'customer_{customer_id}']['due_time']
            
            # Normal time cost (waiting + delay)
            time_cost = wait_cost * max(ready_time - arrival_time, 0) + delay_cost * max(arrival_time - due_time, 0)
            
            # Extra penalty for large TW violations
            if arrival_time > due_time:
                total_tw_penalty += (arrival_time - due_time) * tw_penalty
            if arrival_time < ready_time:
                total_tw_penalty += (ready_time - arrival_time) * tw_penalty * 0.1
            
            sub_route_time_cost = sub_route_time_cost + time_cost
            elapsed_time = arrival_time + instance[f'customer_{customer_id}']['service_time']
            last_customer_id = customer_id
        
        sub_route_distance = sub_route_distance + dist_matrix[last_customer_id][0]
        sub_route_transport_cost = init_cost + unit_cost * sub_route_distance
        sub_route_cost = sub_route_time_cost + sub_route_transport_cost
        total_cost = total_cost + sub_route_cost
    
    # Add penalties to total cost
    total_cost = total_cost + total_ev_penalty + total_tw_penalty
    fitness = 1.0 / total_cost
    return (fitness, )

def cx_partially_matched(ind1, ind2):
    '''gavrptw.core.cx_partially_matched(ind1, ind2)'''
    cxpoint1, cxpoint2 = sorted(random.sample(range(min(len(ind1), len(ind2))), 2))
    part1 = ind2[cxpoint1:cxpoint2+1]
    part2 = ind1[cxpoint1:cxpoint2+1]
    rule1to2 = list(zip(part1, part2))
    is_fully_merged = False
    while not is_fully_merged:
        rule1to2, is_fully_merged = merge_rules(rules=rule1to2)
    rule2to1 = {rule[1]: rule[0] for rule in rule1to2}
    rule1to2 = dict(rule1to2)
    ind1 = [gene if gene not in part2 else rule2to1[gene] for gene in ind1[:cxpoint1]] + part2 + \
        [gene if gene not in part2 else rule2to1[gene] for gene in ind1[cxpoint2+1:]]
    ind2 = [gene if gene not in part1 else rule1to2[gene] for gene in ind2[:cxpoint1]] + part1 + \
        [gene if gene not in part1 else rule1to2[gene] for gene in ind2[cxpoint2+1:]]
    return ind1, ind2


def mut_inverse_indexes(individual):
    '''gavrptw.core.mut_inverse_indexes(individual)'''
    start, stop = sorted(random.sample(range(len(individual)), 2))
    temp = individual[start:stop+1]
    temp.reverse()
    individual[start:stop+1] = temp
    return (individual, )

def calculate_route_distance(route, dist_matrix):
    if not route:
        return 0
    total = dist_matrix[0][route[0]]
    for i in range(len(route) - 1):
        total += dist_matrix[route[i]][route[i+1]]
    total += dist_matrix[route[-1]][0]
    return total

def two_opt(route, dist_matrix):
    if len(route) < 3:
        return route
    improved = True
    best_route = route[:]
    best_distance = calculate_route_distance(best_route, dist_matrix)
    while improved:
        improved = False
        for i in range(1, len(best_route) - 1):
            for j in range(i + 1, len(best_route)):
                if j - i == 1:
                    continue
                new_route = best_route[:i] + best_route[i:j+1][::-1] + best_route[j+1:]
                new_distance = calculate_route_distance(new_route, dist_matrix)
                if new_distance < best_distance - 1e-6:
                    best_route = new_route
                    best_distance = new_distance
                    improved = True
                    break
            if improved:
                break
    return best_route


def run_gavrptw(instance_name, unit_cost, init_cost, wait_cost, delay_cost, ind_size, pop_size, \
    cx_pb, mut_pb, n_gen, export_csv=False, customize_data=False):
    '''gavrptw.core.run_gavrptw(instance_name, unit_cost, init_cost, wait_cost, delay_cost,
        ind_size, pop_size, cx_pb, mut_pb, n_gen, export_csv=False, customize_data=False)'''
    if customize_data:
        json_data_dir = os.path.join(BASE_DIR, 'data', 'json_customize')
    else:
        json_data_dir = os.path.join(BASE_DIR, 'data', 'json')
    json_file = os.path.join(json_data_dir, f'{instance_name}.json')
    instance = load_instance(json_file=json_file)
    if instance is None:
        return
    creator.create('FitnessMax', base.Fitness, weights=(1.0, ))
    creator.create('Individual', list, fitness=creator.FitnessMax)
    toolbox = base.Toolbox()
    # Attribute generator
    toolbox.register('indexes', random.sample, range(1, ind_size + 1), ind_size)
    # Structure initializers
    toolbox.register('individual', tools.initIterate, creator.Individual, toolbox.indexes)
    toolbox.register('population', tools.initRepeat, list, toolbox.individual)
    # Operator registering
    toolbox.register('evaluate', eval_vrptw, instance=instance, unit_cost=unit_cost, \
    init_cost=init_cost, wait_cost=wait_cost, delay_cost=delay_cost, \
    ev_penalty=500.0, tw_penalty=500.0)
    toolbox.register('select', tools.selRoulette)
    toolbox.register('mate', cx_partially_matched)
    toolbox.register('mutate', mut_inverse_indexes)
    pop = toolbox.population(n=pop_size)
    # Results holders for exporting results to CSV file
    csv_data = []
    print('Start of evolution')
    # Evaluate the entire population
    fitnesses = list(map(toolbox.evaluate, pop))
    for ind, fit in zip(pop, fitnesses):
        ind.fitness.values = fit
    print(f'  Evaluated {len(pop)} individuals')
    # Begin the evolution
    for gen in range(n_gen):
        print(f'-- Generation {gen} --')
        # Select the next generation individuals
        offspring = toolbox.select(pop, len(pop))
        # Clone the selected individuals
        offspring = list(map(toolbox.clone, offspring))
        # Apply crossover and mutation on the offspring
        for child1, child2 in zip(offspring[::2], offspring[1::2]):
            if random.random() < cx_pb:
                toolbox.mate(child1, child2)
                del child1.fitness.values
                del child2.fitness.values
        for mutant in offspring:
            if random.random() < mut_pb:
                toolbox.mutate(mutant)
                del mutant.fitness.values
        # Evaluate the individuals with an invalid fitness
        invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
        fitnesses = map(toolbox.evaluate, invalid_ind)
        for ind, fit in zip(invalid_ind, fitnesses):
            ind.fitness.values = fit
        print(f'  Evaluated {len(invalid_ind)} individuals')
        # The population is entirely replaced by the offspring
        pop[:] = offspring
        # Gather all the fitnesses in one list and print the stats
        fits = [ind.fitness.values[0] for ind in pop]
        length = len(pop)
        mean = sum(fits) / length
        sum2 = sum([x**2 for x in fits])
        std = abs(sum2 / length - mean**2)**0.5
        print(f'  Min {min(fits)}')
        print(f'  Max {max(fits)}')
        print(f'  Avg {mean}')
        print(f'  Std {std}')
        # Write data to holders for exporting results to CSV file
        # Write data to holders for exporting results to CSV file
        if export_csv:
            csv_row = {
                'generation': gen,
                'evaluated_individuals': len(invalid_ind),
                'min_fitness': min(fits),
                'max_fitness': max(fits),
                'avg_fitness': mean,
                'std_fitness': std,
            }
            csv_data.append(csv_row)
    
    print('-- End of (successful) evolution --')
    best_ind = tools.selBest(pop, 1)[0]
    print(f'Best individual: {best_ind}')
    print(f'Fitness: {best_ind.fitness.values[0]}')
    
    final_route = ind2route(best_ind, instance)
    print(f"Final route has {len(final_route)} sub-routes")
    for i, sub_route in enumerate(final_route):
        print(f"  Sub-route {i+1}: length {len(sub_route)}")
    
    print(f'Total cost: {1 / best_ind.fitness.values[0]}')
    if export_csv:
        csv_file_name = f'{instance_name}_uC{unit_cost}_iC{init_cost}_wC{wait_cost}' \
            f'_dC{delay_cost}_iS{ind_size}_pS{pop_size}_cP{cx_pb}_mP{mut_pb}_nG{n_gen}.csv'
        csv_file = os.path.join(BASE_DIR, 'results', csv_file_name)
        print(f'Write to file: {csv_file}')
        make_dirs_for_file(path=csv_file)
        if not exist(path=csv_file, overwrite=True):
            with io.open(csv_file, 'wt', encoding='utf-8', newline='') as file_object:
                fieldnames = [
                    'generation',
                    'evaluated_individuals',
                    'min_fitness',
                    'max_fitness',
                    'avg_fitness',
                    'std_fitness',
                ]
                writer = DictWriter(file_object, fieldnames=fieldnames, dialect='excel')
                writer.writeheader()
                for csv_row in csv_data:
                    writer.writerow(csv_row)


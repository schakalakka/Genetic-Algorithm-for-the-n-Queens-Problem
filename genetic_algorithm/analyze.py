import csv
import pygal
import sys

n = 15
key = 'time'
my_type = 'Crossover'


def plot(n, key, mytype):
    if n == 8:
        runs = 500
    else:
        runs = 100
    if key == 'time':
        y_title = 'Average Running Time in Seconds'
    else:
        y_title = 'Average Number of Iterations'

    with open(f'benchmark_{n}_{my_type.lower()}.csv', 'r') as f:
        csv_f = csv.DictReader(f, delimiter='|')
        my_list = []
        for row in csv_f:
            my_list.append(row)

        # my_list = sorted(my_list, key=lambda x: x['time'], reverse=True)

    # crossover
    random_crossover = sum([float(x[key]) for i, x in enumerate(my_list) if x['crossover_method'] == 'random']) / runs
    pmx = sum([float(x[key]) for i, x in enumerate(my_list) if x['crossover_method'] == 'pmx']) / runs
    order_based = sum([float(x[key]) for i, x in enumerate(my_list) if x['crossover_method'] == 'order_based']) / runs
    position_based = sum(
        [float(x[key]) for i, x in enumerate(my_list) if x['crossover_method'] == 'position_based']) / runs

    # selection
    random_selection = sum([float(x[key]) for i, x in enumerate(my_list) if x['selection_method'] == 'random']) / runs
    roulette = sum([float(x[key]) for i, x in enumerate(my_list) if x['selection_method'] == 'roulette']) / runs
    tournament = sum([float(x[key]) for i, x in enumerate(my_list) if x['selection_method'] == 'tournament']) / runs
    truncation = sum([float(x[key]) for i, x in enumerate(my_list) if x['selection_method'] == 'truncation']) / runs

    # truncation01 = sum([i for i, x in enumerate(new_list) if x['truncation_threshold'] == '0.1'])
    # truncation02 = sum([i for i, x in enumerate(new_list) if x['truncation_threshold'] == '0.2'])
    # truncation03 = sum([i for i, x in enumerate(new_list) if x['truncation_threshold'] == '0.3'])
    # truncation04 = sum([i for i, x in enumerate(new_list) if x['truncation_threshold'] == '0.4'])
    # truncation05 = sum([i for i, x in enumerate(new_list) if x['truncation_threshold'] == '0.5'])
    # truncation06 = sum([i for i, x in enumerate(new_list) if x['truncation_threshold'] == '0.6'])
    # truncation07 = sum([i for i, x in enumerate(new_list) if x['truncation_threshold'] == '0.7'])
    # truncation08 = sum([i for i, x in enumerate(new_list) if x['truncation_threshold'] == '0.8'])
    # truncation09 = sum([i for i, x in enumerate(new_list) if x['truncation_threshold'] == '0.9'])

    # tournament3 = sum([i for i, x in enumerate(new_list) if x['tournament_competitors'] == '3'])
    # tournament5 = sum([i for i, x in enumerate(new_list) if x['tournament_competitors'] == '5'])
    # tournament10 = sum([i for i, x in enumerate(new_list) if x['tournament_competitors'] == '10'])
    # tournament15 = sum([i for i, x in enumerate(new_list) if x['tournament_competitors'] == '15'])
    # tournament20 = sum([i for i, x in enumerate(new_list) if x['tournament_competitors'] == '20'])
    # tournament25 = sum([i for i, x in enumerate(new_list) if x['tournament_competitors'] == '25'])
    # tournament30 = sum([i for i, x in enumerate(new_list) if x['tournament_competitors'] == '30'])
    # tournament40 = sum([i for i, x in enumerate(new_list) if x['tournament_competitors'] == '40'])

    # mutation
    random_mutation = sum([float(x[key]) for i, x in enumerate(my_list) if x['mutation_method'] == 'random']) / runs
    exchange = sum([float(x[key]) for i, x in enumerate(my_list) if x['mutation_method'] == 'exchange']) / runs
    scramble = sum([float(x[key]) for i, x in enumerate(my_list) if x['mutation_method'] == 'scramble']) / runs
    insertion = sum([float(x[key]) for i, x in enumerate(my_list) if x['mutation_method'] == 'insertion']) / runs
    inversion = sum([float(x[key]) for i, x in enumerate(my_list) if x['mutation_method'] == 'inversion']) / runs
    displacement = sum([float(x[key]) for i, x in enumerate(my_list) if x['mutation_method'] == 'displacement']) / runs
    displacement_inversion = sum(
        [float(x[key]) for i, x in enumerate(my_list) if x['mutation_method'] == 'displacement_inversion']) / runs

    too_slow = [i for i, x in enumerate(my_list) if x['iterations'] == '10000']

    my_chart = pygal.Bar(show_legend=False, x_label_rotation=20, y_title=y_title)
    my_chart.title = f'{my_type} Methods for the {n}-Queens Problem'

    if my_type == 'Crossover':
        my_chart.x_labels = ['random', 'pmx', 'order_based', 'position_based']
        my_chart.add(f'{my_type} Method', [random_crossover, pmx, order_based, position_based])
    elif my_type == 'Mutation':
        my_chart.x_labels = ['random', 'exchange', 'scramble', 'insertion', 'inversion', 'displacement',
                             'displacement_inversion']
        my_chart.add('Mutation Method',
                     [random_mutation, exchange, scramble, insertion, inversion, displacement, displacement_inversion])
    elif my_type == 'Selection':
        my_chart.x_labels = ['random', 'tournament', 'truncation', 'roulette']
        my_chart.add('Selection Method', [random_selection, tournament, truncation, roulette])
    else:
        print('ERROR!')
        sys.exit(1)

    my_chart.render_to_file(f'images/{my_type.lower()}_{n}_{key}.svg')
    my_chart.render_to_png(f'images/{my_type.lower()}_{n}_{key}.png')
    # my_chart.render_in_browser()


for n in [8, 15]:
    for key in ['time', 'iterations']:
        for my_type in ['Crossover', 'Mutation', 'Selection']:
            plot(n, key, my_type)

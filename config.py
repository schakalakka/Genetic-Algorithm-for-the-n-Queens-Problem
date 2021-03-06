# configuration
# default parameters for the whole algorithm

field_size = 8  # determines the field size nxn and the therefore the number of queens, the problem should be solvable for n>3
number_of_organisms = 100  # number of individuals, i.e. population size
max_iterations = 10000  # number of iteration at which the algorithm will stop and give up, it will still output a fittest but not optimal solution

# SELECTION PARAMETERS
selection_method = 'truncation'  # possible options: 'random', 'tournament', 'truncation', 'roulette'
truncation_threshold = 0.5  # truncation of population, only for truncation method, 0.5 seems to be the best
tournament_competitors = 10  # number of competitors in a selection tournament, 10 till 30 seems  good?
copy_threshold = 0.1  # parameter for copying a percentage from the old population to the new one
selection_method_list = ['tournament', 'truncation', 'roulette']  # used for 'random' selection method, therefore without random

# CROSSOVER PARAMETERS
crossover_method = 'pmx'  # possible options: 'position_based', 'order_based', 'pmx', 'random'
crossover_probability = 0.8  # usually between 0.6 and 1
crossover_method_list = ['pmx', 'position_based', 'order_based']  # used for random crossover_method, therefore without 'random'

# MUTATION PARAMETERS
mutation_method = 'exchange'  # 'random', 'exchange', 'scramble', 'displacement', 'insertion', 'inversion', 'displacement_inversion'
mutation_probability = 0.3
adapt_mutability = True  # if true the mutation_probability will increase over time every 1000 steps
mutation_method_list = ['exchange', 'scramble', 'displacement', 'insertion', 'inversion',
                        'displacement_inversion']  # used for 'random' mutation method therefore without 'random'


# verbose should be set to True if you want to print to the terminal,
# otherwise it will only return the iterations, running time, the fittest individual and the average fitness
# for further processing, we only used False for benchmarking
verbose = True

# configuration
# default parameters for the whole algorithm

field_size = 100  # determines the field size nxn and the therefore the number of queens, the problem should be solvable for n>3
number_of_organisms = 100  # number of individuals, i.e. population size
max_iterations = 10000

# SELECTION PARAMETERS
parent_selection_method = 'random'  # possible options: 'random', 'fast', 'tournament', 'truncation', 'roulette'
truncation_threshold = 0.5  # truncation of population, only for truncation method, 0.5 seems to be the best
tournament_competitors = 10  # number of competitors in a selection tournament, 10 till 30 seems  good?
copy_threshold = 0.1  # parameter for copying a percentage from the old population to the new one

# CROSSOVER PARAMETERS
crossover_method = 'pmx'  # possible options: 'one_point', 'uniform', 'pmx', 'random'
crossover_probability = 0.8  # usually between 0.6 and 1

# MUTATION PARAMETERS
mutation_method = 'random'  # 'random', 'exchange', 'scramble', 'displacement', 'insertion', 'inversion', 'displacement_inversion'
mutation_probability = 0.3
adapt_mutability = True  # if true the mutation_probability will increase over time

verbose = True

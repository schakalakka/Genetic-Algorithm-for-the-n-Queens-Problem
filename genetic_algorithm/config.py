# configuration
# default parameters for the whole algorithm

field_size = 9  # determines the field size nxn and the therefore the number of queens, the problem should be solvable for n>3
number_of_organisms = 100  # number of individuals, i.e. population size
mutation_probability = 0.1
crossover_probability = 0.8  # usually between 0.6 and 1
crossover_method = 'one_point'  # possible options: 'one_point' or 'uniform'
parent_selection_method = 'tournament'  # possible options: 'fast', 'tournament', 'truncation', 'roulette'
truncation_threshold = 0.5
tournament_competitors = 10
copy_threshold = 0.1  # parameter for copying a percentage from the old population to the new one

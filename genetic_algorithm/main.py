import numpy as np
import time
import argparse

from genetic_algorithm.population import Population
from genetic_algorithm import config


def main():
    t0 = time.time()
    # 1
    # generate initial population of N organisms randomly
    # but maybe with given conditions taken into account
    # i.e. one queen per row and one queen per column
    # one individual should probably look like
    # Individual = ([(0,0), (1,2), (2,1), ...,(7,7)], fitness value) as numpy array: np.
    # 2
    # compute fitness of each individual
    # population = individual.compute_fitness_of_all(population)
    my_population = Population(size=config.number_of_organisms, sort=True)

    # compute the max_fitness value, i.e. no collisions, for a given field_size
    max_fitness = config.field_size * (config.field_size - 1) * 0.5
    iterations = 0
    while my_population[0].fitness != max_fitness and iterations < config.max_iterations:
        iterations += 1
        if iterations % 100 == 0 and config.verbose:
            print(iterations, my_population.max_fitness_value())
        if iterations % 1000 == 0 and config.adapt_mutability:
            config.mutation_probability = min(iterations / 10000.0, 1)
        ### NEXT GENERATION ###
        # produce next generation
        # copy the fittest Organisms to the new population "they survive"
        # percentage is determined by config.copy_threshold
        new_pop = Population(my_population[:int(my_population.size() * config.copy_threshold)])

        # repeat as long as the new population is smaller than the population size
        while new_pop.size() < config.number_of_organisms:
            ### SELECTION ###
            # selecting two organisms from old generation for mating
            # choose fitter ones, maybe not THE fittest
            parent1 = my_population.select_parent(method=config.parent_selection_method)
            parent2 = my_population.select_parent(method=config.parent_selection_method)

            ### CROSSOVER ###
            # recombine genetic material with probability p_c, i.e. crossover
            # mutate with very small probability
            # create a pair of children
            child1, child2 = my_population.crossover(parent1, parent2, method=config.crossover_method)

            ### MUTATION ###
            # let the children mutate with a small probability
            if np.random.uniform() < config.mutation_probability:
                child1.mutate(config.mutation_method)
            if np.random.uniform() < config.mutation_probability:
                child2.mutate(config.mutation_method)

            # insert into new population
            new_pop.add(child1, child2)

        # 4
        # replace the old population with the new one
        my_population = new_pop
        my_population.sort()

        # 5
        # if satisfied with fittest individual -> finish
        # if population converged, i.e. 95% of individuals are the same -> finish
        # otherwise go to 3 and repeat

    the_winner = my_population.fittest_organism()
    if config.verbose:
        print(the_winner)
        print(
            f'Number of Iterations:{iterations}\nTotal Time: {time.time()-t0}\nAverage Fitness of final Population: {my_population.compute_average_fitness()}')
    else:
        return iterations, time.time() - t0, the_winner.fitness, my_population.compute_average_fitness()


if __name__ == '__main__':
    main()

import numpy as np
import random
from typing import List, Tuple

from genetic_algorithm.organism import Organism
from genetic_algorithm.population import Population
from genetic_algorithm import config


def main():
    # 1
    # generate initial population of N organisms randomly
    # but maybe with given conditions taken into account
    # i.e. one queen per row and one queen per column
    # one individual should probably look like
    # Individual = ([(0,0), (1,2), (2,1), ...,(7,7)], fitness value) as numpy array: np.
    # 2
    # compute fitness of each individual
    # population = individual.compute_fitness_of_all(population)
    my_population = Population(config.number_of_organisms, sort=True)


    max_fitness = config.field_size*(config.field_size-1) * 0.5
    while my_population[0].fitness != max_fitness:
        average_fitness = my_population.compute_average_fitness()
        print(my_population[0].fitness, max_fitness)
        # print(average_fitness)
        # print(my_population[0].genotype)

        # 3
        # produce new generation by:
        # 3.1.
        new_pop = Population()
        while new_pop.size() < my_population.size():
            # selecting two organisms from old generation for mating
            # choose fitter ones, maybe not THE fittest
            parent1, parent2 = my_population.choose_parents()

            # 3.2
            # recombine genetic material with probability p_c, i.e. crossover
            # mutate with very small probability
            # create a pair of children

            # child1, child2 = my_population.crossover(parent1, parent2, method='uniform')
            child1, child2 = my_population.crossover(parent1, parent2, method='one_point')
            if np.random.uniform() < config.mutation_probablity:
                child1.mutate()
            if np.random.uniform() < config.mutation_probablity:
                child2.mutate()
            # 3.3
            # insert into population
            new_pop.add(child1, child2)
        # 3.4
        # if the size of new population is smaller than the old one, repeat from 3.1 onwards

        # 4
        # replace the old population with the new one
        my_population = new_pop
        my_population.sort()

        # 5
        # if satisfied with fittest individual -> finish
        # if population converged, i.e. 95% of individuals are the same -> finish
        # otherwise go to 3 and repeat


    if len(my_population[0].genotype) != len(set(my_population[0].genotype)):
        print('ERROR!!!')
    print(my_population[0])
    my_population[0].compute_fitness()
    print(average_fitness)


if __name__ == '__main__':
    main()

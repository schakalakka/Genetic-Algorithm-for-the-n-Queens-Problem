import numpy as np
import random
from typing import List

from genetic_algorithm import individual
from genetic_algorithm import config


def sort_population(population: (np.ndarray, int)) -> (np.ndarray, int):
    """
    Sort the population by fitness value in descending order
    :param population:
    :return: sorted population
    """
    return sorted(population, key=lambda x: x.fitness, reverse=True)


def generate_initial_population(population_size: int) -> List[(np.ndarray, int)]:
    """

    :param population_size: int
    :return: population
    """
    population = [individual.generate_individual() for i in range(population_size)]
    return population


def crossover(individual1, individual2):
    pass

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
    population = generate_initial_population(config.number_of_organisms)

    population = sort_population(population)
    print(population)

    while population[0].fitness != 0:
        # 3
        # produce new generation by:
        # 3.1.
        # selecting two organisms from old generation for mating
        # choose fitter ones, maybe not THE fittest
        population2 = population.copy()
        individual1 = population2[int(np.log(random.random(0, np.exp(config.field_size))))]
        population2.remove(individual1)
        individual2 = population2[int(np.log(random.random(0, np.exp(config.field_size - 1))))]
        population2.remove(individual2)

        # 3.2
        # recombine genetic material with probability p_c, i.e. crossover
        # mutate with very small probability
        # create a pair of children

        crossover(individual1, individual2)

        # 3.3
        # compute the fitness of children and insert into population

        # 3.4
        # if the size of new population is smaller than the old one, repeat from 3.1 onwards

        # 4
        # replace the old population with the new one

        # 5
        # if satisfied with fittest individual -> finish
        # if population converged, i.e. 95% of individuals are the same -> finish
        # otherwise go to 3 and repeat


if __name__ == '__main__':
    main()

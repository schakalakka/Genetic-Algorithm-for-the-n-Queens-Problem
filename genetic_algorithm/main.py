import numpy as np
import random
from typing import List, Tuple

from genetic_algorithm import organism
from genetic_algorithm import config


def sort_population(population: (np.ndarray, int)) -> (np.ndarray, int):
    """
    Sort the population by fitness value in descending order
    :param population:
    :return: sorted population
    """
    return sorted(population, key=lambda x: x.fitness, reverse=True)


def generate_initial_population(population_size: int) -> List[Tuple[np.ndarray, int]]:
    """

    :param population_size: int
    :return: population
    """
    population = [organism.generate_individual() for i in range(population_size)]
    return population


def crossover(parent1: organism.Organism, parent2: organism.Organism, method='one_point') -> Tuple[
    organism.Organism, organism.Organism]:
    """
    Returns crossover children computed by the given method
    If a random value is higher than the crossover probability the parents will be returned without any crossover
    :param parent1: Organism
    :param parent2: Organism
    :param method: str, can be 'uniform' or 'one_point'
    :return: two children
    """
    # if random value is higher than crossover probability no children will be produced
    # the parents will be returned
    if np.random.uniform() > config.crossover_probability:
        return parent1, parent2
    else:
        # if method is None use the default crossover method
        method = method if method else config.default_crossover_method
        if method is 'one_point':
            return one_point_crossover(parent1, parent2)
        elif method is 'uniform':
            return uniform_crossover(parent1, parent2)


def one_point_crossover(parent1: organism.Organism, parent2: organism.Organism) -> Tuple[
    organism.Organism, organism.Organism]:
    """
      Computes a one point crossover (for a random point) and produces two children
      :param parent1:
      :param parent2:
      :return: two children
      """
    crossover_point = np.random.randint(1, config.field_size)
    child1_genotype = np.concatenate(
        (parent1.genotype[:crossover_point], parent2.genotype[crossover_point:]), axis=0)
    child2_genotype = np.concatenate(
        (parent2.genotype[:crossover_point], parent1.genotype[crossover_point:]), axis=0)
    child1 = organism.Organism(child1_genotype, organism.compute_fitness(child1_genotype))
    child2 = organism.Organism(child2_genotype, organism.compute_fitness(child2_genotype))
    return child1, child2


def uniform_crossover(parent1: organism.Organism, parent2: organism.Organism) -> Tuple[
    organism.Organism, organism.Organism]:
    """
    Computes a uniform crossover and produces two children
    :param parent1:
    :param parent2:
    :return: two children
    """
    # generate a series of length config.fieldsize of 0s and 1s
    coinflips = random.randint(0, 1, config.field_size)

    # filter the indexes for which the coinflip is 0 or 1 respectively
    indexes_with_0 = [i for i, coinflip in enumerate(coinflips) if coinflip == 0]
    indexes_with_1 = [i for i, coinflip in enumerate(coinflips) if coinflip == 1]

    # compute genotype crossover
    # for child1 take the chromosomes from parent 1 if coinflip is 0
    # and from parent 2 if coinflip is 1
    # for child 2 vice versa
    child1_genotype = np.concatenate(parent1.genotype[indexes_with_0],
                                     parent2.genotype[indexes_with_1], axis=0)
    child2_genotype = np.concatenate(parent1.genotype[indexes_with_1],
                                     parent2.genotype[indexes_with_0], axis=0)

    # create organisms and compoute fitness
    child1 = organism.Organism(child1_genotype, organism.compute_fitness(child1_genotype))
    child2 = organism.Organism(child2_genotype, organism.compute_fitness(child2_genotype))
    return child1, child2


def compute_average_fitness(population):
    return sum([x.fitness for x in population]) / len(population)


def choose_parents(population):
    # compute accumulated fitnesses
    accumulated_fitness_values = np.cumsum([x.fitness for x in population])
    # choose between 0 and max(accumulated_fitness_values) = last element of
    # list (because they were sorted beforehand)
    R = np.random.randint(0, accumulated_fitness_values[-1], 2)
    parent1 = population[next(i for i, acc_fitness in enumerate(accumulated_fitness_values) if acc_fitness >= R[0])]
    parent2 = population[next(i for i, acc_fitness in enumerate(accumulated_fitness_values) if acc_fitness >= R[1])]
    return parent1, parent2


def choose_parents_fast(population):
    """
    !!!!!!!!DOES NOT WORK YET!!!!!!!!!
    :param population:
    :return:
    """
    parent1 = population[int(np.log(np.random.randint(0, np.exp(config.field_size))))]
    parent2 = population[int(np.log(np.random.randint(0, np.exp(config.field_size))))]
    np.random.uniform()
    return parent1, parent2


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
    # print(population)

    while population[0].fitness != 0:
        average_fitness = compute_average_fitness(population)
        print(population[0].fitness)

        # 3
        # produce new generation by:
        # 3.1.
        new_pop = []
        while len(new_pop) < len(population):
            # selecting two organisms from old generation for mating
            # choose fitter ones, maybe not THE fittest
            parent1, parent2 = choose_parents(population)

            # 3.2
            # recombine genetic material with probability p_c, i.e. crossover
            # mutate with very small probability
            # create a pair of children

            child1, child2 = crossover(parent1, parent2)
            # 3.3
            # compute the fitness of children and insert into population
            new_pop.extend([child1, child2])
        # 3.4
        # if the size of new population is smaller than the old one, repeat from 3.1 onwards

        # 4
        # replace the old population with the new one
        population = new_pop
        sort_population(population)


        # 5
        # if satisfied with fittest individual -> finish
        # if population converged, i.e. 95% of individuals are the same -> finish
        # otherwise go to 3 and repeat


if __name__ == '__main__':
    main()

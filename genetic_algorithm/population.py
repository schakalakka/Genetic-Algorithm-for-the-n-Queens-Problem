from typing import Tuple
import numpy as np

from genetic_algorithm.organism import Organism
from genetic_algorithm import config


class Population:

    def __init__(self, size=None, sort=True):
        """
        Generates a list of a given size of Organisms with the genotype that there is only queen per row and column.
        If no size is given an empty population is created
        :param size: int
        """
        if size is None:
            self.population = []
            self.accumulated_fitness_values = []
        else:
            self.population = [Organism() for _ in range(size)]
            if sort:
                self.sort()
        self.accumulated_fitness_values = []
        self.accumulated_fitness_computed = False

    def __getitem__(self, item: int) -> Organism:
        """
        Returns Organism in population with index item
        :param item: index
        :return: Organism
        """
        return self.population[item]

    def size(self) -> int:
        """
        Returns the size of the population. Same as len(my_population).
        :return: number of individuals in the population
        """
        return len(self.population)

    def __len__(self) -> int:
        """
        Returns the size of the population. Same as self.size().
        :return: Number of Organisms in the population
        """
        return len(self.population)

    def add(self, *args):
        """
        Adds arbitrarily many Organisms to the Population
        :param args: one or more Organisms
        :return:
        """
        for arg in args:
            self.population.append(arg)

    def sort(self, reverse=True):
        """
        Sort the population by fitness value in descending order (by default)
        :param reverse: If False it is sorted in ascending order)
        """
        self.population = sorted(self.population, key=lambda x: x.fitness, reverse=reverse)

    def compute_average_fitness(self) -> float:
        """
        Computes the average fitness of the population
        :return:
        """
        return sum([x.fitness for x in self.population]) / len(self.population)

    def fittest_organism(self, force_sorting=False) -> Organism:
        """
        Returns the fittest Organism - the complete organism, i.e. genotype AND fitness.
        Generally it assumes the population is sorted descendingly and it will return the first element in the
        population.
        If not one can force_sorting=True and sort the population before returning.
        :param force_sorting: default False
        :return: Organism
        """
        if force_sorting:
            self.sort()
        return self.population[0]

    def compute_accumulated_fitness_values(self):
        """
        Computes the accumulated fitness values.
        Example: Let the fitness values be like [8,5,3,2] (sorted descendingly)
        then the accumlated fitnesses are [8,13,16,18].
        Useful for choosing fitter Organisms but not THE fittest ones.
        :return:
        """
        self.accumulated_fitness_values = np.cumsum([x.fitness for x in self.population])
        self.accumulated_fitness_computed = True

    def max_fitness_value(self, force_sorting=False) -> int:
        """
        Returns only the fitness value of the fittest Organism.
        Generally it assumes the population is sorted descendingly and it will return the first element's fitness
        in the population.
        If not one can force_sorting=True and sort the population before returning.
        :param force_sorting: default False
        :return: int - fitness value
        """
        if force_sorting:
            self.sort()
        return self.population[0].fitness

    @staticmethod
    def crossover(parent1: Organism, parent2: Organism, method='one_point') -> Tuple:
        """
        Convenience function for computing two children via crossover
        :param parent1: Organism
        :param parent2: Organism
        :param method: default 'one_point'
        :return: two children
        """
        return parent1.crossover(parent2, method=method)

    def choose_parents(self):
        """
        Choose two parents for crossover. It will choose fitter individuals with a higher probability
        :return: two parents/Organisms
        """
        # compute accumulated fitnesses if not already done
        if not self.accumulated_fitness_computed:
            self.compute_accumulated_fitness_values()
        # choose between 0 and max(accumulated_fitness_values) = last element of list
        # (because they were sorted beforehand)
        a, b = np.random.randint(0, self.accumulated_fitness_values[-1], 2)
        parent1 = self.population[
            next(i for i, acc_fitness in enumerate(self.accumulated_fitness_values) if acc_fitness >= a)]
        parent2 = self.population[
            next(i for i, acc_fitness in enumerate(self.accumulated_fitness_values) if acc_fitness >= b)]
        return parent1, parent2

    def choose_parents_fast(self):
        """
        !!!!!!!!DOES NOT WORK YET!!!!!!!!!
        :return:
        """
        parent1 = self.population[int(np.log(np.random.randint(0, np.exp(config.field_size))))]
        parent2 = self.population[int(np.log(np.random.randint(0, np.exp(config.field_size))))]
        np.random.uniform()
        return parent1, parent2

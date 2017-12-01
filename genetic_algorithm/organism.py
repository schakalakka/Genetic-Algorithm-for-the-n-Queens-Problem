import numpy as np
import random
from typing import Tuple

from . import config


class Organism:

    def __init__(self, genotype=None):
        """
        Creates an Organism from either
        A given np.ndarray of the form [(0,0), (1,3), ...]
        A given list of tuples of the form [(0,0), (1,3), ...]
        or if genotype=None one Organism is generated randomly
        :param genotype: np.ndarray, list or None
        """
        if genotype is None:
            rows = list(np.arange(config.field_size))
            cols = list(np.arange(config.field_size))
            genotype = []
            while rows and cols:
                current_row = rows[random.randint(0, len(rows) - 1)]
                current_col = cols[random.randint(0, len(cols) - 1)]
                rows.remove(current_row)
                cols.remove(current_col)
                genotype.append((current_row, current_col))
            self.genotype = np.array(genotype)
        elif type(genotype) is np.ndarray:
            self.genotype = genotype
        elif type(genotype) is list:
            self.genotype = np.array(genotype)
        else:
            print('Type of genotype is not correct. Either specify np.ndarray, list or None.')
        self.fitness = self.compute_fitness()

    def compute_fitness(self) -> int:
        """
        Computes the fitness value
        :return:
        """
        return self.compute_fitness_only_diagonal()

    def compute_fitness_only_diagonal(self) -> int:
        """
        Computes the fitness for an individual
        In particular count the number of times an individual collides with another individual.

        !!!!!!!!!!This version assumes there is only one queen per row and columns!!!!!!!
        Because there is only one queen per row and column this can only happen diagonally.
        This means if the the row/vertical distance is equal to the column/horizontal distance

        :return: fitness value
        """
        fitness = 0
        for i, pos1 in enumerate(self.genotype):
            for pos2 in self.genotype[i + 1:]:
                # compare the vertical and horizontal distances
                # if equal subtract one from base fitness
                if abs(pos1[0] - pos2[0]) == abs(pos1[1] - pos2[1]):
                    fitness -= 1
        return config.field_size * (config.field_size + 1) * 0.5 + fitness

    def compute_fitness_with_diagonal(self) -> int:
        """
        Computes the fitness for an Organism
        In particular count the number of times a queen collides with another queen and
        substract this number from n*(n+1)/2 (the maximal number of collisions)

        :return: fitness value
        """
        fitness = 0
        for i, pos1 in enumerate(self.genotype):
            for pos2 in self.genotype[i + 1:]:
                # compare the vertical and horizontal distances
                # if equal subtract one from base fitness
                if abs(pos1[0] - pos2[0]) == abs(pos1[1] - pos2[1]):
                    fitness -= 1
                if pos1[0] == pos2[0] or pos1[1] == pos2[1]:
                    fitness -= 1
        # add current fitness value from maximal number of collisions
        # for n queens it is n + (n-1) + (n-2) +... + 1 because alle queens can be in one row
        # and collide with each other
        return config.field_size * (config.field_size + 1) * 0.5 + fitness

    def crossover(self, parent2, method='one_point') -> Tuple:
        """
        Returns crossover children computed by the given method
        If a random value is higher than the crossover probability the parents will be returned without any crossover
        :param self: Organism, parent1
        :param parent2: Organism
        :param method: str, can be 'uniform' or 'one_point'
        :return: two children
        """
        # if random value is higher than crossover probability no children will be produced
        # the parents will be returned
        if np.random.uniform() > config.crossover_probability:
            return self, parent2
        else:
            # if method is None use the default crossover method
            method = method if method else config.default_crossover_method
            if method is 'one_point':
                return self.one_point_crossover(parent2)
            elif method is 'uniform':
                return self.uniform_crossover(parent2)

    def one_point_crossover(self, parent2) -> Tuple:
        """
        Computes a one point crossover (for a random point) and produces two children
        :param self: Organism, "parent1"
        :param parent2: Organism
        :return: two children/Organisms
        """
        crossover_point = np.random.randint(1, config.field_size)
        child1_genotype = np.concatenate(
            (self.genotype[:crossover_point], parent2.genotype[crossover_point:]), axis=0)
        child2_genotype = np.concatenate(
            (parent2.genotype[:crossover_point], self.genotype[crossover_point:]), axis=0)
        child1 = Organism(child1_genotype)
        child2 = Organism(child2_genotype)
        return child1, child2

    def uniform_crossover(self, parent2) -> Tuple:
        """
        Computes a uniform crossover and produces two children
        :param self: Organism, parent1
        :param parent2: Organism
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
        child1_genotype = np.concatenate((self.genotype[indexes_with_1], parent2.genotype[indexes_with_1]), axis=0)
        child2_genotype = np.concatenate((self.genotype[indexes_with_1], parent2.genotype[indexes_with_0]), axis=0)

        # create organisms and compoute fitness
        child1 = Organism(child1_genotype)
        child2 = Organism(child2_genotype)
        return child1, child2

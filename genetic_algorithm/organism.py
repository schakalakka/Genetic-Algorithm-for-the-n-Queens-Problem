import numpy as np
import random
from typing import Tuple

from . import config


class Organism:

    def __init__(self, genotype=None):
        """
        Creates an Organism from either
        A given np.ndarray of the form [1,2,4,3,0,5]
        A given list of tuples of the form [1,2,4,3,0,5]
        or if genotype=None one Organism is generated randomly
        :param genotype: np.ndarray, list or None
        """
        if genotype is None:
            self.genotype = np.random.randint(0, config.field_size, config.field_size)
        elif type(genotype) is np.ndarray:
            self.genotype = genotype
        elif type(genotype) is list:
            self.genotype = np.array(genotype)
        else:
            print('Type of genotype is not correct. Either specify np.ndarray, list or None.')
        self.compute_fitness()  # set fitness

    def __repr__(self):
        """
        Representation function for printing, i.e. print(organism)
        :return:
        """
        repr = [f'Fitness: {self.fitness}']
        repr.append(f'Genotype: {self.genotype}')
        repr.append((config.field_size*2+1)*'-')
        for i in self.genotype:
            repr.append('|'+i * ' |' + 'Q|' + (config.field_size - i-1) * ' |')
            repr.append((config.field_size*2+1)*'-')
        return '\n'.join(repr)


    def compute_fitness(self):
        """
        Computes and sets(!) the fitness for an Organism
        In particular count the number of times a queen collides with another queen and
        subtract this number from n*(n+1)/2 (the maximal number of collisions)

        :return:
        """
        fitness = config.field_size * (config.field_size - 1) * 0.5
        for i, pos1 in enumerate(self.genotype):
            for j, pos2 in enumerate(self.genotype[i + 1:]):
                # j+1 is equal to the differences in rows
                # remember there can only be one queen per row but several per column
                # compare j+1 with the difference in columns
                # if equal the queens collides diagonally
                if abs(pos1 - pos2) == j+1:
                    # if equal subtract one from base fitness
                    fitness -= 1
                if pos1 == pos2:
                    # the two queens are in one column
                    fitness -= 1
        # add current fitness value from maximal number of collisions
        # for n queens it is n + (n-1) + (n-2) +... + 1 because all queens can be in one column
        # and collide with each other
        self.fitness =  fitness

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
        coinflips = np.random.randint(0, 1, config.field_size)

        # filter the indexes for which the coinflip is 0 or 1 respectively
        indexes_with_0 = [i for i, coinflip in enumerate(coinflips) if coinflip == 0]
        indexes_with_1 = [i for i, coinflip in enumerate(coinflips) if coinflip == 1]

        # compute genotype crossover
        # for child1 take the chromosomes from parent 1 if coinflip is 0
        # and from parent 2 if coinflip is 1
        # for child 2 vice versa
        child1_genotype = np.concatenate((self.genotype[indexes_with_0], parent2.genotype[indexes_with_1]), axis=0)
        child2_genotype = np.concatenate((self.genotype[indexes_with_1], parent2.genotype[indexes_with_0]), axis=0)

        # create organisms and compoute fitness
        child1 = Organism(child1_genotype)
        child2 = Organism(child2_genotype)
        return child1, child2

    def mutate(self):
        """
        Mutates an Organism, i.e. it chooses a random row (index) and a random column and overwrites it.
        :return:
        """
        row = np.random.randint(0, config.field_size)
        col = np.random.randint(0, config.field_size)
        self.genotype[row] = col
        self.compute_fitness()

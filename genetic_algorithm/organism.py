from collections import namedtuple
import numpy as np
import random

from . import config

Organism = namedtuple('Organism', ['genotype', 'fitness'])


def generate_individual() -> Organism:
    """
    Compute one Organism and its fitness

    An Organism looks like (genotype, fitness) = (np.array([(0,3), (1,0), (2,2), (3,1)]), -1) for a config.field_size
    of 4

    :return: Organism which is a pair of (genotype, fitness)=(np.ndarray, int)
    """
    rows = list(np.arange(config.field_size))
    cols = list(np.arange(config.field_size))
    genotype = []
    while rows and cols:
        current_row = rows[random.randint(0, len(rows) - 1)]
        current_col = cols[random.randint(0, len(cols) - 1)]
        rows.remove(current_row)
        cols.remove(current_col)
        genotype.append((current_row, current_col))
    genotype = np.array(genotype)
    return Organism(genotype, compute_fitness(genotype))


def compute_fitness_only_diagonal(genotype: np.ndarray) -> int:
    """
    Computes the fitness for an individual
    In particular count the number of times an individual collides with another individual.

    !!!!!!!!!!This version assumes there is only one queen per row and columns!!!!!!!
    Because there is only one queen per row and column this can only happen diagonally.
    This means if the the row/vertical distance is equal to the column/horizontal distance

    :param genotype: np.ndarray with config.field_size many pairs of integers
    :return: fitness value
    """
    fitness = 0
    for i, pos1 in enumerate(genotype):
        for pos2 in genotype[i + 1:]:
            # compare the vertical and horizontal distances
            # if equal subtract one from base fitness
            if abs(pos1[0] - pos2[0]) == abs(pos1[1] - pos2[1]):
                fitness -= 1
    return config.field_size * (config.field_size + 1) * 0.5 +  fitness


def compute_fitness(genotype: np.ndarray) -> int:
    """
    Computes the fitness for an Organism
    In particular count the number of times a queen collides with another queen and
    substract this number from n*(n+1)/2 (the maximal number of collisions)

    :param genotype: np.ndarray with config.field_size many pairs of integers
    :return: fitness value
    """
    fitness = 0
    for i, pos1 in enumerate(genotype):
        for pos2 in genotype[i + 1:]:
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

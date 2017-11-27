import numpy as np
import random


def generate_initial_population(n: int):
    population = [generate_indvidual() for i in range(n)]
    return population


def generate_indvidual():
    rows = list(np.arange(8))
    cols = list(np.arange(8))
    individual = []
    while rows and cols:
        current_row = rows[random.randint(0, len(rows) - 1)]
        current_col = cols[random.randint(0, len(cols) - 1)]
        rows.remove(current_row)
        cols.remove(current_col)
        individual.append((current_row, current_col))
    return np.array(individual)


def compute_fitness(individual):
    return None


def compute_fitness_of_all():
    return None


def main():
    number_of_organisms = 100

    # 1
    # generate initial population of N organisms randomly
    # but maybe with given conditions taken into account
    # i.e. one queen per row and one queen per column
    # one individual should probably look like
    # I = [(0,0), (1,2), (2,1), ...,(7,7)] as numpy array: np.
    population = generate_initial_population(number_of_organisms)

    # 2
    # compute fitness of each individual
    compute_fitness_of_all()

    # 3
    # produce new generation by:
    # 3.1.
    # selecting two organisms from old generation for mating
    # choose fitter ones, maybe not THE fittest

    # 3.2
    # recombine genetic material with probability p_c, i.e. crossover
    # mutate with very small probability
    # create a pair of children

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

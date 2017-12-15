from typing import Tuple
import numpy as np

from organism import Organism
import config


class Population:

    def __init__(self, population=None, size=None, sort=True):
        """
        Generates a list of a given size of Organisms with the genotype that there is only queen per row and column.
        If no size is given an empty population is created
        :param population: if not None creates a population from a given (sub) population
        :param size: int
        :param sort: if True it will sort the population
        """
        if population:
            self.population = population
            self.sort()
        else:
            if size is None:
                self.population = []
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
    def crossover(parent1: Organism, parent2: Organism, method: str) -> Tuple:
        """
        Convenience function for computing two children via crossover
        :param parent1: Organism
        :param parent2: Organism
        :param method: 'pmx', 'order_based', 'position_based' or 'random'
        :return: two children
        """
        return parent1.crossover(parent2, method=method)

    ####################################################################################################################
    ## Selection Methods
    ####################################################################################################################

    def select_parent(self, method, **kwargs) -> Organism:
        """
        Switch function for choosing the selection method for parents
        Possible methods:
        'truncation': truncate the population and choose randomly from the fittest x percent,
                        takes additional argument 'truncation_threshold'
        'tournament': choose several competitors/Organisms for a tournament and take the fittest one,
                        takes an additional argument 'competitors' determining the amount of
                        competitors in the tournament
        'roulette': choose randomly with a higher probability for fitter individuals according to their fitness values
        'random': randomly choose one from the methods above
        :param method: 'random', 'tournament', 'truncation', 'roulette'
        :return: parent/Organism
        """
        if method is 'roulette':
            return self.roulette_wheel_selection()
        elif method is 'truncation':
            return self.truncation_selection(kwargs.get('truncation_threshold', config.truncation_threshold))
        elif method is 'tournament':
            return self.tournament_selection(kwargs.get('competitors', config.tournament_competitors))
        elif method is 'random':
            methods_without_random = config.selection_method_list
            return self.select_parent(method=methods_without_random[np.random.randint(0, len(methods_without_random))])

    def roulette_wheel_selection(self) -> Organism:
        """
        Roulette Wheel Selection
        Choose parent for crossover. It will choose fitter individuals with a higher probability by computing
        the accumulated fitnesses.
        :return: two parents/Organisms
        """
        # compute accumulated fitnesses if not already done
        if not self.accumulated_fitness_computed:
            self.compute_accumulated_fitness_values()
        # choose between 0 and max(accumulated_fitness_values) = last element of list
        # (because they were sorted beforehand)
        a, b = np.random.randint(0, self.accumulated_fitness_values[-1], 2)
        parent = self.population[
            next(i for i, acc_fitness in enumerate(self.accumulated_fitness_values) if acc_fitness >= a)]
        return parent

    def truncation_selection(self, truncation_threshold=0.5) -> Organism:
        """
        Truncation Selection:
        Selects an Organism randomly from the best x% of the population.
        If the truncation_threshold is 0.5 then only the best 50% Organisms are considered.
        Too low truncation_threshold values are more elitist
        :param truncation_threshold: between 0 and 1, typically between 0.5 and 0.1
        :return: Organism
        """
        return self[np.random.randint(0, int(self.size() * truncation_threshold))]

    def tournament_selection(self, competitors=10) -> Organism:
        """
        Tournament selection:
        Select a number of Organisms from a population for a tournament
        and return the fittest one
        :param competitors: Number of randomly chosen Organisms for the tournament
        :return: Organism
        """
        choosen_for_tournament = Population(
            [self[i] for i in np.random.randint(0, config.number_of_organisms, competitors)])
        choosen_for_tournament.sort()
        return choosen_for_tournament[0]

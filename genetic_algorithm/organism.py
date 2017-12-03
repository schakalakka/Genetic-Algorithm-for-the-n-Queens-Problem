import numpy as np
from typing import Tuple

from genetic_algorithm import config


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
        self.fitness = 0
        self.compute_fitness()  # set fitness

    def __repr__(self):
        """
        Representation function for printing, i.e. print(organism)
        :return:
        """
        repr = [f'Fitness: {self.fitness}']
        repr.append(f'Genotype: {self.genotype}')
        repr.append((config.field_size * 2 + 1) * '-')
        for i in self.genotype:
            repr.append('|' + i * ' |' + 'Q|' + (config.field_size - i - 1) * ' |')
            repr.append((config.field_size * 2 + 1) * '-')
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
                if abs(pos1 - pos2) == j + 1:
                    # if equal subtract one from base fitness
                    fitness -= 1
                if pos1 == pos2:
                    # the two queens are in one column
                    fitness -= 1
        # add current fitness value from maximal number of collisions
        # for n queens it is n + (n-1) + (n-2) +... + 1 because all queens can be in one column
        # and collide with each other
        self.fitness = fitness

    ####################################################################################################################
    ## Crossover Methods
    ####################################################################################################################

    def crossover(self, parent2, method) -> Tuple:
        """
        Returns crossover children computed by the given method
        If a random value is higher than the crossover probability the parents will be returned without any crossover
        :param self: Organism, parent1
        :param parent2: Organism
        :param method: str, can be 'random', 'uniform', 'pmx' or 'one_point'
        :return: two children
        """
        # if random value is higher than crossover probability no children will be produced
        # the parents will be returned
        if np.random.uniform() > config.crossover_probability:
            return self, parent2
        else:
            # if method is None use the default crossover method
            method = method if method else config.crossover_method
            if method is 'one_point':
                return self.one_point_crossover(parent2)
            elif method is 'uniform':
                return self.uniform_crossover(parent2)
            elif method is 'pmx':
                self.pmx_crossover(parent2)
            elif method is 'random':
                method_list = ['uniform', 'one_point', 'pmx']
                return self.crossover(parent2, method=method_list[np.random.randint(0, len(method_list))])

    def pmx_crossover(self, parent2) -> Tuple:
        pass

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

    ####################################################################################################################
    ## Mutation Methods
    ####################################################################################################################

    def mutate(self, method):
        """
        General mutation method. Chooses the specific mutation method given by 'method'.
        Possible methods:   'exchange': switch two rows randomly
                            'scramble': choose random segment and shuffle its values
                            'single': choose one row randomly and change its column
                            'displacement': choose a segment and move it to another point in the array
                            'insertion': choose one element and insert it in another place, like displacement but only
                                        with one element
                            'inversion': invert the order of a random segment
                            'displacement_inversion': invert the order of random segment and insert it elsewhere,
                                        displacement and inversion together
                            'random': one of the above methods randomly
        :param method: 'exchange', 'scramble', 'single', 'displacement', 'insertion', 'inversion',
                        'displacement_inversion', 'random'
        :return:
        """
        if method is 'single':
            self.single_mutation()
        elif method is 'exchange':
            self.exchange_mutation()
        elif method is 'scramble':
            self.scramble_mutation()
        elif method is 'displacement':
            self.displacement_mutation()
        elif method is 'inversion':
            self.inversion_mutation()
        elif method is 'insertion':
            self.insertion_mutation()
        elif method is 'displacement_inversion':
            self.displacement_inversion_mutation()
        elif method is 'random':
            method_list = ['exchange', 'scramble', 'single', 'displacement', 'insertion', 'inversion',
                           'displacement_inversion']
            self.mutate(method=method_list[np.random.randint(0, len(method_list))])

    def single_mutation(self):
        """
        Single Mutation:
        It chooses a random row (index) and a random column and overwrites it with another value (i.e. column).
        :return:
        """
        row = np.random.randint(0, config.field_size)
        col = np.random.randint(0, config.field_size)
        self.genotype[row] = col
        self.compute_fitness()

    def exchange_mutation(self):
        """
        Exchange Mutation:
        Select two rows randomly and exchange them.
        It is possible/allowed that the same rows are selected. Then nothing will happen
        :return:
        """
        row1 = np.random.randint(0, config.field_size)
        row2 = np.random.randint(0, config.field_size)
        tmp = self.genotype[row2]
        self.genotype[row2] = self.genotype[row1]
        self.genotype[row1] = tmp
        self.compute_fitness()

    def scramble_mutation(self):
        """
        Scramble Mutation:
        Select two indexes randomly and shuffle/scramble the segment between them
        :return:
        """
        # get two random integers in the range, the lower is the start, the greater is the end of the segment
        begin_and_end = np.random.randint(0, config.field_size, 2)
        if begin_and_end[0] != begin_and_end[1]:  # if begin and end are the same there is nothing to do
            # sort such that begin_and_end[0] is the lower one, i.e. the begin of the segment
            begin_and_end.sort()
            # shuffle values in the segment (numpy does it in-place)
            np.random.shuffle(self.genotype[begin_and_end[0]: begin_and_end[1]])
            self.compute_fitness()

    def displacement_mutation(self):
        """
        Displacement Mutation:
        Chooses a random segment (i.e. start and end index) and inserts this segment to a random position
        :return:
        """
        # get two random integers in the range, the lower is the start, the greater is the end of the segment
        begin_and_end = np.random.randint(0, config.field_size, 2)
        if begin_and_end[0] != begin_and_end[1]:  # if begin and end are the same there is nothing to do
            # sort such that begin_and_end[0] is the lower one, i.e. the begin of the segment
            begin_and_end.sort()
            # get new insertion position
            new_position = np.random.randint(0, config.field_size - (begin_and_end[1] - begin_and_end[0]))
            # copy the values from the segment to a temp variable
            vals = self.genotype[begin_and_end[0]: begin_and_end[1]]
            # delete segment
            self.genotype = np.delete(self.genotype, range(begin_and_end[0], begin_and_end[1]))
            # insert segment from new position
            self.genotype = np.insert(self.genotype, new_position, vals)
            # compute new fitness again
            self.compute_fitness()

    def insertion_mutation(self):
        """
        Insertion Mutation:
        chooses one row/index randomly, takes the element and inserts it at another random position
        :return:
        """
        from_index = np.random.randint(0, config.field_size)
        to_index = np.random.randint(0, config.field_size - 1)  # one less because we temporarily remove one element
        val = self.genotype[from_index]
        self.genotype = np.delete(self.genotype, from_index)
        self.genotype = np.insert(self.genotype, to_index, val)
        self.compute_fitness()

    def inversion_mutation(self):
        """
        Inversion Mutation:
        Invert/flip a randomly chosen segment in the genotype
        :return:
        """
        # get two random integers in the range, the lower is the start, the greater is the end of the segment
        begin_and_end = np.random.randint(0, config.field_size, 2)
        if begin_and_end[0] != begin_and_end[1]:  # if begin and end are the same there is nothing to do
            # sort such that begin_and_end[0] is the lower one, i.e. the begin of the segment
            begin_and_end.sort()
            # concatenate:  part before flipped segment
            #               flipped/inverted segment
            #               part after flipped segment
            self.genotype = np.concatenate((self.genotype[:begin_and_end[0]],
                                            np.flip(self.genotype[begin_and_end[0]: begin_and_end[1]], axis=0),
                                            self.genotype[begin_and_end[1]:]))
            self.compute_fitness()

    def displacement_inversion_mutation(self):
        """
        Displacement Mutation:
        Chooses a random segment (i.e. start and end index), flips/inverts it and
        inserts this segment to a random position
        :return:
        """
        # get two random integers in the range, the lower is the start, the greater is the end of the segment
        begin_and_end = np.random.randint(0, config.field_size, 2)
        if begin_and_end[0] != begin_and_end[1]:  # if begin and end are the same there is nothing to do
            # sort such that begin_and_end[0] is the lower one, i.e. the begin of the segment
            begin_and_end.sort()
            # get new insertion position
            new_position = np.random.randint(0, config.field_size - (begin_and_end[1] - begin_and_end[0]))
            # copy the values from the segment to a temp variable, necessary for deleting
            vals = self.genotype[begin_and_end[0]: begin_and_end[1]]
            # flip the temp values, necessary for inserting
            vals_flipped = np.flip(vals, axis=0)
            # delete segment
            self.genotype = np.delete(self.genotype, range(begin_and_end[0], begin_and_end[1]))
            # insert flipped segment from new position
            self.genotype = np.insert(self.genotype, new_position, vals_flipped)
            # compute new fitness again
            self.compute_fitness()

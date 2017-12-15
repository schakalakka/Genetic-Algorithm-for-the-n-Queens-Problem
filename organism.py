import numpy as np
from typing import Tuple
import sys

import config


class Organism:

    def __init__(self, genotype=None):
        """
        Creates an Organism from either
            A given np.ndarray of the form [1,2,4,3,0,5]
            A given list of tuples of the form [1,2,4,3,0,5]
            or if genotype=None one Organism is generated randomly
        There can only be one queen per row and column!
        Per row is guaranteed because the index determines the row.
        Per column is guaranteed with np.unique, i.e. each element (column) does only occur once.
        :param genotype: np.ndarray, list or None
        """
        if genotype is None:
            # self.genotype = np.random.randint(0, config.field_size, config.field_size)
            self.genotype = np.arange(config.field_size)
            np.random.shuffle(self.genotype)
        elif type(genotype) is np.ndarray:
            if len(genotype) == len(np.unique(genotype)):
                self.genotype = genotype
            else:
                print('There are several queens per column! Exit.')
                sys.exit(1)
        elif type(genotype) is list:
            if len(genotype) == len(np.unique(genotype)):
                self.genotype = np.array(genotype)
            else:
                print('There are several queens per column! Exit.')
                sys.exit(1)
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
        # repr.append((config.field_size * 2 + 1) * '-')
        for i in self.genotype:
            repr.append('|' + i * ' |' + 'Q|' + (config.field_size - i - 1) * ' |')
            # repr.append((config.field_size * 2 + 1) * '-')
        return '\n'.join(repr)

    def compute_fitness(self):
        """
        Computes and sets(!) the fitness for an Organism
        In particular count the number of times a queen collides with another queen and
        subtract this number from n*(n-1)/2 (the maximal number of collisions)

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
        :param method: str, can be 'random', 'order_bases', 'pmx'
        :return: two children
        """
        # if random value is higher than crossover probability no children will be produced
        # the parents will be returned
        if np.random.uniform() > config.crossover_probability:
            return self, parent2
        else:
            # if method is None use the default crossover method
            method = method if method else config.crossover_method
            if method is 'order_based':
                return self.order_based_crossover(parent2)
            elif method is 'position_based':
                return self.position_based_crossover(parent2)
            elif method is 'pmx':
                return self.pmx_crossover(parent2)
            elif method is 'random':
                method_list = config.crossover_method_list
                return self.crossover(parent2, method=method_list[np.random.randint(0, len(method_list))])

    def pmx_crossover(self, parent2) -> Tuple:
        """
        Computes a partially mapped crossover and produces two children
        :param self: Organism, "parent1"
        :param parent2: Organism
        :return: two children/Organisms
        """
        size = config.field_size
        cxpoint1 = np.random.randint(0, size)
        cxpoint2 = np.random.randint(0, size)

        if cxpoint2 < cxpoint1:
            cxpoint1, cxpoint2 = cxpoint2, cxpoint1
        cxpoint2 += 1

        child1_genotype = [None] * size
        child2_genotype = [None] * size

        # Copy a slice from first parent
        child1_genotype[cxpoint1:cxpoint2] = self.genotype[cxpoint1:cxpoint2]
        child2_genotype[cxpoint1:cxpoint2] = parent2.genotype[cxpoint1:cxpoint2]

        # Map the same slice in second parent to child using indices from first parent
        for ind, x in enumerate(parent2.genotype[cxpoint1:cxpoint2]):
            ind += cxpoint1
            if x not in child1_genotype:
                while child1_genotype[ind] is not None:
                    ind = list(parent2.genotype).index([self.genotype[ind]])
                child1_genotype[ind] = x

        for ind1, x in enumerate(self.genotype[cxpoint1:cxpoint2]):
            ind1 += cxpoint1
            if x not in child2_genotype:
                while child2_genotype[ind1] is not None:
                    try:
                        ind1 = list(self.genotype).index([parent2.genotype[ind1]])
                    except:
                        print('foo')
                child2_genotype[ind1] = x

        # Copy over the rest from the second parent
        for ind, x in enumerate(child1_genotype):
            if x is None:
                child1_genotype[ind] = parent2.genotype[ind]

        for ind1, x in enumerate(child2_genotype):
            if x is None:
                child2_genotype[ind1] = self.genotype[ind1]

        # create organisms and compute fitness
        child1 = Organism(child1_genotype)
        child2 = Organism(child2_genotype)
        return child1, child2

    def order_based_crossover(self, parent2) -> Tuple:
        """
        Order-based Crossover:
        We take random number of points from a parent genotype.
        The order of these points is kept and applied on the second parent.
        The remaining genotype elements are taken from the second parent.
        For the second child reverse the order of the parents.
        Example:  points = [1,2,5]
                  parent1.genotype = [2,5,0,3,6,1,4,7]
                  order_args_1 = [5,0,1]
                  parent2.genotype = [3,4,0,7,2,5,1,6]
                  order_args_2 = [4,0,5]
                  child1 = [3,4,None,7,2,None,None,6]
                  child2 = [2,None,None,3,6,1,None,7]
                  order_indices_1 = [2,5,6] -- indices of the order args in the other parent
                  order_indices_2 = [1,2,6] -- indices of the order args in the other parent

                  child1 = [3,4,5,7,2,0,1,6]
                  child2 = [2,4,0,3,6,1,5,7]

        :param parent2: Organism
        :return: Two children/Organisms
        """
        # determine randomly how many points are chosen
        number_of_points_to_choose = np.random.randint(1, config.field_size)
        # choose the specific points
        # create an array like [0,1,2,3,...,n]
        points = np.arange(0, config.field_size)
        # shuffle it randomly
        np.random.shuffle(points)
        # cut it to get only the first part
        points = points[0:number_of_points_to_choose]
        # sort
        points.sort()

        # Example:  points = [1,2,5]
        #           parent1.genotype = [2,5,0,3,6,1,4,7]
        #           order_args_1 = [5,0,1]
        #           parent2.genotype = [3,4,0,7,2,5,1,6]
        #           order_args_2 = [4,0,5]

        order_args_1 = self.genotype[points]
        order_args_2 = parent2.genotype[points]

        # copy the parents genotype to the children as a 'base'
        child1 = parent2.genotype.copy()
        child2 = self.genotype.copy()

        # get the indices of the order points
        # Example:  order_indices_1 = [2,5,6]
        #           order_indices_2 = [1,2,6]
        order_indices_1 = np.where(np.isin(parent2.genotype, order_args_1))
        order_indices_2 = np.where(np.isin(self.genotype, order_args_2))

        # apply the order on the points
        child1[order_indices_1] = order_args_1
        child2[order_indices_2] = order_args_2

        # create organisms and compute fitness
        child1 = Organism(child1)
        child2 = Organism(child2)
        return child1, child2

    def position_based_crossover(self, parent2) -> Tuple:
        """
        Position based Crossover:
        We take random number of points from a parent genotype.
        The position of these points is kept and applied on the child.
        The remaining genotype elements of the second parent are inserted sequentially to fill up the missing
        points of the child.
        For the second child reverse the order of the parents.
        Example:    points = [1,2,5]
                    points_minus_index = [1,1,3]
                    parent1.genotype = [2,5,0,3,6,1,4,7]
                    parent2.genotype = [3,4,0,7,2,5,1,6]
                    position_args_1 = [5,0,1]
                    position_args_2 = [4,0,5]
                    position_indices_1 = [2,5,6] -- indices of the position args in the other parent
                    position_indices_2 = [1,2,6] -- indices of the position args in the other parent

                    after deletion of points
                    child1 = [3,4,7,2,6]
                    child2 = [2,3,6,1,7]

                    after insertion of position_args
                    child1 = [3,5,0,4,7,1,2,6]
                    child2 = [2,4,0,3,6,5,1,7]

        :param parent2: Organism
        :return: two children/Organisms
        """
        # determine randomly how many points are chosen
        number_of_points_to_choose = np.random.randint(1, config.field_size)
        # choose the specific points
        # create an array like [0,1,2,3,...,n]
        points = np.arange(0, config.field_size)
        # shuffle it randomly
        np.random.shuffle(points)
        # cut it to get only the first part
        points = points[0:number_of_points_to_choose]
        # sort
        points.sort()
        points_minus_index = [x - i for i, x in enumerate(points)]

        # Example:  points = [1,2,5]
        #           points_minus_index = [1,1,3]
        #           parent1.genotype = [2,5,0,3,6,1,4,7]
        #           position_args_1 = [5,0,1]
        #           parent2.genotype = [3,4,0,7,2,5,1,6]
        #           position_args_2 = [4,0,5]

        child1 = parent2.genotype.copy()
        child2 = self.genotype.copy()

        position_args_1 = self.genotype[points]
        position_args_2 = parent2.genotype[points]

        # get the indices of the position points
        # Example:  position_indices_1 = [2,5,6]
        #           position_indices_2 = [1,2,6]
        position_indices_1 = np.where(np.isin(parent2.genotype, position_args_1))
        position_indices_2 = np.where(np.isin(self.genotype, position_args_2))

        # delete the elements which will be inserted from the other elements
        # to avoid duplicates
        child1 = np.delete(child1, [position_indices_1])
        child2 = np.delete(child2, [position_indices_2])

        # insert the elements to its respective position according to points or points_minus_index
        # we have to use points_minus_index because np.inserts uses the given array throughout the insertion
        child1 = np.insert(child1, points_minus_index, position_args_1)
        child2 = np.insert(child2, points_minus_index, position_args_2)

        # create organisms and compute fitness
        child1 = Organism(child1)
        child2 = Organism(child2)
        return child1, child2

    ####################################################################################################################
    ## Mutation Methods
    ####################################################################################################################

    def mutate(self, method):
        """
        General mutation method. Chooses the specific mutation method given by 'method'.
        Possible methods:   'exchange': switch two rows randomly
                            'scramble': choose random segment and shuffle its values
                            'displacement': choose a segment and move it to another point in the array
                            'insertion': choose one element and insert it in another place, like displacement but only
                                        with one element
                            'inversion': invert the order of a random segment
                            'displacement_inversion': invert the order of random segment and insert it elsewhere,
                                        displacement and inversion together
                            'random': one of the above methods randomly
        :param method: 'exchange', 'scramble', 'displacement', 'insertion', 'inversion',
                        'displacement_inversion', 'random'
        :return:
        """
        if method is 'exchange':
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
            method_list = config.mutation_method_list
            self.mutate(method=method_list[np.random.randint(0, len(method_list))])

    def exchange_mutation(self):
        """
        Exchange Mutation:
        Select two rows randomly and exchange them.
        It is possible/allowed that the same rows are selected. Then nothing will happen
        :return:
        """
        row1 = np.random.randint(0, config.field_size)
        row2 = np.random.randint(0, config.field_size)
        self.genotype[row1], self.genotype[row2] = self.genotype[row2], self.genotype[row1]
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

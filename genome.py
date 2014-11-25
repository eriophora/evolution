'''
Exports a class to manage an agent's genome. Can be instantiated from
nothing, in which case the genome is randomly generated, or it can be
instatiated with a define in-order set of actions.

Initialized with genes, a list of actions to be mapped to the genes
that are generated. Stores genes in a mapping, gene_map, which maps
genes (represented as strings) to behaviors.

Additionally, this generates an agent NAME, a random sequence of 0's
and 1's, whose length is given by NAME_LENGTH. While agents cannot see
each other's genes, they can see each others name. In this sense,
you can consider this class to dictate the agent's phenotype and
the agent's genotype.

Created by NPD on 11/20/14

TODO: find a more efficient representation of the genome, perhaps
by converting the strings into sequences of numbers, or somesuch.
Whether or not we have to do this will depend on how efficiently our
computers can run the simulation.
'''
from random import randint      # to generate gene behaviors
from random import random       # to mutate genes / names
from random import choice       # to generate names
from constants import *
from copy import copy

class Genome():
    def __init__(self, genes=None, name=None):
        self.gene_map = dict()
        self._generateGenes()
        self._populateGenes(genes)
        if name == None:
            self._generateName()
        else:
            self.name = name
    def _generateName(self):
        # generates a wholly random name, composed out of 1's and 0's.
        self.name = ''
        for i in range(NAME_LENGTH):
            self.name += choice(['0','1'])
    def _generateGenes(self):
        # generates the mapping of genes by enumerating through all
        # possible lengths and all possible sequences.
        genes_of_len = self._getAllGenes(GENE_LENGTH)
        for i in genes_of_len:
            self.gene_map[i] = None
    def _getAllGenes(self, gene_len):
        # returns all sets of game events of length gene_len, where the
        # types of events represented is given by GENOME_TYPE
        if GENOME_TYPE=='unary': gene_vals = [str(x) for x in range(2)]
        if GENOME_TYPE=='binary': gene_vals = [str(x) for x in range(4)]
        if gene_len == 0:
            return ['']
        genes_of_len = []
        small_genes = self._getAllGenes(gene_len - 1)
        genes_of_len += small_genes
        for i in gene_vals:
            genes_of_len +=  [i + x for x in small_genes if len(x)==(gene_len - 1)]
        return genes_of_len
    def _populateGenes(self, genes = None):
        # assigns behaviors to the genes, assigning randomly if genes is
        # None.
        if genes == None:
            getRandomAction = lambda: randint(0, N_POS_ACTIONS-1)
            for k in self.gene_map.keys():
                self.gene_map[k] = getRandomAction()
        else:
            for k, act in zip(self.gene_map.keys(), genes):
                self.gene_map[k] = act
    def mutate(self, mutation_rate = None):
        # returns a copy of itself, mutated. If the mutation rate is not
        # specified (i.e., is None), then it will use the global value.
        # NOTE: this does not change the current genome, but instead
        # returns a new one!
        if mutation_rate == None:
            mutation_rate = MUTATION_PROB
        new_genome = copy(self)
        self._mutateGenome(mutation_rate, new_genome)
        self._mutateName(mutation_rate, new_genome)
        return new_genome
    def _mutateGenome(self, mutation_rate, new_genome):
        # handles mutation of the genes on the child genome (new_genome)
        getRandomAction = lambda: randint(0, N_POS_ACTIONS-1)
        new_genome.gene_map = dict.fromkeys(self.gene_map)
        for k in new_genome.gene_map.keys():
            if random() <= mutation_rate:
                new_genome.gene_map[k] = getRandomAction()
            else:
                new_genome.gene_map[k] = self.gene_map[k]
    def _mutateName(self, mutation_rate, new_genome):
        # mutates the name (i.e., the phenotype) of the child
        new_genome.name = ''
        for i in range(NAME_LENGTH):
            if random() <= mutation_rate:
                # mutate, i.e., flip the value
                new_genome.name += str(abs(int(self.name[i])-1))
            else:
                new_genome.name += self.name[i]
    def getAction(self, action_sequence):
        # returns a behavior given a sequence of actions.
        if not self.gene_map.has_key(action_sequence):
            print 'Provided sequence %s for which I dont have a gene!'%action_sequence
        return self.gene_map[action_sequence]


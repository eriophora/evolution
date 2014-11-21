'''
Exports a class to manage an agent's genome. Can be instantiated from
nothing, in which case the genome is randomly generated, or it can be
instatiated with a define in-order set of actions.

Initialized with genes, a list of actions to be mapped to the genes
that are generated. Stores genes in a mapping, geneMap, which maps
genes (represented as strings) to
'''
from random import randint
from random import random
from constants import *
from copy import copy

class Genome():
    def __init__(self, genes=None):
        self.geneMap = dict()
        self.generateGenes()
        self.populateGenes(genes)
    def generateGenes(self):
        # generates the mapping of genes by enumerating through all
        # possible lengths and all possible sequences.
        genesOfLen = self.getAllGenes(GENE_LENGTH)
        for i in genesOfLen:
            self.geneMap[i] = None
    def getAllGenes(self, geneLen):
        # returns all sets of game events of length geneLen, where the
        # types of events represented is given by GENOME_TYPE
        if GENOME_TYPE=='unary': geneVals = [str(x) for x in range(2)]
        if GENOME_TYPE=='binary': geneVals = [str(x) for x in range(4)]
        if geneLen == 0:
            return ['']
        genesOfLen = []
        smallGenes = self.getAllGenes(geneLen - 1)
        genesOfLen += smallGenes
        for i in geneVals:
            genesOfLen +=  [i + x for x in smallGenes if len(x)==(geneLen - 1)]
        return genesOfLen
    def populateGenes(self, genes = None):
        # assigns behaviors to the genes, assigning randomly if genes is
        # None.
        if genes == None:
            if GENOME_TYPE=='unary':
                getRandomAction = lambda: randint(0, 1)
            else:
                getRandomAction = lambda: randint(0, 3)
            for k in self.geneMap.keys():
                self.geneMap[k] = getRandomAction()
        else:
            for k, act in zip(self.geneMap.keys(), genes):
                self.geneMap[k] = act
    def mutate(self):
        # returns a copy of itself, mutated.
        if GENOME_TYPE=='unary':
            getRandomAction = lambda: randint(0, 1)
        else:
            getRandomAction = lambda: randint(0, 3)
        newGenome = copy(self)
        newGenome.geneMap = copy(self.geneMap)
        for k in newGenome.geneMap.keys():
            if random() <= MUTATION_PROB:
                newGenome.geneMap[k] = getRandomAction()
        return newGenome
    def getAction(self, actionSequence):
        # returns a behavior given a sequence of actions.
        if not self.geneMap.has_key(actionSequence):
            print 'Provided sequence %s for which I dont have a gene!'%actionSequence
        return self.geneMap[actionSequence]


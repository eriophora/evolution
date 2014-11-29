'''
trust class manages the trust of the agents, which learns whether or not
to play against an agent based on the agent's name. This is done by
adjusting weights based on the agent's name. It performs stochastic
gradient descent on the agent's name, such that the weights best predict
the fitness of a game played against this agent.
'''

from constants import *
import numpy as np

class Trust():
    def __init__(self):
        self.weights = np.array([0] * (NAME_LENGTH + 1))
        self.alpha = LEARNING_RATE
        self.lossFunction = lossFunction
    def calculateExpectedFitness(self, opp_name):
        # computes the expected fitness against the opponent whose name
        # is opp_name by taking the dot product of that agent's name
        # with the weights.
        return np.dot(self.weights, np.array([1] + [int(x) for x in opp_name]))
    def decideToPlay(self, opp_name):
        # returns True if the expected fitness is greater than or equal to zero
        return self.calculateExpectedFitness(opp_name) >= 0
    def updateWeights(self, opp_name, delta_fitness):
        # updates the agent's weights in accordance with the opponent and the
        # change in fitness experienced during the last game.
        delta_loss = self.lossFunction(self.weights, opp_name, delta_fitness)
        self.weights -= self.alpha * delta_loss
    def reproduce(self):
        # returns a copy of itself
        child = Trust()
        child.weights = [x for x in self.weights]
        return child






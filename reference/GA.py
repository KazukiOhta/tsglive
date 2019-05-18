import random
import numpy as np
from copy import deepcopy
import RuleOfTicTacToe as Rule
import Colosseum
import NN

class Agent:
    def __init__(self, brain):
        self.brain = brain
        self.score1 = None
        self.score2 = None
        self.fitness = None

    def mutate(self):
        self.brain.mutate(0.01)

    def clone(self):
        return Agent(deepcopy(self.brain))
        
    def evaluate(self, S):
        data = Rule.preprocess(S)
        return self.brain.forward(data)

    def move(self, S):
        best_child = None
        best_value = -float('inf')
        for child in Rule.children(S):
            value = self.evaluate(child)
            if value > best_value:
                best_child = child
                best_value = value
        return best_child

    def battle(self, opponents):
        self.score1 = 0
        self.score2 = 0
        self.fitness = 0
        for opponent in opponents:
            if Colosseum.match(self.move, opponent.move):
                self.score1 += 1
        for opponent in opponents:
            if not Colosseum.match(opponent.move, self.move):
                self.score2 += 1
        self.fitness = 1.25**(0.3*self.score1+self.score2)

class Generation:
    def __init__(self, agents, opponents, generation_number=0):
        self.agents = agents
        self.opponents = opponents
        self.generation_number = generation_number
    
    def select1(self):
        fitnesses = np.array([agent.fitness for agent in self.agents])
        weights = fitnesses/sum(fitnesses)
        return np.random.choice(self.agents, p=weights)

    def battle(self, opponents):
        for agent in self.agents:
            agent.battle(opponents)

    def nextGeneration(self):
        self.battle(self.opponents)
        next_agents = []
        for i in range(len(self.agents)):
            next_agent = deepcopy(self.select1())
            if random.random() < 0.5:
                next_agent.mutate()
            next_agents.append(next_agent)
        return Generation(next_agents, self.opponents, self.generation_number+1)

    def bestAgent(self):
        best_agent = None
        best_fitness = -float('inf')
        for agent in self.agents:
            fitness = agent.fitness
            if fitness > best_fitness:
                best_agent = agent
                best_fitness = fitness
        return best_agent


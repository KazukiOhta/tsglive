import numpy as np
import pprint
import NN 
import GA
from copy import deepcopy
def test():
    mynet = NN.TwoLayerNet(2,4,1)
    myX = np.array([1,100])
    myY = mynet.forward(myX)    
    print(myY)
    mynet.mutate(1)
    myY = mynet.forward(myX)
    print(myY)
    print(mynet.hoge)
    mynet.hoge = 1
    print(mynet.hoge)
    print("="*50)
    
    agent1 = GA.Agent(mynet)
    agent1.mutate()

#test()
import RuleOfTicTacToe as Rule
def testAgent():
    mynet = NN.TwoLayerNet(27,20,1)
    myX = Rule.initialState()
    agent1 = GA.Agent(mynet)
    pprint.pprint(agent1.move(myX))



#testAgent()
def testGA():
    agents = [GA.Agent(NN.TwoLayerNet(27,20,1)) for i in range(20)]
    weakagents = [GA.Agent(NN.TwoLayerNet(27,1,1)) for i in range(50)]

    g = GA.Generation(agents, weakagents)
    g.battle(weakagents)
    for n in range(50):
        best_agent = g.bestAgent()
        print("#", n, best_agent.score1, best_agent.score2)
        g = g.nextGeneration()

    best_agent = g.bestAgent()
    print("LAST:", best_agent.score1, best_agent.score2)
    
testGA()

#import RuleOfMarch as Rule
#def testTTT():
#    i_s = Rule.initialState()
#    cs = Rule.children(i_s)



#testTTT()



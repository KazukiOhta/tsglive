import numpy as np
import pprint
import time
#import RuleOfMarch as Rule
import RuleOfTicTacToe as Rule
import shelve

# B(oard) ... turn player: positive,downside.  {1:Soldier, 2:King}

# takes S(tate)
# returns True or Flase (whether positive wins)

countAll = 0
countDouble = 0
evalDict = {}

def complete_evaluation(S):
    global countAll
    global countDouble
    countAll += 1
    if countAll%(10**4)==0: print("countAll =",countAll//10000,"万")

    B,turn = S
    j = Rule.judgeBoard(B)
    r = False
    keyB = tuple(B.flatten())

    if keyB in evalDict:
        countDouble += 1
        r = evalDict[keyB]
    else:
        if j != None: r = j
        else:
            for child in Rule.children(S):
                if not complete_evaluation(child):
                    r = True
                    break
        evalDict[keyB] = r
    
    return r


def complete_analysis_to_s():
    t0 = time.time()
    #M = np.array([[-1,-2,-1,-1],
    #              [ 0, 0, 0, 0],
    #              [ 0, 0, 0, 0],
    #              [ 1, 1, 2, 1]])
    S = Rule.initialState()
    #print(M)
    e = complete_evaluation(S)
    print("Result:",e)
    print("Amount:",countAll-countDouble,"/",countAll,"=",1-(countDouble/countAll))
    print("time:",time.time()-t0,"[sec]")
    print()
    print("【解析結果】")
    #print(M)
    print("先手必勝" if e else "後手必勝")
    print("計算局面数:",countAll//10000,"万")
    print("計算時間:",int(time.time()-t0),"秒")

complete_analysis_to_s()


import numpy as np

# takes B(oard). 
# returns True or False (whether positive wins) or, None
def judgeBoard(B):
    for xi in range(3):
        if np.all(B.T[xi,:] == 1): return True
        if np.all(B.T[xi,:] ==-1): return False
    for yi in range(3):    
        if np.all(B.T[:,yi] == 1): return True
        if np.all(B.T[:,yi] ==-1): return False
    
    if B[0,0]==B[1,1]==B[2,2]== 1: return True
    if B[0,0]==B[1,1]==B[2,2]==-1: return False
    if B[0,2]==B[1,1]==B[2,0]== 1: return True
    if B[0,2]==B[1,1]==B[2,0]==-1: return False
    
    if np.all(B != 0): return True

    return None

# takes shape(of the map),C(oordinate)
# returns whether C is in the map
def isInMap(shape,C):
    return (0 <= C[0] < shape[0] and 0 <= C[1] < shape[1])
    

# takes S(tate) = (B(oard),turn)
# returns set of S(tates) of next turn.
def children(S):
    B,turn = S
    shape = np.shape(B.T)
    nextStates = []
    for xi in range(shape[0]):
        for yi in range(shape[1]):
            if B.T[xi,yi] == 0:
                nextBoard_t = np.array(B.T)
                nextBoard_t[(xi,yi)] = 1
                nextStates.append((nextBoard_t.T[::-1,::-1]*-1, turn+1))
    return nextStates

def initialState():
    initial_board = np.array([[ 0, 0, 0],
                              [ 0, 0, 0],
                              [ 0, 0, 0]])
    return (initial_board,0)

def preprocess(S):
    B, turn = S
    onehotB = np.array([B ==-1,
                        B == 0,
                        B == 1])
    return onehotB.flatten()

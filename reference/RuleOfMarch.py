import numpy as np

# B(oard) ... turn player: positive,downside.  {1:Soldier, 2:King}


# takes B(oard). 
# returns True or False (whether positive wins) or, None
def judgeBoard(B):
    if  2 not in B: return False
    if -2 not in B: return True
    if  2 in B[0] : return True
    if -2 in B[-1]: return False
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
            if B.T[xi,yi] > 0:
                toCs  = [(xi+dx,yi-1) for dx in [-1,0,1] if isInMap(shape,(xi+dx,yi-1)) and B.T[xi+dx,yi-1]<=0]
                for toC in toCs:
                    nextBoard_t = np.array(B.T)
                    nextBoard_t[toC] = nextBoard_t[(xi,yi)]
                    nextBoard_t[(xi,yi)] = 0
                    nextStates.append((nextBoard_t.T[::-1,::-1]*-1,turn+1))
    return nextStates

def initialState():
    initial_board = np.array([[-1,-1,-2,-1,-1,-1],
                              [-1,-1,-1,-1,-1,-1],
                              [ 0, 0, 0, 0, 0, 0],
                              [ 0, 0, 0, 0, 0, 0],
                              [ 1, 1, 1, 1, 1, 1],
                              [ 1, 1, 1, 2, 1, 1]])
    return (initial_board,0)

def preprocess(S):
    B, turn = S
    onehotB = np.array([B ==-2,
                        B ==-1,
                        B == 0,
                        B == 1,
                        B == 2])
    return onehotB.flatten()

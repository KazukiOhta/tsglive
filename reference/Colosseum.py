import RuleOfTicTacToe as Rule

# takes and 2 AIs.
# returns bool whether the first player wins or not.
def match(AI0, AI1):
    S = Rule.initialState()
    while(True):
        B,turn = S
        j = Rule.judgeBoard(B)
        if j != None:
            return (turn%2==0)==j
        if turn%2 == 0:
            S = AI0(S)
        else:
            S = AI1(S)
    

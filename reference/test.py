from main import *

def match(AI0, AI1, show=False, AI0_name = "AI0", AI1_name = "AI1", reverse = True, random_opening = 0):
    march = March()
    for turn in range(100):
        if show:
            print("Turn:", turn)
        if turn < random_opening:
            frm, to = randomAI(march)
        elif turn % 2 == 0:
            frm, to = AI0(march)
        else:
            frm, to = AI1(march)
        assert march.movable(frm, to)
        march.move(frm^to)
        if show:
            if reverse:
                print(AI1_name)
                if turn % 2 == 0:
                    march.reverseBoard()                    
                print(march, AI0_name, sep = "")
                if turn % 2 == 0:
                    march.reverseBoard()      
                print()
            else:
                print(AI0_name if turn % 2 == 0 else AI1_name)
                print(march, AI1_name if turn % 2 == 0 else AI0_name, sep = "")
                print()
            print("richJudge:", march.richJudge())
        j = march.judge()
        if j == 1:
            print("想定外")
        elif j == -1:
            return turn % 2 == 0 # means AI0 wins.

match(vanillaAI(filename="rich20k").move, vanillaAI(filename="rich20k").move, True)

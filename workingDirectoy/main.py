from math import exp
"""
Matrix class (substitution for numpy)
"""
class matrix():
    def __init__(self, lst2d=[], filename=None):
        if filename == None:
            self.matrix = lst2d
        else:
            with open(filename) as f:
                self.matrix = list(map(lambda line: list(map(float, line.split(","))), f.readlines()))
        self.rows = len(self.matrix)
        self.cols = len(self.matrix[0])
        for row in range(self.rows):
            assert len(self.matrix[row]) == self.cols, "inconsistent cols"
        self.shape = (self.rows, self.cols)          
        
    def dot(self, matrix2):
        assert self.cols == matrix2.rows, "M1.rows does not match M2.cols"
        dotproduct = []
        for r in range(self.rows):
            sublist = []
            for c in range(matrix2.cols):
                sublist.append(sum([self.matrix[r][i]*matrix2.matrix[i][c] for i in range(self.cols)]))
            dotproduct.append(sublist)
        return matrix(dotproduct)
    
    def broadcast(self, f):
        mainlist = []
        for row in range(self.rows):
            sublist = list(map(f, self.matrix[row]))
            mainlist.append(sublist)
        return matrix(mainlist)
    
    def __str__(self):
        return str(self.matrix)



"""
vanillaAI class
"""
class vanillaAI:
    def __init__(self, filename, hidden_size = 50):
        self.hidden_size = hidden_size
        self.W1 = matrix(filename="data/"+filename+"W1.csv")
        self.W2 = matrix(filename="data/"+filename+"W2.csv")
        self.record_x = []
        self.record_y = []
           
    def move(self, march, recording=True, showeval = False, epsilon=0.001):
        bestmove = None
        besteval = -float("inf") # Negamax法で、自分の勝率(1-eval)に直してしまう。
        for i in range(9,55):
            frm = 1<<i
            if frm & march.b != 0:
                for to in march.tos(frm):
                    child = March(march.b, march.r, march.bk, march.rk)
                    child.move(frm^to)
                    j = child.richJudge()
                    if j == 1:
                        thiseval = 0
                    elif j == -1:
                        thiseval = 1
                    else:
                        thiseval = (1-epsilon)-self.evaluate(child)[0][0]*(1-2*epsilon)
                    if thiseval == besteval and showeval:
                        print("衝突")
                        print("best:", bestmove, besteval)
                        print("this:", (frm, to), thiseval)
                    if thiseval >= besteval:
                        besteval = thiseval
                        bestmove = (frm, to)
        if recording:
            self.record_x.append(self.boardToOnehotLabel(march))
            self.record_y.append(besteval)
        if showeval:
            print("私の勝率は{0:.1f}%".format((besteval)*100))
        return bestmove
       
    def boardToOnehotLabel(self, march):
        b = bitToVec(march.b)
        r = bitToVec(march.r)
        bk = bitToVec(march.bk)
        rk = bitToVec(march.rk)
        x = b+r+bk+rk        
        return x
        
    def evaluate(self, march):
        # blueの勝率の推定値を返す。(0~1)
        x = matrix(self.boardToOnehotLabel(march))
        sigmoid = lambda x: 1/(1+exp(-x))
        u1 = self.W1.dot(x)
        z1 = u1.broadcast(sigmoid)
        u2 = self.W2.dot(z1)
        y = u2.broadcast(sigmoid)
        return y.matrix






"""
March Rule
"""
class March:
    def __init__(self,b=None,r=None,bk=None,rk=None):
        if b == None:
            #self.b = sum([1 << i for i in range(49, 55)])
            self.b = sum([1 << i for i in range(41, 47)]) + sum([1 << i for i in range(49, 55)])
        else:
            self.b = b
        if r == None:
            #self.r = sum([1 << i for i in range(9, 15)])            
            self.r = sum([1 << i for i in range(9, 15)]) + sum([1 << i for i in range(17, 23)])
        else:
            self.r = r
        if bk == None:
            self.bk = 1 << 52
        else:
            self.bk = bk
        if rk == None:
            self.rk = 1 << 11
        else:
            self.rk = rk
        self.b = (self.b | self.bk)
        self.r = (self.r | self.rk)
        self.wall = sum([1 << i for i in range(0,8)]) | sum([1 << i for i in range(56,64)]) | sum([1 << i for i in range(0,64,8)]) | sum([1 << i for i in range(7,64,8)])
        self.turn = 0
        self.lastmove = 0
   
    def __str__(self):
        s = "" 
        for y in range(8):
            for x in range(8):
                address = 8*y+x
                bit = 1<<address
                if self.bk & bit != 0 :
                    s += "O"
                elif self.rk & bit != 0:
                    s += "X"
                elif self.b & bit != 0:
                    s += "o"
                elif self.r & bit != 0:
                    s += "x"
                elif self.wall & bit != 0:
                    s += "#"
                else:
                    s += "."
                s += " "
            s += "\n"
        return s
    
    def reverseBoard(self):
        self.bk, self.rk = reverse64bit(self.rk), reverse64bit(self.bk)
        self.b, self.r = reverse64bit(self.r), reverse64bit(self.b)
        self.wall = reverse64bit(self.wall)
    
    def judge(self):
        if self.bk == 0:
            return -1
        if self.rk == 0:
            return 1
        blue_goal = (1<<15)-(1<<9) # sum([1 << i for i in range(9, 15)])
        red_goal = (1<<55)-(1<<49) # sum([1 << i for i in range(49, 55)])
        if self.bk & blue_goal != 0:
            return 1
        if self.rk & red_goal != 0:
            return -1
        if not self.existsChildren():
            return -1
        return 0
    
    def richJudge(self):
        #そもそも勝負がついている場合
        j = self.judge()
        if j != 0:
            return j 
        
        #王手をかけている場合
        for i in range(7, 10):
            if (self.rk<<i)&self.b != 0:
                return 1 
            
        #次で必ずゴールできる場合
        blue_sub_goal = (1<<23)-(1<<17) # sum([1 << i for i in range(17, 23)])
        if self.bk & blue_sub_goal != 0:
            return 1 
        
        return 0
    
    def existsChildren(self):
        for i in range(7, 10):
            if (self.b>>i) & ~(self.b|self.wall) != 0:
                return True
        return False
    
    def tos(self, frm):
        assert self.b & frm != 0
        tos = []
        for i in range(7,10):
            to = frm>>i
            if (to & self.wall == 0) and (to & self.b == 0):
                tos.append(to)
        return tos
        
    def move(self, move):
        self.b = self.b ^ move
        if self.bk & move != 0:
            self.bk = self.bk ^ move
        self.r = self.r & ~move
        self.rk = self.rk & ~move
        self.reverseBoard()
        self.turn += 1
        self.lastmove = reverse64bit(move)
    
    def movable(self, frm, to):
        if self.b & frm == 0:
            return False
        if to & self.wall != 0:
            return False
        if to & self.b != 0:
            return False
        for i in range(7,10):
            if to == frm>>i:
                return True
        return False
    
    def children(self):
        children = []
        for i in range(64):
            frm = 1<<i
            if frm & self.b != 0:
                for to in self.tos(frm):
                    child = March(self.b, self.r, self.bk, self.rk)
                    child.move(frm^to)
                    children.append(child)
        return children

"""
AImove
"""
def AImove(AI, march):
    frm, to = AI(march)#AI.move(march)
    march.move(frm^to)
    if march.judge() != 0:
        #march = March()
        pass


"""
Bit Board Manager
"""
def bitprint(bit,name="    ",num=None):
    print(name,(num if num != None else " "),bin(bit).zfill(66))

def bitlist(bit):
    lst = []
    for i in range(64):
        if bit&(1<<i) != 0:
            lst.append(i)
    return lst

def reverse64bit(bit):
    ones = (1<<64)-1
    mask = lambda x: ones//((1<<(1<<x))+1)
    for i in range(6): # 2**6 = 64
        a = bit &  mask(i)
        b = bit & ~mask(i)
        bit = (a<<(1<<i))|(b>>(1<<i))
    return bit

def bitToVec(bit):
    return list(map(lambda x: [int(x)], (bin(bit)[2:].zfill(64))[::-1]))

"""
URL access
"""
import urllib.request
def url2text(url):
    data = urllib.request.urlopen(url)
    return data.read().decode()
    
"""
Graphical User Interface
"""
from kivy.app import App
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.uix.textinput import TextInput
from kivy.graphics import Color
Window.size = (450, 800)
color_dict = {"b":(0.725,0.825,0.925,1),
              "r":(1    ,0.75 ,0.85 ,1),
              "bk":(0, 0, 1, 1),
              "rk":(1, 0, 0, 1),
              "space":(1, 1, 1, 1),
              "outside":(0.95 ,0.95 ,0.95 ,1)}

class URLTextInput1(TextInput):
    multiline = False
    def on_text_validate(self):
        print("W1:", self.text)
        text = url2text(self.text)
        self.parent.bw.AI.W1.matrix = list(map(lambda x:list(map(float, x.split(","))), text.split("\n")[:-1]))
        with open("data/AIW1.csv", mode="w") as f:
            f.write(text)

class URLTextInput2(TextInput):
    multiline = False
    def on_text_validate(self):
        print("W2:", self.text)
        text = url2text(self.text)
        self.parent.bw.AI.W2.matrix =  list(map(lambda x:list(map(float, x.split(","))), text.split("\n")[:-1]))
        with open("data/AIW2.csv", mode="w") as f:
            f.write(text)



class GridButton(Button):
    def on_press(self):
        if self.parent.frm == None:
            if self.parent.march.b & self.value != 0:
                self.parent.frm = self.value
        else:
            if self.parent.march.movable(self.parent.frm, self.value):
                self.parent.march.move(self.parent.frm ^ self.value)
                if self.parent.march.judge() == 0:
                    AImove(AI = self.parent.parent.AI, march = self.parent.march)
                else:
                    self.parent.march.reverseBoard()
            self.parent.frm = None
        if self.parent.march.judge() != 0:
            #self.parent.march = March()
            pass
        self.parent.updateColor()

class BoardGrid(GridLayout):
    def __init__(self,  **kwargs):
        super().__init__(**kwargs)
        self.rows = 6
        self.cols = 6
        self.buttons = []
        self.march = March()
        self.frm = None
        for row in range(self.rows):
            sub_buttons = []
            for col in range(self.cols):
                btn = GridButton()
                btn.background_normal = "white.png" 
                btn.font_size = 100
                btn.value = 1<<(8*(row+1)+(col+1))
                sub_buttons.append(btn)
                self.add_widget(btn)
            self.buttons.append(sub_buttons)
        self.updateColor()
        self.background_normal = "white.png" 



    def updateColor(self):
        for row in range(self.rows):
            for col in range(self.cols):
                address = 1<<(8*(row+1)+(col+1))
                if self.march.bk & address != 0:
                    color = color_dict["bk"]
                elif self.march.rk & address != 0:
                    color = color_dict["rk"]
                elif self.march.b & address != 0:
                    color = color_dict["b"]
                elif self.march.r & address != 0:
                    color = color_dict["r"]
                else:
                    color = color_dict["space"]
                self.buttons[row][col].background_color = color
                if self.march.lastmove & address != 0:
                    self.buttons[row][col].text = "•"
                else:
                    self.buttons[row][col].text = ""
                self.buttons[row][col].color = color_dict["space"]
                if self.frm == None:
                    pass
                else:
                    if self.frm & address != 0:
                        self.buttons[row][col].text = "•"
                    if any([to & address != 0 for to in self.march.tos(self.frm)]):
                        self.buttons[row][col].color = color_dict["b"]
                        self.buttons[row][col].text = "•"

class RedPlayerButton(Button):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.value = 0
        self.text = RedAINames[self.value]
        self.font_size = 25
    
    def on_press(self):
        RedAIDict = RedAIDictFunc()
        self.value = (self.value + 1)%len(RedAIDict)
        print(self.value)
        self.parent.AI = RedAIDict[self.value]
        self.parent.bw.march = March()
        self.parent.bw.updateColor()
        self.text = RedAINames[self.value]
        
    
class BluePlayerButton(Button):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.value = 0
        self.font_size = 75

    def on_press(self):
        self.value = (self.value + 1) %2
        self.text = ["", "Q-network"][self.value]
        self.parent.bw.march = March()
        self.parent.bw.updateColor()

class BattleBox(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "vertical"
        self.redbtn = RedPlayerButton()
        self.redbtn.background_color = color_dict["outside"]
        self.bw = BoardGrid()
        self.bluebtn = Label()#BluePlayerButton()
        self.add_widget(self.redbtn)
        self.add_widget(self.bw)
        self.add_widget(self.bluebtn)
        self.AI = RedAIDictFunc()[self.redbtn.value]

    def on_size(self, *args):
        self.bw.size_hint_y = None
        self.bw.height = self.width
        

class RootBox(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.battleView()

    def battleView(self):
        self.clear_widgets()
        self.add_widget(BattleBox())


class MarchApp(App):
    def build(self):
        return RootBox()










































"""
LIVE AI
"""
import numpy as np
def RedAIDictFunc():
    #RedAIDict = [greedyAI, doubleCalculationAI, singleCalculationAI, randomAI] #vanillaAI(filename="AI").move
    #RedAIDict = [greedyAI, doubleCalculationAI]#, singleCalculationAI, randomAI] #vanillaAI(filename="AI").move
    RedAIDict = [vanillaAI(filename="AI").move]
    return RedAIDict
RedAINames = ["vanillaAI"]#["greedyAI", "doubleCalculationAI"]#, "singleCalculationAI", "randomAI"]













# ランダムなAI
def randomAI(march):
    while True:
        frm = 1<<np.random.randint(64)
        to = frm>>(9-np.random.randint(3))
        if march.movable(frm, to):
            return frm, to

# 王手をかけていれば取る。(Working in Progress)
def singleCalculationAI(march):
    
    for i in range(9, 55):
        frm = 1<<i
        if frm & march.b != 0:
            for to in march.tos(frm):
                child = March(march.b, march.r, march.bk, march.rk)
                child.move(frm^to)
                if child.judge() == -1:
                    return (frm, to)

    return randomAI(march)

# 負けにいかない。
def doubleCalculationAI(march):
    retVal = (0, 0)
    randlist = list(range(9, 55))
    np.random.shuffle(randlist)
    for i in randlist:
        frm = 1<<i
        if frm & march.b != 0:
            for to in march.tos(frm):
                child = March(march.b, march.r, march.bk, march.rk)
                child.move(frm^to)
                if child.richJudge() == -1:
                    return (frm, to)
                if child.richJudge() == 0:
                    retVal = (frm, to)
    if retVal == (0, 0):
        return randomAI(march)
    else:
        return retVal


# 取れるコマは絶対に取る！
def greedyEval(march):
    if march.richJudge() == 1:
        return 10000
    elif march.richJudge() == -1:
        return -10000
    blueEval = sum(np.array(list(bin(march.b)))=="1")
    redEval = sum(np.array(list(bin(march.r)))=="1")
    return blueEval - redEval #+np.random.randn()


def greedyAI(march):
    bestmove = (0, 0)
    bestEval = -100000
    randlist = list(range(9, 55))
    np.random.shuffle(randlist)
    for i in randlist:
        frm = 1<<i
        if frm & march.b != 0:
            for to in march.tos(frm):
                child = March(march.b, march.r, march.bk, march.rk)
                child.move(frm^to)
                Eval = -greedyEval(child)
                if Eval >= bestEval:
                    bestmove = (frm, to)
                    bestEval = Eval

    print(bestEval)
    if bestmove == (0, 0):
        return randomAI(march)
    else:
        return bestmove





#def greedyAI2(march):
#    bestmove = (0, 0)
#    bestEval = -100000
#    for i in range(9, 55):
#        frm = 1<<i
#        if frm & march.b != 0:
#            for to in march.tos(frm):
#                child = March(march.b, march.r, march.bk, march.rk)
#                child.move(frm^to)
#                for j in range(9, 55):
#                    frm2 = 1<<j
#                    if frm2 & march.b != 0:
#                        for to in march.tos(frm):

























MarchApp().run()

import numpy as np
import copy

class AffineLayer:
    def __init__(self, nodes_in, nodes_out, sigma=0.01):
        self.W = sigma*np.random.randn(nodes_in, nodes_out)
        self.B = sigma*np.zeros(nodes_out)

    def forward(self, X):
        A = np.dot(X, self.W) + self.B
        return A

    def mutate(self, rate):
        Wmask = (np.random.random_sample(self.W.shape) < rate)
        Bmask = (np.random.random_sample(self.B.shape) < rate)
        self.W = (1-Wmask)*self.W + 0.01*Wmask*(np.random.random_sample(self.W.shape)*2-1)
        self.B = (1-Bmask)*self.B + 0.01*Bmask*(np.random.random_sample(self.B.shape)*2-1)

class SigmoidLayer:
    def __init__(self, nodes):
        pass

    def sigmoid(self, A):
        return 1/(1+np.exp(-A))    
        
    def forward(self, A):
        Z = self.sigmoid(A)
        return Z

class TwoLayerNet:
    def __init__(self, nodes_in, nodes_hidden, nodes_out, regression = True):
        self.Affine1 = AffineLayer(nodes_in, nodes_hidden)
        self.Activation1 = SigmoidLayer(nodes_hidden)
        if regression:
            self.Affine2 = AffineLayer(nodes_hidden, nodes_out)
        else:
            #TODO
            pass
        self.hoge = 0

    def forward(self, X):
        A1 = self.Affine1.forward(X)
        Z1 = self.Activation1.forward(A1)
        A2 = self.Affine2.forward(Z1)
        return A2

    def mutate(self, rate=0.01):
        self.Affine1.mutate(rate)
        self.Affine2.mutate(rate)
    
    def copy(self):
        return copy.deepcopy(self)

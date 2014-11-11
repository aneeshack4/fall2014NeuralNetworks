import os
import sys
import time

import numpy
import scipy

import theano
import theano.tensor as T

TS = T.matrix('training-set')
W = T.matrix('weights')
E = T.matrix('expected')

O = T.nnet.sigmoid(T.dot(TS, W))

def_err = ((E - O) ** 2).sum()

err = theano.function([W, TS, E], def_err)
grad_err = theano.function([W, TS, E], T.grad(def_err, W))

# Load in the data
W = scipy.random.standard_normal((3, 1))
TS = [[0,0,0],[0,0,1], [0,1,1], [0,1,0], [1,0,0], [1,0,1], [1,1,0], [1,1,1]]
E = [[0], [0], [0], [0], [0], [0], [0], [1]]

learn_rate = 0.01
for i in range(1000):
    err_val = err(W, TS, E)
    err_grad_val = grad_err(W, TS, E)
    W -= learn_rate * err_grad_val
    	#print("Iteration " + str(i) + ", squared error : " + str(err_val))

print("-------- Training result -------")
print("Final squared error : " + str(err(W, TS, E)))
print("Computed weight vector :")
print(W)

#temp = theano.function([W, TS, E], def_err)
#print()

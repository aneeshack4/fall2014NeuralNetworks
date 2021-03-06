import os
import sys
import time

import numpy
import scipy

import theano
import theano.tensor as T


from logistic_sgd import LogisticRegression, load_data

class HiddenLayer(object):
    def __init__(self, rng, input, n_in, n_out, W=None, b=None,
                 activation=T.tanh):
        """
        Typical hidden layer of a MLP: units are fully-connected and have
        sigmoidal activation function. Weight matrix W is of shape (n_in,n_out)
        and the bias vector b is of shape (n_out,).

        NOTE : The nonlinearity used here is tanh

        Hidden unit activation is given by: tanh(dot(input,W) + b)

        :type rng: numpy.random.RandomState
        :param rng: a random number generator used to initialize weights

        :type input: theano.tensor.dmatrix
        :param input: a symbolic tensor of shape (n_examples, n_in)

        :type n_in: int
        :param n_in: dimensionality of input

        :type n_out: int
        :param n_out: number of hidden units

        :type activation: theano.Op or function
        :param activation: Non linearity to be applied in the hidden
                           layer
        """
        self.input = input

        # `W` is initialized with `W_values` which is uniformely sampled
        # from sqrt(-6./(n_in+n_hidden)) and sqrt(6./(n_in+n_hidden))
        # for tanh activation function
        # the output of uniform if converted using asarray to dtype
        # theano.config.floatX so that the code is runable on GPU
        # Note : optimal initialization of weights is dependent on the
        #        activation function used (among other things).
        #        For example, results presented in [Xavier10] suggest that you
        #        should use 4 times larger initial weights for sigmoid
        #        compared to tanh
        #        We have no info for other function, so we use the same as
        #        tanh.
        if W is None:
            W_values = numpy.asarray(rng.uniform(
                    low=-numpy.sqrt(6. / (n_in + n_out)),
                    high=numpy.sqrt(6. / (n_in + n_out)),
                    size=(n_in, n_out)), dtype=theano.config.floatX)
            if activation == theano.tensor.nnet.sigmoid:
                W_values *= 4

            W = theano.shared(value=W_values, name='W', borrow=True)

        if b is None:
            b_values = numpy.zeros((n_out,), dtype=theano.config.floatX)
            b = theano.shared(value=b_values, name='b', borrow=True)

        self.W = W
        self.b = b

        lin_output = T.dot(input, self.W) + self.b
        self.output = (lin_output if activation is None
                       else activation(lin_output))
        # parameters of the model
        self.params = [self.W, self.b]

class MLP(object):
    """Multi-Layer Perceptron Class

    A multilayer perceptron is a feedforward artificial neural network model
    that has one layer or more of hidden units and nonlinear activations.
    Intermediate layers usually have as activation function tanh or the
    sigmoid function (defined here by a ``HiddenLayer`` class)  while the
    top layer is a softamx layer (defined here by a ``LogisticRegression``
    class).
    """

    def __init__(self, rng, input, n_in, n_hidden, n_out):
        """Initialize the parameters for the multilayer perceptron

        :type rng: numpy.random.RandomState
        :param rng: a random number generator used to initialize weights

        :type input: theano.tensor.TensorType
        :param input: symbolic variable that describes the input of the
        architecture (one minibatch)

        :type n_in: int
        :param n_in: number of input units, the dimension of the space in
        which the datapoints lie

        :type n_hidden: int
        :param n_hidden: number of hidden units

        :type n_out: int
        :param n_out: number of output units, the dimension of the space in
        which the labels lie

        """

        # Since we are dealing with a one hidden layer MLP, this will translate
        # into a HiddenLayer with a tanh activation function connected to the
        # LogisticRegression layer; the activation function can be replaced by
        # sigmoid or any other nonlinear function
        self.hiddenLayer = HiddenLayer(rng=rng, input=input,
                                       n_in=n_in, n_out=n_hidden,
                                       activation=T.tanh)

        # The logistic regression layer gets as input the hidden units
        # of the hidden layer
        self.logRegressionLayer = LogisticRegression(
            input=self.hiddenLayer.output,
            n_in=n_hidden,
            n_out=n_out)

        # L1 norm ; one regularization option is to enforce L1 norm to
        # be small
        self.L1 = abs(self.hiddenLayer.W).sum() \
                + abs(self.logRegressionLayer.W).sum()

        # square of L2 norm ; one regularization option is to enforce
        # square of L2 norm to be small
        self.L2_sqr = (self.hiddenLayer.W ** 2).sum() \
                    + (self.logRegressionLayer.W ** 2).sum()

        # negative log likelihood of the MLP is given by the negative
        # log likelihood of the output of the model, computed in the
        # logistic regression layer
        self.negative_log_likelihood = self.logRegressionLayer.negative_log_likelihood
        # same holds for the function computing the number of errors
        self.errors = self.logRegressionLayer.errors

        # the parameters of the model are the parameters of the two layer it is
        # made out of
        self.params = self.hiddenLayer.params + self.logRegressionLayer.params
        self.y_pred= self.logRegressionLayer.y_pred

def test_mlp(learning_rate=0.05, L1_reg=0.00, L2_reg=0.0001, n_epochs=1000, batch_size=1, n_hidden=3):
	# Load in the data

	train_set_x = theano.shared(numpy.array([[0,0,0],[0,0,1], [0,1,1], [0,1,0], [1,0,0], [1,0,1], [1,1,0], [1,1,1]]))
	train_set_y = theano.shared(numpy.array([0, 0, 0,0, 0, 0, 0, 1]))

	print "...initializing the variables and functions"
	index = T.lscalar() 
	x = T.lmatrix('x')
	y = T.lvector('y')

	rng = numpy.random.RandomState(1234)
	classifier = MLP(rng, x, 3, n_hidden, 2)

	cost = classifier.negative_log_likelihood(y) \
     + L1_reg * classifier.L1 \
     + L2_reg * classifier.L2_sqr
        errors = classifier.errors(y)
        predict = classifier.y_pred 

	# compute the gradient of cost with respect to theta (sotred in params)
	# the resulting gradients will be stored in a list gparams
	gparams = []
	for param in classifier.params:
	    gparam = T.grad(cost, param)
	    gparams.append(gparam)

	# specify how to update the parameters of the model as a list of
	# (variable, update expression) pairs
	updates = []
	# given two list the zip A = [a1, a2, a3, a4] and B = [b1, b2, b3, b4] of
	# same length, zip generates a list C of same size, where each element
	# is a pair formed from the two lists :
	#    C = [(a1, b1), (a2, b2), (a3, b3), (a4, b4)]
	for param, gparam in zip(classifier.params, gparams):
	    updates.append((param, param - learning_rate * gparam))

	train_model = theano.function(inputs=[], 
			outputs=[cost,errors,predict],
			updates=updates, 
			givens={
				x: train_set_x,
				y: train_set_y})

	print '...building the model'

	epoch = 0
	threshold = 0.1
        predict=None
	while(epoch < n_epochs):
		epoch += 1
		minibatch_average_cost,errors,predict = train_model()
		print float(minibatch_average_cost), float(errors), epoch
        print predict

if __name__ == '__main__':
	test_mlp()

"""The entire neural network's functionality
"""
import numpy as np



class Network:

    def __init__(self, shouldInitialize=False):
        self.layer_size = ((10, 5), (5, 5), (5, 2))
        self.layer = []
        if (shouldInitialize):
            self.randomize_layers()
        else:
            self.load_layers()
    
    def randomize_layers(self):
        for i in range(self.layer_size):
            print()

    def load_layers(self):
        #TODO: convert the large matrix to tuples that can be passed into the Layer_Dense
        for i in range(self.layer_size):
            print()

    


# Dense layer
class Layer_Dense:
    """Deals with the neurons, bias, and forward pass through a layer.
    """

    # Layer initialization
    def __init__(self, n_inputs=False, n_neurons=False, weightbiastuple=False):
        """Either neurons and inputs, or just weightbiastuple

        Args:
            n_inputs ([type]): how many neurons in previous layer. Defaults to False.
            n_neurons ([type]): how many neurons for this layer. Defaults to False.
            weightbiastuple (bool, optional): (weightslist, bias). Defaults to False.
        """
        if weightbiastuple:
            self.weights = weightbiastuple[0]
            self.biases = weightbiastuple[1]
        else:
            self.weights = 0.01 * np.random.randn(n_inputs, n_neurons)
            self.biases = np.zeros((1, n_neurons))

    # Forward pass
    def forward(self, inputs):
        # Calculate output values from inputs, weights and biases
        self.output = np.dot(inputs, self.weights) + self.biases


# ReLU activation
class Activation_ReLU:
    """Used for the inner layers of the neural network
    less than 0, 0. Greater than 0, keep the input.
    """
    # Forward pass
    def forward(self, inputs):
        # Calculate output values from inputs
        self.output = np.maximum(0, inputs)


# Softmax activation
class Activation_Softmax:
    """Used for the final layer of the neural network.

    """
    # Forward pass
    def forward(self, inputs):
        # Get unnormalized probabilities
        #e^k where k (-inf, 0] gives only values between 0 and 1 
        exp_values = np.exp(inputs - np.max(inputs, axis=1,
        keepdims=True))
        # Normalize them for each sample
        probabilities = exp_values / np.sum(exp_values, axis=1,
        keepdims=True)
        self.output = probabilities
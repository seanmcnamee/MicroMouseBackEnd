"""The entire neural network's functionality
"""
import numpy as np
import project.fileio.filemanager as fm



class Network:
    """Deals with each overall operation of each layer
    """

    def __init__(self, layer_sizes, shouldInitialize=False):
        self.layer_size = layer_sizes
        self.layer = []
        self.activations = []
        if (shouldInitialize):
            self.randomize_layers()
        else:
            self.load_layers()
        for i in range(len(layer_sizes)-1):
            self.activations.append(Activation_ReLU())
        self.activations.append(Activation_Softmax())
    
    def randomize_layers(self):
        """initialize each layer with no data
        """
        for i in range(len(self.layer_size)):
            self.layer.append(Layer_Dense(n_inputs=self.layer_size[i][0], n_neurons=self.layer_size[i][1]))

    def load_layers(self):
        """Initialize each layer with the stored data
        """
        weights, biases = fm.retrieve_weights(self.layer_size)
        for i in range(len(weights)):
            self.layer.append(Layer_Dense(weightbiastuple=(weights[i], biases[i])))

    def store_layers(self):
        """Store the data from this session back into memory
        """
        weights = []
        biases = []
        for i in range(len(self.layer)):
            weights.append(self.layer[i].weights)
            biases.append(self.layer[i].biases)
        fm.store_weights_and_biases(weights, biases)

    def calculate_outputs(self, normalized_tuple):
        previous_output = list(normalized_tuple)
        for i in range(len(self.layer)):
            self.layer[i].forward(previous_output)
            self.activations[i].forward(self.layer[i].output)
            previous_output = self.activations[i].output
        return previous_output[0]

    


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

        print(self.weights)

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
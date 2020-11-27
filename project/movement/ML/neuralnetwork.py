"""The entire neural network's functionality
"""
import numpy as np
import project.fileio.filemanager as fm



class Network:
    """Deals with each overall operation of each layer
    Create the network, add all your layers, set the loss function and optimizer, then
    finalize the connections between layers

    Usage: add_data and then forward.
        Then train.
    """

    def __init__(self, layerSizes):
        # Create a list of network objects
        self.layers = []
        # Softmax classifier's output object
        self.softmax_classifier_output = None
        self.layerSizes = layerSizes
        self.loadingWB = fm.retrieve_weights(layerSizes)
        self.loadIndex = 0
        self.normalized_datas = []
        # print(self.loadingWB)
        # print("L1:", (self.loadingWB[0][0], self.loadingWB[1][0]))
        # print("L2:", (self.loadingWB[0][1], self.loadingWB[1][1]))
        # print("L3:", (self.loadingWB[0][2], self.loadingWB[1][2]))
        

    def add(self, layer):
        self.layers.append(layer)

    def add_randomized_dense(self):
        """initialize each layer with no data
        """
        self.layers.append(Layer_Dense(n_inputs=self.layerSizes[self.loadIndex][0], n_neurons=self.layerSizes[self.loadIndex][1]))
        self.loadIndex += 1

    def add_stored_dense(self):
        """Initialize each layer with the stored data
        """
        self.layers.append(Layer_Dense(weightbiastuple=(self.loadingWB[0][self.loadIndex], self.loadingWB[1][self.loadIndex])))
        self.loadIndex += 1

    # Set loss and optimizer
    def set(self, *, loss=None, optimizer=None):
        if loss is not None:
            self.loss = loss
        if optimizer is not None:
            self.optimizer = optimizer

    
    # Finalize the model
    def finalize(self):
        # Create and set the input layer
        self.input_layer = Layer_Input()
        # Count all the objects
        layer_count = len(self.layers)
        # Initialize a list containing trainable layers:
        self.trainable_layers = []
        # Iterate the objects
        for i in range(layer_count):
            # If it's the first layer,
            # the previous layer object is the input layer
            if i == 0:
                self.layers[i].prev = self.input_layer
                self.layers[i].next = self.layers[i+1]
            # All layers except for the first and the last
            elif i < layer_count - 1:
                self.layers[i].prev = self.layers[i-1]
                self.layers[i].next = self.layers[i+1]
            # The last layer - the next object is the loss
            # Also let's save aside the reference to the last object
            # whose output is the model's output
            else:
                self.layers[i].prev = self.layers[i-1]
                self.layers[i].next = self.loss
                self.output_layer_activation = self.layers[i]

            # If layer contains an attribute called "weights",
            # it's a trainable layer -
            # add it to the list of trainable layers
            # We don't need to check for biases -
            # checking for weights is enough
            if hasattr(self.layers[i], 'weights'):
                self.trainable_layers.append(self.layers[i])
        
        # Update loss object with trainable layers
        if self.loss is not None:
            self.loss.remember_trainable_layers(
                self.trainable_layers
            )

        # If output activation is Softmax and
        # loss function is Categorical Cross-Entropy
        # create an object of combined activation
        # and loss function containing
        # faster gradient calculation
        if isinstance(self.layers[-1], Activation_Softmax) and \
            isinstance(self.loss, Loss_CategoricalCrossentropy):
            # Create an object of combined activation
            # and loss functions
            self.softmax_classifier_output = \
            Activation_Softmax_Loss_CategoricalCrossentropy()

    def print_layers(self):
        for i in range(len(self.layers)):
            if isinstance(self.layers[i], Layer_Dense):
                print("Weights: \n", self.layers[i].weights)

    def store_layers(self):
        """Store the data from this session back into memory
        """
        weights = []
        biases = []
        for i in range(len(self.layers)):
            if isinstance(self.layers[i], Layer_Dense):
                weights.append(self.layers[i].weights)
                biases.append(self.layers[i].biases)
        fm.store_weights_and_biases(weights, biases)

    # def calculate_outputs(self, normalized_tuple):
    #     previous_output = list(normalized_tuple)
    #     for i in range(len(self.layers)):
    #         self.layers[i].forward(previous_output)
    #         self.activations[i].forward(self.layers[i].output)
    #         previous_output = self.activations[i].output
    #     return previous_output[0]

    def add_data(self, normalized_tuple):
        self.normalized_datas.append(normalized_tuple)

        # Performs forward pass
    def forward(self, normalized_tuple, training):
        # Call forward method on the input layer
        # this will set the output property that
        # the first layer in "prev" object is expecting
        self.input_layer.forward(normalized_tuple, training)
        # Call forward method of every object in a chain
        # Pass output of the previous object as a parameter
        for layer in self.layers:
            layer.forward(layer.prev.output, training)
        # "layer" is now the last object from the list,
        # return its output
        return layer.output

    def train_network(self, all_correct_percents, last_x, training_iterations=10):
        for i in range(training_iterations):
            self.loss.new_pass()
            # Perform the forward pass
            output = self.forward(self.normalized_datas[-last_x:], training=True)
            # Calculate loss
            data_loss, regularization_loss = self.loss.calculate(output[-last_x:], all_correct_percents[-last_x:], include_regularization=True)
            # loss = data_loss + regularization_loss
            # Get predictions and calculate an accuracy
            # predictions = self.output_layer_activation.predictions(output)

            #print("Output: ", output)
            #print("Correct percents: ", all_correct_percents)
            # Perform backward pass
            self.backward(output[-last_x:], all_correct_percents[-last_x:])
            # Optimize (update parameters)
            self.optimizer.pre_update_params()
            for layer in self.trainable_layers:
                self.optimizer.update_params(layer)
            self.optimizer.post_update_params()


    # Performs backward pass
    def backward(self, output, y):
        # If softmax classifier
        if self.softmax_classifier_output is not None:
            # First call backward method
            # on the combined activation/loss
            # this will set dinputs property
            self.softmax_classifier_output.backward(output, y)
            # Since we'll not call backward method of the last layer
            # which is Softmax activation
            # as we used combined activation/loss
            # object, let's set dinputs in this object
            self.layers[-1].dinputs = \
                self.softmax_classifier_output.dinputs
            # Call backward method going through
            # all the objects but last
            # in reversed order passing dinputs as a parameter
            for layer in reversed(self.layers[:-1]):
                layer.backward(layer.next.dinputs)
            return
        # First call backward method on the loss
        # this will set dinputs property that the last
        # layer will try to access shortly
        self.loss.backward(output, y)
        # Call backward method going through all the objects
        # in reversed order passing dinputs as a parameter
        for layer in reversed(self.layers):
            layer.backward(layer.next.dinputs)



# Dense layer
class Layer_Dense:
    """Deals with the neurons, bias, and forward pass through a layer.
    """

    # Layer initialization
    def __init__(self, n_inputs=False, n_neurons=False, weightbiastuple=False,
                weight_regularizer_l1=0, weight_regularizer_l2=0,
                bias_regularizer_l1=0, bias_regularizer_l2=0):
        """Either neurons and inputs, or just weightbiastuple

        Args:
            n_inputs (int): how many neurons in previous layer. Defaults to False.
            n_neurons (int): how many neurons for this layer. Defaults to False.
            weightbiastuple (bool, optional): (weightslist, bias). Defaults to False.
        """
        if weightbiastuple:
            self.weights = weightbiastuple[0]
            self.biases = weightbiastuple[1]
        else:
            self.weights = 0.01 * np.random.randn(n_inputs, n_neurons)
            self.biases = np.zeros((1, n_neurons))
        # Set regularization strength
        self.weight_regularizer_l1 = weight_regularizer_l1
        self.weight_regularizer_l2 = weight_regularizer_l2
        self.bias_regularizer_l1 = bias_regularizer_l1
        self.bias_regularizer_l2 = bias_regularizer_l2
        print("Layer weights:\n", self.weights)

    # Forward pass
    def forward(self, inputs, training):
        # Remember input values
        self.inputs = np.array(inputs)
        # Calculate output values from inputs, weights and biases
        self.output = np.dot(inputs, self.weights) + self.biases
        

    # Backward pass
    def backward(self, dvalues):
        # Gradients on parameters
        self.dweights = np.dot(self.inputs.T, dvalues)
        self.dbiases = np.sum(dvalues, axis=0, keepdims=True)
        # Gradients on regularization
        # L1 on weights
        if self.weight_regularizer_l1 > 0:
            dL1 = np.ones_like(self.weights)
            dL1[self.weights < 0] = -1
            self.dweights += self.weight_regularizer_l1 * dL1
        # L2 on weights
        if self.weight_regularizer_l2 > 0:
            self.dweights += 2 * self.weight_regularizer_l2 * \
            self.weights
        # L1 on biases
        if self.bias_regularizer_l1 > 0:
            dL1 = np.ones_like(self.biases)
            dL1[self.biases < 0] = -1
            self.dbiases += self.bias_regularizer_l1 * dL1
        # L2 on biases
        if self.bias_regularizer_l2 > 0:
            self.dbiases += 2 * self.bias_regularizer_l2 * \
            self.biases
        # Gradient on values
        self.dinputs = np.dot(dvalues, self.weights.T)

    # Retrieve layer parameters
    def get_parameters(self):
        return self.weights, self.biases

    # Set weights and biases in a layer instance
    def set_parameters(self, weights, biases):
        self.weights = weights
        self.biases = biases

# Dropout
class Layer_Dropout:

    # Init
    def __init__(self, rate):
        # Store rate, we invert it as for example for dropout
        # of 0.1 we need success rate of 0.9
        self.rate = 1 - rate

    # Forward pass
    def forward(self, inputs, training):
        # Save input values
        self.inputs = inputs
        # If not in the training mode - return values
        if not training:
            self.output = inputs.copy()
            return
        # Generate and save scaled mask
        self.binary_mask = np.random.binomial(1, self.rate,
                            size=inputs.shape) / self.rate
        # Apply mask to output values
        self.output = inputs * self.binary_mask

    # Backward pass
    def backward(self, dvalues):
        # Gradient on values
        self.dinputs = dvalues * self.binary_mask

# Input "layer"
class Layer_Input:

    # Forward pass
    def forward(self, inputs, training):
        self.output = inputs






# ReLU activation
class Activation_ReLU:
    """Used for the inner layers of the neural network
    less than 0, 0. Greater than 0, keep the input.
    """
    # Forward pass
    def forward(self, inputs, training):
        # Remember input values
        self.inputs = inputs
        # Calculate output values from inputs
        self.output = np.maximum(0, inputs)

    # Backward pass
    def backward(self, dvalues):
        # Since we need to modify original variable,
        # let's make a copy of values first
        self.dinputs = dvalues.copy()
        # Zero gradient where input values were negative
        self.dinputs[self.inputs <= 0] = 0


# Softmax activation
class Activation_Softmax:
    """Used for the final layer of the neural network.
    """
    # Forward pass
    def forward(self, inputs, training):
        # Get unnormalized probabilities
        #e^k where k (-inf, 0] gives only values between 0 and 1 
        exp_values = np.exp(inputs - np.max(inputs, axis=1,
                                            keepdims=True))
        # Normalize them for each sample
        probabilities = exp_values / np.sum(exp_values, axis=1,
                                            keepdims=True)
        self.output = probabilities
    
    # Backward pass
    def backward(self, dvalues):
        # Create uninitialized array
        self.dinputs = np.empty_like(dvalues)
        # Enumerate outputs and gradients
        for index, (single_output, single_dvalues) in \
        enumerate(zip(self.output, dvalues)):
            # Flatten output array
            single_output = single_output.reshape(-1, 1)
            # Calculate Jacobian matrix of the output
            jacobian_matrix = np.diagflat(single_output) - \
                                np.dot(single_output, single_output.T)
            # Calculate sample-wise gradient
            # and add it to the array of sample gradients
            self.dinputs[index] = np.dot(jacobian_matrix,
                                        single_dvalues)






# Common loss class
class Loss:
    # Regularization loss calculation
    def regularization_loss(self):
        # 0 by default
        regularization_loss = 0
        # Calculate regularization loss
        # iterate all trainable layers
        for layer in self.trainable_layers:
            # L1 regularization - weights
            # calculate only when factor greater than 0
            if layer.weight_regularizer_l1 > 0:
                regularization_loss += layer.weight_regularizer_l1 * \
                                        np.sum(np.abs(layer.weights))

            # L2 regularization - weights
            if layer.weight_regularizer_l2 > 0:
                regularization_loss += layer.weight_regularizer_l2 * \
                                        np.sum(layer.weights * \
                                            layer.weights)

            # L1 regularization - biases
            # calculate only when factor greater than 0
            if layer.bias_regularizer_l1 > 0:
                regularization_loss += layer.bias_regularizer_l1 * \
                                        np.sum(np.abs(layer.biases))

            # L2 regularization - biases
            if layer.bias_regularizer_l2 > 0:
                regularization_loss += layer.bias_regularizer_l2 * \
                                        np.sum(layer.biases * \
                                            layer.biases)
        return regularization_loss


    # Set/remember trainable layers
    def remember_trainable_layers(self, trainable_layers):
        self.trainable_layers = trainable_layers

    # Calculates accumulated loss
    def calculate_accumulated(self, *, include_regularization=False):
        # Calculate mean loss
        data_loss = self.accumulated_sum / self.accumulated_count
        # If just data loss - return it
        if not include_regularization:
            return data_loss
        # Return the data and regularization losses
        return data_loss, self.regularization_loss()

    # Reset variables for accumulated loss
    def new_pass(self):
        self.accumulated_sum = 0
        self.accumulated_count = 0

# Cross-entropy loss
class Loss_CategoricalCrossentropy(Loss):
    # Forward pass
    def forward(self, y_pred, y_true):
        # Number of samples in a batch
        samples = len(y_pred)
        # Clip data to prevent division by 0
        # Clip both sides to not drag mean towards any value
        y_pred_clipped = np.clip(y_pred, 1e-7, 1 - 1e-7)
        # Probabilities for target values -
        # only if categorical labels
        if len(y_true.shape) == 1:
            correct_confidences = y_pred_clipped[
                range(samples),
                y_true
            ]
        # Mask values - only for one-hot encoded labels
        elif len(y_true.shape) == 2:
            correct_confidences = np.sum(
                y_pred_clipped * y_true,
                axis=1
            )
        # Losses
        negative_log_likelihoods = -np.log(correct_confidences)
        return negative_log_likelihoods
    
    # Calculates the data and regularization losses
    # given model output and ground truth values
    def calculate(self, output, y, *, include_regularization=False):
        # Calculate sample losses
        sample_losses = self.forward(output, y)
        # Calculate mean loss
        data_loss = np.mean(sample_losses)
        # Add accumulated sum of losses and sample count
        self.accumulated_sum += np.sum(sample_losses)
        self.accumulated_count += len(sample_losses)
        # If just data loss - return it
        if not include_regularization:
            return data_loss
        # Return the data and regularization losses
        return data_loss, self.regularization_loss()

    # Backward pass
    def backward(self, dvalues, y_true):
        # Number of samples
        samples = len(dvalues)
        # Number of labels in every sample
        # We'll use the first sample to count them
        labels = len(dvalues[0])
        # If labels are sparse, turn them into one-hot vector
        if len(y_true.shape) == 1:
            y_true = np.eye(labels)[y_true]
        # Calculate gradient
        self.dinputs = -y_true / dvalues
        # Normalize gradient
        self.dinputs = self.dinputs / samples



# Softmax classifier - combined Softmax activation
# and cross-entropy loss for faster backward step
class Activation_Softmax_Loss_CategoricalCrossentropy():
    # Backward pass
    def backward(self, dvalues, y_true):
        # Number of samples
        samples = len(dvalues)
        # If labels are one-hot encoded,
        # turn them into discrete values
        if len(y_true.shape) == 2:
            y_true = np.argmax(y_true, axis=1)
        # Copy so we can safely modify
        self.dinputs = dvalues.copy()
        # Calculate gradient
        self.dinputs[range(samples), y_true] -= 1
        # Normalize gradient
        self.dinputs = self.dinputs / samples







# SGD optimizer
class Optimizer_SGD:
    # Initialize optimizer - set settings,
    # learning rate of 1. is default for this optimizer
    def __init__(self, learning_rate=1., decay=0., momentum=0.):
        self.learning_rate = learning_rate
        self.current_learning_rate = learning_rate
        self.decay = decay
        self.iterations = 0
        self.momentum = momentum

    # Call once before any parameter updates
    def pre_update_params(self):
        if self.decay:
            self.current_learning_rate = self.learning_rate * \
                (1. / (1. + self.decay * self.iterations))

    # Update parameters
    def update_params(self, layer):
        # If we use momentum
        if self.momentum:
            # If layer does not contain momentum arrays, create them
            # filled with zeros
            if not hasattr(layer, 'weight_momentums'):
                layer.weight_momentums = np.zeros_like(layer.weights)
                # If there is no momentum array for weights
                # The array doesn't exist for biases yet either.
                layer.bias_momentums = np.zeros_like(layer.biases)
            
            # Build weight updates with momentum - take previous
            # updates multiplied by retain factor and update with
            # current gradients
            weight_updates = \
                self.momentum * layer.weight_momentums - \
                self.current_learning_rate * layer.dweights
            layer.weight_momentums = weight_updates

            # Build bias updates
            bias_updates = \
                self.momentum * layer.bias_momentums - \
                self.current_learning_rate * layer.dbiases
            layer.bias_momentums = bias_updates
            # Vanilla SGD updates (as before momentum update)
        else:
            weight_updates = -self.current_learning_rate * \
                layer.dweights
            bias_updates = -self.current_learning_rate * \
                layer.dbiases
        # Update weights and biases using either
        # vanilla or momentum updates
        layer.weights += weight_updates
        layer.biases += bias_updates

    # Call once after any parameter updates
    def post_update_params(self):
        self.iterations += 1
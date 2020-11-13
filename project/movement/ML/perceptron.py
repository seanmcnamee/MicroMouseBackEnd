from math import exp

def default_activation_function(summation):
        return 1 / (1+exp(-summation))

class Perceptron:
    
    def __init__(self, name, weights=None, function=default_activation_function):
        self.activation_function = function
        self.weights = weights
        self.name = name


    def summation(self, inputs):
        if self.weights == None:
            self.weights = []
            for i in range(len(inputs)):
                self.weights.append(1)
        return sum(x * y for x,y in zip(inputs, self.weights))


    def calculate(self, inputs):
        return self.activation_function(self.summation(inputs))
import numpy as np
import pandas as pd
from sklearn import preprocessing

import perceptron

class LearnStraight:
    weights_file = 'project//movement//ML//learnstraight.csv'
    weights_columns = ['', 'left', 'front-left', 'front', 'front-right', 'right', 'back-right', 'back', 'back-left', 'leftMotor', 'rightMotor']

def store_weights(perceptrons):
    #Get current records
    perceptron_weights = []
    for i in range(len(perceptrons)):
        perceptron_weights.append(perceptrons[i].weights)
    current_weights = pd.DataFrame.from_records(perceptron_weights, columns=LearnStraight.weights_columns)

    
    previous_weights = retrieve_weights()
    previous_weights.update(current_weights)

def retrieve_weights():
    return pd.read_csv(LearnStraight.weights_file)

def retrieve_perceptrons():
    stored_weights = retrieve_weights()
    print(stored_weights)

def normalize_in_range(input_data, input_min_max=None, output_min_max=(0,1)):
    if input_min_max is None:
        input_min_max = (input_data.min(), input_data.max())
    return (input_data / (input_min_max[1]-input_min_max[0]) + input_min_max[0]) * (output_min_max[1]-output_min_max[0]) + output_min_max[0]

def test1():
    testdata = np.array([[1, 2, 3, 4, 5]])
    normalized = normalize_in_range(testdata, (0, 10))

    print("data: ", testdata, " and ", normalized)
    p = perceptron.Perceptron('test')
    print(p.calculate(testdata[0]))
    #print(p.calculate(testdata[1]))
    print(p.calculate(normalized[0]))
    #print(p.calculate(normalized[1]))

retrieve_perceptrons()
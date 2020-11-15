import project.movement.robotcontrol as RobotControl
import project.fileio.filemanager as fm
import project.movement.ML.neuralnetwork as NN
import numpy as np

class MainClass():
    def __init__(self, port):
        self.robot = RobotControl.RobotControl(port)

    def explore(self):
        should_continue = True

        while should_continue:
            print("test")

sizingTuples = [(5, 3), (3, 2)]
print(len(sizingTuples))

def storeRandWeights():
    layer = NN.Layer_Dense(n_inputs=sizingTuples[0][0], n_neurons=sizingTuples[0][1])
    print("Printing NN")
    print(layer.weights.transpose())

    layer2 = NN.Layer_Dense(n_inputs=sizingTuples[1][0], n_neurons=sizingTuples[1][1])
    print("Printing NN")
    print(layer2.weights.transpose())

    arrboth = [layer.weights, layer2.weights]
    biasboth = [layer.biases, layer2.biases]

    fm.store_weights_and_biases(arrboth, biasboth)

def getWeights():
    arr = fm.retrieve_weights(sizingTuples)
    print("weights: ", arr[0][1])
    print("bias: ", arr[1][1])


#file = fm.FileManager()
#control = MainClass(file)


#storeRandWeights()
getWeights()



print("complete")

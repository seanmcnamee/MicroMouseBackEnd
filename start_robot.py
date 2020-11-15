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

def storeRandWeights():
    layer = NN.Layer_Dense(5, 2)
    print("Printing NN")
    print(layer.weights.transpose())

    layer2 = NN.Layer_Dense(5, 2)
    print("Printing NN")
    print(layer2.weights.transpose())

    arrboth = [layer.weights, layer2.weights]
    biasboth = [layer.biases, layer2.biases]

    fm.store_weights_and_biases(arrboth, biasboth)

def getWeights():
    arr = fm.retrieve_weights()
    print("Data frame: ", arr)


#file = fm.FileManager()
#control = MainClass(file)


#storeRandWeights()
getWeights()



print("complete")

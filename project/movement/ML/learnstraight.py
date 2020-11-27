import project.movement.ML.neuralnetwork as nn
import project.movement.robotcontrol as rc
import project.fileio.filemanager as fm
import numpy as np
import random

class LearnStraight:
    def __init__(self, file=fm.FileManager(), lastX=3):
        self.max_closeness = .4
        self.max_forward_closeness = .05
        self.last_x = lastX
        self.correct_percents = None
        self.outputlist = []
        self.correct_percents = []
        self.robot = rc.RobotControl(file=file)
        self.network_structure = ((10, 5), (5, 5), (5, 2))
        self.network = nn.Network(self.network_structure)
        self.network.add_stored_dense()
        activ1 = nn.Activation_ReLU()
        self.network.add(activ1)
        self.network.add_stored_dense()
        activ2 = nn.Activation_ReLU()
        self.network.add(activ2)
        self.network.add_stored_dense()
        softmax = nn.Activation_Softmax()
        self.network.add(softmax)
        self.network.set(
            loss=nn.Loss_CategoricalCrossentropy(),
            optimizer=nn.Optimizer_SGD(learning_rate=.2)
        )
        self.network.finalize()
    
    def start(self):
        sensor_data = (0, 0, 0, 0, 0, 0, 0, 0)
        outputs = [[0, 0]]
        while max(sensor_data[:-5]) < self.max_closeness and sensor_data[2] < self.max_forward_closeness:
            #sensor_data = self.get_normalized_data_tuple(outputs[0][0], outputs[0][1])
            sensor_data = self.robot.get_normalized_data_tuple(outputs[0][0], outputs[0][1])
            self.network.add_data(sensor_data)
            self.outputlist.append(sensor_data)
            outputs = self.network.forward(sensor_data, False)

            print("Outputs: ", outputs)

            self.robot.set_motors(outputs[0][0], outputs[0][1])
        self.robot.set_motors(0, 0)

        self.set_correct_percents(max(sensor_data[0], sensor_data[1], sensor_data[7]) >= self.max_closeness, \
                                max(sensor_data[3:6]) >= self.max_closeness)

        for i in range(len(self.outputlist)):
            print("Largest: ", max(self.outputlist[i][:-5]), ", L-R: ", self.outputlist[i][-2:])
    
    def train(self):
        self.network.train_network(self.correct_percents, self.last_x, 1)
        self.network.store_layers()

    def get_normalized_data_tuple(self, motorL, motorR):
        return (0.3, 0.3, 0.01, 0.3, 0.3, 0.3, 0.3, 0.3, motorL, motorR)

    def set_correct_percents(self, hitLeft, hitRight):
        print("LEFT-RIGHT: ", hitLeft, " ", hitRight)
        gamma = .1
        leftSide = .55 if hitLeft else .45
        rightSide = .55 if hitRight else .45
        for i in range(len(self.outputlist)-self.last_x, len(self.outputlist)):
            if not(hitLeft) and not(hitRight):
                self.correct_percents.append((self.outputlist[i][-2], self.outputlist[i][-1]))
            else:
                self.correct_percents.append((leftSide*gamma**i, rightSide*gamma**i))
        self.correct_percents = np.array(self.correct_percents)
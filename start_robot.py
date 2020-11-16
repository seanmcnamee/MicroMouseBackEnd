import project.movement.robotcontrol as RobotControl
import project.fileio.filemanager as fm
import project.movement.ML.neuralnetwork as NN
import numpy as np

class MainClass():
    def __init__(self, file):
        self.robot = RobotControl.RobotControl(file)

    def explore(self):
        should_continue = True

        while should_continue:
            print("test")

def updateLargest():
    file = fm.FileManager()
    robot = RobotControl.RobotControl(file)
    tuple_readings = robot.get_sensor_readings()
    print(tuple_readings)
    fm.store_highest_data(tuple_readings)





updateLargest()


#storeRandWeights()
#getWeights()
#network = NN.Network()
#network.store_layers()

print("complete")

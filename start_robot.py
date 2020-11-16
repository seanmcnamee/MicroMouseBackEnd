import project.movement.robotcontrol as RobotControl
import project.fileio.filemanager as fm
import project.movement.ML.learnstraight as learn
import project.movement.ML.neuralnetwork as NN
import numpy as np



def updateLargest():
    file = fm.FileManager()
    robot = RobotControl.RobotControl(file)
    tuple_readings = robot.get_sensor_readings()
    print(tuple_readings)
    fm.store_highest_data(tuple_readings)

def testThrough():
    runner = learn.LearnStraight()
    print("About to run the robot")
    runner.start()




#updateLargest()
testThrough()




#storeRandWeights()
#getWeights()
#network = NN.Network()
#network.store_layers()

print("complete")

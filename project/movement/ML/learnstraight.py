import project.movement.ML.neuralnetwork as nn
import project.movement.robotcontrol as rc
import project.fileio.filemanager as fm

class LearnStraight:
    def __init__(self, file=fm.FileManager()):
        self.max_closeness = .4
        self.max_forward_closeness = .05
        self.outputlist = []
        self.robot = rc.RobotControl(file=file)
        self.network_structure = ((10, 5), (5, 5), (5, 2))
        self.network = nn.Network(self.network_structure)
    
    def start(self):
        sensor_data = (0, 0, 0, 0, 0, 0, 0, 0, 0)
        outputs = [0, 0]
        while max(sensor_data[:-5]) < self.max_closeness and sensor_data[2] < self.max_forward_closeness:
            sensor_data = self.robot.get_normalized_data_tuple(outputs[0], outputs[1])
            self.outputlist.append(sensor_data)
            outputs = self.network.calculate_outputs(sensor_data)
            self.robot.set_motors(outputs[0], outputs[1])
        self.robot.set_motors(0, 0)
        for i in range(len(self.outputlist)):
            print("Largest: ", max(self.outputlist[i][:-5]), ", L-R: ", self.outputlist[i][-2:])
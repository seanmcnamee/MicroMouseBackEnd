import project.movement.robotcontrol as RobotControl
import project.fileio.filemanager as fm

class MainClass():
    def __init__(self, port):
        self.robot = RobotControl.RobotControl(port)

    def explore(self):
        should_continue = True

        while should_continue:
            print("test")

file = fm.FileManager()
#control = MainClass(file)
print(file.get_raw_data())

import numpy as np
a1 = [1, 2, 3, 4]
a2 = [5, 6, 7, 8]
a3 = [9, 1, 2, 3]

a = np.array([a1, a2, a3])
print(a)


print("complete")

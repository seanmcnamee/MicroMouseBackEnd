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
control = MainClass(file)


print("complete")

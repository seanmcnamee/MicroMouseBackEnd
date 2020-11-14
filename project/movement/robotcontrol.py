import FA
import project.fileio.filemanager as fm

FULL_POWER = 100

class RobotControl():
    """Deals with Robot movement and data fetching
    """
    
    def __init__(self, file=fm.FileManager()):
        self.file = file
        self.robot = FA.Create()
        self.robot.ComOpen(file.port)

    def set_motors(self, left_percent, right_percent):
        """Sets the motor speeds based on percentages of each motor's top speed

        Args:
            leftPercent ([type]): this being larger will result in a right turn
            rightPercent ([type]): this being larger will result in a left turn
        """
        self.robot.SetMotors(left_percent*FULL_POWER, right_percent*FULL_POWER)

    def get_sensor_readings(self, left_percent, right_percent):
        """Returns a 9-tuple. 7 sensor readings and the leftPercent then rightPercent

        Returns:
            9-Tuple: Used for the ML input data and storage
        """
        d_0 = self.robot.ReadIR(0) #left
        d_1 = self.robot.ReadIR(1) #frontleft
        d_2 = self.robot.ReadIR(2) #front
        d_3 = self.robot.ReadIR(3) #frontright
        d_4 = self.robot.ReadIR(4) #right
        d_5 = self.robot.ReadIR(5) #backright
        d_6 = self.robot.ReadIR(6) #back
        d_7 = self.robot.ReadIR(7) #backleft
        return (d_0, d_1, d_2, d_3, d_4, d_5, d_6, d_7, left_percent, right_percent)
        

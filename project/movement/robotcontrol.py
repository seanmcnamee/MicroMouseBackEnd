import FA
import project.fileio.filemanager as fm

FULL_POWER = 100

class RobotControl():
    """Deals with Robot movement and data fetching
    """
    
    def __init__(self, file=fm.FileManager()):
        self.file = file
        self.max_readings = fm.retrieve_highest_sensors()
        self.robot = FA.Create()
        self.robot.ComOpen(file.port)

    def set_motors(self, left_percent, right_percent):
        """Sets the motor speeds based on percentages of each motor's top speed

        Args:
            leftPercent ([type]): this being larger will result in a right turn
            rightPercent ([type]): this being larger will result in a left turn
        """
        self.robot.SetMotors(left_percent*FULL_POWER, right_percent*FULL_POWER)

    def get_sensor_readings(self):
        """Returns a 7-tuple of sensor readings

        Returns:
            7-Tuple: Used for the tracking the sensor max values
        """
        d_0 = self.robot.ReadIR(0) #left
        d_1 = self.robot.ReadIR(1) #frontleft
        d_2 = self.robot.ReadIR(2) #front
        d_3 = self.robot.ReadIR(3) #frontright
        d_4 = self.robot.ReadIR(4) #right
        d_5 = self.robot.ReadIR(5) #backright
        d_6 = self.robot.ReadIR(6) #back
        d_7 = self.robot.ReadIR(7) #backleft
        return (d_0, d_1, d_2, d_3, d_4, d_5, d_6, d_7)

    def get_normalized_data_tuple(self, left_percent, right_percent):
        """All values returned should be between 0 and 1

        Returns:
            9-tuple: normalized sensor readings and motor percents
        """
        raw_readings = self.get_data_tuple(left_percent, right_percent)
        normalized_tuple = tuple(raw_readings[i]/(self.max_readings[i] if i < len(self.max_readings) else 1) for i in range(len(raw_readings)))
        return normalized_tuple

    def get_data_tuple(self, left_percent, right_percent):
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
        

import FA
import project.robot_commands as RobotCommands

class RobotControl():

    def __init__(self):
        self.full_power = 100
        self.one_block_distance = 185
        self.right_angle_turn = 90
        self.degree_adjustment = 4
        self.open_adjacency_max = 10
        
        self.robot = FA.Create()
        self.robot.ComOpen(16)  #83 is 16   #other is 15
        self.robot.Forwards(30)
        #self.robot.SetMotors(self.full_power, self.full_power)

    def convertFromInstructionsToMovementAndReturnReverse(self, cmd_stack):
        reverse_stack = []
        while len(cmd_stack) > 0:
            command = cmd_stack.pop(-1)
            #print("Stack length: " + str(len(cmd_stack)))
            #print("Command: " + str(len(reverse_stack)))
            inv_command = RobotCommands.Directions(-1*int(command))
            #print("\tInv-Cmd: " + str(inv_command))
            reverse_stack.append(inv_command)
            self.moveFromCommand(command)
        return reverse_stack

    def moveFromCommand(self, command):
        self.adjustStraight()
        if command == RobotCommands.Directions.forwards:
            self.robot.Forwards(self.one_block_distance)
        elif command == RobotCommands.Directions.right:
            self.robot.Right(self.right_angle_turn)
        elif command == RobotCommands.Directions.left:
            self.robot.Left(self.right_angle_turn)

    def adjustStraight(self):
        left_side = self.robot.ReadIR(1)
        right_side = self.robot.ReadIR(3)

        if left_side <= self.open_adjacency_max and right_side <= self.open_adjacency_max:
            if (left_side > right_side):
                self.robot.Right(self.degree_adjustment)
            else:
                self.robot.Left(self.degree_adjustment)

        print("Readings LR: " + str(left_side) + " - " + str(right_side))

    def getAdjacencyReadings(self):
        """returns a 3-dim boolean tuple in the form of (LEFT, FORWARD, RIGHT) where each represents an open path"""
        front = self.robot.ReadIR(2)
        left = self.robot.ReadIR(0)
        right = self.robot.ReadIR(4)
        print("\tReadings: " + str(left) + " - " + str(front) + " - " + str(right))
        return (left<=self.open_adjacency_max, front<=self.open_adjacency_max, right<=self.open_adjacency_max)
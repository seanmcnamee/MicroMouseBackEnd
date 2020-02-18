
"""import project.robot_commands as RobotCommands

class RobotControl():
    def __init__(self):
        self.dummy = 0

    def convertFromInstructionsToMovementAndReturnReverse(self, cmd_stack):
        reverse_stack = []
        while len(cmd_stack) > 0:
            command = cmd_stack.pop(-1)
            print("\t"+str(command))
            inv_command = RobotCommands.Directions(-1*int(command))
            reverse_stack.append(inv_command)
            self.moveFromCommand(command)
        return reverse_stack

    def moveFromCommand(self, command):
        print("\t\t\t\t\t\t\t\t\t\t\t\tFollowing Command\t\t"+str(command))

    def getAdjacencyReadings(self):
        print("Looking at L-F-R sensors (1-0)")
        left = input("\tLeft: ")=='1'
        forward = input("\tForward: ")=='1'
        right = input("\tRight: ")=='1'
        print(str(left) + " - " + str(forward) + " - " + str(right))
        return((left, forward, right))
    """

import FA
import project.robot_commands as RobotCommands

class RobotControl():

    def __init__(self):
        self.full_power = 100
        self.one_block_distance = 175 #180 for 83
        self.right_angle_turn = 87
        self.degree_adjustment = 4
        self.open_adjacency_max = 25
        self.needs_adjustment_min = 30
        self.straight_enough_margin = 100
        self.tooFarFromWall = 200
        
        self.robot = FA.Create()
        self.robot.ComOpen(15)  #83 is 16   #720 is 15
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
            self.robot.SetMotors(self.full_power, self.full_power)
            self.robot.Forwards(self.one_block_distance)
        elif command == RobotCommands.Directions.right:
            self.robot.Right(self.right_angle_turn)
        elif command == RobotCommands.Directions.left:
            self.robot.Left(self.right_angle_turn)
        elif command == RobotCommands.Directions.turnAround:
            self.robot.Right(2*self.right_angle_turn)

    def adjustStraight(self):
        left_side = self.robot.ReadIR(0)
        front_left = self.robot.ReadIR(1)
        back_left = self.robot.ReadIR(7)

        right_side = self.robot.ReadIR(4)
        front_right = self.robot.ReadIR(3)
        back_right = self.robot.ReadIR(5)
        print("\t\t\t\t\t\t\t\t\t\tLeft-Right Adjust Readings: " + str(left_side) + " - " + str(right_side))
        print("\t\t\t\t\t\t\t\t\t\tLeft-Front-Back Adjust Readings: " + str(front_left) + " - " + str(back_left))
        print("\t\t\t\t\t\t\t\t\t\tRight-Front-Back Adjust Readings: " + str(front_right) + " - " + str(back_right))

        if (left_side > self.needs_adjustment_min and right_side > self.needs_adjustment_min) and (abs(right_side-left_side)>self.straight_enough_margin):
            
            if (left_side > right_side):
                print("\tRight Straight Adjustment")
                self.robot.Right(self.degree_adjustment)
            else:
                print("\tLeft Straight Adjustment")
                self.robot.Left(self.degree_adjustment)
        elif left_side > self.needs_adjustment_min:
            if back_left - front_left > self.straight_enough_margin or left_side < self.tooFarFromWall:
            #if front_left > left_side:
                print("left side is too close")
                self.robot.Left(self.degree_adjustment)
            elif front_left - back_left > self.straight_enough_margin:
                self.robot.Right(self.degree_adjustment)
        elif right_side > self.needs_adjustment_min:
            if back_right - front_right > self.straight_enough_margin or right_side < self.tooFarFromWall:
                print("right side is too close")
                self.robot.Right(self.degree_adjustment)
            elif front_right - back_right > self.straight_enough_margin:
                self.robot.Left(self.degree_adjustment)
        else:
            print("\tNo adjustment required")
        """
        else:
            if left_side > 200:
                print("\tRight Straight Adjustment")
                self.robot.Right(self.degree_adjustment)
            elif right_side > 200:
                print("\tLeft Straight Adjustment")
                self.robot.Left(self.degree_adjustment)
            else:
                
        """

        print("Readings LR: " + str(left_side) + " - " + str(right_side))

    def getAdjacencyReadings(self):
        #returns a 3-dim boolean tuple in the form of (LEFT, FORWARD, RIGHT) where each represents an open path
        front = self.robot.ReadIR(2)
        left = self.robot.ReadIR(0)
        right = self.robot.ReadIR(4)
        print("\tReadings: " + str(left) + " - " + str(front) + " - " + str(right))
        return (left<=self.open_adjacency_max, front<=self.open_adjacency_max, right<=self.open_adjacency_max)



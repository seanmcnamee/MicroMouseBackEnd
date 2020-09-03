import enum
import FA
class Directions(enum.IntEnum):
    left = -1
    forwards = 0
    right = 1
    
def convertFromInstructionsToMovement(cmd_stack):
    reverse_stack = []
    while len(cmd_stack) > 0:
        command = cmd_stack.pop(-1)
        #print("Stack length: " + str(len(cmd_stack)))
        #print("Command: " + str(len(reverse_stack)))

        inv_command = Directions(-1*int(command))
        
        #print("\tInv-Cmd: " + str(inv_command))
        reverse_stack.append(inv_command)
        moveFromCommand(command)
    return reverse_stack

def moveFromCommand(command):
    one_block_distance = 185
    adjustStraight()
    if command == Directions.forwards:
        robot.Forwards(one_block_distance)
    elif command == Directions.right:
        robot.Right(90)
    elif command == Directions.left:
        robot.Left(90)

def adjustStraight():
    left_side = robot.ReadIR(1)
    right_side = robot.ReadIR(3)

    if (left_side > right_side):
        robot.Right(4)
    else:
        robot.Left(4)

    print("Readings LR: " + str(left_side) + " - " + str(right_side))
    #max_size = max(left_side, right_side)
    #full_power = 100
    #robot.SetMotors(left_side/max_size * full_power, right_side/max_size * full_power)

def explore():
    front = robot.ReadIR(2)
    left = robot.ReadIR(0)
    right = robot.ReadIR(4)

    print("Left: " + str(left) + ", front: " + str(front) + ", Right: " + str(right))

#Initialize Connection and open port
robot = FA.Create()
robot.ComOpen(16)
#83 is 16
#other is 15

full_power = 100
#Test robot controls

print("Let's Go!")
#cmd_stack = [Directions.forwards, Directions.left, Directions.forwards, Directions.left, Directions.forwards, Directions.forwards, Directions.forwards, Directions.forwards, Directions.forwards, Directions.forwards, Directions.forwards, Directions.forwards, Directions.forwards, Directions.forwards, Directions.forwards, Directions.forwards, Directions.forwards, Directions.forwards, Directions.forwards, Directions.forwards, Directions.forwards, Directions.forwards]
#cmd_stack = [Directions.forwards, Directions.right, Directions.forwards, Directions.forwards, Directions.forwards, Directions.forwards, Directions.forwards]
#reverse_stack = convertFromInstructionsToMovement(cmd_stack)
#adjustStraight()
#robot.Right(180)
#convertFromInstructionsToMovement(reverse_stack)
explore()

print("complete")
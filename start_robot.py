import project.movement.robotcontrol as RobotControl
import project.robot_commands as RobotCommands
import project.mapstructure.map as Map
import project.mapstructure.GUI.gui as GUI

class RobotMazeLink():
    def __init__(self):
        self.robot = RobotControl.RobotControl()
        self.maze = Map.Map()
        self.commandStack = []

    def addAndReturnOpenAdjacents(self):
        adjacency_tuple = self.robot.getAdjacencyReadings()
        adjacent_coords = self.convertFromBooleansToCoordinates(adjacency_tuple)
        for coord in adjacent_coords:
            if not(coord==None):
                self.maze.add_node(coord)
        return adjacent_coords

    def convertFromBooleansToCoordinates(self, adjacency_tuple):
        current_direction = self.maze.current_direction
        current_location = self.maze.current_node.location
        leftCoord = rightCoord = forwardCoord = None
        print("Current location: " + str(current_location))

        if (adjacency_tuple[0] == True): #Left
            new_direction = (-current_direction[1], current_direction[0])
            print("LEFT direction: " + str(new_direction))
            leftCoord = (current_location[0]+new_direction[0], current_location[1]+new_direction[1])
        if (adjacency_tuple[1] == True): #Forward
            print("forward direction: " + str(current_direction))
            forwardCoord = (current_location[0]+current_direction[0], current_location[1]+current_direction[1])
        if (adjacency_tuple[2] == True): #Right
            new_direction = (current_direction[1], -current_direction[0])
            print("RIGHT direction: " + str(new_direction))
            rightCoord = (current_location[0]+new_direction[0], current_location[1]+new_direction[1])
        print("Adjacent Locations: " + str((leftCoord, forwardCoord, rightCoord)))
        return (leftCoord, forwardCoord, rightCoord)

    def visitOneOfAdjacents(self, coordList):
        adjacency_list = self.maze.current_node.get_adjacently_list()
        for node in adjacency_list:
            if not(node.visited):
                self.visit(node, coordList)
                return True
        return False

    def visit(self, node, coordList):
        self.maze.visit(node.location)

        commands = [RobotCommands.Directions.forwards]
        if node.location==coordList[0]:
            commands.append(RobotCommands.Directions.left)
        elif node.location==coordList[2]:
            commands.append(RobotCommands.Directions.right)

        commandsToBacktrack = self.robot.convertFromInstructionsToMovementAndReturnReverse(commands)

        for command in commandsToBacktrack:
            self.commandStack.append(command)




link = RobotMazeLink()

#TODO add an explore function for the robot

print("Let's Go!")
adjacents = link.addAndReturnOpenAdjacents()
print("Printing Adjacent Coordinates 1")
for coord in adjacents:
    print("\t"+str(coord))

print("Visiting One 1")
link.visitOneOfAdjacents(adjacents)

print("\t\t" + str(link.commandStack))

adjacents = link.addAndReturnOpenAdjacents()
print("Printing Adjacent Coordinates 2")
for coord in adjacents:
    print("\t"+str(coord))

print("Visiting One 2")
link.visitOneOfAdjacents(adjacents)

print("\t\t" + str(link.commandStack))



adjacents = link.addAndReturnOpenAdjacents()
print("Printing Adjacent Coordinates 3")
for coord in adjacents:
    print("\t"+str(coord))

print("Visiting One 3")
link.visitOneOfAdjacents(adjacents)

print("\t\t" + str(link.commandStack))



#cmd_stack = [Directions.forwards, Directions.left, Directions.forwards, Directions.left, Directions.forwards, Directions.forwards, Directions.forwards, Directions.forwards, Directions.forwards, Directions.forwards, Directions.forwards, Directions.forwards, Directions.forwards, Directions.forwards, Directions.forwards, Directions.forwards, Directions.forwards, Directions.forwards, Directions.forwards, Directions.forwards, Directions.forwards, Directions.forwards]
#cmd_stack = [Directions.forwards, Directions.right, Directions.forwards, Directions.forwards, Directions.forwards, Directions.forwards, Directions.forwards]
#reverse_stack = convertFromInstructionsToMovement(cmd_stack)
#adjustStraight()
#robot.Right(180)
#convertFromInstructionsToMovement(reverse_stack)

print("complete")
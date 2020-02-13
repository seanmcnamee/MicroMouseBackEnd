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
            leftCoord = self.getLeftDirection(current_location, current_direction)
        if (adjacency_tuple[1] == True): #Forward
            forwardCoord = self.getForwardDirection(current_location, current_direction)
        if (adjacency_tuple[2] == True): #Right
            rightCoord = self.getRightDirection(current_location, current_direction)
        print("Adjacent Locations: " + str((leftCoord, forwardCoord, rightCoord)))
        return (leftCoord, forwardCoord, rightCoord)

    def getCoordFromCommand(self, command):
        current_direction = self.maze.current_direction
        current_location = self.maze.current_node.location
        if command==RobotCommands.Directions.forwards:
            return self.getForwardDirection(current_location, current_direction)
        if command==RobotCommands.Directions.left:
            return self.getLeftDirection(current_location, current_direction)
        if command==RobotCommands.Directions.right:
            return self.getRightDirection(current_location, current_direction)


    def getLeftDirection(self, current_location, current_direction):
        new_direction = (-current_direction[1], current_direction[0])
        print("LEFT direction: " + str(new_direction))
        leftCoord = (current_location[0]+new_direction[0], current_location[1]+new_direction[1])
        return leftCoord

    def getForwardDirection(self, current_location, current_direction):
        print("forward direction: " + str(current_direction))
        forwardCoord = (current_location[0]+current_direction[0], current_location[1]+current_direction[1])
        return forwardCoord

    def getRightDirection(self, current_location, current_direction):
        new_direction = (current_direction[1], -current_direction[0])
        print("RIGHT direction: " + str(new_direction))
        rightCoord = (current_location[0]+new_direction[0], current_location[1]+new_direction[1])
        return rightCoord

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

    def exploreUntilDeadEnd(self):
        nodeVisited = True
        while nodeVisited:
            adjacents = self.addAndReturnOpenAdjacents()
            for coord in adjacents:
                print("\t"+str(coord))
            nodeVisited = self.visitOneOfAdjacents(adjacents)
        
    
    def backtrackOntoIntersection(self):
        adjacentNodes = []
        while len(adjacentNodes) <= 0 and len(self.commandStack) > 0:
            topCommand = self.commandStack.pop()
            next_coord = self.getCoordFromCommand(topCommand)
            maze.visit(next_coord)
            adjacentNodes = maze.current_node.get_adjacently_list()
        if len(self.commandStack) > 0:
            continueOntoNextPath(adjacentNodes)
            return True
        else:
            return False
    
    def continueOntoNextPath(self, adjacentNodes):
        most_recent_command = self.commandStack.pop()
        adjacents = self.addAndReturnOpenAdjacents()
        print("At intersection")
        for coord in adjacents:
            print("\t"+str(coord))
                
        adjacency_list = self.maze.current_node.get_adjacently_list()
        for node in adjacency_list:
            if not(node.visited):
                self.visitAndEditCommandStack(node, adjacents, most_recent_command)
                return True
        return False

    def visitAndEditCommandStack(self, node, coordList, most_recent_command):
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

link.explore()
print("\t\t" + str(link.commandStack))



#cmd_stack = [Directions.forwards, Directions.left, Directions.forwards, Directions.left, Directions.forwards, Directions.forwards, Directions.forwards, Directions.forwards, Directions.forwards, Directions.forwards, Directions.forwards, Directions.forwards, Directions.forwards, Directions.forwards, Directions.forwards, Directions.forwards, Directions.forwards, Directions.forwards, Directions.forwards, Directions.forwards, Directions.forwards, Directions.forwards]
#cmd_stack = [Directions.forwards, Directions.right, Directions.forwards, Directions.forwards, Directions.forwards, Directions.forwards, Directions.forwards]
#reverse_stack = convertFromInstructionsToMovement(cmd_stack)
#adjustStraight()
#robot.Right(180)
#convertFromInstructionsToMovement(reverse_stack)

print("complete")
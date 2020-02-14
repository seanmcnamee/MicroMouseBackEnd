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
            leftCoord = self.getLeftDirectionCoord(current_location, current_direction)
        if (adjacency_tuple[1] == True): #Forward
            forwardCoord = self.getForwardDirectionCoord(current_location, current_direction)
        if (adjacency_tuple[2] == True): #Right
            rightCoord = self.getRightDirectionCoord(current_location, current_direction)
        print("\tAdjacent Locations: " + str((leftCoord, forwardCoord, rightCoord)))
        return (leftCoord, forwardCoord, rightCoord)

    def getCoordFromCommand(self, command):
        current_direction = self.maze.current_direction#TODO SEE WHY HE IS NONE
        current_location = self.maze.current_node.location
        print("Forward and Location: " + str(current_direction) + " - " + str(current_location))
        if command==RobotCommands.Directions.forwards:
            return self.getForwardDirectionCoord(current_location, current_direction)
        if command==RobotCommands.Directions.left:
            return self.getLeftDirectionCoord(current_location, current_direction)
        if command==RobotCommands.Directions.right:
            return self.getRightDirectionCoord(current_location, current_direction)

    def getCommandFromCoord(self, coord):
        current_direction = self.maze.current_direction
        current_location = self.maze.current_node.location
        if coord == self.getForwardDirectionCoord(current_location, current_direction):
            return RobotCommands.Directions.forwards
        if coord==self.getLeftDirectionCoord(current_location, current_direction):
            return RobotCommands.Directions.left
        if coord==self.getRightDirectionCoord(current_location, current_direction):
            return RobotCommands.Directions.right

    def getNewFacingDirection(self, command):
        current_direction = self.maze.current_direction
        if command==RobotCommands.Directions.turnAround:
            return self.getReverseDirection(current_direction)
        if command==RobotCommands.Directions.left:
            return self.getLeftDirection(current_direction)
        if command==RobotCommands.Directions.right:
            return self.getRightDirection(current_direction)
        if command==RobotCommands.Directions.forwards:
            return current_direction
        raise Exception("Can't find new facing direction for" + str(command))

    def getLeftDirectionCoord(self, current_location, current_direction):
        new_direction = self.getLeftDirection(current_direction)
        print("\tLEFT direction: " + str(new_direction))
        leftCoord = (current_location[0]+new_direction[0], current_location[1]+new_direction[1])
        return leftCoord

    def getLeftDirection(self, current_direction):
        return (-current_direction[1], current_direction[0])

    def getForwardDirectionCoord(self, current_location, current_direction):
        print("\tFORWARD direction: " + str(current_direction))
        forwardCoord = (current_location[0]+current_direction[0], current_location[1]+current_direction[1])
        return forwardCoord

    def getRightDirectionCoord(self, current_location, current_direction):
        new_direction = self.getRightDirection(current_direction)
        print("\tRIGHT direction: " + str(new_direction))
        rightCoord = (current_location[0]+new_direction[0], current_location[1]+new_direction[1])
        return rightCoord

    def getRightDirection(self, current_direction):
        return (current_direction[1], -current_direction[0])

    def getReverseDirection(self, current_direction):
        return (-current_direction[0], -current_direction[1])
        

    def visitOneOfAdjacents(self, coordList):
        adjacency_list = self.maze.current_node.get_adjacently_list(False)
        for node in adjacency_list:
            self.visitAndUpdateReverseStack(node, coordList)
            return True
        return False

    def visitAndUpdateReverseStack(self, node, coordList):
        commands = [RobotCommands.Directions.forwards]
        if node.location==coordList[0]:
            commands.append(RobotCommands.Directions.left)
        elif node.location==coordList[2]:
            commands.append(RobotCommands.Directions.right)

        commandsToBacktrack = self.robot.convertFromInstructionsToMovementAndReturnReverse(commands)

        self.maze.visit(node.location)

        for command in commandsToBacktrack:
            self.commandStack.append(command)


    def explore(self):
        should_continue = True

        while should_continue:
            self.exploreUntilDeadEnd()
            should_continue = self.backtrackOntoIntersection()

        print("End location: " + str(self.maze.current_node.location))



    def exploreUntilDeadEnd(self):
        print("--Exploring Untiul Dead End--")
        nodeVisited = True
        while nodeVisited:
            adjacents = self.addAndReturnOpenAdjacents()
            nodeVisited = self.visitOneOfAdjacents(adjacents)
        
    
    def backtrackOntoIntersection(self):
        print("--Backtracking Until Intersection--")
        self.robot.moveFromCommand(RobotCommands.Directions.turnAround)
        self.maze.current_direction = self.getNewFacingDirection(RobotCommands.Directions.turnAround)
        print("New facing direction after spin: " + str(self.maze.current_direction))
        #self.commandStack.append(RobotCommands.Directions.turnAround)
        unvisitedAdjacentNodes = []
        while len(unvisitedAdjacentNodes) <= 0 and len(self.commandStack) > 0:
            print("Currently at " + str(self.maze.current_node.location))
            topCommand = self.commandStack.pop()
            self.robot.moveFromCommand(topCommand)
            print("Robot just did: " + str(topCommand))
            self.maze.current_direction = self.getNewFacingDirection(topCommand)
            print("New facing direction: " + str(self.maze.current_direction))
            if topCommand == RobotCommands.Directions.forwards:
                next_coord = self.getCoordFromCommand(topCommand)
                self.maze.visit(next_coord)
                unvisitedAdjacentNodes = self.maze.current_node.get_adjacently_list(False)
            print("Unvisited Adjacent Nodes:")
            for node in unvisitedAdjacentNodes:
                print("\t"+str(node.location))
        if len(self.commandStack) > 0:
            self.continueOntoNextPath(unvisitedAdjacentNodes)
            return True
        else:
            return False
    
    def continueOntoNextPath(self, unvisitedAdjacentNodes):
        print("--Continuing onto next path--")
        most_recent_command = self.commandStack.pop() #this is the command that we have to edit

        node_visiting = unvisitedAdjacentNodes.pop()
        command_to_proceed = self.getCommandFromCoord(node_visiting.location) #Which direction should I go next?
        new_stack_command = self.revStackCommandBasedOn(most_recent_command, command_to_proceed) #How will this affect my way back

        self.robot.moveFromCommand(command_to_proceed)
        self.maze.visit(node_visiting.location)
        self.commandStack.append(new_stack_command)

    def revStackCommandBasedOn(self, most_recent_command, command_to_proceed):
        if (most_recent_command==RobotCommands.Directions.forwards):
            return RobotCommands.Directions(-1*int(command_to_proceed))
        else:
            formula_solution = -int(most_recent_command)*((abs(int(most_recent_command))+1)%2)
            return RobotCommands.Directions(formula_solution)

    def getToMiddleAndBack(self):
        self.commandStack = self.robot.convertFromInstructionsToMovementAndReturnReverse(self.maze.find_fastest_path())
        self.robot.convertFromInstructionsToMovementAndReturnReverse(commandStack)



link = RobotMazeLink()

#TODO add an explore function for the robot


print("Let's Go!")

link.explore()
print("\t\t" + str(link.commandStack))

link.getToMiddleAndBack()

#cmd_stack = [Directions.forwards, Directions.left, Directions.forwards, Directions.left, Directions.forwards, Directions.forwards, Directions.forwards, Directions.forwards, Directions.forwards, Directions.forwards, Directions.forwards, Directions.forwards, Directions.forwards, Directions.forwards, Directions.forwards, Directions.forwards, Directions.forwards, Directions.forwards, Directions.forwards, Directions.forwards, Directions.forwards, Directions.forwards]
#cmd_stack = [Directions.forwards, Directions.right, Directions.forwards, Directions.forwards, Directions.forwards, Directions.forwards, Directions.forwards]
#reverse_stack = convertFromInstructionsToMovement(cmd_stack)
#adjustStraight()
#robot.Right(180)
#convertFromInstructionsToMovement(reverse_stack)

print("complete")
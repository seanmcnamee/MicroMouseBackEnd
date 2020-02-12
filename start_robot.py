import project.movement.robotcontrol as RobotControl
import project.mapstructure.map as Map
import project.mapstructure.GUI.gui as GUI

class RobotMazeLink():
    def __init__(self):
        self.robot = RobotControl.RobotControl()
        self.maze = Map.Map()

    def addOpenAdjacents(self):
        adjacency_tuple = self.robot.getAdjacencyReadings()


    def convertFromBooleansToCoordinates(self, adjacency_tuple):
        coordinates_to_add = []
        current_location_x = self.maze.current_node[self.maze.current_node.xval]
        current_location_y = self.maze.current_node[self.maze.current_node.yval]
        if (adjacency_tuple[0] == True): #Left
            current_direction = self.maze.current_direction
            new_x = current_location_x + current_direction[1] 
            new_y = current_location_y - current_direction[0]
            coordinates_to_add.append((current_location_x))





link = RobotMazeLink()

#TODO add an explore function for the robot



commandList = maze.find_fastest_path()

print("Let's Go!")
#cmd_stack = [Directions.forwards, Directions.left, Directions.forwards, Directions.left, Directions.forwards, Directions.forwards, Directions.forwards, Directions.forwards, Directions.forwards, Directions.forwards, Directions.forwards, Directions.forwards, Directions.forwards, Directions.forwards, Directions.forwards, Directions.forwards, Directions.forwards, Directions.forwards, Directions.forwards, Directions.forwards, Directions.forwards, Directions.forwards]
#cmd_stack = [Directions.forwards, Directions.right, Directions.forwards, Directions.forwards, Directions.forwards, Directions.forwards, Directions.forwards]
#reverse_stack = convertFromInstructionsToMovement(cmd_stack)
#adjustStraight()
#robot.Right(180)
#convertFromInstructionsToMovement(reverse_stack)
explore()

print("complete")
import project.movement.robotcontrol as RobotControl
import project.robot_commands as RobotCommands
import project.mapstructure.map as Map
import project.mapstructure.GUI.gui as GUI

class RobotMazeLink():
    def __init__(self, user='SeanPC', robot_name='FA-20'):
        self.robot = RobotControl.RobotControl(user, robot_name)
        self.maze = Map.Map()
        self.command_stack = []

    def add_and_return_open_adjacents(self):
        adjacency_tuple = self.robot.getAdjacencyReadings()
        adjacent_coords = self.convert_from_booleans_to_coordinates(adjacency_tuple)
        for coord in adjacent_coords:
            if not(coord is None):
                self.maze.add_node(coord)
        return adjacent_coords

    def convert_from_booleans_to_coordinates(self, adjacency_tuple):
        left_coord = None
        right_coord = None
        forward_coord = None

        if adjacency_tuple[0]: #Left
            left_coord = self.maze.get_left_direction_coord()
        if adjacency_tuple[1]: #Forward
            forward_coord = self.maze.get_forward_direction_coord()
        if adjacency_tuple[2]: #Right
            right_coord = self.maze.get_right_direction_coord()
        print("\tAdjacent Locations: " + str((left_coord, forward_coord, right_coord)))
        return (left_coord, forward_coord, right_coord)

    def visit_one_of_adjacents(self, coordList):
        adjacency_list = self.maze.current_node.get_adjacently_list(False)
        for node in adjacency_list:
            self.visit_and_update_reverse_stack(node, coordList)
            return True
        return False

    def visit_and_update_reverse_stack(self, node, coordList):
        commands = [RobotCommands.Directions.forwards]
        if node.location == coordList[0]:
            commands.append(RobotCommands.Directions.left)
        elif node.location == coordList[2]:
            commands.append(RobotCommands.Directions.right)

        commands_to_backtrack = self.robot.convertFromInstructionsToMovementAndReturnReverse(commands)

        self.maze.visit(node.location)

        for command in commands_to_backtrack:
            self.command_stack.append(command)


    def explore(self):
        should_continue = True

        while should_continue:
            self.explore_until_dead_end()
            should_continue = self.backtrack_through_intersection()

        print("End location: " + str(self.maze.current_node.location))



    def explore_until_dead_end(self):
        print("--Exploring Untiul Dead End--")
        node_visited = True
        while node_visited:
            print("\tCommands in stack:")
            print("\t"+str(self.command_stack))
            adjacents = self.add_and_return_open_adjacents()
            node_visited = self.visit_one_of_adjacents(adjacents)
        
    
    def backtrack_through_intersection(self):
        print("--Backtracking Until Intersection--")
        self.robot.moveFromCommand(RobotCommands.Directions.turnAround)
        self.maze.current_direction = self.maze.get_new_facing_direction(RobotCommands.Directions.turnAround)
        print("New facing direction after spin: " + str(self.maze.current_direction))
        #self.commandStack.append(RobotCommands.Directions.turnAround)
        unvisited_adjacent_nodes = []
        while len(unvisited_adjacent_nodes) <= 0 and len(self.command_stack) > 0:
            print("Currently at " + str(self.maze.current_node.location))
            top_command = self.command_stack.pop()
            self.robot.moveFromCommand(top_command)
            print("Robot just did: " + str(top_command))
            self.maze.current_direction = self.maze.get_new_facing_direction(top_command)
            print("New facing direction: " + str(self.maze.current_direction))
            if top_command == RobotCommands.Directions.forwards:
                next_coord = self.maze.get_coord_from_command(top_command)
                self.maze.visit(next_coord)
                unvisited_adjacent_nodes = self.maze.current_node.get_adjacently_list(False)
            print("Unvisited Adjacent Nodes:")
            for node in unvisited_adjacent_nodes:
                print("\t"+str(node.location))
            print("\tCommands in stack:")
            print("\t"+str(self.command_stack))
        if len(self.command_stack) > 0:
            self.continue_onto_next_branch(unvisited_adjacent_nodes)
            return True
        else:
            return False
    
    def continue_onto_next_branch(self, unvisitedAdjacentNodes):
        print("--Continuing onto next path--")
        most_recent_command = self.command_stack.pop() #this is the command that we have to edit

        
        if most_recent_command == RobotCommands.Directions.forwards:
            print("\tRetaining the 'forward' to get to the intersection")
            self.command_stack.append(most_recent_command)

        node_visiting = unvisitedAdjacentNodes.pop()
        command_to_proceed = self.maze.get_command_from_coord(node_visiting.location) #Which direction should I go next?
        new_stack_command = self.rev_stack_command_based_on(most_recent_command, command_to_proceed) #How will this affect my way back

        self.command_stack.append(new_stack_command) #This is replacing the top command

        self.robot.moveFromCommand(command_to_proceed) #This is the command to face properly or continue
        self.maze.visit(node_visiting.location)
        
        if command_to_proceed != RobotCommands.Directions.forwards: #If you haven't actually continued, do so
            self.robot.moveFromCommand(RobotCommands.Directions.forwards)
            #self.command_stack.append(RobotCommands.Directions.forwards)
        if new_stack_command != RobotCommands.Directions.forwards:
            self.command_stack.append(RobotCommands.Directions.forwards)
    
        print("\tCommands in stack:")
        print("\t"+str(self.command_stack))

    def rev_stack_command_based_on(self, most_recent_command, command_to_proceed):
        print("Most recent stack movement: " + str(most_recent_command))
        if (most_recent_command == RobotCommands.Directions.forwards):
            return command_to_proceed
        else:
            print("Int of command: " + str(int(command_to_proceed)))
            print("(abs(^^)+1) %2 : " + str(((abs(int(command_to_proceed))+1)%2)))
            formula_solution = -int(most_recent_command)*((abs(int(command_to_proceed))+1)%2)
            print("End num: " + str(formula_solution))
            print("New direction: " + str(RobotCommands.Directions(formula_solution)))
            return RobotCommands.Directions(formula_solution)

    def get_to_middle_and_back(self):
        self.maze.reset_node_visits()
        self.maze.choose_finish_node()
        self.robot.moveFromCommand(RobotCommands.Directions.turnAround)
        self.command_stack = self.robot.convertFromInstructionsToMovementAndReturnReverse(self.maze.find_fastest_path())
        self.robot.moveFromCommand(RobotCommands.Directions.turnAround)
        #self.robot.convertFromInstructionsToMovementAndReturnReverse(self.command_stack)

    def humanControl(self):
        command = ""
        while (command != "q"):
            command = input("Command (w-a-s-d-r q): ")
            if (command == "w"):
                self.robot.moveFromCommand(RobotCommands.Directions.forwards)
            elif (command == "a"):
                self.robot.moveFromCommand(RobotCommands.Directions.left)
            elif (command == "s"):
                self.robot.moveFromCommand(RobotCommands.Directions.turnAround)
            elif (command == "d"):
                self.robot.moveFromCommand(RobotCommands.Directions.right)
            elif (command == "r"):
                self.robot.adjustStraight()


LINK = RobotMazeLink(user='SeanLaptop', robot_name='FA-20')

#LINK.robot.adjustStraight()
#TODO add an explore function for the robot
LINK.humanControl()

LINK.robot.saveToCSV()
"""
print("Let's Go!")

LINK.explore()
print("\t\t" + str(LINK.command_stack))


LINK.get_to_middle_and_back()
"""

#GUI = GUI.GUI(LINK.maze)
#GUI.display()

#cmd_stack = [Directions.forwards, Directions.left, Directions.forwards, Directions.left, Directions.forwards, Directions.forwards, Directions.forwards, Directions.forwards, Directions.forwards, Directions.forwards, Directions.forwards, Directions.forwards, Directions.forwards, Directions.forwards, Directions.forwards, Directions.forwards, Directions.forwards, Directions.forwards, Directions.forwards, Directions.forwards, Directions.forwards, Directions.forwards]
#cmd_stack = [Directions.forwards, Directions.right, Directions.forwards, Directions.forwards, Directions.forwards, Directions.forwards, Directions.forwards]
#reverse_stack = convertFromInstructionsToMovement(cmd_stack)
#adjustStraight()
#robot.Right(180)
#convertFromInstructionsToMovement(reverse_stack)

print("complete")

import project.mapstructure.node as Node
import project.robot_commands as RobotCommands
import project.mapstructure.priority_queue as PQ


class Map:
    """Oversees the connection of nodes for the maze"""

    def __init__(self):
        start_location = (0, 0)
        self.default_facing = (0, 1)
        self.start = Node.Node(start_location)
        self.current_node = None
        self.node_set = {self.start} #Exists to make sure duplicate nodes aren't created
        self.visit(start_location)
        self.finish = None

        self.turn_weight = 1
        self.straight_weight = 1

        self.node_index = 0
        self.priority_index = 1
        
    def add_node(self, new_location):
        """create new node at new_location and create the connections"""
        node_to_connect = Node.Node(new_location)
        already_exists = False
        for node in self.node_set:
            if node.equals(new_location):
                already_exists = True
                node_to_connect = node

        self.set_both_connections(node_to_connect)
        if not(already_exists):
            self.node_set.add(node_to_connect)

    def set_both_connections(self, new_node):
        """Set the connections between the nodes"""
        distance_to_new = self.current_node.distance_between(new_node.location)
        self.current_node.set_adjacent_from_direction(distance_to_new, new_node)
        reverse_distance = new_node.distance_between(self.current_node.location)
        new_node.set_adjacent_from_direction(reverse_distance, self.current_node)



    def visit(self, location):
        for node in self.node_set:
            if node.equals(location):
                self.current_direction = self.default_facing #Hold a record of the current way you are facing
                if not(self.current_node==None):
                    self.current_direction = self.current_node.distance_between(node.location)
                self.current_node = node #And save the current node you are at
                node.visit()
                print("\t\t\t\t\t\t\t\t\t\t\tvisited " + str(node.location))
                return True
        raise Exception("Can't visit a node that doesn't exist (" + str(location) + ")")

    def find_fastest_path(self):
        #create a dictionary connecting each node to the path_length to it from self.start
        node_keys = {self.start: (None, 0)}
        for node in self.node_set:
            node.unvisit() #Unvisit every node
            if not(node==self.start):
                node_keys[node] = (None, float("inf"))

        #Create Priority Queue of nodes based on the dictionary data
        priority_nodes = PQ.PriorityQueue(node_keys)

        while not(self.finish.visited):
            current_node = priority_nodes.pop()[self.node_index]
            for node in current_node.get_adjacently_list(False):
                new_length = self.calc_new_distance(node_keys, current_node, node)
                if (new_length < node_keys[node][self.priority_index]):
                    node_keys[node] = (current_node, new_length)
                    priority_nodes.update((node, new_length))
            current_node.visit()
        
        return self.convert_to_commands(node_keys)
                
    def calc_new_distance(self, node_keys, current_node, next_node):
        new_length = 0
        new_length += node_keys[current_node][self.priority_index] + self.straight_weight

        #Default facing direction
        current_direction = self.default_facing
        if (not(current_node == self.start)):
            previous_node = node_keys[current_node][self.node_index]
            current_direction = current_node.distance_between(previous_node.location)
    
        next_direction = next_node.distance_between(current_node.location)
        if not(current_direction[0] == next_direction[0]) or not(current_direction[1] == next_direction[1]):
            new_length += self.turn_weight
        return new_length   
 
    def convert_to_commands(self, dictionary):
        """Dictionary is in the form {node, (previousNode, totalPathSize)}"""
        distance_stack = []
        cmd_stack = []
        current_node = self.finish
        next_node = dictionary[current_node][self.node_index]
        
        while not(next_node == None):
            next_distance = next_node.distance_between(current_node.location)
            if len(distance_stack)>0:
                self.add_turn_if_needed(cmd_stack, distance_stack[-1], next_distance)
            distance_stack.append(next_distance)
            cmd_stack.append(RobotCommands.Directions.forwards)

            current_node = next_node
            next_node = dictionary[current_node][self.node_index]

        return cmd_stack

    def add_turn_if_needed(self, cmd_stack, current_dist, previous_dist):
        if not(previous_dist[self.current_node.xval] == current_dist[self.current_node.xval]) and not(previous_dist[self.current_node.yval] == current_dist[self.current_node.yval]):
            print("\tChecking " + str(previous_dist) + " to " + str(current_dist))
            if (previous_dist[self.current_node.xval] == 0):
                if previous_dist[self.current_node.yval] == current_dist[self.current_node.xval]:
                    cmd_stack.append(RobotCommands.Directions.right)
                    print("\t\tx=0  Right")
                else:
                    cmd_stack.append(RobotCommands.Directions.left)
                    print("\t\tx=0 Left")
            else: #y=0
                if previous_dist[self.current_node.xval] == current_dist[self.current_node.yval]:
                    cmd_stack.append(RobotCommands.Directions.left)
                    print("\t\ty=0  Left")
                else:
                    cmd_stack.append(RobotCommands.Directions.right)
                    print("\t\ty=0  Right")

    def get_coord_from_command(self, command):
        if command == RobotCommands.Directions.forwards:
            return self.get_forward_direction_coord()
        if command == RobotCommands.Directions.left:
            return self.get_left_direction_coord()
        if command == RobotCommands.Directions.right:
            return self.get_right_direction_coord()

    def get_command_from_coord(self, coord):
        if coord == self.get_forward_direction_coord():
            return RobotCommands.Directions.forwards
        if coord == self.get_left_direction_coord():
            return RobotCommands.Directions.left
        if coord == self.get_right_direction_coord():
            return RobotCommands.Directions.right

    def get_new_facing_direction(self, command):
        if command == RobotCommands.Directions.turnAround:
            return self.get_reverse_direction()
        if command == RobotCommands.Directions.left:
            return self.get_left_direction()
        if command == RobotCommands.Directions.right:
            return self.get_right_direction()
        if command == RobotCommands.Directions.forwards:
            return self.current_direction
        raise Exception("Can't find new facing direction for" + str(command))

    def get_left_direction_coord(self):
        new_direction = self.get_left_direction()
        print("\tLEFT direction: " + str(new_direction))
        left_coord = (self.current_node.location[0]+new_direction[0], self.current_node.location[1]+new_direction[1])
        return left_coord

    def get_left_direction(self):
        return (-self.current_direction[1], self.current_direction[0])

    def get_forward_direction_coord(self):
        forward_coord = (self.current_node.location[0]+self.current_direction[0], self.current_node.location[1]+self.current_direction[1])
        return forward_coord

    def get_right_direction_coord(self):
        new_direction = self.get_right_direction()
        right_coord = (self.current_node.location[0]+new_direction[0], self.current_node.location[1]+new_direction[1])
        return right_coord

    def get_right_direction(self):
        return (self.current_direction[1], -self.current_direction[0])

    def get_reverse_direction(self):
        return (-self.current_direction[0], -self.current_direction[1])

    def reset_node_visits(self):
        for node in self.node_set:
            node.unvisit()

    def choose_finish_node(self):
        for node in self.node_set:
            adjacency_list = node.get_adjacently_list(False)
            if len(adjacency_list) == 3:
                print("Candidate at " + str(node.location))
                adj0 = set(adjacency_list[0].get_adjacently_list(False))
                adj1 = set(adjacency_list[1].get_adjacently_list(False))
                adj2 = set(adjacency_list[2].get_adjacently_list(False))

                inters1 = adj0.intersection(adj1)
                inters2 = adj0.intersection(adj2)
                inters3 = adj1.intersection(adj2)

                adjUnion = inters1.union(inters2).union(inters3)


                if len(adjUnion) >= 2:
                    self.finish = node
                    print("Finish of maze at " + str(node.location))
                    return True
        raise Exception("There's no finish square for this maze!")



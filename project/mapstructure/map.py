import mapstructure.node as Node
import mapstructure.robot_commands as RobotCommands
import mapstructure.priority_queue as PQ


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
        distance_to_new = self.current_node.distance_between(new_node)
        self.current_node.set_adjacent_from_direction(distance_to_new, new_node)
        reverse_distance = new_node.distance_between(self.current_node)#(-1*distance_to_new[0], -1*distance_to_new[1]) #TODO make sure new code works
        new_node.set_adjacent_from_direction(reverse_distance, self.current_node)



    def visit(self, location):
        for node in self.node_set:
            if node.equals(location):
                self.current_direction = self.default_facing #Hold a record of the current way you are facing
                if not(self.current_node==None):
                    self.current_direction = self.current_node.distance_between(node)
                self.current_node = node
                node.visit()
                print("visited " + str(node.location))
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
            for node in current_node.get_adjacently_list():
                new_length = self.calc_new_distance(node_keys, current_node, node)
                if (new_length < node_keys[node][self.priority_index]):
                    node_keys[node] = (current_node, new_length)
                    priority_nodes.update((node, new_length))
            current_node.visit()
        
        return self.convert_to_commands(node_keys)
                
                

    def calc_new_distance(self, node_keys, current_node, next_node):
        new_length = 0
        new_length += node_keys[current_node][self.priority_index] + self.straight_weight

        #previous_node = Node.Node((self.start.location[0]-self.default_facing[0], self.start.location[1]-self.default_facing[1])) #Default facing direction node
        current_direction = self.default_facing
        if (not(current_node==self.start)):
            previous_node = node_keys[current_node][self.node_index]
            current_direction = current_node.distance_between(previous_node)
    
        next_direction = next_node.distance_between(current_node)
        if not(current_direction[0] == next_direction[0]) or not(current_direction[1] == next_direction[1]):
            new_length += self.turn_weight

        return new_length

        """#TODO TODO TODO TODO THIS LOOKS FUCKING  W R O N G
        previous_node = Node.Node((self.start.location[0], self.start.location[1]-1)) #This shows that you always start by facing "North"
        if not(previous_node==None): #TODO this looks like it should say if not(node_keys[current_node][self.node_index]==None)
            previous_node = node_keys[current_node][self.node_index]
        
        current_dist = (0, 1)#current_node.distance_between(previous_node)
        next_dist = (0, 1)#next_node.distance_between(current_node)
        if current_dist[0] == next_dist[0] and current_dist[1] == next_dist[1]:
            new_length += self.turn_weight

        return new_length
        """

    """Dictionary is in the form {node, (previousNode, totalPathSize)}"""
    def convert_to_commands(self, dictionary):
        distance_stack = []
        cmd_stack = []
        current_node = self.finish
        next_node = dictionary[current_node][self.node_index]
        
        while not(next_node==None):
            next_distance = next_node.distance_between(current_node)
            if len(distance_stack)>0:
                self.add_turn_if_needed(cmd_stack, distance_stack[-1], next_distance)
            distance_stack.append(next_distance)
            cmd_stack.append(RobotCommands.Commands.forwards)

            current_node = next_node
            next_node = dictionary[current_node][self.node_index]

        return cmd_stack

        
    def add_turn_if_needed(self, cmd_stack, current_dist, previous_dist):
        x = 0
        y = 1
        if not(previous_dist[x]==current_dist[x]) and not(previous_dist[y]==current_dist[y]):
            print("\tChecking " + str(previous_dist) + " to " + str(current_dist))
            if (previous_dist[x] == 0):
                if previous_dist[y] == current_dist[x]:
                    cmd_stack.append(RobotCommands.Commands.right)
                    print("\t\tx=0  Right")
                else:
                    cmd_stack.append(RobotCommands.Commands.left)
                    print("\t\tx=0 Left")
            else: #y=0
                if previous_dist[x] == current_dist[y]:
                    cmd_stack.append(RobotCommands.Commands.left)
                    print("\t\ty=0  Left")
                else:
                    cmd_stack.append(RobotCommands.Commands.right)
                    print("\t\ty=0  Right")


        
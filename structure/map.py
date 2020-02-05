import structure.node as Node

class Map:
    """Oversees the connection of nodes for the maze"""

    def __init__(self):
        start_location = (0, 0)
        self.start = Node.Node(start_location)
        self.node_set = {self.start} #Exists to make sure duplicate nodes aren't created
        self.visit(start_location)
        self.finish = None
        
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
        reverse_distance = (-1*distance_to_new[0], -1*distance_to_new[1])
        new_node.set_adjacent_from_direction(reverse_distance, self.current_node)


    def visit(self, location):
        for node in self.node_set:
            if node.equals(location):
                self.current_node = node
                node.visit()
                print("visited " + str(node.location))
                return True
        raise Exception("Can't visit a node that doesn't exist (" + str(location) + ")")

        
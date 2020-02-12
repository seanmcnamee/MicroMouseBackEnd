class Node:
    """A singular intersection in the map."""
    def __init__(self, location):
        self.xval = 0
        self.yval = 1
        self.location = location
        self.visited = False
        self.north_node = None
        self.south_node = None
        self.east_node = None
        self.west_node = None

    #TODO make this take take in a tuple (location) so that the user doesn't have to worry about storing nodes?
    def distance_between(self, other_node):
        """Find the distance between 2 nodes (not two directional)"""
        x_distance = other_node.location[self.xval]-self.location[self.xval]
        y_distance = other_node.location[self.yval]-self.location[self.yval]
        print("Distance between " + str(self.location) + " and " + str(other_node.location) + " is " + str(x_distance) + ", " + str(y_distance))
        return (x_distance, y_distance)

    def set_adjacent_from_direction(self, direction, new_node):
        """Choose the proper adjacent node depending on direction"""
        print("\t Setting connection from " + str(self.location) + " to " + str(new_node.location) + " based on direction " + str(direction))
        if direction[self.xval] == 0:
            if direction[self.yval] < 0:
                self.north_node = new_node
            else:
                self.south_node = new_node
        elif direction[self.xval] < 0:
            self.west_node = new_node
        else:
            self.east_node = new_node

    def visit(self):
        self.visited = True

    def unvisit(self):
        self.visited = False

    def equals(self, other_location):
        """Is this node's location equal to the given location?"""
        x_equal = other_location[self.xval] == self.location[self.xval]
        y_equal = other_location[self.yval] == self.location[self.yval]
        return x_equal and y_equal

    def get_adjacently_list(self):
        adj_list = []
        if not(self.north_node==None):
            adj_list.append(self.north_node) 
        if not(self.south_node==None):
            adj_list.append(self.south_node)
        if not(self.east_node==None):
            adj_list.append(self.east_node)
        if not(self.west_node==None):
            adj_list.append(self.west_node) 
        return adj_list

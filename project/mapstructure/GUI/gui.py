import turtle
import project.mapstructure.map as Map
import project.mapstructure.node as Node


class GUI:

    def __init__(self, map):
        self.map = map
        self.scale = 50
        self.shiftY = -200

        xSway = 0
        for node in self.map.node_set:
            if abs(node.location[node.xval]) > abs(xSway):
                xSway = node.location[node.xval]
        self.shiftX = -self.scale*xSway/2.0

    def display(self):
        print("Displaying...")
        turtle.hideturtle()
        turtle.speed(0)
        for node in self.map.node_set:
            print("\tNode at " + str(node.location))
            turtle.penup()
            turtle.goto(self.scale*node.location[node.xval] + self.shiftX, self.scale*node.location[node.yval] + self.shiftY)
            turtle.pendown()
            self.draw_square()
            for adjacent in node.get_adjacently_list():
                self.draw_connection_between(node, adjacent)
        input("Okie")


    def draw_square(self):
        turtle.setheading(90)
        turtle.pencolor("black")
        turtle.forward(self.scale)
        turtle.right(90)
        turtle.forward(self.scale)
        turtle.right(90)
        turtle.forward(self.scale)
        turtle.right(90)
        turtle.forward(self.scale)

    def draw_connection_between(self, current, adjacent):
        print("Connection")
        turtle.penup()
        turtle.goto(self.scale*current.location[current.xval] + self.scale/2.0 + self.shiftX, self.scale*current.location[current.yval]+self.scale/2.0 + self.shiftY)
        turtle.pendown()
        dist_between = current.distance_between(adjacent)
        heading = 90
        if dist_between == (0, 1):
            heading = 90
        elif dist_between == (0, -1):
            heading = 270
        elif dist_between == (-1, 0):
            heading = 180
        elif dist_between == (1, 0):
            heading = 0
        turtle.pencolor("blue")
        turtle.setheading(heading)
        turtle.forward(self.scale/2.0)


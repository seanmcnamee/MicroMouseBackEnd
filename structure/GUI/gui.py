import structure.map as Map
import structure.node as Node
import turtle

class GUI:

    def __init__(self, map):
        self.map = map
        self.scale = 50
        self.y_factor = -1
        #self.g = turtle.Turtle()
        #g.

    def display(self):
        print("Displaying...")
        turtle.hideturtle()
        turtle.speed(0)
        for node in self.map.node_set:
            print("\tNode at " + str(node.location))
            turtle.penup()
            turtle.goto(self.scale*node.location[node.xval], self.y_factor*self.scale*node.location[node.yval])
            turtle.pendown()
            self.draw_square()
        input("Okie")


    def draw_square(self):
        turtle.setheading(0)
        turtle.forward(self.scale)
        turtle.right(90)
        turtle.forward(self.scale)
        turtle.right(90)
        turtle.forward(self.scale)
        turtle.right(90)
        turtle.forward(self.scale)

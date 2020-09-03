import mapstructure.map as Map
import mapstructure.GUI.gui as GUI

print("Imported!")


maze = Map.Map()

#When adding a node, it connect to the previously added node ((0, 0) is default start
#We can add all adjacent nodes and only travel to one!
n00 = maze.current_node
maze.add_node((0, 1))
maze.add_node((1, 0))
maze.visit((1, 0)) #We only travel to the second
n10 = maze.current_node
maze.add_node((2, 0))   #then from that node, add another
maze.visit((2, 0))      #and visit it
n20 = maze.current_node
maze.finish = n20

print("Printinng directions froms start to finish")
commandList = maze.find_fastest_path()
for command in commandList:
    print(command.name)
"""Therefore, when the robot is exploring, it will do the following:

1. look for all adjacent pathways and add their coordinates as nodes
2. pick one to follow

The trick is to always pick an unexplored node, and keep a list of node coordinates so

"""

print("GUI display")

gui = GUI.GUI(maze)
gui.display()

print("Done!")



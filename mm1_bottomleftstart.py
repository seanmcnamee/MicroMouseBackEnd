import mapstructure.map as Map
import mapstructure.GUI.gui as GUI

maze = Map.Map()


maze.add_node((0, 1))
maze.visit((0, 1))

maze.add_node((-1, 1))
maze.visit((-1, 1))

maze.add_node((-1, 0)) 
maze.add_node((-1, 2))
maze.visit((-1, 0))

maze.add_node((-2, 0))
maze.visit((-2, 0))

maze.add_node((-3, 0))
maze.visit((-3, 0))

maze.add_node((-4, 0))
maze.visit((-4, 0))

maze.add_node((-5, 0))
maze.add_node((-4, 1))
maze.visit((-4, 1))

maze.add_node((-5, 1))
maze.add_node((-4, 2))
maze.visit((-5, 1))

maze.add_node((-6, 1))
maze.visit((-6, 1))

maze.add_node((-6, 0))
maze.visit((-6, 0))
maze.start = maze.current_node #Changing the start node to the bottom left
##Dead end (bottom left)

maze.visit((-4, 2))

maze.add_node((-3, 2))
maze.add_node((-5, 2))
maze.visit((-3, 2))

maze.add_node((-2, 2))
maze.visit((-2, 2))

maze.add_node((-2, 3))
maze.add_node((-2, 1))
maze.visit((-2, 1))

maze.add_node((-3, 1))
#dead end (bottom middle boot)

maze.visit((-5, 2))

maze.add_node((-5, 3))
maze.visit((-5, 3))

maze.add_node((-6, 3))
maze.visit((-6, 3))

maze.add_node((-6, 2))
maze.add_node((-6, 4))
maze.visit((-6, 4))

maze.add_node((-6, 5))
maze.add_node((-5, 4))
maze.visit((-6, 5))

maze.add_node((-6, 6))
maze.visit((-6, 6))

maze.add_node((-5, 6))
#dead end (top left)

maze.visit((-5, 4))

maze.add_node((-5, 5))
maze.add_node((-4, 4))
maze.visit((-4, 4))

maze.add_node((-4, 3))
maze.add_node((-3, 4))
maze.visit((-4, 3))

maze.add_node((-3, 3))
maze.visit((-3, 3))

maze.add_node((-3, 4))
maze.finish = maze.current_node #Set the middle when we get to it
#dead end (center)

maze.visit((-5, 5))

maze.add_node((-4, 5))
maze.visit((-4, 5))

maze.add_node((-3, 5))
maze.visit((-3, 5))

maze.add_node((-2, 5))
maze.visit((-2, 5))

maze.add_node((-2, 4))
maze.visit((-2, 4))

maze.add_node((-1, 4))
maze.visit((-1, 4))

maze.add_node((-1, 3))
maze.visit((-1, 3))

maze.add_node((0, 3))
maze.visit((0, 3))

maze.add_node((0, 2))
maze.add_node((0, 4)) 
maze.visit((0, 4))

maze.add_node((0, 5))
maze.visit((0, 5))

maze.add_node((0, 6))
maze.visit((0, 6))

maze.add_node((-1, 6))
maze.visit((-1, 6))

maze.add_node((-1, 5))
maze.add_node((-2, 6))
maze.visit((-2, 6))

maze.add_node((-3, 6))
maze.visit((-3, 6))

maze.add_node((-4, 6))
#dead end (top middle)

maze.visit((0, 2))

maze.add_node((-1, 2))
#Done


commandList = maze.find_fastest_path()

print("Printinng directions froms start to finish")
for i in range(len(commandList)):
    print(commandList[-(i+1)].name + "     \t" + str(i))

    
print("GUI display")

gui = GUI.GUI(maze)
gui.display()

print("Done!")



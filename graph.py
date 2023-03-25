import random
# from cmu_112_graphics import *

class Node:
    nodeTypes = ['wall', 'cell', 'key', 'goal']
    def __init__(self, row, col, t, color):
        self.row = row
        self.col = col
        self.t = t
        self.color = color
        
    def __repr__(self):
        return f"Node({self.row}, {self.col}, {self.t}, {self.color})"
    
    def getPos(self):
        return (self.row, self.col)
    
    def getType(self):
        return self.t
    
    def getColor(self):
        return self.color

class Wall(Node):
    def __init__(self, row, col, color):
        super().__init__(row, col, 'wall', color)
    
    def __repr__(self):
        return f"Wall({self.row}, {self.col}, {self.color})"

class Cell(Node):
    def __init__(self, row, col, color):
        super().__init__(row, col, 'cell', color)
    
    def __repr__(self):
        return f"Cell({self.row}, {self.col}, {self.color})"

#Idea for graph class (and some funcitons) from Graph Algorithm Mini-Lecture
class Graph:
    def __init__(self, wallColor='white', cellColor='white'):
        self.table = {}
        self.cellColor = cellColor
        self.wallColor = wallColor


    def __repr__(self):
        return f'{self.table}'
    
    def addEdge(self, nodeA, nodeB, weight=1):
        if nodeA not in self.table:
            self.table[nodeA] = {}
        if nodeB not in self.table:
            self.table[nodeB] = {}
        self.table[nodeA][nodeB] = weight
        self.table[nodeB][nodeA] = weight
    
    def getNodes(self):
        return list(self.table)
    
    def getNeighbors(self, node):
        return set(self.table.get(node, {}))
    
    def convertTo2DList(self):
        #All walls
        maze = [[Wall(row, col, self.wallColor) for col in range(self.cols*2-1)] for row in range(self.rows*2-1)]
        
        #Puts all cells into the maze
        for node in self.table:
            row, col = node.getPos()
            maze[row*2][col*2] = Cell(row, col, self.cellColor)

        #Makes paths between cells
        for row, col in self.table:
            neighbors = self.getNeighbors((row, col))
            for neighbor in neighbors:
                nrow, ncol = neighbor
                drow, dcol = nrow - row, ncol - col
                maze[row*2+drow][col*2+dcol] = Cell(row, col, self.cellColor)
        self.L = maze

    def render(self, canvas):
        for row in range(len(self.L)):
            for col in range(len(self.L[0])):
                node = self.L[row][col]
                canvas.create_rectangle(col*self.cellSize, row*self.cellSize, 
                                            (col+1)*self.cellSize, (row+1)*self.cellSize, 
                                            fill=node.getColor())


class Maze(Graph):
    mazeTypes = ['dfs', 'prim', 'kruskal']

    @staticmethod
    def getTypes():
        return Maze.mazeTypes

    def __init__(self, rows, cols, mazeType, wallColor='white', goalColors=None, keyColor='orange', cellColor='white'):
        super().__init__(wallColor, cellColor)
        self.goalColors = goalColors if goalColors else ['blue', 'red']
        self.keyColor = keyColor

        self.rows = rows
        self.cols = cols
        self.mazeType = mazeType

    def generate(self):
        #Generates a maze
        if self.mazeType == 'dfs':
            self.generateIterDFS()
        elif self.mazeType == 'prim':
            self.generatePrim()
        elif self.mazeType == 'kruskal':
            self.generateKruskal()
        self.convertTo2DList()
        self.addGoals()
        self.addKey()
    
    def generateIterDFS(self):
        pass

    def generatePrim(self):
        pass

    def generateKruskal(self):
        pass

    def checkPos(self, row, col):
        return 0 <= row < self.rows and 0 <= col < self.cols and self.L[row][col] != 'wall'

    def render3D(self, canvas):
        pass
    
    #TODO make gotKey
    def renderMinimap(self, canvas, gotKey=False):
        #Draws the minimap
        for row in range(len(self.L)):
            for col in range(len(self.L[0])):
                node = self.L[row][col]
                canvas.create_rectangle(col*self.cellSize, row*self.cellSize, 
                                            (col+1)*self.cellSize, (row+1)*self.cellSize, 
                                            fill=node.getColor())

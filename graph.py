import random
# from cmu_112_graphics import *

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
        maze = [['wall']*(self.cols*2-1) for _ in range(self.rows*2-1)]
        
        #Puts all cells into the maze
        for row, col in self.table:
            maze[row*2][col*2] = 'cell'

        #Makes paths between cells
        for row, col in self.table:
            neighbors = self.getNeighbors((row, col))
            for neighbor in neighbors:
                nrow, ncol = neighbor
                drow, dcol = nrow - row, ncol - col
                maze[row*2+drow][col*2+dcol] = 'cell'
        self.L = maze

    def render(self, canvas):
        for row in range(len(self.L)):
            for col in range(len(self.L[0])):
                if self.L[row][col] == 'wall':
                    canvas.create_rectangle(col*self.cellSize, row*self.cellSize, 
                                            (col+1)*self.cellSize, (row+1)*self.cellSize, 
                                            fill=self.wallColor)
                elif self.L[row][col] == 'cell':
                    canvas.create_rectangle(col*self.cellSize, row*self.cellSize, 
                                            (col+1)*self.cellSize, (row+1)*self.cellSize, 
                                            fill=self.cellColor)



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
    
    def checkPos(self, row, col):
        return 0 <= row < self.rows and 0 <= col < self.cols and self.L[row][col] != 'wall'

    def render3D(self, canvas):
        pass
    
    #TODO make gotKey
    def renderMinimap(self, canvas, gotKey=False):
        #Draws the minimap
        for row in range(len(self.L)):
            for col in range(len(self.L[0])):
                if self.L[row][col] == 'wall':
                    canvas.create_rectangle(col*self.cellSize, row*self.cellSize, 
                                            (col+1)*self.cellSize, (row+1)*self.cellSize, 
                                            fill=self.wallColor)
                elif self.L[row][col] == 'cell':
                    canvas.create_rectangle(col*self.cellSize, row*self.cellSize, 
                                            (col+1)*self.cellSize, (row+1)*self.cellSize, 
                                            fill=self.cellColor)
                elif self.L[row][col] == 'key':
                    canvas.create_rectangle(col*self.cellSize, row*self.cellSize, 
                                            (col+1)*self.cellSize, (row+1)*self.cellSize, 
                                            fill=self.cellColor)
                elif self.L[row][col] == 'goal':
                    canvas.create_rectangle(col*self.cellSize, row*self.cellSize, 
                                            (col+1)*self.cellSize, (row+1)*self.cellSize, 
                                            fill=self.goalColors[1] if gotKey else self.goalColors[0])
import random
from cmu_112_graphics import *

#Idea for graph class (and some funcitons) from Graph Algorithm Mini-Lecture
class Graph():
    def __init__(self):
        self.table = {}
    
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

    #dfs
    def dfsGetPath(self, nodeA, nodeB):
        path = self.dfsGetPathHelper(nodeA, nodeB, dict())
        newPath = {}

        if path is None: return path

        for node in path:
            if path[node] != None:
                newPath[node] = path[node]

        return newPath

    def dfsGetPathHelper(self, nodeA, nodeB, visited):
        if nodeA == nodeB:
            return visited
        else:
            visited[nodeA] = None
            #Search neighbors
            for neighbor in self.getNeighbors(nodeA):
                if neighbor not in visited:
                    
                    visited[nodeA] = neighbor
                    result = self.dfsGetPathHelper(neighbor, nodeB, visited)
                    if result != None:
                        return result

                    #If we get nowhere, backtrack
                    visited.pop(nodeA)
            return None
    
    #bfs
    #Algorithm inspired from https://learn.co/lessons/maze-solver
    #and https://hurna.io/academy/algorithms/maze_pathfinder/bfs.html
    def bfsGetPath(self, nodeA, nodeB):
        #Start with a queue with the node and the path it took to get to the node
        queue = [(nodeA, {})]
        visited = {nodeA}
        while queue != []:
            node, path = queue.pop(0)
            
            neighbors = self.getNeighbors(node)
            for neighbor in neighbors:
                if neighbor not in visited:
                    #Edits path
                    newPath = copy.deepcopy(path)
                    newPath[node] = neighbor
                    
                    visited.add(neighbor)
                    queue.append((neighbor, newPath))
                    
                    if neighbor == nodeB:
                        return newPath
        return None


'''
FROM GRAPH TO MAZE
'''
class Maze(Graph):
    def __init__(self, app):
        super().__init__()
        self.app = app
    #Checks if the move is legal or not
    def isLegalMove(self, row, col, visited):
        if 0 <= row < self.rows and 0 <= col < self.cols:
            if (row, col) not in visited:
                return True
        return False


    '''
    Maze Generation
    '''
    #Adds edges to make the maze not perfect
    def randomize(self, paths):
        for _ in range(paths):
            row, col = random.randrange(self.rows), random.randrange(self.cols)
            
            possibleWalls = [(0,1), (0,-1), (1, 0), (-1, 0)]
            i = random.randrange(len(possibleWalls))
            direction = possibleWalls.pop(i)
            drow, dcol = direction
            neighbor = row+drow, col+dcol
            
            while neighbor in self.getNeighbors((row, col)) or neighbor not in self.table:
                i = random.randrange(len(possibleWalls))
                direction = possibleWalls.pop(i)
                drow, dcol = direction
                neighbor = row+drow, col+dcol
                
                #If there are no possible walls, choose new cell
                if possibleWalls == []:
                    row, col = random.randrange(self.rows), random.randrange(self.cols)
                    possibleWalls = [(0,1), (0,-1), (1, 0), (-1, 0)]
                           
            self.addEdge((row,col), neighbor)

    #Idea for Maze Generation from https://en.wikipedia.org/wiki/Maze_generation_algorithm
    #Makes a dfs Maze
    def dfsMaze(self, rows, cols):
        self.rows = rows
        self.cols = cols
        return self.dfsMazeHelper(0, 0, visited=set())

    def dfsMazeHelper(self, row, col, visited):
        if len(visited) == self.rows*self.cols:
            return self
        else:
            #Randomized moves
            visited.add((row, col))
            moves = [(0,1), (0,-1), (1, 0), (-1, 0)]
            random.shuffle(moves)
            for move in moves:
                drow, dcol = move
                #Inherent backtracking because doesn't change row or col
                newRow = row + drow
                newCol = col + dcol
                if self.isLegalMove(newRow, newCol, visited):
                    #Makes a path between the two
                    self.addEdge((row, col), (newRow, newCol))
                    result = self.dfsMazeHelper(newRow, newCol, visited)
                    if result != None:
                        return result
            return None

    #Algorithm inspired from: https://courses.cs.washington.edu/courses/cse326/07su/prj2/kruskal.html
    #and also https://en.wikipedia.org/wiki/Maze_generation_algorithm
    def kruskalMaze(self, rows, cols):
        #Makes a grid of empty cells
        self.rows = rows
        self.cols = cols
        for row in range(rows):
            for col in range(cols):
                cell = (row, col)
                self.table[cell] = {}
        
        cells = list(self.table)
        wallsDown = 0

        #Finally generates maze
        while wallsDown < (rows)*(cols) - 1:
            #Picks a random cell
            cell = random.choice(cells)
            row, col = cell
            
            #Finds a possible random neighbor
            possibleWalls = [(0,1), (0,-1), (1, 0), (-1, 0)]
            direction = random.choice(possibleWalls)
            drow, dcol = direction
            neighbor = row+drow, col+dcol
            
            #Neighbor check and legality check
            if neighbor in self.table and neighbor not in self.getNeighbors(cell):
                
                #Mergeing if there isn't a path
                if self.bfsGetPath(cell, neighbor) is None:
                    self.addEdge(cell, neighbor)
                    wallsDown += 1

    #Algorithm inspired from: https://courses.cs.washington.edu/courses/cse326/07su/prj2/kruskal.html
    #and also https://en.wikipedia.org/wiki/Maze_generation_algorithm
    def primsMaze(self, rows, cols):
        self.rows = rows
        self.cols = cols
        
        visited = set()
        cells = set()
        
        cell = (random.randrange(rows), random.randrange(cols))
        cells.add(cell)
        visited.add(cell)
        
        while cells != set():
            cell = random.choice(list(cells))
            visited.add(cell)
            row, col = cell
            
            #Checks for all the possible walls that can be moved to
            possibleWalls = [(0,1), (0,-1), (1, 0), (-1, 0)]
            neighbors = []
            for drow, dcol in possibleWalls:
                neighbor = nrow, ncol = row+drow, col+dcol
                if 0 <= nrow < rows and 0 <= ncol < cols and self.bfsGetPath(cell, neighbor) is None:
                    cells.add(neighbor)
                    neighbors.append(neighbor)
            
            #Chooses a random neighbor to go to
            if neighbors != []:
                neighbor = random.choice(neighbors)
                self.addEdge(cell, neighbor)
            visited.add(cell)
            cells.remove(cell)
            
    '''
    DRAWING THE MAZE
    '''   
    def drawCell(self, canvas, row, col, color = 'white'):
        x0, x1, y0, y1 = self.getCellBounds(row, col)
        canvas.create_rectangle(x0, y0, x1, y1, fill = color, outline = '')
    
    def getCellBounds2(self, row, col):
        #Taken from 112 Notes/Lecture (also what do we do about the app.table)
        gridWidth  = self.app.width/4
        gridHeight = self.app.height/4
        cellWidth = gridWidth / len(self.listMaze)
        cellHeight = gridHeight / len(self.listMaze[0])
        x0 = col * cellWidth
        x1 = (col+1) * cellWidth
        y0 = row * cellHeight
        y1 = (row+1) * cellHeight
        return x0, x1, y0, y1

    def convertTo2DList(self):
        #All walls
        maze = [[1]*(self.cols*2-1) for _ in range(self.rows*2-1)]
        
        #Puts all cells into the maze
        for row, col in self.table:
            maze[row*2][col*2] = 0

        #Makes paths between cells
        for cell in self.table:
            row, col = cell
            neighbors = self.getNeighbors(cell)
            for neighbor in neighbors:
                nrow, ncol = neighbor
                drow, dcol = nrow - row, ncol - col
                maze[row*2+drow][col*2+dcol] = 0
        self.listMaze = maze
        return maze

    def drawListMaze(self, canvas):
        numRows = len(self.listMaze)
        numCols = len(self.listMaze[0])
        for row in range(numRows):
            for col in range(numCols):
                color = 'white'
                if self.listMaze[row][col] == 1:
                    color = 'black'
                elif self.listMaze[row][col] == 2:
                    if self.app.getKey:
                        color = 'blue'
                    else:
                        color = 'red'
                elif self.listMaze[row][col] == 3:
                    color = 'orange'
                x0, x1, y0, y1 = self.getCellBounds2(row, col)
                canvas.create_rectangle(x0, y0, x1, y1, fill = color, outline = '')

    def render(self, canvas):
        self.drawListMaze(canvas)
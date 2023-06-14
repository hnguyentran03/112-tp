import random
from cmu_112_graphics import *
from helpers import print2dList


class Vertex:
    vertexTypes = ['wall', 'cell', 'key', 'goal']

    def __init__(self, row, col, t, color):
        self.row = row
        self.col = col
        self.t = t
        self.color = color

    def __repr__(self):
        return f"Vertex({self.row}, {self.col}, {self.t}, {self.color})"

    def getPos(self):
        return (self.row, self.col)

    def getType(self):
        return self.t

    def getColor(self):
        return self.color


class Wall(Vertex):
    def __init__(self, row, col, color):
        super().__init__(row, col, 'wall', color)

    def __repr__(self): return "1"
    # return f"Wall({self.row}, {self.col}, {self.color})"


class Cell(Vertex):
    def __init__(self, row, col, color):
        super().__init__(row, col, 'cell', color)

    def __repr__(self): return "0"
    # return f"Cell({self.row}, {self.col}, {self.color})"

# Idea for graph class (and some funcitons) from Graph Algorithm Mini-Lecture


class Graph:
    def __init__(self, wallColor='white', cellColor='white'):
        self.table = {}  # Adjacency table
        self.cellColor = cellColor
        self.wallColor = wallColor

    def __repr__(self):
        return f'{self.table}'

    # Adds a directed edge between vertexA and vertexB
    def addEdge(self, vertexA, vertexB, weight=1):
        if vertexA not in self.table:
            self.table[vertexA] = {}
        if vertexB not in self.table:
            self.table[vertexB] = {}
        self.table[vertexA][vertexB] = weight
        # self.table[vertexB][vertexA] = weight

    def getVertexs(self):
        return list(self.table)

    def getNeighbors(self, vertex):
        return set(self.table.get(vertex, {}))

    def convertTo2DList(self):
        # All walls
        maze = [[Wall(row, col, self.wallColor) for col in range(
            self.cols*2-1)] for row in range(self.rows*2-1)]

        # Puts all cells into the maze
        for row, col in self.table:
            maze[row*2][col*2] = Cell(row, col, self.cellColor)

        # Makes paths between cells
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
                vertex = self.L[row][col]
                canvas.create_rectangle(col*self.cellSize, row*self.cellSize,
                                        (col+1)*self.cellSize, (row+1) *
                                        self.cellSize,
                                        fill=vertex.getColor(), outline=vertex.getColor())


class Maze(Graph):
    mazeTypes = ['dfs', 'prim', 'kruskal']

    @staticmethod
    def getTypes():
        return Maze.mazeTypes

    def __init__(self, rows, cols, mazeType, cellSize, wallColor='black', goalColors=None, keyColor='orange', cellColor='white'):
        super().__init__(wallColor, cellColor)
        self.goalColors = goalColors if goalColors else ['blue', 'red']
        self.keyColor = keyColor

        self.rows = rows
        self.cols = cols
        self.mazeType = mazeType
        self.cellSize = cellSize

    def generate(self):
        # Generates a maze
        if self.mazeType == 'dfs':
            self.generateIterDFS()
        elif self.mazeType == 'prim':
            self.generatePrim()
        # elif self.mazeType == 'kruskal':
        #     self.generateKruskal()
        self.convertTo2DList()
        # self.addGoals()
        # self.addKey()

    # Taken from https://en.wikipedia.org/wiki/Maze_generation_algorithm
    def generateIterDFS(self):
        visited = set()
        frontier = []  # Stack
        start = (random.randrange(0, self.rows),
                 random.randrange(0, self.cols))

        frontier.append(start)

        # While there are still cells to explore
        while frontier:
            vertex = row, col = frontier.pop()
            visited.add(vertex)

            # Find all unvisited neighbors
            neighbors = []
            for drow, dcol in [(0, 1), (0, -1), (1, 0), (-1, 0)]:  # Right, Left, Down, Up
                neighbor = nrow, ncol = (row + drow, col + dcol)
                if 0 <= nrow < self.rows and 0 <= ncol < self.cols and neighbor not in visited:
                    neighbors.append(neighbor)

            # If there are neighbors, choose one to add to maze
            # Otherwise, do nothing
            if neighbors:
                frontier.append(vertex)
                nextVertex = random.choice(neighbors)
                self.addEdge(vertex, nextVertex)
                self.addEdge(nextVertex, vertex)
                frontier.append(nextVertex)

    # Taken from https://en.wikipedia.org/wiki/Prim%27s_algorithm
    def generatePrim(self):
        visited = set()
        frontier = []
        start = (random.randrange(0, self.rows),
                 random.randrange(0, self.cols))

        frontier.append(start)

        # While there are still walls
        while frontier:
            vertex = row, col = random.choice(frontier)
            frontier.remove(vertex)
            visited.add(vertex)

            # Find all neighboring walls
            neighbors = []
            for drow, dcol in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                neighbor = nrow, ncol = (row + drow, col + dcol)
                if 0 <= nrow < self.rows and 0 <= ncol < self.cols and neighbor not in visited:
                    frontier.append(neighbor)
                    neighbors.append(neighbor)

            # If there are walls, break one of them down
            # Otherwise, do nothing
            if neighbors:
                nextVertex = random.choice(neighbors)
                self.addEdge(vertex, nextVertex)
                self.addEdge(nextVertex, vertex)

    def generateKruskal(self):
        pass

    def checkPos(self, row, col):
        return 0 <= row < self.rows and 0 <= col < self.cols and self.L[row][col] != 'wall'

    def render3D(self, canvas):
        pass

    # TODO make getKey to modify maze
    def renderMinimap(self, canvas):
        # Draws the minimap
        for row in range(len(self.L)):
            for col in range(len(self.L[0])):
                vertex = self.L[row][col]
                canvas.create_rectangle(col*self.cellSize, row*self.cellSize,
                                        (col+1)*self.cellSize, (row+1) *
                                        self.cellSize,
                                        fill=vertex.getColor(), outline=vertex.getColor())


def testMaze(app):
    print('Testing Maze Class...')
    app.m = Maze(5, 5, 'prim', app.height/9)
    app.m.generate()
    print2dList(app.m.L)
    print('Passed!')


def appStarted(app):
    testMaze(app)


def keyPressed(app, event):
    if event.key == "r":
        testMaze(app)


def redrawAll(app, canvas):
    app.m.renderMinimap(canvas)


runApp(width=800, height=800)

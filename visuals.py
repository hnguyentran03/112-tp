from tpTest import *

def generateMaze(app):
    rows = cols = 10
    app.margin = 5
    app.maze = Maze()
    app.maze.dfsMaze(rows, cols)

def drawMaze(app, canvas):
    for row, col in app.maze.table:
        drawCell(app, canvas, row, col)
    pass

def drawCell(app, canvas, row, col):
    x0, x1, y0, y1 = getCellBounds(app, row, col)
    canvas.create_rectangle(x0, y0, x1, y1, fill = 'white')

def getCellBounds(app, row, col):
        
    #Taken from 112 Notes/Lecture
    gridWidth  = app.width - 2*app.margin
    gridHeight = app.height - 2*app.margin
    cellWidth = gridWidth / app.maze.cols
    cellHeight = gridHeight / app.maze.rows
    x0 = app.margin + col * cellWidth
    x1 = app.margin + (col+1) * cellWidth
    y0 = app.margin + row * cellHeight
    y1 = app.margin + (row+1) * cellHeight

    return x0, x1, y0, y1

def appStarted(app):
    generateMaze(app)
    pass

def timerFired(app):
    pass

def redrawAll(app, canvas):
    drawMaze(app, canvas)
    pass

runApp(width=500,height=500)
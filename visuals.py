from graph import *

def appStarted(app):
    generateMaze(app)
    app.cellMargin = 5
    pass

def generateMaze(app):
    rows = cols = 10
    app.margin = 10
    app.maze = Maze()
    app.maze.dfsMaze(rows, cols)


'''
Draw
'''
def getCellBounds(app, row, col):
    #Taken from 112 Notes/Lecture
    gridWidth  = app.width - 2*app.margin
    gridHeight = app.height - 2*app.margin
    cellWidth = gridWidth / app.maze.cols
    cellHeight = gridHeight / app.maze.rows
    x0 = app.margin + col * cellWidth + app.cellMargin
    x1 = app.margin + (col+1) * cellWidth - app.cellMargin
    y0 = app.margin + row * cellHeight + app.cellMargin
    y1 = app.margin + (row+1) * cellHeight - app.cellMargin
    return x0, x1, y0, y1
            
def drawCell(app, canvas, row, col, color = 'white'):
    x0, x1, y0, y1 = getCellBounds(app, row, col)
    canvas.create_rectangle(x0, y0, x1, y1, fill = color, outline = '')

def drawPath(app, canvas):
    path = app.maze.getPath((0, 0), (app.maze.rows - 1, app.maze.cols - 1))
    for row, col in app.maze.table:
        if (row, col) in path:
            color = 'blue'
        else:
            color = 'white'

        drawCell(app, canvas, row, col, color)

def drawEdges(app, canvas):
    for row, col in app.maze.table:
        for neighborRow, neighborCol in app.maze.table[(row, col)]:
            pathRow = (row + neighborRow) / 2
            pathCol = (col + neighborCol) / 2
            drawCell(app, canvas, pathRow, pathCol)

def drawMaze(app, canvas):
    for row, col in app.maze.table:
        drawCell(app, canvas, row, col)


'''
Movement
'''
def mousePressed(app, event):
    pass


'''
Timer
'''
def timerFired(app):
    pass

def redrawAll(app, canvas):
    canvas.create_rectangle(0, 0, app.width, app.height, fill = 'black')
    drawMaze(app, canvas)
    drawEdges(app, canvas)
    drawPath(app, canvas)


runApp(width=500,height=500)
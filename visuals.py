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

def drawCell(app, canvas, row, col, color = 'white'):
    x0, x1, y0, y1 = getCellBounds(app, row, col)
    canvas.create_rectangle(x0, y0, x1, y1, fill = color, outline = '')

def drawPath(app, canvas):
    path = app.maze.getPath((0, 0), (app.maze.rows - 1, app.maze.cols - 1))
    print(path)
    for row, col in app.maze.table:
        if (row, col) in path:
            color = 'blue'
        else:
            color = 'white'

        drawCell(app, canvas, row, col, color)
    

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
    x0 += 5
    y0 += 5
    x1 -= 5
    y1 -= 5
    return x0, x1, y0, y1

def drawEdges(app, canvas):
    for row, col in app.maze.table:
        for neighborRow, neighborCol in app.maze.table[(row, col)]:
            pathRow = (row + neighborRow) / 2
            pathCol = (col + neighborCol) / 2
            drawCell(app, canvas, pathRow, pathCol)
            

def appStarted(app):
    generateMaze(app)
    pass

def timerFired(app):
    pass

def redrawAll(app, canvas):
    canvas.create_rectangle(0, 0, app.width, app.height, fill = 'black')
    drawMaze(app, canvas)
    drawEdges(app, canvas)
    # drawPath(app, canvas)
    pass


runApp(width=500,height=500)
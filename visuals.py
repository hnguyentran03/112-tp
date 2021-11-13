from graph import *
from player import *

def appStarted(app):
    generateMaze(app)
    app.player = Player(app)
    app.path = False
    pass

def generateMaze(app):
    rows = cols = 10
    app.margin = 10
    app.cellMargin = 5
    app.maze = Maze()
    app.maze.dfsMaze(rows, cols)

'''
Draw
'''
# def checkPlayerLocation(app):
#     cx, cy = app.player.location
#     gridWidth  = app.width - 2*app.margin
#     gridHeight = app.height - 2*app.margin
#     cellWidth = gridWidth / app.maze.cols
#     cellHeight = gridHeight / app.maze.rows
#     col = (cx - app.margin - app.cellMargin)/(cellWidth)
#     row = (cy - app.margin - app.cellMargin)/(cellHeight)
#     return int(row), int(col)

# def getCellBounds(app, row, col):
#     #Taken from 112 Notes/Lecture
#     gridWidth  = app.width - 2*app.margin
#     gridHeight = app.height - 2*app.margin
#     cellWidth = gridWidth / app.maze.cols
#     cellHeight = gridHeight / app.maze.rows
#     x0 = app.margin + col * cellWidth + app.cellMargin
#     x1 = app.margin + (col+1) * cellWidth - app.cellMargin
#     y0 = app.margin + row * cellHeight + app.cellMargin
#     y1 = app.margin + (row+1) * cellHeight - app.cellMargin
#     return x0, x1, y0, y1
            
# def drawCell(app, canvas, row, col, color = 'white'):
#     x0, x1, y0, y1 = getCellBounds(app, row, col)
#     canvas.create_rectangle(x0, y0, x1, y1, fill = color, outline = '')

def drawPath(app, canvas):
    path = app.maze.getPath(app.player.checkLocation(app), (app.maze.rows-1, app.maze.cols-1))
    for row, col in path:
        
        x0, x1, y0, y1 = app.maze.getCellBounds(app, row, col)
        cx, cy = (x1 + x0)/2, (y1 + y0)/2

        nrow, ncol = path[(row, col)]
        nx0, nx1, ny0, ny1 = app.maze.getCellBounds(app, nrow, ncol)
        ncx, ncy = (nx1 + nx0)/2, (ny1 + ny0)/2
        canvas.create_line(cx, cy, ncx, ncy, fill = 'blue', width = 5)

# def drawEdges(app, canvas):
#     for row, col in app.maze.table:
#         for neighborRow, neighborCol in app.maze.table[(row, col)]:
#             pathRow = (row + neighborRow) / 2
#             pathCol = (col + neighborCol) / 2
#             drawCell(app, canvas, pathRow, pathCol)

# def drawMaze(app, canvas):
#     for row, col in app.maze.table:
#         drawCell(app, canvas, row, col)


'''
Movement
'''
def keyPressed(app, event):
    if event.key == 'p':
        app.path = not app.path
    elif event.key == 'r':
        generateMaze(app)

    #Moving
    app.player.moveWithKeys(app, event)

# def movePlayer(app, dx, dy):
#     cx, cy = app.player
#     cx += dx
#     cy += dy
#     app.player = (cx, cy)

# def drawPlayer(app, canvas):
#     cx, cy = app.player
#     x0, x1 = cx - 5, cx + 5
#     y0, y1 = cy - 5, cy + 5
#     canvas.create_oval(x0, y0, x1, y1, fill = 'red', outline = 'red')

'''
Timer
'''
def timerFired(app):
    pass

def redrawAll(app, canvas):
    canvas.create_rectangle(0, 0, app.width, app.height, fill = 'black')
    app.maze.render(app, canvas)
    if app.path:
        drawPath(app, canvas)
    app.player.render(app, canvas)


runApp(width=400,height=400)
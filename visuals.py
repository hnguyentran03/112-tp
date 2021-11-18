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
    app.maze = Maze(app)
    app.maze.dfsMaze(rows, cols)
    app.maze.convertTo2DList()


def drawPath(app, canvas):
    path = app.maze.getPath(app.player.checkLocation(), (app.maze.rows-1, app.maze.cols-1))
    for row, col in path:
        
        x0, x1, y0, y1 = app.maze.getCellBounds(row, col)
        cx, cy = (x1 + x0)/2, (y1 + y0)/2

        nrow, ncol = path[(row, col)]
        nx0, nx1, ny0, ny1 = app.maze.getCellBounds(nrow, ncol)
        ncx, ncy = (nx1 + nx0)/2, (ny1 + ny0)/2
        canvas.create_line(cx, cy, ncx, ncy, fill = 'blue', width = 5)

'''
Movement
'''
def keyPressed(app, event):
    if event.key == 'p':
        app.path = not app.path
    elif event.key == 'r':
        generateMaze(app)

    #Moving
    app.player.moveWithKeys(event)

'''
Timer
'''
def timerFired(app):
    pass

def redrawAll(app, canvas):
    canvas.create_rectangle(0, 0, app.width, app.height, fill = 'black')
    app.maze.render(canvas)
    if app.path:
        drawPath(app, canvas)
    app.player.render(canvas)


runApp(width=500,height=500)
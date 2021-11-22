from graph import *
from player import *
from ray import *

def appStarted(app):
    generateMaze(app)
    cellDimension(app)
    app.player = Player(app)
    app.path = False
    app.state = False
    app.numRays = int(len(app.maze)*10)
    createRays(app)

def cellDimension(app):
    gridWidth  = 500
    gridHeight = 500
    app.cellWidth = gridWidth / len(app.maze[0])
    app.cellHeight = gridHeight / len(app.maze)


'''
Generation
'''
def generateMaze(app):
    rows = cols = 5
    app.margin = 0
    app.cellMargin = 0
    app.mazeGen = Maze(app)
    app.mazeGen.dfsMaze(rows, cols)
    app.maze = app.mazeGen.convertTo2DList()

def createRays(app):
    app.rays = []
    for difference in range(app.numRays):
        angleDifference = math.pi/(2**9)*difference
        
        leftAngle = app.player.angle-angleDifference
        rightAngle = app.player.angle+angleDifference
        if leftAngle < 0: leftAngle += 2*math.pi
        elif leftAngle > 2*math.pi: leftAngle -= 2*math.pi
        if rightAngle < 0: rightAngle += 2*math.pi
        elif rightAngle > 2*math.pi: rightAngle -= 2*math.pi

        leftRay = Ray(app, leftAngle)
        rightRay = Ray(app, rightAngle)
        app.rays.insert(0, leftRay)
        app.rays.append(rightRay)

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

    createRays(app)

    if event.key == 'l':
        app.state = not app.state

'''
Timer
'''
def timerFired(app):
    pass

'''
Drawing
'''
def draw3D(app, canvas):
    wallHeight = 200
    constant = 255
    midpoint = app.height/2
    dx = app.width / app.numRays
    for i, ray in enumerate(app.rays):
        distanceToWall = ray.getDistance()
        try:
            color = f'#00{hex(int(255*(app.cellHeight/distanceToWall)))[-2:]}00'
            height = wallHeight/(distanceToWall)*constant
        except ZeroDivisionError:
            color = f'#00{hex(int(255*(app.cellHeight/(distanceToWall+1))))[-2:]}00'
            height = wallHeight/(distanceToWall+1)*constant
        y0 = midpoint - height/2
        y1 = midpoint + height/2
        x0 = dx * i
        x1 = dx * (i + 1)
        canvas.create_rectangle(x0, y0, x1, y1, fill = color, outline = '')

def drawPath(app, canvas):
    path = app.mazeGen.getPath(app.player.checkLocation(), (app.mazeGen.rows-1, app.mazeGen.cols-1))
    for row, col in path:
        
        x0, x1, y0, y1 = app.mazeGen.getCellBounds2(row, col)
        cx, cy = (x1 + x0)/2, (y1 + y0)/2

        nrow, ncol = path[(row, col)]
        nx0, nx1, ny0, ny1 = app.mazeGen.getCellBounds2(nrow, ncol)
        ncx, ncy = (nx1 + nx0)/2, (ny1 + ny0)/2
        canvas.create_line(cx, cy, ncx, ncy, fill = 'blue', width = 5)

def redrawAll(app, canvas):
    if app.path:
        drawPath(app, canvas)
    if app.state:
        draw3D(app, canvas)

    else:
        app.mazeGen.render(canvas)
        app.player.render(canvas)
        for ray in app.rays:
            ray.render(canvas)

runApp(width=500,height=500)







from graph import *
from player import *
from ray import *

def appStarted(app):
    generateMaze(app)
    cellDimension(app)
    app.player = Player(app)
    app.path = False
    app.state = False
    app.numRays = 100
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
    rows = cols = 10
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
        
        #Adds the ray to the far left
        app.rays.insert(0, leftRay)

        #Adds a ray to the far right
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
    constant = 1/app.mazeGen.rows * 500
    midpoint = app.height/2
    dx = app.width / (2*app.numRays)
    
    for i, ray in enumerate(app.rays):
        distanceToWall = ray.getDistance()

        wallAngle = app.player.angle - ray.angle

        if wallAngle < 0: wallAngle += 2*math.pi
        elif wallAngle > 2*math.pi: wallAngle -= 2*math.pi
        
        distanceToWall *= math.cos(wallAngle)

        height = wallHeight/(distanceToWall)*constant
        colorDec =int(16+239*(height/app.height))
        
        if colorDec > 255:
            colorDec = 255
        
        color = f'#00{hex(colorDec)[-2:]}00'

        y0 = midpoint - height/2
        y1 = midpoint + height/2
        x0 = dx * i
        x1 = dx * (i + 1)

        canvas.create_rectangle(x0, y0, x1, y1, fill = color, outline = '')


def drawPath(app, canvas, endRow, endCol):
    px, py = app.player.location
    prow, pcol = app.player.checkLocation(px, py)
    
    if prow % 2 == 1: prow -= 1
    if pcol %2 == 1: pcol -= 1

    path = app.mazeGen.getPath((), (endRow, endCol))
    for row, col in path:
        x0, x1, y0, y1 = app.mazeGen.getCellBounds2(row*2, col*2)
        cx, cy = (x1 + x0)/2, (y1 + y0)/2

        nrow, ncol = path[(row, col)]
        nx0, nx1, ny0, ny1 = app.mazeGen.getCellBounds2(nrow*2, ncol*2)
        ncx, ncy = (nx1 + nx0)/2, (ny1 + ny0)/2
        canvas.create_line(cx, cy, ncx, ncy, fill = 'blue', width = 5)



def redrawAll(app, canvas):
    canvas.create_rectangle(0, 0, app.width, app.height, fill = 'black')
    if app.state:
        draw3D(app, canvas)

    else:
        app.mazeGen.render(canvas)
        app.player.render(canvas)
        for ray in app.rays:
            ray.render(canvas)
        if app.path:
            drawPath(app, canvas, 5, 5)

runApp(width=500,height=500)







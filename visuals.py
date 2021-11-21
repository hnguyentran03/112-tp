from graph import *
from player import *
from ray import *

def appStarted(app):
    generateMaze(app)
    app.player = Player(app)
    app.path = False
    app.state = False
    cellDimension(app)
    app.numRays = int(len(app.maze)*10)
    createRays(app)

def cellDimension(app):
    gridWidth  = 500
    gridHeight = 500
    app.cellWidth = gridWidth / len(app.maze[0])
    app.cellHeight = gridHeight / len(app.maze)

# def appStarted(app):
#     app.playerAngle = 1/2*math.pi
#     app.mazeGen = Maze(app)
#     app.mazeGen.dfsMaze(5,5)
#     # app.maze =[[1, 0, 1, 1, 1, 1, 0, 1, 1, 1],
#     #            [0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
#     #            [1, 0, 1, 0, 1, 1, 1, 1, 0, 0],
#     #            [1, 0, 0, 0, 0, 1, 0, 0, 0, 1],
#     #            [1, 0, 1, 1, 0, 1, 0, 1, 1, 1],
#     #            [1, 0, 1, 1, 1, 1, 0, 1, 1, 1],
#     #            [0, 0, 0, 0, 1, 0, 0, 0, 1, 1],
#     #            [1, 0, 1, 0, 1, 1, 0, 0, 0, 0],
#     #            [1, 0, 1, 0, 0, 0, 0, 0, 0, 1],
#     #            [1, 0, 1, 1, 0, 1, 0, 1, 1, 1]]

#     app.maze = app.mazeGen.convertTo2DList()


#     app.state = False
#     app.step = len(app.maze)/2
#     if app.step > 0:
#         app.turn = int(app.step)-1
#     else:
#         app.turn = int(app.step)
#     app.playerMove = (app.step*math.cos(app.playerAngle), app.step*math.sin(app.playerAngle))

def generateMaze(app):
    rows = cols = 10
    app.margin = 10
    app.cellMargin = 5
    app.mazeGen = Maze(app)
    app.mazeGen.dfsMaze(rows, cols)
    app.maze = app.mazeGen.convertTo2DList()


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

    createRays(app)

    if event.key == 'l':
        app.state = not app.state

'''
Timer
'''
def timerFired(app):
    pass

# def redrawAll(app, canvas):
#     canvas.create_rectangle(0, 0, app.width, app.height, fill = 'black')
#     app.maze.render(canvas)
#     if app.path:
#         drawPath(app, canvas)
#     app.player.render(canvas)

def redrawAll(app, canvas):
    if app.state:
        draw3D(app, canvas)
    else:
        app.maze.render(canvas)
        app.player.render(canvas)
        for ray in app.rays:
            ray.render(canvas)

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



# def movePlayer(app, direction, directionName):
#     cx, cy = app.player
#     dx, dy = app.playerMove
#     if directionName == 'Up' or directionName == 'Down':
#         cx += dx * direction
#         cy += dy * direction
#     elif directionName == 'Left' or directionName == 'Right':
#         cx += dy * direction
#         cy += dx * direction
    
#     app.player = (cx, cy)

# def keyPressed(app, event):
#     if event.key == 'w':
#         movePlayer(app, 1, 'Up')
#     elif event.key == 's':
#         movePlayer(app, -1, 'Down')
#     elif event.key == 'a':
#         movePlayer(app, -1, 'Left')
#     elif event.key == 'd':
#         movePlayer(app, 1, 'Right')
#     if event.key == 'Left':
#         app.playerAngle -= math.pi/(3*(2**app.turn))
#         if app.playerAngle < 0:
#             app.playerAngle += 2*math.pi
#         dx, dy = app.playerMove
#         dx = math.cos(app.playerAngle)
#         dy = math.sin(app.playerAngle)
#         app.playerMove = (app.step*dx, app.step*dy)
   
#     elif event.key == 'Right':
#         app.playerAngle += math.pi/ (3*(2**app.turn))
#         if app.playerAngle > 2*math.pi:
#             app.playerAngle -= 2*math.pi
#         dx, dy = app.playerMove
#         dx = math.cos(app.playerAngle)
#         dy = math.sin(app.playerAngle)
#         app.playerMove = (app.step*dx, app.step*dy)
    


#USEFUL
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

runApp(width=500,height=500)







runApp(width=500,height=500)
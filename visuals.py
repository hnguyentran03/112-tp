from graph import *
from player import *
from ray import *
from sprite import *
import random

def appStarted(app):
    app.splash = True
    generateMaze(app)
    app.path = False
    app.state = False
    app.numRays = 100
    createRays(app)

def cellDimension(app):
    gridWidth  = app.width
    gridHeight = app.height
    app.cellWidth = gridWidth / len(app.maze[0])
    app.cellHeight = gridHeight / len(app.maze)

def normalize(row, col):
    if row % 2 == 1: row -= 1
    if col %2 == 1: col -= 1

    return row//2, col//2


'''
Generation
'''
def generateMaze(app):
    rows = cols = 10
    app.clearMaze = False
    app.getKey = False
    app.margin = 0
    app.cellMargin = 0
    app.mazeGen = Maze(app)
    app.mazeGen.dfsMaze(rows, cols)
    app.maze = app.mazeGen.convertTo2DList()
    cellDimension(app)
    app.player = Player(app)

    app.enemies = []
    makeEnemy(app)

    mazeExit(app)

def makeEnemy(app):
    row, col = random.randrange(1,len(app.maze)), random.randrange(1, len(app.maze[0]))
    x0, x1, y0, y1 = app.mazeGen.getCellBounds2(row, col)
    enemy = Enemy(app, ((x0+x1)/2, (y0+y1)/2))
    
    while app.maze[row][col] == 1:
        row, col = random.randrange(1,len(app.maze)), random.randrange(1, len(app.maze[0]))
        x0, x1, y0, y1 = app.mazeGen.getCellBounds2(row, col)
        enemy = Enemy(app, ((x0+x1)/2, (y0+y1)/2))

    app.enemies.append(enemy)

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

def mazeExit(app):
    endRow, endCol = len(app.maze)-1, len(app.maze[0])-1
    app.endLocation = endRow, endCol
    keyRow, keyCol = random.randrange(app.mazeGen.rows), random.randrange(app.mazeGen.cols)
    keyRow, keyCol = keyRow*2, keyCol*2
    
    while app.maze[keyRow][keyRow] == 1:
        keyRow, keyCol = random.randrange(app.mazeGen.rows), random.randrange(app.mazeGen.cols)
        keyRow, keyCol = keyRow*2, keyCol*2
    app.keyLocation = keyRow, keyCol
    
    app.maze[keyRow][keyCol] = 3
    app.maze[endRow][endCol] = 2

def startButtonBounds(app):
    x0 = app.width * 2/5
    x1 = app.width * 3/5
    y0 = app.height * 3/5
    y1 = app.height * 4/5
    return x0, x1, y0, y1

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

def mousePressed(app, event):
    x0, x1, y0, y1 = startButtonBounds(app)
    if x0 < event.x < x1 and y0 < event.y < y1:
        app.splash = False

'''
Timer
'''
def timerFired(app):
    px, py = app.player.location
    playerLocation = app.player.checkLocation(px, py)
    
    if playerLocation == app.keyLocation:
        app.getKey = True
        keyRow, keyCol = app.keyLocation
        app.maze[keyRow][keyCol] = 0
    
    if playerLocation == app.endLocation and app.getKey:
        app.clearMaze = True
    
    for enemy in app.enemies:
        enemy.getPath()

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

        #Take out fisheye
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
    prow, pcol = normalize(prow, pcol)

    path = app.mazeGen.getPath((prow, pcol), (endRow, endCol))
    for row, col in path:
        x0, x1, y0, y1 = app.mazeGen.getCellBounds2(row*2, col*2)
        cx, cy = (x1 + x0)/2, (y1 + y0)/2

        #Next cell
        nrow, ncol = path[(row, col)]
        nx0, nx1, ny0, ny1 = app.mazeGen.getCellBounds2(nrow*2, ncol*2)
        ncx, ncy = (nx1 + nx0)/2, (ny1 + ny0)/2

        canvas.create_line(cx, cy, ncx, ncy, fill = 'blue', width = 5)

def drawMazeClear(app, canvas):
    height = app.height/4
    canvas.create_rectangle(0, app.height/2-height, app.width, app.height/2+height, fill = 'black')
    canvas.create_text(app.height/2, app.width/2, text = 'Maze Clear', font = f'Arial {app.height//10} bold', fill = 'white')

def drawSplashScreen(app, canvas):
    x0, x1, y0, y1 = startButtonBounds(app)
    canvas.create_rectangle(0, 0, app.width, app.height, fill = 'white')
    canvas.create_text(app.width/2, app.height * 2/5, text = '112maze', font = f'Arial {app.height//10}', fill = 'black')
    canvas.create_rectangle(x0, y0, x1, y1, fill = 'blue')
    canvas.create_text((x0+x1)/2, (y0+y1)/2, text = 'Start', font = f'Arial {app.height//20}', fill = 'white')

def redrawAll(app, canvas):
    if app.splash:
        drawSplashScreen(app, canvas)
    else:
        canvas.create_rectangle(0, 0, app.width, app.height, fill = 'white')
        if app.clearMaze:
                drawMazeClear(app, canvas)
        else:
            
            if app.state:
                draw3D(app, canvas)
            else:
                app.mazeGen.render(canvas)
                for ray in app.rays:
                    ray.render(canvas)
                
                for enemy in app.enemies:
                    enemy.render(canvas)

                if app.path:
                    if app.getKey:
                        drawPath(app, canvas, app.mazeGen.rows-1, app.mazeGen.cols-1)
                    else:
                        keyRow, keyCol = app.keyLocation
                        keyRow, keyCol = normalize(keyRow, keyCol)
                        drawPath(app, canvas, keyRow, keyCol)
                app.player.render(canvas)

runApp(width=500,height=500)
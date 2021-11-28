from graph import *
from player import *
from ray import *
from sprite import *
import random

def appStarted(app):
    app.splash = True
    app.level = 1
    app.rows = app.cols = 5
    generateMaze(app)
    app.path = False
    app.state = False
    app.numRays = 100
    app.timerDelay = 10
    createRays(app)

def cellDimension(app):
    gridWidth  = app.width/4
    gridHeight = app.height/4
    app.cellWidth = gridWidth / len(app.maze[0])
    app.cellHeight = gridHeight / len(app.maze)

def startButtonBounds(app):
    x0 = app.width * 2/5
    x1 = app.width * 3/5
    y0 = app.height * 3/5
    y1 = app.height * 4/5
    return x0, x1, y0, y1

def normalize(row, col):
    if row % 2 == 1: row -= 1
    if col %2 == 1: col -= 1

    return row//2, col//2


'''
Generation
'''
def generateMaze(app):
    app.enemyRays = {}

    app.timePassed = 0
    app.enemyMove = 500

    app.gameOver = False
    app.clearMaze = False
    app.getKey = False
    
    app.margin = 0
    app.cellMargin = 0
    
    app.mazeGen = Maze(app)
    app.mazeGen.dfsMaze(app.rows, app.cols)
    app.maze = app.mazeGen.convertTo2DList()
    cellDimension(app)
    
    app.player = Player(app)

    app.enemies = []
    for _ in range(app.level):
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
    #Creates the end goal
    endRow, endCol = len(app.maze)-1, len(app.maze[0])-1
    app.endLocation = endRow, endCol
    
    #Creates the key
    keyRow, keyCol = random.randrange(1, app.mazeGen.rows), random.randrange(1, app.mazeGen.cols)
    keyRow, keyCol = keyRow*2, keyCol*2
    
    while app.maze[keyRow][keyRow] == 1:
        keyRow, keyCol = random.randrange(1, app.mazeGen.rows), random.randrange(1, app.mazeGen.cols)
        keyRow, keyCol = keyRow*2, keyCol*2
    app.keyLocation = keyRow, keyCol
    
    app.maze[keyRow][keyCol] = 3
    app.maze[endRow][endCol] = 2

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
    checkEnemies(app)

    for enemy in app.enemies:
        enemy.getPath()

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
    if not app.splash:
        px, py = app.player.location
        playerLocation = app.player.checkLocation(px, py)
        
        #Key collection
        if playerLocation == app.keyLocation and not app.getKey:
            app.getKey = True
            keyRow, keyCol = app.keyLocation
            app.maze[keyRow][keyCol] = 0
            makeEnemy(app)
        
        #Goal check
        if playerLocation == app.endLocation and app.getKey:
            app.splash = True
            app.clearMaze = True
            app.rows += 1
            app.cols += 1
            app.level += 1
            generateMaze(app)
        
        checkEnemyCollision(app)

        #Enemy movement
        app.timePassed += app.timerDelay
        if app.timePassed > app.enemyMove:
            for enemy in app.enemies:
                enemy.getPath()
                enemy.move()
                
            checkEnemies(app)
        
            app.timePassed = 0

#Adds enemies and the ray that hits the enemy
def checkEnemies(app):
    app.enemyRays = {}
    for j, enemy in enumerate(app.enemies):
        for i, ray in enumerate(app.rays):
            if ray.hitEnemy(enemy):
                rays = app.enemyRays.get((j, enemy), set())
                rays.add((i, ray))
                app.enemyRays[(j, enemy)] = rays

def checkEnemyCollision(app):
    for i, enemy in enumerate(app.enemies):
        cx, cy = enemy.location
        px, py = app.player.location
        
        #If the player is within the same row and col
        if app.player.checkLocation(px, py) == enemy.checkLocation(cx, cy):
            app.gameOver = True

        px, py = app.player.location
        prow, pcol = app.player.checkLocation(px, py)
        prow, pcol = normalize(prow, pcol)
        playerPath = app.mazeGen.getPath((prow, pcol), (app.mazeGen.rows-1, app.mazeGen.cols-1))
        enemy.getPath()
        
        #Subset check taken from https://stackoverflow.com/questions/49904181/python-checking-for-subdictionary/49904235
        if set(enemy.path.items()).issubset(set(playerPath.items())):
            app.enemies.pop(i)

'''
Drawing
'''
def drawEnemies(app, canvas):
    constant = 1000
    midpoint = app.height/2
    dx = app.width / (2*app.numRays)

    for key, val in app.enemyRays.items():
        j, enemy = key
        rays = val
       
        #Coordinates for enemy
        x, y = enemy.location
        cx, cy = app.player.location
        distance = ((cx-x)**2 + (cy-y)**2)**(1/2)
        height = constant/(distance+0.01)
        y0 = midpoint - height/2
        y1 = midpoint + height/2
        
        #Takes the middle ray to draw
        avgI = 0
        for i, ray in rays:
            avgI += i
        
        avgI //= len(rays)
        
        x0 = dx * avgI
        x1 = dx * (avgI + 1)
        canvas.create_line(x0, y0, x1, y1, fill = 'purple', width = height*len(app.enemyRays))


#Drawing walls from https://permadi.com/1996/05/ray-casting-tutorial-9/
def draw3D(app, canvas):
    wallHeight = 200
    constant = 1/app.mazeGen.rows * 200
    midpoint = app.height/2
    dx = app.width / (2*app.numRays)
    
    for i, ray in enumerate(app.rays):
        distanceToWall = ray.getDistance()

        #Take out fisheye taken from https://www.youtube.com/watch?v=gYRrGTC7GtA
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
        nrow, ncol = path.get((row, col))
        nx0, nx1, ny0, ny1 = app.mazeGen.getCellBounds2(nrow*2, ncol*2)
        ncx, ncy = (nx1 + nx0)/2, (ny1 + ny0)/2

        canvas.create_line(cx, cy, ncx, ncy, fill = 'blue', width = 5)

def drawMazeClear(app, canvas):
    height = app.height/4
    canvas.create_rectangle(0, app.height/2-height, app.width, app.height/2+height, fill = 'black')
    canvas.create_text(app.height/2, app.width/2, text = 'Maze Clear', font = f'Arial {app.height//10} bold', fill = 'white')

def drawGameOver(app, canvas):
    height = app.height/4
    canvas.create_rectangle(0, app.height/2-height, app.width, app.height/2+height, fill = 'black')
    canvas.create_text(app.height/2, app.width/2, text = 'Game Over', font = f'Arial {app.height//10} bold', fill = 'white')

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
        elif app.gameOver:
            drawGameOver(app, canvas)
        else: 
            draw3D(app, canvas)
            drawEnemies(app, canvas)
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
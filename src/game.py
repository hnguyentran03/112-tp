import math, random
from cmu_112_graphics import *
# TODO from player import Player
# TODO from maze import Maze
# TODO from ray import Ray


def setupRays(app):
    app.fov = math.pi/2 #90 degrees
    app.numRays = 100

def game_appStarted(app):
    setupRays(app)

    app.showMinimap = False
    # app.showPath = False
   
    app.timerDelay = 10

    # app.player = Player()


def restartGame(app):


    app.level = 1
    app.rows = app.cols = 5

    # TODO generateMaze(app)
    # TODO createRays(app)

def generateMaze(app):
    app.paused = False
    app.gameOver = False

    # app.timePassed = 0
    # app.enemyMoveTime = 500 

    mazeType = random.choice(Maze.getTypes())
    app.maze = Maze(app.rows, app.cols, mazeType)

def game_keyPressed(app, event):
    if event.key == 'r':
        restartGame(app)  
    if app.gameOver:
        return
    
    if event.key == 'p':
        app.paused = not app.paused
    if app.paused:
        return
    
    app.player.keyPressed(event)
    # TODO createRays(app)

def game_mouseMoved(app, event):
    app.player.mouseMoved(event)
    # TODO createRays(app)

def game_redrawAll(app, canvas):
    app.maze.render3D(app, canvas)

    if app.showMinimap:
        app.maze.renderMinimap(canvas)



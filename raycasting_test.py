#FROM https://www.youtube.com/watch?v=gYRrGTC7GtA
#raycasting test
from cmu_112_graphics import *
import math


def appStarted(app):
    app.margin = 5
    app.player = (150, 150)
    app.playerAngle = 0
    app.playerMove = (10*math.cos(app.playerAngle), 10*math.sin(app.playerAngle))
    app.maze =[[1, 1, 1, 1, 1],
               [1, 0, 0, 0, 1],
               [1, 0, 1, 0, 1],
               [1, 0, 0, 0, 1],
               [1, 1, 1, 1, 1]]

def drawMaze(app, canvas):
    for row in range(len(app.maze)):
        for col in range(len(app.maze[0])):
            color = 'black'
            if app.maze[row][col] == 1:
                color = 'white'
            drawCell(app, canvas, row, col, color)


def drawCell(app, canvas, row, col, color = 'white'):
    x0, x1, y0, y1 = getCellBounds(app, row, col)
    canvas.create_rectangle(x0, y0, x1, y1, fill = color, outline = 'grey', width = 3)

def getCellBounds(app, row, col):
    #Taken from 112 Notes/Lecture (also what do we do about the app.table)
    gridWidth  = app.width - 2*app.margin
    gridHeight = app.height - 2*app.margin
    cellWidth = gridWidth / len(app.maze[0])
    cellHeight = gridHeight / len(app.maze)
    x0 = app.margin + col * cellWidth
    x1 = app.margin + (col+1) * cellWidth
    y0 = app.margin + row * cellHeight
    y1 = app.margin + (row+1) * cellHeight
    return x0, x1, y0, y1

def drawPlayer(app, canvas):
    cx, cy = app.player
    dx, dy = app.playerMove
    r = 5
    canvas.create_oval(cx-r, cy-r, cx+r, cy+r, fill = 'yellow')
    canvas.create_line(cx, cy, cx+2*dx, cy+2*dy, fill = 'yellow', width = 3)

def redrawAll(app, canvas):
    drawMaze(app, canvas)
    drawPlayer(app, canvas)

def movePlayer(app):
    cx, cy = app.player
    dx, dy = app.playerMove
    cx += dx
    cy += dy
    app.player = (cx, cy)

def keyPressed(app, event):
    if event.key == 'Up' or event.key == 'Down':
        movePlayer(app)
    
    if event.key == 'Left':
        app.playerAngle -= 0.2
        if app.playerAngle < 0:
            app.playerAngle += 2*math.pi
        dx, dy = app.playerMove
        dx = math.cos(app.playerAngle)
        dy = math.sin(app.playerAngle)
        app.playerMove = (10*dx, 10*dy)
   
    elif event.key == 'Right':
        app.playerAngle += 0.2
        if app.playerAngle < 2*math.pi:
            app.playerAngle -= 2*math.pi
        dx, dy = app.playerMove
        dx = math.cos(app.playerAngle)
        dy = math.sin(app.playerAngle)
        app.playerMove = (10*dx, 10*dy)

        




runApp(width=500,height=500)
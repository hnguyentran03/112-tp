from cmu_112_graphics import *
from splash import *


def appStarted(app):
    app.colorIndex = 0
    app.bgColors = ['white']
    app.textColors = ['black']

    # Button Colors
    app.buttonColors = ['white']
    app.buttonOutline = ['black']
    app.buttonHover = ['grey']

    app.mode = 'splash'
    splash_appStarted(app)


# def redrawAll(app, canvas):
#     canvas.create_rectangle(0, 0, 100, 100, fill='black')


if __name__ == '__main__':
    runApp(width=800, height=800)

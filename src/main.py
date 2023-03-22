from cmu_112_graphics import *
from splash import splash_appStarted

def appStarted(app):
    app.mode = 'splash'
    splash_appStarted(app)


if __name__ == '__main__':
    runApp(width=600, height=600)
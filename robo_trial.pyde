from Robo import RoboClass
from Walls import WallClass
import math

w = 10

def setup():
    global roborobo
    size(840,840)
    background(255)
    roborobo = RoboClass(50)
    roborobo.placeObjs()
    global grid
    grid = WallClass(roborobo.grid)# roborobo.grid # WallClass(roborobo.grid)
    roborobo.grid = grid
    # roborobo.setWalls(grid)
    makeWalls()
    # frameRate(10)
    # noLoop()

def draw():
    # background(255)
    # x, y = 0, 0
    # for row in grid:
    #     for col in row:
    #         if col == 'O':
    #             fill(255, 0, 0)
    #         elif col == 'D':
    #             fill(0, 0, 0)
    #         else:
    #             fill(255, 255, 255)
    #         rect(x, y, w, w)
    #         x = x + w
    #     y = y + w
    #     x = 0
    # background(255, 255, 255)
    makeWalls()
    roborobo.update()

def mousePressed():
    roborobo.showCircle()

def keyPressed():
  if key == CODED:
    if keyCode == UP:
        roborobo.showSteps()
#     redraw()
    
def makeWalls():
    x, y = 0, 0
    stroke(0)
    for row in grid:
        for col in row:
            if col == 'W':
                fill(255, 100, 20)
                rect(x*w, y*w, w, w)
            elif col == 'D':
                fill(0, 0, 0)
                rect(x*w, y*w, w, w)
            elif col == 'O':
                fill(255, 0, 0)
                rect(x*w, y*w, w, w)
            x += 1 
        y += 1
        x = 0
    

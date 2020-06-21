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
    # creates walls in the matrix
    grid = WallClass(roborobo.grid)
    roborobo.grid = grid
    makeWalls()
    # frameRate(10)

def draw():
    makeWalls()
    roborobo.update()

"""
method is used to draw sensing circle around bots
"""
def mousePressed():
    roborobo.showCircle()

"""
method is used to print steps taken by bots
"""
def keyPressed():
  if key == CODED:
    if keyCode == UP:
        roborobo.showSteps()

"""
method is called continuously and draws all the stationary objects
including the goal, origin (if exists) and walls
"""
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
    

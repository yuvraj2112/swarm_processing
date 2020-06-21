from robot_class import robot
import math
w = 10
matrixDim = 84
objPlaceX = 20
objPlaceY = 10

class RoboClass:
    """
    class constructor is used to initialize bots at the location specified by 'x, y'
    """
    def __init__(self, n):
        self.steps = 0
        self.found = False
        self.circ = False
        self.skip = False
        self.grid=[['.']*matrixDim for x in range(matrixDim)]
        self.robos = []
        roboMatrixLen = int(round(math.sqrt(n)))
        x, y = 1, 1
        id = 1
        for vert in range(x, roboMatrixLen + x):
            for hori in range(y, roboMatrixLen + y):
                robo = robot(id, hori, vert)
                id += 1
                self.robos.append(robo)
                self.grid[vert][hori] = 'x'
        extras = n - (roboMatrixLen * roboMatrixLen) + 1 if self.skip else n - (roboMatrixLen * roboMatrixLen)
        for extra in range(extras):
            robo = robot(id, extra + y, roboMatrixLen + x)
            id += 1
            self.robos.append(robo)
            self.grid[roboMatrixLen + x][extra + y] = 'x'
            
    def setWalls(self, grid):
        self.grid = grid
    
    def placeObjs(self):
        self.grid[matrixDim - objPlaceX][matrixDim - objPlaceY] = 'D'
        
    def showCircle(self):
        for robot in self.robos:
            robot.drawCirc()
        self.circ = not self.circ
        
    def showSteps(self):
        print (self.steps)
        
    def update(self):
        if not self.found:
            self.steps += 1
        else:
            print (self.steps)
        for robot in self.robos:
            status = robot.STATUS
            if status == 'WAIT':
                self.grid = robot.process(self.grid)
            else:
                if status == 'BROADCAST':
                    self.found = True
                robot.update()

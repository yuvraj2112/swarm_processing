from robot_class import robot
import math
w = 10
matrixDim = 84
objPlace = 20

class RoboClass:
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
                # if row == 1 and col == 1:
                #     self.skip = True
                #     continue
                print (vert, hori)
                robo = robot(id, hori, vert)
                id += 1
                self.robos.append(robo)
                self.grid[vert][hori] = 'x'
        extras = n - (roboMatrixLen * roboMatrixLen) + 1 if self.skip else n - (roboMatrixLen * roboMatrixLen)
        for extra in range(extras):
            robo = robot(id, roboMatrixLen + x, extra + y)
            id += 1
            self.robos.append(robo)
            self.grid[extra + y][roboMatrixLen + x] = 'x'
            
    def setWalls(self, grid):
        self.grid = grid
    
    def placeObjs(self):
        # self.grid[1][1] = 'O'
        self.grid[matrixDim - objPlace][matrixDim - objPlace] = 'D'
        
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

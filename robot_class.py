import random
import copy
w = 10
rw = w / 2
matrixDim = 84
directions = ['n', 'ne', 'e', 'se', 's', 'sw', 'w', 'nw']
oppDirection = {'n': 's', 'ne': 'sw', 'e': 'w', 'se': 'nw', 's': 'n', 'sw': 'ne', 'w': 'e', 'nw': 'se'}

class robot:
    def __init__(self, id, x, y):
        self.ID = id
        self.x = x
        self.y = y
        self.nextX = 0
        self.nextY = 0
        self.prevX = x
        self.prevY = y
        self.dir = directions[5]
        self.randomMove = True
        self.waitingSince = 0
        self.STATUS = 'WAIT'
        fill(5, 130, 200)
        rect(self.y * w + rw, self.x * w + rw, rw, rw)
        
    def update(self):
        if self.STATUS == 'MOVE':
            fill(255)
            stroke(255)
            rect(self.y * w + rw, self.x * w + rw, rw, rw)
            self.x = self.nextX
            self.y = self.nextY
            self.nextX = 0
            self.nextY = 0
            stroke(0)
            fill(5, 130, 200)
            rect(self.y * w + rw, self.x * w + rw, rw, rw)
            self.STATUS = 'WAIT'
        else:
            stroke(0)
            fill(255,0,0)
            rect(self.y * w + rw, self.x * w + rw, rw, rw)
        
    def process(self, grid):
        matrix = copy.deepcopy(grid)
        # look for object
        nextMove = self.__lookAround(matrix, self.STATUS == 'BROADCAST')
        if nextMove == None:
            if self.waitingSince > 100 and self.randomMove == True:
                nextMove = None
                if random.randrange(1, 100) < 11:
                    self.dir = oppDirection[self.dir]
                    nextMove = self.__lookAround(matrix, lost = True)
                self.waitingSince = 0
                if nextMove == None:
                    return matrix
                self.waitingSince = 0
                self.dir = nextMove[0]
                self.nextX = nextMove[1][0]
                self.nextY = nextMove[1][1]
                self.prevX = self.x
                self.prevY = self.y
                self.STATUS = 'MOVE'
                matrix[nextMove[1][0]][nextMove[1][1]] = 'x'
                matrix[self.x][self.y] = '.'
                return matrix
            else:
                self.waitingSince += 1
                return matrix
        if nextMove[0] == 'Broadcast':
            self.STATUS = 'BROADCAST'
            self.dir = nextMove[1]
            matrix[self.x][self.y] = 'D'
            return matrix
        self.nextX = nextMove[1][0]
        self.nextY = nextMove[1][1]
        self.prevX = self.x
        self.prevY = self.y
        self.dir = nextMove[0]
        self.STATUS = 'MOVE'
        matrix[nextMove[1][0]][nextMove[1][1]] = 'x'
        matrix[self.x][self.y] = '.'
        return matrix

    def display(self):
        fill(0,255,205)
        rect(self.x * w + rw, self.y * w + rw, rw, rw)
        
    def __lookAround(self, grid, lost = False):
        weights = {
        "n": 0,
        "e": 0,
        "s": 0,
        "w": 0,
        "ne": 0,
        "nw": 0,
        "se": 0,
        "sw": 0,
        }
        neighbours = {
        "se": self.searchNeigh(grid, self.x, self.y, 'se'),
        "ne": self.searchNeigh(grid, self.x, self.y, 'ne'),
        "nw": self.searchNeigh(grid, self.x, self.y, 'nw'),
        "sw": self.searchNeigh(grid, self.x, self.y, 'sw'),
        "n": self.searchNeigh(grid, self.x, self.y, 'n'),
        "s": self.searchNeigh(grid, self.x, self.y, 's'),
        "w": self.searchNeigh(grid, self.x, self.y, 'w'),
        "e": self.searchNeigh(grid, self.x, self.y, 'e'),
        }
        return self.nextMove(grid, neighbours, weights, lost)

    def nextMove(self, grid, neigh, weights, forced):
        # print (neigh)
        for dir in directions:
            if (len(neigh[dir]) and neigh[dir][0][2] == 'D'):
                return ('Broadcast', dir)
            # if len(neigh[dir]) and neigh[dir][0][2] == 'W':
            #     print (neigh[dir])
                # weights[dir] = -5
                # continue
            newCoord = self.getDirCoords(dir, self.x, self.y)
            weights[dir] = 5
            if newCoord[0] == None or newCoord[1] == None or grid[newCoord[0]][newCoord[1]] != '.':
                weights[dir] = 0
                continue
            else:
                if (not forced and len(neigh[oppDirection[dir]]) == 0 and (self.x != 0 and self.y != 0)):
                    weights[dir] = 0
                    continue
                if not len(neigh[dir]) and grid[newCoord[0]][newCoord[1]] == '.':
                    weights[dir] += 1
                if (newCoord[0] == self.prevX) or dir == oppDirection[self.dir]:
                    weights[dir] -= 1
                if self.dir == dir:
                    weights[dir] += 1
                if len(neigh[dir]) == 0:
                    weights[dir] += 1
                if len(neigh[oppDirection[dir]]) > 0:
                    weights[dir] += (5 - neigh[oppDirection[dir]][0][3])#1 # neigh[oppDirection[dir]][0][3] / 2 # (5 - neigh[oppDirection[dir]][0][3]) # neigh[oppDirection[dir]][0][3] / 3
                if len(neigh[dir]) and neigh[dir][0][2] == 'W' and neigh[dir][0][3] < 2:
                    if neigh[dir][0][3] < 2:
                         weights[dir] = 0
                    else:
                        weights[dir] -= (5 - neigh[dir][0][3])
        maxi = max(weights.values())
        all_maxes = [ele for ele in weights if weights[ele] == maxi]
        maxi = random.choice(all_maxes)
        if weights[maxi] < 1:
            return None
        if random.randrange(1, 100) < 21:
            newDict = dict()
            for (key, value) in weights.items():
                if key != maxi and value > 0: # and key != oppDirection[maxi]:
                    newDict[key] = value
                if len(newDict) > 0:
                    choice = random.choice(list(newDict))
                    coords = self.getDirCoords(choice, self.x, self.y)
                    return (choice, coords)
        coords = self.getDirCoords(maxi, self.x, self.y)
        return (maxi, coords)
    
    def drawCirc(self):
        stroke(0)
        fill(100, 100, 100)
        circle(self.y * w + rw, self.x * w + rw, 85)
        stroke(0)
        fill(5, 130, 200)
        rect(self.y * w + rw, self.x * w + rw, rw, rw)

    def getDirCoords(self, dir, x, y):
        if dir == 'n':
            x, y = x, y - 1
        elif dir == 's':
            x, y = x, y + 1
        elif dir == 'e':
            x, y = x + 1, y
        elif dir == 'w':
            x, y = x - 1, y
        elif dir == 'ne':
            x, y = x + 1, y - 1
        elif dir == 'nw':
            x, y = x - 1, y - 1
        elif dir == 'se':
            x, y = x + 1, y + 1
        elif dir == 'sw':
            x, y = x - 1, y + 1
        x = x if x > -1 and x < matrixDim else None
        y = y if y > -1 and y < matrixDim else None
        return x, y
    
    def searchNeigh(self, grid, x, y, dir, distance = 1):
        found = []
        nextX, nextY = self.getDirCoords(dir, x, y)
        steps = distance
        while steps < 6 and nextX != None and nextY != None:
            if grid[nextX][nextY] == 'x' or grid[nextX][nextY] == 'D' or grid[nextX][nextY] == 'W':
                found.append((nextX, nextY, grid[nextX][nextY], steps))
                return found
            if dir in ['se', 'sw', 'ne', 'nw']:
                found += self.searchNeigh(grid, nextX, nextY, dir[0], steps - 1)
                found += self.searchNeigh(grid, nextX, nextY, dir[1], steps - 1)
                if len(found):
                    return found
            nextX, nextY = self.getDirCoords(dir, nextX, nextY)
            steps += 1
        return found

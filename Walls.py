# class WallClass:
#     def __init__(self, n = 'auto'):
#         self.mode = 
import copy

def makeOuter(grid):
    for i in range(83):
        grid[i][0] = 'W'
        grid[i][83] = 'W'
    for i in range(83):
        grid[0][i] = 'W'
        grid[83][i] = 'W'
    return grid

def makeSquare(x,y,x1,y1, grid):
    for i in range(x,x1+1):
        grid[i][y] = 'W'
        grid[i][y1] = 'W'
    for i in range(y,y1):
        grid[x][i] = 'W'
        grid[x1][i] = 'W'
    return grid

def makeALine(x,y,l,dir,grid):
    for i in range(l):
        if dir == 'v':
            grid[x+i][y] = 'W'
        else:
            grid[x][y+i] = 'W'
    return grid
    
'''
  initiates walls in the matrix, marking them as 'W'
'''
def WallClass(grid):
    gr = copy.deepcopy(grid)
    gr = makeOuter(gr)
    gr = makeSquare(50,50,60,60,gr)
    gr = makeSquare(20,10,30,30,gr)
    gr = makeSquare(50,50,60,60,gr)
    gr = makeSquare(50,10,60,25,gr)
    gr = makeSquare(10,50,20,60,gr)
    gr = makeALine(40,30,25,'h',gr)
    gr = makeALine(60,1,25,'h',gr)
    gr = makeALine(1,10,10,'v',gr)
    return gr

import sys
import copy
import numpy as np
import time
from datetime import datetime
import copy


def applyGravity(gridArray):
    for j in range(0, sizeOfGrid):
        copyArray = gridArray[:, j]
        for k in range(0, sizeOfGrid):
            if (copyArray[k] == '*'):
                copyArray = np.delete(copyArray, k)
                copyArray = np.insert(copyArray, 0, '*')
        gridArray[:, j] = copyArray
    return gridArray


def isInBound(x, y):
    if (x >= 0 and y >= 0 and x < sizeOfGrid and y < sizeOfGrid):
        return True
    return False


def checkRegions(x, y, grid, number, dontGo, region, gridCheck):
    if (isInBound(x, y)):
        if (gridCheck[x][y] == False):
            if (grid[x][y] == number):
                region.append((x, y))
                gridCheck[x][y] = True
                if (dontGo != 'u'):
                    checkRegions(x - 1, y, grid, number, 'd', region, gridCheck)
                if (dontGo != 'd'):
                    checkRegions(x + 1, y, grid, number, 'u', region, gridCheck)
                if (dontGo != 'r'):
                    checkRegions(x, y + 1, grid, number, 'l', region, gridCheck)
                if (dontGo != 'l'):
                    checkRegions(x, y - 1, grid, number, 'r', region, gridCheck)


def popRegion(gridSent, region):
    grid = gridSent.copy()
    for j, k in region:
        grid[j][k] = '*'
    applyGravity(grid)
    return grid


class Node:
    gridArray = []
    children = []
    myScore = 0
    opScore = 0
    starCount = 0

    def __init__(self, gridPassed, stars, myScorePassed=0, opScorePassed=0, popped=None):
        self.gridArray = gridPassed.copy()
        self.children = []
        self.myScore = myScorePassed
        self.opScore = opScorePassed
        self.value = 0
        self.starCount = stars
        self.popped = popped
        self.calledFunction = 0


def alphaBetaMax(node, alpha, beta, depthLimit):
    #alphaBetaMax.counter = alphaBetaMax.counter + 1
    if depthLimit < 0 or node.starCount >= maximumStars:
        node.value = node.myScore - node.opScore
    else:
        node.value = - sys.maxsize
        regions = []
        gridCheck = np.zeros((sizeOfGrid, sizeOfGrid), dtype=bool)
        for i in range(0, sizeOfGrid):
            for j in range(0, sizeOfGrid):
                # If not already part of a region.
                if (gridCheck[i][j] == False):

                    # Make part of region
                    gridCheck[i][j] = True

                    # Check if element is '*', if yes, skip.
                    if (node.gridArray[i][j] != '*'):
                        # Create a new region and add this index to it.
                        region = []
                        region.append((i, j))

                        # Get the fruit at that location.
                        fruit = node.gridArray[i][j]

                        # Check for an existing region for this fruit on the right.
                        checkRegions(i, j + 1, node.gridArray, fruit, 'l', region, gridCheck)
                        # Check for an existing region for this fruit below.
                        checkRegions(i + 1, j, node.gridArray, fruit, 'u', region, gridCheck)

                        # Add this newly detected region into the list of regions for this node.
                        regions.append(region)
        sortRegions(regions)
        for region in regions:

            # Update the score to the right measure if this region is popped.
            myScore = node.myScore
            opScore = node.opScore

            gridChild = copy.deepcopy(popRegion(node.gridArray, region))

            myScore = myScore + np.square(region.__len__())
            stars = node.starCount + region.__len__()

            # Create a new child node and add it to the children of this node.
            childNode = Node(gridChild, stars, myScore, opScore, (chr(64 + 1 + region[0][1]), region[0][0] + 1))

            node.value = max(node.value, alphaBetaMin(childNode, alpha, beta, depthLimit - 1))
            node.calledFunction += 1
            if (node.value >= beta):
                return node.value
            alpha = max(alpha, node.value)

            node.children.append(childNode)

        # Terminal Test
        if (regions.__len__() == 0):
            node.value = node.myScore - node.opScore

    return node.value


def alphaBetaMin(node, alpha, beta, depthLimit):
    #alphaBetaMin.counter = alphaBetaMin.counter + 1
    if depthLimit < 0 or node.starCount == maximumStars:
        node.value = node.myScore - node.opScore
    else:
        node.value = sys.maxsize
        count = 0
        regions = []
        # ti1 = datetime.now()

        gridCheck = np.zeros((sizeOfGrid, sizeOfGrid), dtype=bool)
        for i in range(0, sizeOfGrid):
            for j in range(0, sizeOfGrid):
                # If not already part of a region.
                if (gridCheck[i][j] == False):

                    # Make part of region
                    gridCheck[i][j] = True

                    # Check if element is '*', if yes, skip.
                    if (node.gridArray[i][j] != '*'):
                        # Create a new region and add this index to it.
                        region = []
                        region.append((i, j))

                        # Get the fruit at that location.
                        fruit = node.gridArray[i][j]

                        # Check for an existing region for this fruit on the right.
                        checkRegions(i, j + 1, node.gridArray, fruit, 'l', region, gridCheck)
                        # Check for an existing region for this fruit below.
                        checkRegions(i + 1, j, node.gridArray, fruit, 'u', region, gridCheck)

                        # Add this newly detected region into the list of regions for this node.
                        regions.append(region)
        sortRegions(regions)
        for region in regions:
            # Update the score to the right measure if this region is popped.
            myScore = node.myScore
            opScore = node.opScore

            gridChild = popRegion(node.gridArray, region)

            opScore = opScore + np.square(region.__len__())

            stars = node.starCount + region.__len__()

            count += 1

            # Create a new child node and add it to the children of this node.
            childNode = Node(gridChild, stars, myScore, opScore, (chr(64 + 1 + j), i + 1))
            node.value = min(node.value, alphaBetaMax(childNode, alpha, beta, depthLimit - 1))
            node.calledFunction += 1

            if (node.value <= alpha):
                return node.value
            beta = min(beta, node.value)

            node.children.append(childNode)
        # ti2 = datetime.now()

        # print('Time for generating ', count,' children: ', ti2-ti1,' at depth ', depthLimit)

        # Terminal Test
        if (regions.__len__() == 0):
            node.value = node.myScore - node.opScore

    return node.value


def sortRegions(listToSort):
    if len(listToSort) > 1:
        centerIndex = len(listToSort) // 2
        regionsLeft = listToSort[:centerIndex]
        regionsRight = listToSort[centerIndex:]

        sortRegions(regionsLeft)
        sortRegions(regionsRight)

        one = 0
        two = 0
        three = 0
        while one < len(regionsLeft) and two < len(regionsRight):
            if regionsLeft[one].__len__() > regionsRight[two].__len__():
                listToSort[three] = regionsLeft[one]
                one = one + 1
            else:
                listToSort[three] = regionsRight[two]
                two = two + 1
            three = three + 1

        while one < len(regionsLeft):
            listToSort[three] = regionsLeft[one]
            one = one + 1
            three = three + 1

        while two < len(regionsRight):
            listToSort[three] = regionsRight[two]
            two = two + 1
            three = three + 1




# Start reading from file
fileVar = open('input.txt', 'r')
alphaBetaMin.counter = 0
alphaBetaMax.counter = 0
depth = 1

sizeOfGrid = int(fileVar.readline())
print(sizeOfGrid)
typesOfFruit = int(fileVar.readline())
print(typesOfFruit)
timeToRun = (fileVar.readline())
print(timeToRun)
grid = []
if float(timeToRun) < 60:
    depth = 0
elif(sizeOfGrid<=7 and float(timeToRun) > 150):
    depth =3
elif sizeOfGrid >= 10 and float(timeToRun) < 150:
    depth = 0

print('Depth: ', depth)
for j in range(0, sizeOfGrid):
    grid.append(list(fileVar.readline())[:sizeOfGrid])

grid = np.array(grid)
gridCheck = np.full((sizeOfGrid, sizeOfGrid), False, dtype=bool)
# print(grid)

# Start detecting regions
regions = []

t1 = datetime.now()
stars = 0
for i in range(0, sizeOfGrid):
    for j in range(0, sizeOfGrid):
        # print((i,j))
        if grid[i][j] == '*':
            stars = stars + 1

maximumStars = np.square(sizeOfGrid)
node = Node(grid, stars)

finalValue = alphaBetaMax(node, -sys.maxsize, sys.maxsize, depth)

selectedMove = None
for i in range(0, node.children.__len__()):
    if (node.children[i].value == finalValue):
        selectedMove = node.children[i]
        break
#if selectedMove != None:
#    print(selectedMove.gridArray)
t2 = datetime.now()

print(t2 - t1)

totalCount = alphaBetaMin.counter + alphaBetaMax.counter
print(totalCount)
print('Outputting.')
output = open('output.txt', 'w')
output.write(selectedMove.popped[0] + selectedMove.popped[1].__str__() + '\n')
for s in range(0, sizeOfGrid):
    for p in range(0, sizeOfGrid):
        output.write(selectedMove.gridArray[s][p])
    output.write('\n')
output.close()

## use numpy to make it more efficient
import math
from MazeNode import *

def isCrossIntersection(left,right,up,down):
    if right != "#" and up != "#" and left != "#" and down != "#":
        return True
    else:
        return False
def isTIntersection(left,right,up,down):
    rightT = (right != "#" and up != "#" and down != "#")
    leftT = (left != "#" and up != "#" and down != "#")
    downT = (right != "#" and left != "#" and down != "#")
    upT = (right != "#" and left != "#" and up != "#")
    if rightT or leftT or downT or upT:
        return True
    else:
        return False
def isLIntersection(left,right,up,down):
    l = up != "#" and right != "#"
    rightL = right != "#" and down != "#"
    downL = down != "#" and left != "#"
    leftL = left != "#" and up != "#"
    if l or rightL or downL or leftL:
        return True
    else:
        return False
    
def isNode(maze,i,j):
    ## This will provide the values above, below, and to the side of a point
    right,left,up,down = maze[i][j+1], maze[i][j-1], maze[i-1][j], maze[i+1][j]
    ## If it is a cross node
    if isCrossIntersection(left,right,up,down) == True:
        return True
    ## If it is a T intersection
    elif isTIntersection(left,right,up,down) == True:
        return True
    ## If it is an L intersection
    elif isLIntersection(left,right,up,down) == True:
        return True
    else:
        return False

def findNodes(maze):
    ## creates a dictionary of the nodes. A list will describe the
    ## the properties. The list will read [name,distance,row,column,prior node]
    nodes = {}
    num = 0
    for i in range(len(maze)):
        for j in range(len(maze)):
            if maze[i,j] == "S":
                nodes["S"] = ["S", 0, i, j, None]
            elif maze[i,j] == "E":
                nodes["E"] = ["E",math.inf, i, j, None]
            elif maze[i,j] == " ":
                if isNode(maze,i,j) == True:
                    nodes[num] = [num,math.inf,i,j, None]
                    num += 1
    return nodes

def getChildren(maze,nodes):
    tree = {} ## Create an empty dictionary that will contain the parents and children
    for node in nodes: ## Go through each node
        tree[node] = [] ## each node will have a list
        nodeI,nodeJ = nodes[node][2],nodes[node][3] ## The positions of the node will be gathered
        right,left,up,down = 0,0,0,0 ## Initialize for 4 children max
        for n in nodes: ## Go through each node again
            otherNodeI,otherNodeJ = nodes[n][2],nodes[n][3] ## Get other node location
            if (otherNodeI == nodeI and otherNodeJ == nodeJ): ## blocks current node
                pass
            elif nodeI == otherNodeI: ## If the i position of the matrix is the same look at it
                if nodeJ < otherNodeJ and right < 1: ## If the current node is to the left and there are no children to the right
                    row = maze[nodeI, nodeJ:otherNodeJ] ## splice the row
                    if "#" not in row:
                        tree[node].append(nodes[n][0])
                        right += 1
                elif nodeJ > otherNodeJ and left < 1: ## Do the smae for the left
                    row = maze[nodeI][otherNodeJ:nodeJ]
                    if "#" not in row:
                        tree[node].append(nodes[n][0])
                        left += 1
            elif nodeJ == otherNodeJ: ## If the columns are the same
                col = [row[nodeJ] for row in maze] ## get the column
                if nodeI < otherNodeI and down < 1: 
                    col = col[nodeI:otherNodeI]
                    if "#" not in col:
                        tree[node].append(nodes[n][0])
                        down += 1

        for n in reversed(list(nodes)): ## Now look up
            otherNodeI,otherNodeJ = nodes[n][2],nodes[n][3]
            if (otherNodeI == nodeI and otherNodeJ == nodeJ):
                pass
            elif nodeJ == otherNodeJ:
                col = [row[nodeJ] for row in maze]
                if nodeI > otherNodeI and up < 1:
                    col = col[otherNodeI:nodeI]
                    if "#" not in col:
                        tree[node].append(nodes[n][0])
                        up += 1
    return tree

def unvisitedNodes(nodes):
    unvisited = []
    for node in nodes:
        unvisited.append(node)
    return unvisited

def nodeBuildMain(maze):
    nodes = findNodes(maze)
    tree = getChildren(maze,nodes)
    return tree,nodes

import random as rd
import numpy as np
import queue 
from PIL import Image

class Maze:

    def __init__(self,rows,columns):
        ## define the class varaibles
        self.rows = rows
        self.columns = columns

    def generateInitialMatrix(self):
        ## Generate the canvas
        ## Mark the start and finish
        ## Create the matrix of visited and unvisited

        maze = self.setUpRows( " ", "#","str")

        start = (0,self.initialPoints())
        end = self.initialPoints()
        maze[0, start[1]] = "S"
        maze[self.rows-1, end] = "E"

        visited = self.setUpRows(0, 1,"int")
        visited[self.rows-1,end] = 0
        return maze,visited,start

    def setUpRows(self,space,barrier,dataType):
        ## This will create a generic set up of the rows/columns
        barrierArray = np.array([barrier]*self.columns)
        openBarrierArray = np.array([barrier,space] * int(((self.columns-1)/2)))
        openBarrierArray = np.append(openBarrierArray,barrier)
        mat = np.empty((self.rows,self.columns),dtype=dataType)
        mat[0] = barrierArray
        mat[-1] = barrierArray
        for i in range(1,self.rows-1):
            if i%2 == 0:
                mat[i] = openBarrierArray
            else:
                mat[i] = barrierArray
        return mat

    def initialPoints (self):
        ## Generate the start and end Point. Maintain perimeter
        j = rd.randrange(1,self.columns-2,2)
        return j

    def findNeighbors(self,visited,currentCell):
        ## This functions finds the neighbors if there are any
        neighbors = []
        ## Create boundaries 
        leftBound, rightBound, upBound, downBound = 3, self.columns - 4, 4, self.rows - 2
        inc = 2
        ## Check values to the left
        if currentCell[1] >= leftBound and visited[currentCell[0], currentCell[1] - inc] == 0:
            neighbor = (currentCell[0], currentCell[1] - inc)
            neighbors.append(neighbor)
        ## Check values to the right
        if currentCell[1] <= rightBound and visited[currentCell[0], currentCell[1] + inc] == 0:
            neighbor = (currentCell[0], currentCell[1] + inc)
            neighbors.append(neighbor)
        ## Check values above
        if currentCell[0] >= upBound and visited[currentCell[0] - inc, currentCell[1]] == 0:
            neighbor = (currentCell[0] - inc, currentCell[1])
            neighbors.append(neighbor)
        ## Check values below
        if currentCell[0] <= downBound and visited[currentCell[0] + inc, currentCell[1]] == 0:
            neighbor = (currentCell[0] + inc, currentCell[1])
            neighbors.append(neighbor)

        return neighbors

    def removeWall(self,maze,currentCell,choosenCell):
        ## this function will remove the wall between open spaces
        if currentCell[0] == choosenCell[0]:
            if currentCell[1] < choosenCell[1]:
                maze[currentCell[0], currentCell[1] + 1] = " "
            else:
                maze[currentCell[0], currentCell[1] - 1] = " "
        if currentCell[1] == choosenCell[1]:
            if currentCell[0] < choosenCell[0]:
                maze[currentCell[0] + 1, currentCell[1]] = " "
            else:
                maze[currentCell[0] - 1, currentCell[1]] = " "

        return maze

    def backtrack(self,maze,visited,start):
        ## This is just a backtrakc algorithm but in a loop format
        q = queue.LifoQueue()
        q.put(start)
        visited[start[0], start[1]] = 1

        while q.empty() == False:
            currentCell = q.get()
            neighbors = self.findNeighbors(visited,currentCell)
            ## If neghbors then go through process
            if len(neighbors) > 0:
                q.put(currentCell)
                choosenCell = rd.choice(neighbors)
                maze = self.removeWall(maze,currentCell,choosenCell)
                visited[choosenCell[0],choosenCell[1]] = 1
                q.put(choosenCell)
        return maze

    def generateImage(self,maze):
        ## Create the image
        mazeImage = Image.new('RGB',(self.rows,self.columns))
        pixels = mazeImage.load()
        
        for i in range(self.rows):
            for j in range(self.columns-1):
                if maze[i,j] == " " :
                    pixels[j,i] = (255,255,255)
                elif maze[i,j] == "S":
                    pixels[j,i] = (0,255,0)
                elif maze[i,j] == "E":
                    pixels[j,i] = (255,0,0)
                elif maze[i,j] == "o":
                    pixels[j,i] = (0,0,255)

        return mazeImage

    def generateMaze(self):
            maze,visited,start = self.generateInitialMatrix()
            maze = self.backtrack(maze,visited,start)
            return maze

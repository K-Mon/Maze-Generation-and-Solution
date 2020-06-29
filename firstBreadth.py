import queue
import numpy as np

class firstBreadthSolver:

    def __init__(self,maze):
        ## Initialize the varaibles
        self.maze = maze
        self.mazeDims = len(maze[0])
        self.start = None
        self.end = None
        self.que = queue.Queue()
        self.searching = True
        self.truthTable = np.ones((len(maze[0]), len(maze[0])),dtype=bool)

    def generateTtable(self):
        ## Generate the truth table
        for i in range(self.mazeDims):
            for j in range(self.mazeDims):
                if self.maze[i,j] == " " or self.maze[i,j] == "E":
                    self.truthTable[i,j] = False

    def getStartPos(self):
        ## Get the start and end position of the maze
        for i in range(self.mazeDims):
            if self.maze[0,i] == "S":
                self.start = (0,i)
        for i in range(self.mazeDims):
            if self.maze[-1,i] == "E":
                self.end = (self.mazeDims-1,i)
    
    def calculatePosition(self,x,y,letter):
        ## calculate the new position based on the letter
        if letter == "L":
                y -= 1
        elif letter == "R":
                y += 1
        elif letter == "U":
                x -= 1
        elif letter == "D":
                x += 1
        return x,y
    
    def readPhrase(self,item):
        ## Take the item which contains directions
        ## Read it and find the path
        x,y = self.start[0],self.start[1]
        if item != "":
            for letter in item:
                x,y = self.calculatePosition(x,y,letter)
        return x,y
    
    def printPositions(self,item):
        ## Take the phrase and print it
        x,y = self.start[0],self.start[1]
        for letter in item:
            x,y = self.calculatePosition(x,y,letter)
            self.maze[x,y] = "o"
    
    def addOrEnd(self,qItem,x,y,letter):
        ## Determine if the phrase has reached the end or
        ## or if it should be added to the queue
        if self.end[0] == x and self.end[1] == y:
            self.searching = False
            self.printPositions(qItem)
        else:
            self.que.put("".join([qItem,letter]))
            self.truthTable[x,y] = True
        
    def getNewItems(self, qItem):
        ## Get the paths
        x,y = self.readPhrase(qItem)
        if x <= self.mazeDims-2 and self.truthTable[x+1,y] == False:
            self.addOrEnd(qItem,x+1,y,"D")
        if x >= 1 and self.truthTable[x-1,y] == False:
            self.addOrEnd(qItem,x-1,y,"U")
        if y <= self.mazeDims-2 and self.truthTable[x,y+1] == False:
            self.addOrEnd(qItem,x,y+1,"R")
        if y >= 1 and self.truthTable[x,y-1] == False:
            self.addOrEnd(qItem,x,y-1,"L")
            
    def process(self):
        ## the power house that will run the entire solution
        ## returns the solution matrix
        self.generateTtable()
        self.getStartPos()
        self.que.put("")
        while self.searching == True:
            qItem = self.que.get()
            self.getNewItems(qItem)
        return self.maze
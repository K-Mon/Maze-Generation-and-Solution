class node:
    def __init__(self,name,i,j):
        self.name = name
        self.i = i
        self.j = j
        self.priorNode = None
    def updatePrior(self,point):
        self.priorNode = point
    def getPriorNode(self):
        return self.priorNode.getNode()
    def getI(self):
        return self.i
    def getJ(self):
        return self.j
    def getNode(self):
        return self.i,self.j
    def getName(self):
        return self.name

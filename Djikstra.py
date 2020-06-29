from NodeBuildDic import *
import math
from queue import *

class djikstraSolver:
    def __init__ (self,maze):
        self.maze = maze

    def getDistance(self,x1,x2,y1,y2):
        dist = int(math.sqrt(math.pow((x1-x2),2) + math.pow((y1-y2),2)))
        return dist

    def djikstra(self,nodes,tree):
        visited = [] ## Make a list of visited nodes
        que = PriorityQueue() ## create a priority Queue
        startLetter,startDistance = nodes["S"][0],nodes["S"][1] ## Start with the Start node
        que.put((startDistance, startLetter)) ## Put the start node in the que
        while que.empty() == False: ## While the que is not empty
            parent = que.get() ## Get the item with the shortest distance
            if parent[1] not in visited: ## Continue if the parent has not been visited
                visited.append(parent[1]) ## mark it as visited
                for child in tree[parent[1]]: ## For each parent nodes child
                    if child not in visited: ## Only look at nodes that have been visited
                        parentI,parentJ = nodes[parent[1]][2],nodes[parent[1]][3] ## Get the i,j of hte parent
                        childI,childJ = nodes[child][2],nodes[child][3] ## Get the i,j of the child
                        dist = self.getDistance(parentI,childI,parentJ,childJ) + parent[0] ## Get distance to the child
                        if dist < nodes[child][1]: ## If the distnace is shorter than the existing distance, update it and the parent node
                            nodes[child][1] = dist
                            nodes[child][4] = parent[1]
                        if child != "E": ## If the child is not the end add it to the queue
                            que.put((nodes[child][1],child))

        return nodes, tree

    def makePathPoints(self,i,j,loopRange,val):
        if val == "j":
            for col in loopRange:
                if self.maze[i][col] == " ":
                    self.maze[i][col] = "o"
        else:
            for row in loopRange:
                if self.maze[row][j] == " ":
                    self.maze[row][j] = "o"

    def makePath(self,nodes):
        node = nodes["E"]
        while node[0] != "S":
            print(nodes[node[4]])
            i,j = node[2],node[3]
            node2 = nodes[node[4]]
            node2i,node2j = node2[2],node2[3]
            if node2i == i:
                if node2j > j:
                    self.makePathPoints(i,j,range(j,node2j+1),"j")
                else:
                    self.makePathPoints(i,j,range(node2j,j+1),"j")
            elif node2j == j:
                if node2i > i:
                    self.makePathPoints(i,j,range(i,node2i+1),"i")
                else:
                    self.makePathPoints(i,j,range(node2i,i+1),"i")
        
            node = node2
    
        
    def getPath(self):
        nodes = findNodes(self.maze)
        tree,nodes = nodeBuildMain(self.maze)
        print(tree)
        nodes, tree = self.djikstra(nodes,tree)
        self.makePath(nodes)
        return self.maze
    
 

import backTrack
import Djikstra
import firstBreadth

def main():
    rows = 2
    print("This python file will generate and solve a square maze\n")
    question = "Please enter the width of the maze,\nit must be odd and greater than 7: "
    while rows < 7 and rows%2==0:
        rows = int(input(question))
    ## Generate the maze
    generatedMaze = backTrack.Maze(rows,rows)
    maze = generatedMaze.generateMaze()

    print('(1) Djikstra \n(2) Breadth First Search\n')
    searchMove = input("Enter: ")

    if searchMove == "1":
        djikstraPath = Djikstra.djikstraSolver(maze)
        dMaze = djikstraPath.getPath()
        generatedMaze.generateImage(dMaze).show()

    elif searchMove == "2":
        generatedMaze.generateImage(maze).show()
        fbSolver = firstBreadth.firstBreadthSolver(maze)
        fbMaze = fbSolver.process()
        generatedMaze.generateImage(fbMaze).show()

main()





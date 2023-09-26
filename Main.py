from Node        import Node
from Graph       import Graph


# CPSC 322 Assignment 2 Question 2
# graph as an adjacency matrix where
# a node's weight to itself is its heuristic value.
                   # S   A   B   C   D   E   F   G   H   Z
mainGraph = Graph([[24,  3,  9,  4,  0,  0,  0,  0,  0,  0],  # S
                   [ 0, 21,  0,  2,  0,  0,  0,  0,  0,  0],  # A
                   [ 0,  0, 19, 13,  0,  0,  0,  0,  0,  0],  # B
                   [ 0,  0,  0, 19,  5,  4,  8,  0,  0,  0],  # C
                   [ 0,  0,  0,  0,  9,  0,  5,  0,  0,  0],  # D
                   [ 0,  0,  0,  0,  0, 11,  7,  0,  0,  0],  # E
                   [ 0,  0,  0,  0,  0,  0, 12,  8,  7, 18],  # F
                   [ 0,  0,  0,  0,  0,  0,  0,  4,  0,  9],  # G
                   [ 0,  0,  0,  0,  0,  0,  0,  0,  6,  6],  # H
                   [ 0,  0,  0,  0,  0,  0,  0,  0,  0,  0]]) # Z

mainGraphSize = len(mainGraph.getNodes())
Node.setLabels(['S', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'Z'])

# ----------- GENERIC SEARCH ALGORITHM ----------- #

def search(g:Graph) -> bool:
    print("Found: ", end='')  # Output formatting.

    # Add start node to frontier
    frontier:list[list[Node]] = [[g.getStart()]]

    # While frontier is not empty, get the next path and 
    # the last node of that path from the frontier. 
    # If the node is a goal node, return True,
    # otherwise expand the node according to 
    # externally defined logic.
    while len(frontier) != 0:
        curPath:list[Node] = frontier[::-1][0]
        curNode:Node       = curPath [::-1][0]

        print(curNode, end='')  # Print expanded nodes.

        if g.isGoal(curNode):
            print("\nPath:  " + printPath(curPath), end='\n\n')  # Print on solution found.
            return True
        
        frontier = addToFrontier(frontier)
    
    print("\nNo path found.")  # Print on solution not found.
    return False

# ---------------- EXTERNAL LOGIC ---------------- #
# Defines the frontier behaviour as specified
# by the top-level functions.

def frontierBehaviour(reverseFrontier:bool=False, reverseNeighbours:bool=False, depth:int=mainGraphSize, sortByCost:bool=False, sortByH:bool=False):
    # reverseFrontier and reverseNeighbours allow for FIFO and LIFO
    # behaviour with basic array splicing. depth allows the implementation
    # of IDS. sortByCost and sortByH are used in LCFS, BestFS, and A*.
    global addToFrontier
    def addToFrontier(frontier:list[list[Node]]) -> list[list[Node]]:
        curPath    = frontier.pop()
        curNode    = curPath[::-1][0]
        # -2*(int(bool))+1 --> False=1, True=-1 --> False=list[::1], True=list[::-1]
        neighbours = list(curNode.getNeighbours())[::-2*int(reverseNeighbours)+1]   

        if len(curPath)<=depth:
            for neighbour in neighbours:
                frontier = frontier[::-2*int(reverseFrontier)+1]
                t = curPath.copy()
                t.append(neighbour)
                frontier.append(t)
                frontier = frontier[::-2*int(reverseFrontier)+1]
        
        # Sorts frontier as specified.
        costDict = {tuple(p):(int(sortByCost)*fx(p, sortByCost, sortByH)) for p in frontier}
        return [list(p) for p,fp in sorted(costDict.items(), key=lambda item: item[1], reverse=True)]

# Calculates path cost for use in LCFS, A*, and BandB.
def fx(path:list[Node], pathCost:bool, h:bool) -> int:
    cost = 0
    if pathCost:
        for i in range(0, len(path)-1):
            cost += path[i].getNeighbours()[path[i+1]]
    if h:
        cost += path[::-1][0].getH()
    return cost

def printPath(path:list[Node]):
    return "<" + ",".join(n.__str__() for n in path) + ">"

# ---------- TOP-LEVEL SEARCH FUNCTIONS ---------- #
# Each function changes the frontier behaviour 
# based on the selected search algorithm.

def BFS(g:Graph):
    print("BFS")
    frontierBehaviour(True)
    search(g)

def DFS(g:Graph):
    print("DFS")
    frontierBehaviour(False, True)
    search(g)

def IDS(g:Graph):
    print("IDS")
    depth = 0
    result = False
    # Increments search depth until solution is found.
    while result==False and depth <= mainGraphSize:
        depth += 1
        # DFS behaviour with depth limiting
        frontierBehaviour(True, False, depth)
        result = search(g)

def LCFS(g:Graph):
    print("LCFS")
    # BFS (queue) behaviour preserves alphabetical order
    # when sorted (by path cost)
    frontierBehaviour(True, False, mainGraphSize, True)
    search(g)

def BestFS(g:Graph):
    print("BestFS")
    # BFS (queue) behaviour preserves alphabetical order
    # when sorted (by node heuristic value)
    frontierBehaviour(True, False, mainGraphSize, False, True)
    search(g)

def AStar(g:Graph):
    print("A*")
    # BFS (queue) behaviour preserves alphabetical order
    # when sorted (by f(p))
    frontierBehaviour(True, False, mainGraphSize, True, True)
    search(g)

# Separate branch-and-bound search function.
def BandB(g:Graph) -> bool:
    frontierBehaviour(False, True)  # Frontier behaves as in DFS.
    ub       = float('inf')
    bestPath = []

    print("BandB")
    print("Found: ", end='')

    frontier:list[list[Node]] = [[g.getStart()]]

    while len(frontier) != 0:
        curPath:list[Node] = frontier[::-1][0]
        curNode:Node       = curPath [::-1][0]

        print(curNode, end='')

        # Only considers a path if f(p) < ub
        # Does not return when solution found, 
        # instead continues search with lower ub.
        if fx(curPath, True, True)< ub:
            if g.isGoal(curNode):
                bestPath = curPath
                ub = fx(curPath, True, False)
            
            frontier = addToFrontier(frontier)
        else:
            # Discards current path.
            frontier.pop()
    
    if bestPath != []:
        print("\nPath:  " + printPath(bestPath), end='\n\n')
        return True
    
    print("\nNo path found.")
    return False

BFS   (mainGraph)
DFS   (mainGraph)
IDS   (mainGraph)
LCFS  (mainGraph)
BestFS(mainGraph)
AStar (mainGraph)
BandB (mainGraph)
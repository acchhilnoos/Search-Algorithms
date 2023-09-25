from collections import deque
from Node        import Node
from Path        import Path
from Graph       import Graph

# ----------- GENERIC SEARCH ALGORITHM ----------- #

def search(g:Graph) -> bool:
    # Output formatting
    print("Found: ", end='')

    # frontier <-- [<s>];
    frontier:deque[list[Node]] = deque([[g.getStart()]])

    # while frontier is not empty
    while len(frontier) != 0:
        # select and remove path <no,....,nk> from frontier;
        curPath = frontier.pop()
        curNode = curPath[::-1][0]

        # output formatting
        print(curNode, end='')

        # if goal(nk)
        if g.isGoal(curNode):
            #output formatting
            print("\nPath:  " + Path(curPath).__str__(), end='\n\n')

            # return <no,....,nk>;
            return True
        
        # for every neighbor n of nk
        # add <no,....,nk, n> to frontier;
        # behaviour determined by EXTERNAL LOGIC section
        frontier = addToFrontier(frontier, curPath, curNode)
    
    # output formatting
    print("\nNo path found.")

    # return NULL
    return False

# Q2 graph as an adjacency matrix 
# a node's weight to itself is its heuristic value
                 # S   A   B   C   D   E   F   G   H   Z
q2Graph = Graph([[24,  3,  9,  4,  0,  0,  0,  0,  0,  0],  # S
                 [ 0, 21,  0,  2,  0,  0,  0,  0,  0,  0],  # A
                 [ 0,  0, 19, 13,  0,  0,  0,  0,  0,  0],  # B
                 [ 0,  0,  0, 19,  5,  4,  8,  0,  0,  0],  # C
                 [ 0,  0,  0,  0,  9,  0,  5,  0,  0,  0],  # D
                 [ 0,  0,  0,  0,  0, 11,  7,  0,  0,  0],  # E
                 [ 0,  0,  0,  0,  0,  0, 12,  8,  7, 18],  # F
                 [ 0,  0,  0,  0,  0,  0,  0,  4,  0,  9],  # G
                 [ 0,  0,  0,  0,  0,  0,  0,  0,  6,  6],  # H
                 [ 0,  0,  0,  0,  0,  0,  0,  0,  0,  0]]) # Z

# ---------------- EXTERNAL LOGIC ---------------- #
# defines the frontier behaviour as chosen
# by the top-level functions

# appends paths to left of frontier as in a queue
def FIFOFrontier():
    global addToFrontier
    def addToFrontier(frontier:deque[list[Node]], curPath:list[Node], curNode:Node) -> deque[list[Node]]:
        for neighbour in curNode.getNeighbours():
            t = curPath.copy()
            t.append(neighbour)
            frontier.appendleft(t)
        return frontier

# appends paths to right of frontier as in a stack
# in reverse to preserve alphabetical order
# additional depth argument allows for re-use in IDS
def FILOFrontier(depth:int):
    global addToFrontier
    def addToFrontier(frontier:deque[list[Node]], curPath:list[Node], curNode:Node) -> deque[list[Node]]:
        if len(curPath)<=depth:
            for neighbour in reversed(curNode.getNeighbours()):
                t = curPath.copy()
                t.append(neighbour)
                frontier.append(t)
        return frontier

# calculates path cost for use in LCFS and A*
def pathCost(p:list[Node]) -> int:
    cost = 0
    for i in range(0, len(p)-1):
        cost += p[i].getNeighbours()[p[i+1]]
    return cost

# sorts frontier based on passed function
def sortedFrontier(sort):
    global addToFrontier
    def addToFrontier(frontier:deque[list[Node]], curPath:list[Node], curNode:Node) -> deque[list[Node]]:
        for neighbour in curNode.getNeighbours():
            t = curPath.copy()
            t.append(neighbour)
            frontier.appendleft(t)
        return sort(frontier)

# ---------- TOP-LEVEL SEARCH FUNCTIONS ---------- #
# each function determines the frontier behaviour 
# based on the selected search algorithm

def BFS():
    print("BFS")
    FIFOFrontier()
    search(q2Graph)

def DFS():
    print("DFS")
    FILOFrontier(len(q2Graph.getNodes()))
    search(q2Graph)

def IDS():
    print("IDS")
    depth = 0
    result = False
    # incrementally increase search depth until solution is found
    while result==False and depth <= len(q2Graph.getNodes()):
        depth += 1
        FILOFrontier(depth)
        result = search(q2Graph)

def LCFS():
    print("LCFS")
    # sorts frontier by path cost
    def __sort(frontier:deque[list[Node]]):
        costDict = {tuple(p):pathCost(p) for p in frontier}
        return deque([list(p) for p,c in sorted(costDict.items(), key=lambda item: item[1], reverse=True)])
    sortedFrontier(__sort)
    search(q2Graph)

def BestFS():
    print("BestFS")
    # sorts frontier by heuristic value
    def __sort(frontier:deque[list[Node]]):
        costDict = {tuple(p):p[::-1][0].getH() for p in frontier}
        return deque([list(p) for p,h in sorted(costDict.items(), key=lambda item: item[1], reverse=True)])
    sortedFrontier(__sort)
    search(q2Graph)

def AStar():
    print("A*")
    # sorts frontier by path cost + heuristic value
    def __sort(frontier:deque[list[Node]]):
        costDict = {tuple(p):(p[::-1][0].getH() + pathCost(p)) for p in frontier}
        return deque([list(p) for p,f in sorted(costDict.items(), key=lambda item: item[1], reverse=True)])
    sortedFrontier(__sort)
    search(q2Graph)

def BandB(g:Graph) -> bool:
    # Output formatting
    FILOFrontier(len(g.getNodes()))
    ub = float('inf')
    print("BandB\nFound: ", end='')

    # frontier <-- [<s>];
    frontier:deque[list[Node]] = deque([[g.getStart()]])

    # while frontier is not empty
    while len(frontier) != 0:
        # select and remove path <no,....,nk> from frontier;
        curPath = frontier.pop()
        curNode = curPath[::-1][0]

        # output formatting
        print(curNode, end='')

        # if goal(nk)
        if g.isGoal(curNode):
            #output formatting
            print("\nPath:  " + Path(curPath).__str__(), end='\n\n')

            # return <no,....,nk>;
            return True
        
        # for every neighbor n of nk
        # add <no,....,nk, n> to frontier;
        # behaviour determined by EXTERNAL LOGIC section
        if pathCost(curPath) + curNode.getH() < ub:
            ub = pathCost(curPath) + curNode.getH()
            frontier = addToFrontier(frontier, curPath, curNode)
    
    # output formatting
    print("\nNo path found.")

    # return NULL
    return False
    

DFS()
BFS()
IDS()
LCFS()
BestFS()
AStar()
BandB()
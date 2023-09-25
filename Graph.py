from Node import Node

class Graph:
    def __init__(self, adjM:list[list[int]]) -> None:
        self._nodes:list[Node] = []
        
        # initialize graph nodes
        for i in range(0, len(adjM)):
            self._nodes.append(Node(i, adjM[i][i], {}))
        
        # add node neighbours and edges
        for i in range(0, len(adjM)):
            for j in range(0, len(adjM[i])):
                if j!=i and adjM[i][j] != 0:
                    self._nodes[i].addNeighbour(self._nodes[j], adjM[i][j])
        
        # set start node to first row of matrix
        self._start = self._nodes[0]
        # set goal node to last row of matrix
        self._goal  = self._nodes[::-1][0]
    
    def isGoal(self, n:Node):
        return n == self._goal
    
    def getStart(self):
        return self._start
    def getGoal(self):
        return self._goal
    def getNodes(self):
        return self._nodes
    
    # sadly unused adjacency matrix generator
    def __str__(self) -> str:
        return [[self._nodes[i].getH()
                 if i==j
                 else (self._nodes[i].getNeighbours()[self._nodes[j]]
                       if self._nodes[j] in self._nodes[i].getNeighbours()
                       else 0)
                       for j in range(0, len(self._nodes))]
                       for i in range(0, len(self._nodes))]._str_()
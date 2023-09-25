from Node import Node

class Path:
    def __init__(self, p:list[Node]):
        self._p = p
    
    def __str__(self) -> str:
        return "<" + ",".join(n.__str__() for n in self._p) + ">"
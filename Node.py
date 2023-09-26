from __future__ import annotations

class Node:
    _labels = []

    def __init__(self, index:int, h:int, neighbours:dict[Node, int]) -> None:
        self._index      = index
        self._h          = h
        self._neighbours = neighbours

    def addNeighbour(self, other:Node, weight:int):
        self._neighbours[other] = weight

    def getIndex(self):
        return self._index
    def getH(self):
        return self._h
    def getNeighbours(self):
        return self._neighbours

    def setLabels(labels:list[str]):
        Node._labels = labels

    def __str__(self) -> str:
        return self._labels[self._index]
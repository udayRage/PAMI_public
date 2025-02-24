class Vertex:
    def __init__(self, iD, vLabel):
        self.id = iD
        self.vLabel = vLabel
        self.eList = []

    def addEdge(self, edge):
        self.eList.append(edge)

    def getId(self):
        return self.id

    def getLabel(self):
        return self.vLabel

    def getEdgeList(self):
        return self.eList

    def removeEdge(self, edgeToRemove):
        self.eList = [edge for edge in self.eList if edge != edgeToRemove]

    def __eq__(self, other):
        if not isinstance(other, Vertex):
            return False
        return self.id == other.id

    def __lt__(self, other):
        if not isinstance(other, Vertex):
            return NotImplemented
        return self.id < other.id

    def __repr__(self):
        return f"Vertex(ID: {self.id}, Label: {self.vLabel})"

    def __hash__(self):
        return hash(self.id)



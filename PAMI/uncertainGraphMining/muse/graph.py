from vertex import Vertex
from edge import Edge
from dfsCode import DFSCode

class UncertainGraph:
    def __init__(self, iD, vertexMap=None, dfsCode=None):
        self.id = iD
        self.vertexMap = {}
        self.implicatedGraphs = []

        if vertexMap is not None:
            self.vertexMap = vertexMap

        if dfsCode is not None:
            self.buildFromDFSCode(dfsCode)

    def buildFromDFSCode(self, dfsCode):
        for ee in dfsCode.getEeList():
            v1, v2, v1Label, v2Label, eLabel = ee.getV1(), ee.getV2(), ee.getVLabel1(), ee.getVLabel2(), ee.getEdgeLabel()

            e = Edge(v1, v2, eLabel, 1.0)  # Assuming existenceProbability is 1.0 for all edges in DFS code
            if v1 not in self.vertexMap:
                self.vertexMap[v1] = Vertex(v1, v1Label)
            if v2 not in self.vertexMap:
                self.vertexMap[v2] = Vertex(v2, v2Label)

            self.vertexMap[v1].addEdge(e)
            self.vertexMap[v2].addEdge(e)

    def getVertexMap(self):
        return self.vertexMap

    def toDFSCode(self):
        dfsCode = DFSCode()
        for vertex in self.vertexMap.values():
            for edge in vertex.getEdgeList():
                v1, v2 = edge.v1, edge.v2
                if v1 < v2:
                    v1Label, v2Label = self.vertexMap[v1].getLabel(), self.vertexMap[v2].getLabel()
                else:
                    v1, v2 = v2, v1
                    v1Label, v2Label = self.vertexMap[v1].getLabel(), self.vertexMap[v2].getLabel()
                eLabel = edge.edgeLabel
                dfsCode.addEdge(v1, v2, v1Label, v2Label, eLabel)
        return dfsCode

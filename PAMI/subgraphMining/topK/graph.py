from .edge import Edge
from .vertex import Vertex

class Graph:
    """
    Represents a graph structure composed of vertices and edges.

    Attributes:
        EMPTY_VERTEX_LIST (list): An empty list used as a default value for vertex lists.
        EMPTY_INTEGER_ARRAY (list): An empty list used as a default value for integer arrays.

    """
    EMPTY_VERTEX_LIST = []
    EMPTY_INTEGER_ARRAY = []

    def __init__(self, iD, vMap=None, dfsCode=None):
        """
        Initializes the Graph object with optional parameters.
        """
        self.vMap = {}
        self.id = iD
        if vMap is not None:
            self.vMap = vMap
        elif dfsCode is not None:
            for ee in dfsCode.getEeList():
                v1, v2, v1Label, v2Label, eLabel = ee.getV1(), ee.getV2(), ee.getVLabel1(), ee.getVLabel2(), ee.getEdgeLabel()
                
                e = Edge(v1, v2, eLabel)
                if v1 not in self.vMap:
                    self.vMap[v1] = Vertex(v1, v1Label)
                if v2 not in self.vMap:
                    self.vMap[v2] = Vertex(v2, v2Label)

                self.vMap[v1].addEdge(e)
                self.vMap[v2].addEdge(e)

            self.id = -1

        self.vertices = []
        self.neighborCache = {}
        self.mapLabelToVertexIds = {}
        self.edgeCount = 0

        self.precalculateVertexList()
        self.precalculateVertexNeighbors()
        self.precalculateLabelsToVertices()

    def getId(self):
        """
        Retrieves the ID of the graph.
        """
        return self.id

    def removeInfrequentLabel(self, label):
        """
        Removes vertices with infrequent labels and their associated edges.
        """
        toRemove = [key for key, vertex in self.vMap.items() if vertex.getLabel() == label]
        for key in toRemove:
            del self.vMap[key]

        for vertex in self.vMap.values():
            edgesToRemove = [edge for edge in vertex.getEdgeList() 
                               if edge.v1 not in self.vMap or edge.v2 not in self.vMap]

            for edge in edgesToRemove:
                vertex.getEdgeList().remove(edge)

    def precalculateVertexNeighbors(self):
        """
        Precalculates and caches the neighbor vertices for each vertex.
        """
        self.neighborCache = {}
        self.edgeCount = 0

        for vertexId, vertex in self.vMap.items():
            neighbors = []

            for edge in vertex.getEdgeList():
                neighborVertex = self.vMap[edge.another(vertexId)]
                neighbors.append(neighborVertex)

            neighbors.sort(key=lambda x: x.id)

            self.neighborCache[vertexId] = neighbors
            self.edgeCount += len(neighbors)

        self.edgeCount //= 2    
    
    def precalculateVertexList(self):
        """
        Precalculates and caches the list of vertices.
        """
        self.vertices = []
        for _, vertex in self.vMap.items():
            self.vertices.append(vertex)

    def precalculateLabelsToVertices(self):
        """
        Precalculates and caches a mapping of labels to vertex IDs.
        """
        self.mapLabelToVertexIds = {}
        for vertex in self.vertices:
            label = vertex.getLabel()
            if label not in self.mapLabelToVertexIds:
                sameIds = [v.getId() for v in self.vertices if v.getLabel() == label]
                self.mapLabelToVertexIds[label] = sameIds

    def findAllWithLabel(self, targetLabel):
        """
        Finds all vertices with a specified label.
        """
        if targetLabel in self.mapLabelToVertexIds:
            return self.mapLabelToVertexIds[targetLabel]
        else:
            return []
        
    def getAllNeighbors(self, v):
        """
        Retrieves all neighbors of a vertex.
        """
        try:
            neighbors = self.neighborCache[v]
        except KeyError:
            neighbors = []
        return neighbors
    
    def getVLabel(self, v):
        """
        Retrieves the label of a vertex.
        """
        return self.vMap[v].getLabel()
    
    def getEdgeLabel(self, v1, v2):
        """
        Retrieves the label of an edge between two vertices.
        """
        for e in self.vMap.get(v1).getEdgeList():
            if e.v1 == v1 and e.v2 == v2:
                return e.getEdgeLabel()
            elif e.v1 == v2 and e.v2 == v1:
                return e.getEdgeLabel()
        return -1
    

    def getEdge(self, v1, v2):
        """
        Retrieves the edge between two vertices.
        """
        for e in self.vMap.get(v1).getEdgeList():
            if e.v1 == v1 and e.v2 == v2:
                return e
            elif e.v1 == v2 and e.v2 == v1:
                return e
        return None
    
    def getNonPrecalculatedAllVertices(self):
        """
        Retrieves all vertices that have not been precalculated.

        """
        return list(self.vMap.values())
    
    def isNeighboring(self, v1, v2):
        """

        Checks if two vertices are neighbors.

        """
        neighborsOfV1 = self.neighborCache.get(v1, [])
        low = 0
        high = len(neighborsOfV1) - 1

        while high >= low:
            middle = (low + high) // 2
            val = neighborsOfV1[middle].id
            if val == v2:
                return True
            if val < v2:
                low = middle + 1
            if val > v2:
                high = middle - 1
        return False

    def getAllVertices(self):
        """
        Retrieves all vertices in the graph.
        """
        return self.vertices
    
    def getEdgeCount(self):
        """
        Retrieves the total number of edges in the graph.
        """
        return self.edgeCount

# gSpan is a subgraph mining algorithm that uses DFS and DFS codes to mine subgraphs
#
# **Importing this algorithm into a python program**
#
#             from PAMI.subgraphMining.basic import gspan as alg
#
#             obj = alg.GSpan(iFile, minSupport)
#
#             obj.mine()
#
#             obj.run()
#
#             frequentGraphs = obj.getFrequentSubgraphs()
#
#             memUSS = obj.getMemoryUSS()
#
#             obj.save(oFile)
#
#             print("Total Memory in USS:", memUSS)
#
#             memRSS = obj.getMemoryRSS()
#
#             print("Total Memory in RSS", memRSS)
#
#             run = obj.getRuntime()
#
#             print("Total ExecutionTime in seconds:", run)
#


__copyright__ = """
 Copyright (C)  2021 Rage Uday Kiran

     This program is free software: you can redistribute it and/or modify
     it under the terms of the GNU General Public License as published by
     the Free Software Foundation, either version 3 of the License, or
     (at your option) any later version.

     This program is distributed in the hope that it will be useful,
     but WITHOUT ANY WARRANTY; without even the implied warranty of
     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
     GNU General Public License for more details.

     You should have received a copy of the GNU General Public License
     along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

from .edge import Edge
from .vertex import Vertex

class Graph:
    emptyVertexList = []
    emptyIntegerArray = []

    def __init__(self, iD, vMap=None, dfsCode=None):
        """
        The `__init__` function initializes a graph object with optional parameters for vertex mapping and
        DFS code.
        """
        self.vMap = {}
        self.id = iD
        if vMap is not None:
            self.vMap = vMap
        elif dfsCode is not None:
            for ee in dfsCode.getEeList():
                v1, v2, v1Label, v2Label, eLabel = ee.v1, ee.v2, ee.vLabel1, ee.vLabel2, ee.edgeLabel
                
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
        return self.id

    def removeInfrequentLabel(self, label):
        """
        The function removes vertices with a specific label from the graph and updates the edges accordingly.
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
        The function precalculates the neighbors of each vertex in a graph and stores them in a cache.
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
        The function precalculateVertexList creates a list of vertices by iterating through a dictionary of
        vertices.
        """
        self.vertices = []
        for _, vertex in self.vMap.items():
            self.vertices.append(vertex)

    def precalculateLabelsToVertices(self):
        """
        This function precalculates and stores mappings of vertex labels to their corresponding vertex IDs.
        """
        self.mapLabelToVertexIds = {}
        for vertex in self.vertices:
            label = vertex.getLabel()
            if label not in self.mapLabelToVertexIds:
                sameIds = [v.getId() for v in self.vertices if v.getLabel() == label]
                self.mapLabelToVertexIds[label] = sameIds

    def findAllWithLabel(self, targetLabel):
        if targetLabel in self.mapLabelToVertexIds:
            return self.mapLabelToVertexIds[targetLabel]
        else:
            return []
        
    def getAllNeighbors(self, v):
        try:
            neighbors = self.neighborCache[v]
        except KeyError:
            neighbors = []
        return neighbors
    
    def getVLabel(self, v):
        return self.vMap[v].getLabel()
    
    def getEdgeLabel(self, v1, v2):
        for e in self.vMap.get(v1).getEdgeList():
            if e.v1 == v1 and e.v2 == v2:
                return e.getEdgeLabel()
            elif e.v1 == v2 and e.v2 == v1:
                return e.getEdgeLabel()
        return -1

    def getEdge(self, v1, v2):
        for e in self.vMap.get(v1).getEdgeList():
            if e.v1 == v1 and e.v2 == v2:
                return e
            elif e.v1 == v2 and e.v2 == v1:
                return e
        return None
    
    def getNonPrecalculatedAllVertices(self):
        return list(self.vMap.values())
    
    def isNeighboring(self, v1, v2):
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
        return self.vertices
    
    def getEdgeCount(self):
        return self.edgeCount

#
# obj = SyntheticGraphGenerator(numOfGraphTransactions, avgNumVertices, avgNumEdges, distinctVertexlLabels, distinctEdgeLabels, 'oFile', graphFormat)
# graphFormat = 'old' or 'new', default is 'old'
#
import random
from PAMI.extras.visualize import graphs

class SyntheticGraphGenerator:
    def __init__(self, numGraphs, avgNumVertices, avgNumEdges, numVertexLabels, numEdgeLabels, outputFileName, graphFormat='old'):
        self.numGraphs = numGraphs
        self.avgNumVertices = avgNumVertices
        self.avgNumEdges = avgNumEdges
        self.numVertexLabels = numVertexLabels
        self.numEdgeLabels = numEdgeLabels
        self.outputFileName = outputFileName
        self.format = graphFormat
        self._validate()
        self.generate()

    def _validate(self):
        if self.avgNumVertices < 1:
            raise ValueError("Average number of vertices should be greater than 0")
        if self.avgNumEdges < 0:
            raise ValueError("Average number of edges should be greater than or equal to 0")
        if self.numVertexLabels < 1:
            raise ValueError("Number of labels should be greater than 0")
        if self.numEdgeLabels < 1:
            raise ValueError("Number of labels should be greater than 0")
        if self.numGraphs < 1:
            raise ValueError("Number of graphs should be greater than 0")

        if self.avgNumVertices < self.avgNumEdges:
            raise ValueError("Average number of vertices should be greater than or equal to average number of edges")

        if self.avgNumEdges > self.avgNumVertices * (self.avgNumVertices - 1) / 2:
            raise ValueError("Average number of edges should be less than or equal to n(n-1)/2")

        if self.avgNumVertices < self.numVertexLabels:
            raise ValueError("Average number of vertices should be greater than or equal to number of vertex labels")

        if self.avgNumEdges < self.numEdgeLabels:
            raise ValueError("Average number of edges should be greater than or equal to number of edge labels")

    def generate(self):
        with open(self.outputFileName, 'w') as oFile:
            for i in range(self.numGraphs):
                numVertices = random.randint(max(self.avgNumVertices-3, 1), self.avgNumVertices+3)
                numEdges = random.randint(max(self.avgNumEdges-3, 0), self.avgNumEdges+3)

                if numVertices < numEdges:
                    numVertices = numEdges + 1

                if numEdges > numVertices * (numVertices - 1) / 2:
                    numEdges = numVertices * (numVertices - 1) // 2

                if numVertices < self.numVertexLabels:
                    numVertices = self.numVertexLabels

                if numEdges < self.numEdgeLabels:
                    numEdges = self.numEdgeLabels

                graph = {'nodes': [], 'edges': []}

                # Add vertices
                for j in range(numVertices):
                    graph['nodes'].append((j, random.randint(0, self.numVertexLabels-1)))

                # Ensure connectivity by creating a spanning tree first
                connectedNodes = set()
                connectedNodes.add(0)
                while len(connectedNodes) < numVertices:
                    u = random.choice(list(connectedNodes))
                    v = random.choice([node for node in range(numVertices) if node not in connectedNodes])
                    graph['edges'].append((u, v, random.randint(0, self.numEdgeLabels-1)))
                    connectedNodes.add(v)

                # Add remaining edges randomly
                additionalEdges = numEdges - (numVertices - 1)
                for _ in range(additionalEdges):
                    while True:
                        u = random.randint(0, numVertices-1)
                        v = random.randint(0, numVertices-1)
                        if u != v and (u, v, _) not in graph['edges'] and (v, u, _) not in graph['edges']:
                            graph['edges'].append((u, v, random.randint(0, self.numEdgeLabels-1)))
                            break

                if self.format == 'new':
                    self._writeGraphToFileNewFormat(graph, oFile)
                else:
                    self._writeGraphToFile(graph, oFile, i)


    @staticmethod
    def _writeGraphToFile(graph, oFile, i):
        oFile.write(f't # {i}\n')
        for node in graph['nodes']:
            oFile.write(f"v {node[0]} {node[1]}\n")
        for edge in graph['edges']:
            oFile.write(f"e {edge[0]} {edge[1]} {edge[2]}\n")

    @staticmethod
    def _writeGraphToFileNewFormat(graph, oFile):
        node_str = ' '.join(f"{node} {label}" for node, label in sorted(graph['nodes']))
        edge_str = ' '.join(f"{u} {v} {label}" for u, v, label in graph['edges'])
        oFile.write(f"{node_str} : {edge_str}\n")

if __name__ == "__main__":
    obj = SyntheticGraphGenerator(10, 2, 1, 1, 1, 'synthetic_graphs.txt', 'old')
    vis = graphs.graphDatabase('synthetic_graphs.txt')
    vis.plot()
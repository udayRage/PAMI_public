#
#    from PAMI.extras.graph import graphTransactionsExtras as gte
#
#    gte = gte.GraphTransactionExtras("path/to/file")
#
#    graph = gte.getGraphById(graphId)
#
#    gte.plotGraphById(graphId)
#
#    allGraphs = gte.getAllGraphs()


import matplotlib.pyplot as plt
import networkx as nx
from PAMI.subgraphMining.basic import abstract as _ab


class GraphTransactionExtras:
    def __init__(self, filePath):
        """
        Initialize the GraphDatabase with the given file path.
        :param filePath: Path to the file containing graph transactions.
        """
        self.filePath = filePath
        self.graphs = self.readGraphs()

    def readGraphs(self):
        """
        Reads graph data from the specified file and constructs a list of graphs.
        :return: A list of graph objects.
        """
        graphs = []
        with open(self.filePath, 'r') as br:
            vMap = {}
            gId = None

            for line in br:
                line = line.strip()

                if line.startswith("t"):
                    if vMap:  # If vMap is not empty, it means a graph was read
                        graphs.append(_ab.Graph(gId, vMap))
                        vMap = {}  # Reset for the next graph

                    gId = int(line.split(" ")[2])

                elif line.startswith("v"):
                    items = line.split(" ")
                    vId = int(items[1])
                    vLabel = int(items[2])
                    vMap[vId] = _ab.Vertex(vId, vLabel)

                elif line.startswith("e"):
                    items = line.split(" ")
                    v1 = int(items[1])
                    v2 = int(items[2])
                    eLabel = int(items[3])
                    e = _ab.Edge(v1, v2, eLabel)
                    vMap[v1].addEdge(e)
                    vMap[v2].addEdge(e)

            if vMap:
                graphs.append(_ab.Graph(gId, vMap))

        return graphs

    def getGraphById(self, graphId):
        """
        Retrieves a specific graph by its ID.
        :param graphId: The ID of the graph to retrieve.
        :return: The graph object with the specified ID or None if not found.
        """
        for graph in self.graphs:
            if graph.getId() == graphId:
                return graph
        return None

    def getAllGraphs(self):
        """
        Retrieves all graphs in the database.
        :return: A list of all graph objects.
        """
        return self.graphs

    def plotGraphById(self, graphId):
        """
        Plots a graph by its ID using matplotlib and networkx.
        :param graphId: The ID of the graph to plot.
        """
        graph = self.getGraphById(graphId)
        if not graph:
            print(f"Graph with ID {graphId} not found.")
            return

        G = nx.Graph()

        for vertex in graph.getAllVertices():
            G.add_node(vertex.getId(), label=vertex.getLabel())
            for edge in vertex.getEdgeList():
                G.add_edge(edge.v1, edge.v2, label=edge.getEdgeLabel())

        pos = nx.spring_layout(G)  # You can use other layouts like circular_layout, shell_layout, etc.
        labels = nx.get_node_attributes(G, 'label')
        edge_labels = nx.get_edge_attributes(G, 'label')

        # Draw nodes
        nx.draw_networkx_nodes(G, pos, node_size=700, node_color='lightblue')

        # Draw edges
        nx.draw_networkx_edges(G, pos, width=2)

        # Draw node labels
        nx.draw_networkx_labels(G, pos, labels, font_size=12, font_color='black')

        # Draw edge labels
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color='red', font_size=10)

        plt.title(f"Graph ID {graphId}")
        plt.axis('off')  # Hide the axes
        plt.show()


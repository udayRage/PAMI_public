class Vertex:
    """
    Represents a vertex in a graph.

    Attributes:
        id (int): The identifier of the vertex.
        vLabel: The label associated with the vertex.
        eList (list): A list of edges connected to the vertex.

    """
    def __init__(self, iD, vLabel):
        """
        Initializes the Vertex object.
        """
        self.id = iD
        self.vLabel = vLabel
        self.eList = []  

    def addEdge(self, edge):
        """
        Adds an edge to the vertex's edge list.
        """
        self.eList.append(edge)

    def getId(self):
        """
        Retrieves the identifier of the vertex.
        """
        return self.id

    def getLabel(self):
        """
        Retrieves the label of the vertex.
        """
        return self.vLabel

    def getEdgeList(self):
        """
        Retrieves the list of edges connected to the vertex.
        """
        return self.eList

    def __eq__(self, other):
        """
        Checks if two vertices are equal based on their identifiers.
        """
        if not isinstance(other, Vertex):
            return False
        return self.id == other.id

    def __lt__(self, other):
        """
        Compares two vertices based on their identifiers for sorting purposes.
        """
        if not isinstance(other, Vertex):
            return NotImplemented
        return self.id < other.id

    def __repr__(self):
        """
        Returns a string representation of the vertex.
        """
        return f"Vertex(ID: {self.id}, Label: {self.vLabel})"
    
    def removeEdge(self, edgeToRemove):
        """
        Removes a specified edge from the vertex's edge list.
        """
        self.eList = [edge for edge in self.eList if edge != edgeToRemove]

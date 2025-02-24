# gSpan is a subgraph mining algorithm that uses DFS and DFS codes to mine subgraphs
# **Importing this algorithm into a python program**
# --------------------------------------------------------
#
#             from PAMI.subgraphMining.basic import gspan as alg
#
#             obj = alg.GSpan(iFile, minSupport)
#
#             obj.mine()
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



from PAMI.subgraphMining.basic import abstract as _ab

class GSpan(_ab._gSpan):

    eliminate_infrequent_vertices = True
    eliminate_infrequent_vertex_pairs = True
    eliminate_infrequent_edge_labels = True
    edge_count_pruning = True

    def __init__(self, iFile, minSupport, outputSingleVertices=True, maxNumberOfEdges=float('inf'), outputGraphIds=False) -> None:
        """
        Initialize variables
        """
        
        self.minSup = minSupport
        self.frequentSubgraphs = []
        self._runtime = 0
        self.maxMem = 0
        self.graphCount = 0
        self.patternCount = 0
        self.frequentVertexLabels = []
        self.infrequentVerticesRemovedCount = 0
        self.infrequentVertexPairsRemoved = 0
        self.edgeRemovedByLabel = 0
        self.eliminatedWithMaxSize = 0
        self.emptyGraphsRemoved = 0
        self.pruneByEdgeCount = 0
        self.inPath = iFile
        self.outPath = None
        self.outputSingleVertices = outputSingleVertices
        self.maxNumberOfEdges = maxNumberOfEdges
        self.outputGraphIds = outputGraphIds
        self._memoryUSS = float()
        self._memoryRSS = float()

        self.label_mapping = {}
        self.current_label = 0
        self.edge_label_mapping = {}
        self.current_edge_label = 0


    def mine(self):

        if self.maxNumberOfEdges <= 0:
            return
        
        self.frequentSubgraphs = []

        self.patternCount = 0

        # Record the start time
        t1 = _ab.time.time()

        # Read graphs
        graphDb = self.readGraphs(self.inPath)

        # Calculate minimum support as a number of graphs
        self.minSup = _ab.math.ceil(self.minSup * len(graphDb))

        # Mining
        self.gSpan(graphDb, self.outputSingleVertices)

        # Output
        # self.writeResultToFile(self.outPath)

        t2 = _ab.time.time()

        #Calculate runtime
        self._runtime = (t2 - t1)

        process = _ab._psutil.Process(_ab._os.getpid())

        self._memoryUSS = float()

        self._memoryRSS = float()

        self._memoryUSS = process.memory_full_info().uss

        self._memoryRSS = process.memory_info().rss

        self.patternCount = len(self.frequentSubgraphs)


    def save(self, oFile):
        """
        The `save` function writes information about frequent subgraphs to a specified
        output file in a specific format.
        
        :param oFile: The `save` method is used to write the results of frequent
        subgraphs to a file specified by the `outputPath` parameter. The method iterates over each
        frequent subgraph in `self.frequentSubgraphs` and writes the subgraph information to the file
        """
        reverse_label_mapping = {v: k for k, v in self.label_mapping.items()}
        reverse_edge_label_mapping = {v: k for k, v in self.edge_label_mapping.items()}

        with open(oFile, 'w') as bw:
            i = 0
            for subgraph in self.frequentSubgraphs:
                sb = []

                dfsCode = subgraph.dfsCode
                sb.append(f"t # {i} * {subgraph.support}\n")
                if dfsCode.size == 1:
                    ee = dfsCode.getEeList()[0]
                    vLabel1 = reverse_label_mapping.get(ee.vLabel1, ee.vLabel1)
                    sb.append(f"v 0 {vLabel1}\n")
                    if ee.edgeLabel != -1:
                        vLabel2 = reverse_label_mapping.get(ee.vLabel2, ee.vLabel2)
                        edgeLabel = reverse_edge_label_mapping.get(ee.edgeLabel, ee.edgeLabel)
                        sb.append(f"v 1 {vLabel2}\n")
                        sb.append(f"e 0 1 {edgeLabel}\n")
                else:
                    vLabels = [reverse_label_mapping.get(label, label) for label in dfsCode.getAllVLabels()]
                    for j, vLabel in enumerate(vLabels):
                        sb.append(f"v {j} {vLabel}\n")
                    for ee in dfsCode.getEeList():
                        edgeLabel = reverse_edge_label_mapping.get(ee.edgeLabel, ee.edgeLabel)
                        sb.append(f"e {ee.v1} {ee.v2} {edgeLabel}\n")

                if self.outputGraphIds:
                    sb.append("x " + " ".join(str(iD) for iD in subgraph.setOfGraphsIds))

                sb.append("\n\n")
                bw.write("".join(sb))
                i += 1

    def readGraphs(self, path):
        """
        The `readGraphs` function reads graph data from a file and constructs a list of graphs with vertices
        and edges.
        
        :param path: The `path` parameter in the `readGraphs` method is the file path to the text file
        containing the graph data that needs to be read and processed.
        :return: The `readGraphs` method reads graph data from a file specified by the `path` parameter. It
        parses the data to create a list of graph objects and returns this list. Each graph object contains
        information about vertices and edges within the graph.
        """
        with open(path, 'r') as br:
            graphDatabase = []
            vMap = {}
            gId = None

            for line in br:
                line = line.strip()

                if line.startswith("t"):
                    if vMap:  # If vMap is not empty, it means a graph was read
                        graphDatabase.append(_ab.Graph(gId, vMap))
                        vMap = {}  # Reset for the next graph

                    gId = int(line.split(" ")[2])

                elif line.startswith("v"):
                    items = line.split(" ")
                    vId = int(items[1])
                    # Map vertex label
                    if items[2].isdigit():
                        vLabel = int(items[2])
                    else:
                        vLabel = self.get_label(items[2])
                    vMap[vId] = _ab.Vertex(vId, vLabel)

                elif line.startswith("e"):
                    items = line.split(" ")
                    v1 = int(items[1])
                    v2 = int(items[2])
                    # Map edge label
                    if items[3].isdigit():
                        eLabel = int(items[3])
                    else:
                        eLabel = self.get_edge_label(items[3])
                    e = _ab.Edge(v1, v2, eLabel)
                    vMap[v1].addEdge(e)
                    vMap[v2].addEdge(e)

            if vMap:
                graphDatabase.append(_ab.Graph(gId, vMap))

        self.graphCount = len(graphDatabase)
        return graphDatabase

    def get_label(self, label_char):
        if label_char not in self.label_mapping:
            self.label_mapping[label_char] = self.current_label
            self.current_label += 1
        return self.label_mapping[label_char]

    def get_edge_label(self, label_char):
        if label_char not in self.edge_label_mapping:
            self.edge_label_mapping[label_char] = self.current_edge_label
            self.current_edge_label += 1
        return self.edge_label_mapping[label_char]

    def subgraphIsomorphisms(self, c: _ab.DFSCode, g: _ab.Graph):
        """
        The function `subgraphIsomorphisms` takes a DFS code and a graph as input, and finds all subgraph
        isomorphisms between the DFS code and the graph.
        
        :param c: The parameter `c` in the `subgraphIsomorphisms` function is of type `_ab.DFSCode`, which
        seems to represent a Depth-First Search code.
        :param g: The parameter `g` in the `subgraphIsomorphisms` function represents a graph object. The
        function is trying to find subgraph isomorphisms between a given DFS code `c` and the graph `g`. It
        iterates through the vertices of the graph starting with a specific
        :return: The function `subgraphIsomorphisms` returns a list of dictionaries, where each dictionary
        represents a subgraph isomorphism mapping between the input DFS code `c` and the input graph `g`.
        Each dictionary in the list maps vertex IDs from the DFS code to corresponding vertex IDs in the
        graph, indicating a valid subgraph isomorphism.
        """
        isoms = []    
        startLabel = c.getEeList()[0].getVLabel1()

        # Find all vertices in the graph that match the start label and initialize isomorphisms with them
        for vId in g.findAllWithLabel(startLabel):
            hMap = {0: vId}
            isoms.append(hMap)

        # For each edge in the DFS code, try to extend each partial isomorphism
        for ee in c.getEeList():
            v1, v2, v2Label, eLabel = ee.getV1(), ee.getV2(), ee.getVLabel2(), ee.getEdgeLabel() 
            updateIsoms = []
            # Try to extend each current isomorphism with the current edge
            for iso in isoms:
                mappedV1 = iso.get(v1)
                # Forward edge
                if v1 < v2:
                    mappedVertices = list(iso.values())
                    for mappedV2 in g.getAllNeighbors(mappedV1):
                        if (v2Label == mappedV2.getLabel() and
                            mappedV2.getId() not in mappedVertices and
                                eLabel == g.getEdgeLabel(mappedV1, mappedV2.getId())):

                            tempM = iso.copy()
                            tempM[v2] = mappedV2.getId()

                            updateIsoms.append(tempM)

                # Backward edge
                else:
                    mappedV2 = iso.get(v2)
                    # Check if the backward edge exists in the graph matching the DFS code edge
                    if g.isNeighboring(mappedV1, mappedV2) and eLabel == g.getEdgeLabel(mappedV1, mappedV2):
                        updateIsoms.append(iso)

            isoms = updateIsoms
        return isoms

    
    def rightMostPathExtensionsFromSingle(self, c: _ab.DFSCode, g: _ab.Graph):
        """
        The function `rightMostPathExtensionsFromSingle` generates extensions for a given DFS code and
        graph, focusing on the rightmost path.
        
        :param c: The parameter `c` is of type `_ab.DFSCode`, which seems to represent a Depth-First Search
        code. It is used in the `rightMostPathExtensionsFromSingle` method to perform operations related to
        DFS codes
        :param g: The parameter `g` in the provided code snippet represents a graph object. It seems to be
        an instance of a graph data structure that contains vertices and edges. The code is designed to
        find and return extensions from a given DFS code `c` based on the provided graph `g`. The function
        `
        :return: The function `rightMostPathExtensionsFromSingle` returns a dictionary `extensions`
        containing extended edges as keys and sets of graph IDs as values.
        """
        # Get the unique identifier for the given graph
        gid = g.getId()
        # Initialize a dictionary to store potential extensions
        extensions = {}

        # If the DFS code is empty, consider all edges of the graph for extension
        if c.isEmpty():
            for vertex in g.vertices:
                for e in vertex.getEdgeList():
                    # Determine the order of vertex labels to maintain consistency
                    v1Label = g.getVLabel(e.v1)
                    v2Label = g.getVLabel(e.v2)
                    if v1Label < v2Label:
                        ee1 = _ab.ExtendedEdge(0, 1, v1Label, v2Label, e.getEdgeLabel())
                    else:
                        ee1 = _ab.ExtendedEdge(0, 1, v2Label, v1Label, e.getEdgeLabel())

                    # Update the extensions dictionary with new or existing extended edges
                    setOfGraphIds = extensions.get(ee1, set())
                    setOfGraphIds.add(gid)
                    extensions[ee1] = setOfGraphIds
        else:
            # For non-empty DFS code, focus on extending from the rightmost path
            rightMost = c.getRightMost()
            isoms = self.subgraphIsomorphisms(c, g)

            # Iterate through all isomorphisms to find valid extensions
            for isom in isoms:
                invertedIsom = {v: k for k, v in isom.items()}
                mappedRm = isom[rightMost]
                mappedRmLabel = g.getVLabel(mappedRm)
                for x in g.getAllNeighbors(mappedRm):
                    invertedX = invertedIsom.get(x.getId())
                    if invertedX is not None and c.onRightMostPath(invertedX) and c.notPreOfRm(invertedX) and not c.containEdge(rightMost, invertedX):
                        ee = _ab.ExtendedEdge(rightMost, invertedX, mappedRmLabel, x.getLabel(), g.getEdgeLabel(mappedRm, x.getId()))
                        extensions.setdefault(ee, set()).add(gid)

                mappedVertices = set(isom.values())
                for v in c.getRightMostPath():
                    mappedV = isom[v]
                    mappedVLabel = g.getVLabel(mappedV)
                    for x in g.getAllNeighbors(mappedV):
                        if x.getId() not in mappedVertices:
                            ee = _ab.ExtendedEdge(v, rightMost + 1, mappedVLabel, x.getLabel(), g.getEdgeLabel(mappedV, x.getId()))
                            extensions.setdefault(ee, set()).add(gid)

        return extensions


    def rightMostPathExtensions(self, c: _ab.DFSCode, graphDb, graphIds):
        """
        The function `rightMostPathExtensions` generates extensions for a given DFS code by considering
        rightmost paths in a graph database.
        
        :param c: The parameter `c` in the `rightMostPathExtensions` method is of type `_ab.DFSCode`. It
        seems to represent a Depth-First Search code used in graph algorithms. The method is responsible
        for generating extensions based on the rightmost path in a graph
        :param graphDb: The `graphDb` parameter in the `rightMostPathExtensions` method is a
        database that stores graph data. It is used to retrieve graph objects based on
        their IDs, which are provided in the `graphIds` parameter. The method then performs operations on
        these graph objects to generate
        :param graphIds: The `graphIds` parameter in the `rightMostPathExtensions` function represents a
        list of graph identifiers. These identifiers are used to retrieve specific graphs from the
        `graphDb` database in order to perform operations on them within the function. Each ID in the
        `graphIds` list corresponds to an identifier.
        :return: The function `rightMostPathExtensions` returns a dictionary `extensions` containing
        extended edges as keys and sets of graph IDs as values.
        """
        extensions = {}
        if c.isEmpty():
            for iD in graphIds:
                g = graphDb[iD]
                # Skip graphs if pruning based on edge count is enabled and applicable
                if GSpan.edge_count_pruning and c.size >= g.getEdgeCount():
                    self.pruneByEdgeCount += 1
                    continue
                for v in g.vertices:
                    for e in v.getEdgeList():
                        # Organize the vertex labels to maintain consistent ordering
                        v1L = g.getVLabel(e.v1)
                        v2L = g.getVLabel(e.v2)
                        if v1L < v2L:
                            ee1 = _ab.ExtendedEdge(0, 1, v1L, v2L, e.getEdgeLabel())
                        else:
                            ee1 = _ab.ExtendedEdge(0, 1, v2L, v1L, e.getEdgeLabel())

                        # Add the new or existing extensions to the dictionary                       
                        setOfGraphIds = extensions.get(ee1, set())
                        setOfGraphIds.add(iD)
                        extensions[ee1] = setOfGraphIds
        else:
            # For non-empty DFS codes, extend based on the rightmost path of each graph
            rightMost = c.getRightMost()
            for iD in graphIds:
                g = graphDb[iD]
                if GSpan.edge_count_pruning and c.size >= g.getEdgeCount():
                    self.pruneByEdgeCount += 1
                    continue
                isoms = self.subgraphIsomorphisms(c, g)
                for isom in isoms:
                    invertedIsom = {}
                    for key, value in isom.items():
                        invertedIsom[value] = key
                    mappedRM = isom.get(rightMost)
                    mappedRMLabel = g.getVLabel(mappedRM)
                    for x in g.getAllNeighbors(mappedRM):
                        invertedX = invertedIsom.get(x.getId())
                        if invertedX is not None and c.onRightMostPath(invertedX) and \
                        c.notPreOfRm(invertedX) and not c.containEdge(rightMost, invertedX):
                            
                            ee = _ab.ExtendedEdge(rightMost, invertedX, mappedRMLabel, x.getLabel(),
                                            g.getEdgeLabel(mappedRM, x.getId()))

                            if ee not in extensions:
                                extensions[ee] = set()
                            extensions[ee].add(g.getId())

                    mappedVertices = isom.values()
                    for v in c.getRightMostPath():
                        mappedV = isom[v]
                        mappedVLabel = g.getVLabel(mappedV)
                        for x in g.getAllNeighbors(mappedV):
                            if x.getId() not in mappedVertices:
                                ee = _ab.ExtendedEdge(v, rightMost + 1, mappedVLabel, x.getLabel(),
                                                g.getEdgeLabel(mappedV, x.getId()))

                                if ee not in extensions:
                                    extensions[ee] = set()
                                extensions[ee].add(g.getId())
        return extensions



    def gspanDFS(self, c: _ab.DFSCode, graphDb, subgraphId):
        """
        The `gspanDFS` function recursively explores graph patterns using the gSpan algorithm to find
        frequent subgraphs in a graph database.
        
        :param c: In the provided code snippet, the parameter `c` is an instance of the `_ab.DFSCode` class.
        It is used as an input to the `gspanDFS` method for performing Depth-First Search (DFS) traversal in
        a graph mining algorithm. The `c` parameter represents
        :type c: _ab.DFSCode
        :param graphDb: The `graphDb` parameter  refers to a graph database that the algorithm is 
        operating on.
        :param subgraphId: The `subgraphId` parameter in the `gspanDFS` method refers to an
        ID represents a specific subgraph within the graph database `graphDb`. 
        :return: The `gspanDFS` method is a recursive function that is called within itself to explore the graph 
        structure and find frequent subgraphs. The function does not have a return value, but it modifies 
        the `self.frequentSubgraphs` list by appending new frequent subgraphs found during the DFS traversal.
        """

        if c.size == self.maxNumberOfEdges - 1:
            return
        extensions = self.rightMostPathExtensions(c, graphDb, subgraphId)

        for extension, newGraphIds in extensions.items():
            sup = len(newGraphIds)
            
            if sup >= self.minSup:
                newC = c.copy()
                newC.add(extension)
                
                if self.isCanonical(newC):
                    subgraph = _ab.FrequentSubgraph(newC, newGraphIds, sup)
                    self.frequentSubgraphs.append(subgraph)

                    self.gspanDFS(newC, graphDb, newGraphIds)


    def isCanonical(self, c: _ab.DFSCode):
        """
        The function `isCanonical` checks if a given DFS code is canonical by comparing it with its
        rightmost path extensions.
        
        :param c: The parameter `c` is an instance of the `_ab.DFSCode` class
        :type c: _ab.DFSCode
        :return: a boolean value. It returns True if the input DFSCode `c` is canonical, and False if it is
        not canonical.
        """
        canC = _ab.DFSCode()
        for i in range(c.size):
            extensions = self.rightMostPathExtensionsFromSingle(canC, _ab.Graph(-1, None, c))
            minEe = None
            for ee in extensions.keys():
                if minEe is None or ee.smallerThan(minEe):
                    minEe = ee

            if minEe is not None and minEe.smallerThan(c.getAt(i)):
                return False
            
            if minEe is not None:
                canC.add(minEe)
        return True
    

    def gSpan(self, graphDb, outputSingleVertices):
        """
        The gSpan function in Python processes a graph database by precalculating vertex lists, removing
        infrequent vertex pairs, and performing a depth-first search algorithm.
        
        :param graphDb: The `graphDb` parameter  refers to a graph database that the algorithm is 
        operating on.
        :param outputSingleVertices: The `outputFrequentVertices` parameter is a boolean flag that
        determines whether single vertices should be output or not.
        """
        if outputSingleVertices or GSpan.eliminate_infrequent_vertices:
            self.findAllOnlyOneVertex(graphDb, outputSingleVertices)

        for g in graphDb:
            g.precalculateVertexList()

        if GSpan.eliminate_infrequent_vertex_pairs or GSpan.eliminate_infrequent_edge_labels:
            self.removeInfrequentVertexPairs(graphDb)

        graphIds = set()
        for i, g in enumerate(graphDb):
            if g.vertices is not None and len(g.vertices) != 0:
                if self.infrequentVerticesRemovedCount > 0:
                    g.precalculateVertexList()

                graphIds.add(i)
                g.precalculateVertexNeighbors()
                g.precalculateLabelsToVertices()
            else:
                self.emptyGraphsRemoved += 1

        if len(self.frequentVertexLabels) != 0:
            self.gspanDFS(_ab.DFSCode(), graphDb, graphIds)


    class Pair:
        def __init__(self, x, y):
            if x < y:
                self.x = x
                self.y = y
            else:
                self.x = y
                self.y = x

        def __eq__(self, other):
            if isinstance(other, GSpan.Pair):
                return self.x == other.x and self.y == other.y
            return False

        def __hash__(self):
            return self.x + 100 * self.y


    def findAllOnlyOneVertex(self, graphDb, outputFrequentVertices):
        """
        The function `findAllOnlyOneVertex` iterates through a graph database to find frequent vertices
        based on a minimum support threshold, storing the results and optionally removing infrequent
        vertices.
        
        :param graphDb: The `graphDb` parameter  refers to a graph database that the algorithm is 
        operating on.
        :param outputFrequentVertices: The `outputFrequentVertices` parameter is a boolean flag that
        determines whether single vertices should be included in the output or not.
        """
        self.frequentVertexLabels = []
        labelM = {} 
        for g in graphDb:
            for v in g.getNonPrecalculatedAllVertices():
                if v.getEdgeList():
                    vLabel = v.getLabel()
                    labelM.setdefault(vLabel, set()).add(g.getId())
        # Check each label for frequency against the minimum support threshold
        for label, tempSupG in labelM.items():                
            sup = len(tempSupG)
            if sup >= self.minSup:
                self.frequentVertexLabels.append(label)
                if outputFrequentVertices:
                    tempD = _ab.DFSCode()
                    tempD.add(_ab.ExtendedEdge(0, 0, label, label, -1))
                    self.frequentSubgraphs.append(_ab.FrequentSubgraph(tempD, tempSupG, sup))
            elif GSpan.eliminate_infrequent_vertices:
                for graphId in tempSupG:
                    g = graphDb[graphId]
                    g.removeInfrequentLabel(label)
                    self.infrequentVerticesRemovedCount += 1


    def removeInfrequentVertexPairs(self, graphDb):
        """
        The function `removeInfrequentVertexPairs` processes a graph database by removing infrequent vertex
        pairs and edge labels based on specified support thresholds.
        
        :param graphDb: The `graphDb` parameter  refers to a graph database that the algorithm is 
        operating on.
        """
        alreadySeenPair = None
        matrix = None
        mapEdgeLabelToSupport = None
        alreadySeenEdgeLabel = None


        if GSpan.eliminate_infrequent_edge_labels:
            matrix = _ab.SparseTriangularMatrix()
            alreadySeenPair = set() # To avoid double counting pairs in the same graph

        if GSpan.eliminate_infrequent_edge_labels:
            mapEdgeLabelToSupport = {}
            alreadySeenEdgeLabel = set() # To avoid double counting edge labels in the same graph

        for g in graphDb:
            vertices = g.getAllVertices()

            # Check each vertex and its edges for infrequent pairs and labels
            for v1 in vertices:
                labelV1 = v1.getLabel()

                for edge in v1.getEdgeList():
                    v2 = edge.another(v1.getId())
                    labelV2 = g.getVLabel(v2)

                    # Track vertex label pairs for infrequency analysis
                    if GSpan.eliminate_infrequent_edge_labels:
                        pair = self.Pair(labelV1, labelV2)
                        if pair not in alreadySeenPair:
                            matrix.incrementCount(labelV1, labelV2)
                            alreadySeenPair.add(pair)

                    # Track edge labels for infrequency analysis
                    if GSpan.eliminate_infrequent_edge_labels:
                        edgeLabel = edge.getEdgeLabel()
                        if edgeLabel not in alreadySeenEdgeLabel:
                            alreadySeenEdgeLabel.add(edgeLabel)
                            edgeSupport = mapEdgeLabelToSupport.get(edgeLabel, 0)
                            mapEdgeLabelToSupport[edgeLabel] = edgeSupport + 1

            if GSpan.eliminate_infrequent_vertex_pairs:
                alreadySeenPair.clear()
            if GSpan.eliminate_infrequent_edge_labels:
                alreadySeenEdgeLabel.clear()

        if GSpan.eliminate_infrequent_vertex_pairs:
            matrix.removeInfrequentEntriesFromMatrix(self.minSup)

        if GSpan.eliminate_infrequent_vertex_pairs or GSpan.eliminate_infrequent_edge_labels:
            for g in graphDb:
                vertices = g.getAllVertices()

                for v1 in vertices:
                    iterEdges = iter(v1.getEdgeList())
                    for edge in iterEdges:
                        v2 = edge.another(v1.getId())
                        labelV2 = g.getVLabel(v2)
                        count = matrix.getSupportForItems(v1.getLabel(), labelV2)

                        # Remove edges based on infrequency criteria
                        if GSpan.eliminate_infrequent_vertex_pairs and count < self.minSup:
                            v1.removeEdge(edge)
                            self.infrequentVertexPairsRemoved += 1

                        elif GSpan.eliminate_infrequent_edge_labels and \
                                mapEdgeLabelToSupport.get(edge.getEdgeLabel(), 0) < self.minSup:
                            v1.removeEdge(edge)
                            self.edgeRemovedByLabel += 1
    

    def getMemoryRSS(self):
        return self._memoryRSS

    def getMemoryUSS(self):
        return self._memoryUSS

    def getRuntime(self):
        return self._runtime
    
    def getFrequentSubgraphs(self):
        sb = []  
        for i, subgraph in enumerate(self.frequentSubgraphs):  
            dfsCode = subgraph.dfsCode
            subgraphDescription = [f"t # {i} * {subgraph.support}"]  
            
            if dfsCode.size == 1:
                ee = dfsCode.getEeList()[0]
                subgraphDescription.append(f"v 0 {ee.vLabel1}")
                if ee.edgeLabel != -1:
                    subgraphDescription.append(f"v 1 {ee.vLabel2}")
                    subgraphDescription.append(f"e 0 1 {ee.edgeLabel}")
            else:
                vLabels = dfsCode.getAllVLabels()
                for j, vLabel in enumerate(vLabels):
                    subgraphDescription.append(f"v {j} {vLabel}")
                for ee in dfsCode.getEeList():
                    subgraphDescription.append(f"e {ee.v1} {ee.v2} {ee.edgeLabel}")
            
            sb.append('\n'.join(subgraphDescription))  
        return '\n'.join(sb)  

    def getSubgraphGraphMapping(self):
        """
        Return a list of mappings from subgraphs to the graph IDs they belong to in the format <FID, Clabel, GIDs[]>.
        """
        mappings = []
        for i, subgraph in enumerate(self.frequentSubgraphs):
            mapping = {
                "FID": i,
                "Clabel": str(subgraph.dfsCode),
                "GIDs": list(subgraph.setOfGraphsIds)
            }
            mappings.append(mapping)
        return mappings

    def saveSubgraphsByGraphId(self, oFile):
        """
        Save subgraphs by graph ID as a flat transaction, such that each row represents the graph ID and each row can contain multiple subgraph IDs.
        """
        graphToSubgraphs = {}
        
        for i, subgraph in enumerate(self.frequentSubgraphs):
            for graphId in subgraph.setOfGraphsIds:
                if graphId not in graphToSubgraphs:
                    graphToSubgraphs[graphId] = []
                graphToSubgraphs[graphId].append(i)

        graphToSubgraphs = {k: graphToSubgraphs[k] for k in sorted(graphToSubgraphs)}

        with open(oFile, 'w') as f:
            for _, subgraphIds in graphToSubgraphs.items():
                f.write(f"{' '.join(map(str, subgraphIds))}\n")


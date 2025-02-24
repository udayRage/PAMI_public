# from PAMI.subgraphMining.topK import tkg as alg

# obj = alg.TKG(iFile, k)

# obj.mine()

# frequentGraphs = obj.getKSubgraphs()

# memUSS = obj.getMemoryUSS()

# obj.save(oFile)

# print("Total Memory in USS:", memUSS)

# memRSS = obj.getMemoryRSS()

# print("Total Memory in RSS", memRSS)

# run = obj.getRuntime()

# print("Total ExecutionTime in seconds:", run)

# minSup = obj.getMinSupport()

# print("Minimum support:", minSup)


from PAMI.subgraphMining.topK import abstract as _ab


class TKG(_ab._TKG):
    ELIMINATE_INFREQUENT_VERTICES = True
    ELIMINATE_INFREQUENT_VERTEX_PAIRS = True
    ELIMINATE_INFREQUENT_EDGE_LABELS = True
    EDGE_COUNT_PRUNING = True
    DYNAMIC_SEARCH = True
    THREADED_DYNAMIC_SEARCH = True

    def __init__(self, iFile, k, maxNumberOfEdges=float('inf'), outputSingleVertices=True, outputGraphIds=False):
        self._memoryRSS = None
        self._memoryUSS = None
        self.runtime = None
        self.minSup = None
        self.candidates = None
        self.kSubgraphs = None
        self.iFile = iFile
        self.k = k
        self.outputGraphIds = outputGraphIds
        self.outputSingleVertices = outputSingleVertices
        self.maxNumberOfEdges = maxNumberOfEdges
        self.graphCount = 0
        self.patternCount = 0
        self.frequentVertexLabels = []
        self.infrequentVerticesRemovedCount = 0
        self.infrequentVertexPairsRemovedCount = 0
        self.skipStrategyCount = 0
        self.threadCount = 1
        self.edgeRemovedByLabel = 0
        self.eliminatedWithMaxSize = 0
        self.emptyGraphsRemoved = 0
        self.pruneByEdgeCount = 0
        self.label_mapping = {}
        self.reverse_label_mapping = {}
        self.current_label = 0

    def mine(self):
        """
        This Python function starts a mining process on a graph database, calculates runtime, pattern count,
        and memory usage metrics.
        """
        if self.maxNumberOfEdges <= 0:
            return

        self.kSubgraphs = _ab.PriorityQueue()
        self.candidates = _ab.PriorityQueue()
        
        self.runtime = 0

        t1 = _ab.time.time()
        graphDb = self.readGraphs(self.iFile)
        self.minSup = 1

        self.gSpan(graphDb, self.outputSingleVertices)

        t2 = _ab.time.time()
        self.runtime = t2 - t1
        self.patternCount = self.getQueueSize(self.kSubgraphs)

        process = _ab._psutil.Process(_ab._os.getpid())

        self._memoryUSS = float()

        self._memoryRSS = float()

        self._memoryUSS = process.memory_full_info().uss

        self._memoryRSS = process.memory_info().rss



    def readGraphs(self, path):
        """
        Reads graph data from a file and constructs a list of graphs with vertices and edges.
        Handles character vertex labels by mapping them to unique integers.
        Edge labels are assumed to be integers.
        """
        with open(path, 'r') as br:
            graphDatabase = []
            vMap = {}
            gId = None

            for line in br:
                line = line.strip()
                if line.startswith("t"):
                    if vMap:
                        graphDatabase.append(_ab.Graph(gId, vMap))
                        vMap = {}
                    gId = int(line.split()[2])
                elif line.startswith("v"):
                    items = line.split()
                    vId = int(items[1])
                    label = items[2]
                    # Map vertex label if it's a string, else convert to integer
                    if label.isdigit():
                        vLabel = int(label)
                    else:
                        vLabel = self.get_label(label)
                    vMap[vId] = _ab.Vertex(vId, vLabel)
                elif line.startswith("e"):
                    items = line.split()
                    v1 = int(items[1])
                    v2 = int(items[2])
                    eLabel = int(items[3])  # Assuming edge labels are integers
                    edge = _ab.Edge(v1, v2, eLabel)
                    vMap[v1].addEdge(edge)
                    vMap[v2].addEdge(edge)

            if vMap:
                graphDatabase.append(_ab.Graph(gId, vMap))

        self.graphCount = len(graphDatabase)
        return graphDatabase


    def get_label(self, label_char):
        """
        Maps a character vertex label to a unique integer.
        If the label is already mapped, returns the existing integer.
        Otherwise, assigns a new integer to the label.
        """
        if label_char not in self.label_mapping:
            self.label_mapping[label_char] = self.current_label
            self.reverse_label_mapping[self.current_label] = label_char
            self.current_label += 1
        return self.label_mapping[label_char]

    def save(self, oFile):
        """
        Saves the frequent subgraphs to an output file.
        Converts integer vertex labels back to their original characters.
        """
        subgraphsList = self.getSubgraphsList()

        with open(oFile, 'w') as bw:
            for i, subgraph in enumerate(subgraphsList):
                sb = []
                dfsCode = subgraph.dfsCode

                sb.append(f"t # {i} * {subgraph.support}\n")
                if len(dfsCode.eeList) == 1:
                    ee = dfsCode.eeList[0]
                    # Convert labels back to characters if mapped
                    vLabel1 = self.reverse_label_mapping.get(ee.vLabel1, ee.vLabel1)
                    sb.append(f"v 0 {vLabel1}\n")
                    if ee.edgeLabel != -1:
                        vLabel2 = self.reverse_label_mapping.get(ee.vLabel2, ee.vLabel2)
                        sb.append(f"v 1 {vLabel2}\n")
                        sb.append(f"e 0 1 {ee.edgeLabel}\n")
                else:
                    vLabels = dfsCode.getAllVLabels()
                    for j, vLabel in enumerate(vLabels):
                        # Convert labels back to characters if mapped
                        vLabel = self.reverse_label_mapping.get(vLabel, vLabel)
                        sb.append(f"v {j} {vLabel}\n")
                    for ee in dfsCode.eeList:
                        sb.append(f"e {ee.v1} {ee.v2} {ee.edgeLabel}\n")

                # Include graph IDs if the feature is enabled
                if self.outputGraphIds and subgraph.setOfGraphsIds:
                    sb.append("x " + " ".join(str(iD) for iD in subgraph.setOfGraphsIds))

                sb.append("\n\n")
                bw.write("".join(sb))

    def savePattern(self, subgraph):
        # previousMinSup = self.minSup

        self.kSubgraphs.put(subgraph)
        if self.kSubgraphs.qsize() > self.k:
            while self.kSubgraphs.qsize() > self.k:
                lower = self.kSubgraphs.get()

                if lower.support > self.minSup:
                    self.minSup = lower.support


    def getQueueSize(self, queue):
        size = 0
        tempQueue = _ab.PriorityQueue()
        
        while not queue.empty():
            item = queue.get()
            tempQueue.put(item)
            size += 1
        
        while not tempQueue.empty():
            queue.put(tempQueue.get())
        
        return size

    def subgraphIsomorphisms(self, c, g):
        isoms = []
        startLabel = c.getEeList()[0].vLabel1
        for vId in g.findAllWithLabel(startLabel):
            isoms.append({0: vId})
        
        for ee in c.getEeList():
            v1, v2, v2Label, eLabel = ee.v1, ee.v2, ee.vLabel2, ee.edgeLabel
            updateIsoms = []
            for iso in isoms:
                mappedV1 = iso[v1]
                if v1 < v2:
                    mappedVertices = set(iso.values())
                    for mappedV2 in g.getAllNeighbors(mappedV1):
                        if v2Label == mappedV2.getLabel() and mappedV2.getId() not in mappedVertices and eLabel == g.getEdgeLabel(mappedV1, mappedV2.getId()):
                            tempIso = iso.copy()
                            tempIso[v2] = mappedV2.getId()
                            updateIsoms.append(tempIso)
                else:
                    mappedV2 = iso[v2]
                    if g.isNeighboring(mappedV1, mappedV2) and eLabel == g.getEdgeLabel(mappedV1, mappedV2):
                        updateIsoms.append(iso)
            isoms = updateIsoms
        return isoms



    def rightMostPathExtensionsFromSingle(self, c, g):
        gid = g.getId()
        extensions = {}
    
        if c.isEmpty():
            for vertex in g.vertices:
                for e in vertex.getEdgeList():
                    v1Label = g.getVLabel(e.v1)
                    v2Label = g.getVLabel(e.v2)
                    if v1Label < v2Label:
                        ee1 = _ab.ExtendedEdge(0, 1, v1Label, v2Label, e.getEdgeLabel())
                    else:
                        ee1 = _ab.ExtendedEdge(0, 1, v2Label, v1Label, e.getEdgeLabel())
                    extensions.setdefault(ee1, set()).add(gid)
        else:
            rightMost = c.getRightMost()
            isoms = self.subgraphIsomorphisms(c, g)
            for iso in isoms:
                invertedIsom = {v: k for k, v in iso.items()}
                mappedRm = iso[rightMost]
                mappedRmLabel = g.getVLabel(mappedRm)
                for x in g.getAllNeighbors(mappedRm):
                    invertedX = invertedIsom.get(x.getId())
                    if invertedX is not None and c.onRightMostPath(invertedX) and not c.containEdge(rightMost, invertedX):
                        ee = _ab.ExtendedEdge(rightMost, invertedX, mappedRmLabel, x.getLabel(), g.getEdgeLabel(mappedRm, x.getId()))
                        extensions.setdefault(ee, set()).add(gid)
                mappedVertices = set(iso.values())
                for v in c.getRightMostPath():
                    mappedV = iso[v]
                    mappedVLabel = g.getVLabel(mappedV)
                    for x in g.getAllNeighbors(mappedV):
                        if x.getId() not in mappedVertices:
                            ee = _ab.ExtendedEdge(v, rightMost + 1, mappedVLabel, x.getLabel(), g.getEdgeLabel(mappedV, x.getId()))
                            extensions.setdefault(ee, set()).add(gid)
        return extensions

    def rightMostPathExtensions(self, c, graphDB, graphIds):
        extensions = {}
    
        if c.isEmpty():
            for graphId in graphIds:
                g = graphDB[graphId]
                if self.EDGE_COUNT_PRUNING and c.size >= g.getEdgeCount():
                    self.pruneByEdgeCount += 1
                    continue
                for vertex in g.vertices:
                    for e in vertex.getEdgeList():
                        v1Label = g.getVLabel(e.v1)
                        v2Label = g.getVLabel(e.v2)
                        if v1Label < v2Label:
                            ee1 = _ab.ExtendedEdge(0, 1, v1Label, v2Label, e.getEdgeLabel())
                        else:
                            ee1 = _ab.ExtendedEdge(0, 1, v2Label, v1Label, e.getEdgeLabel())
                        extensions.setdefault(ee1, set()).add(graphId)
        else:
            rightMost = c.getRightMost()
            for graphId in graphIds:
                g = graphDB[graphId]
                if self.EDGE_COUNT_PRUNING and c.size >= g.getEdgeCount():
                    self.pruneByEdgeCount += 1
                    continue
                isoms = self.subgraphIsomorphisms(c, g)
                for isom in isoms:
                    invertedIsom = {v: k for k, v in isom.items()}
                    mappedRm = isom[rightMost]
                    mappedRmLabel = g.getVLabel(mappedRm)
                    for x in g.getAllNeighbors(mappedRm):
                        invertedX = invertedIsom.get(x.getId())
                        if invertedX is not None and c.onRightMostPath(invertedX) and not c.containEdge(rightMost, invertedX):
                            ee = _ab.ExtendedEdge(rightMost, invertedX, mappedRmLabel, x.getLabel(), g.getEdgeLabel(mappedRm, x.getId()))
                            extensions.setdefault(ee, set()).add(g.getId())
                    mappedVertices = set(isom.values())
                    for v in c.getRightMostPath():
                        mappedV = isom[v]
                        mappedVLabel = g.getVLabel(mappedV)
                        for x in g.getAllNeighbors(mappedV):
                            if x.getId() not in mappedVertices:
                                ee = _ab.ExtendedEdge(v, rightMost + 1, mappedVLabel, x.getLabel(), g.getEdgeLabel(mappedV, x.getId()))
                                extensions.setdefault(ee, set()).add(g.getId())
        return extensions



    def gSpan(self, graphDB, outputFrequentVertices):
        if outputFrequentVertices or self.ELIMINATE_INFREQUENT_VERTICES:
            self.findAllOnlyOneVertex(graphDB, outputFrequentVertices)
        
        for g in graphDB:
            g.precalculateVertexList()
    
        if self.ELIMINATE_INFREQUENT_VERTEX_PAIRS or self.ELIMINATE_INFREQUENT_EDGE_LABELS:
            self.removeInfrequentVertexPairs(graphDB)
    
        graphIds = set()
        for i, g in enumerate(graphDB):
            if g.vertices and len(g.vertices) != 0:
                if self.infrequentVerticesRemovedCount > 0:
                    g.precalculateVertexList()
    
                graphIds.add(i)
                g.precalculateVertexNeighbors()
                g.precalculateLabelsToVertices()
            else:
                self.emptyGraphsRemoved += 1
    
        if not outputFrequentVertices or self.frequentVertexLabels:
            if self.DYNAMIC_SEARCH:
                self.gspanDynamicDFS(_ab.DfsCode(), graphDB, graphIds)
                
                if self.THREADED_DYNAMIC_SEARCH:
                    self.startThreads(graphDB, self.candidates, self.minSup)

                else:
                    while self.candidates:
                        candidate = self.candidates.pop()
                        if len(candidate.setOfGraphsIds) < self.minSup:
                            continue
                        self.gspanDynamicDFS(candidate.dfsCode, graphDB, candidate.setOfGraphsIds)
            else:
                self.gspanDfs(_ab.DfsCode(), graphDB, graphIds)

    def startThreads(self, graphDB, candidates, minSup):
        threads = []
        for _ in range(self.threadCount):
            thread = _ab.DfsThread(graphDB, candidates, minSup, self)
            thread.start()
            threads.append(thread)
    
        for thread in threads:
            thread.join()

    def gspanDfs(self, c: _ab.DfsCode, graphDB, subgraphId):
        if c.size == self.maxNumberOfEdges - 1:
            return
        extensions = self.rightMostPathExtensions(c, graphDB, subgraphId)
        for extension, newGraphIds in extensions.items():
            sup = len(newGraphIds)
            if sup >= self.minSup:
                newC = c.copy()
                newC.add(extension)
    
                if self.isCanonical(newC):
                    self.savePattern(_ab.FrequentSubgraph(newC, newGraphIds, sup))
                    self.gspanDfs(newC, graphDB, newGraphIds)

    
    def gspanDynamicDFS(self, c, graphDB, graphIds):
        if c.size == self.maxNumberOfEdges - 1:
            return

        extensions = self.rightMostPathExtensions(c, graphDB, graphIds)
        for extension, newGraphIds in extensions.items():
            support = len(newGraphIds)

            if support >= self.minSup:
                newC = c.copy()
                newC.add(extension)
                if self.isCanonical(newC):
                    subgraph = _ab.FrequentSubgraph(newC, newGraphIds, support)
                    self.savePattern(subgraph)
                    self.registerAsCandidate(subgraph)
    
    def registerAsCandidate(self, subgraph):
        self.candidates.put((-subgraph.support, subgraph))

    
    def isCanonical(self, c: _ab.DfsCode):
        canC = _ab.DfsCode()
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


    class Pair:
        def __init__(self, x, y):
            if x < y:
                self.x = x
                self.y = y
            else:
                self.x = y
                self.y = x

        def __eq__(self, other):
            if isinstance(other, TKG.Pair):
                return self.x == other.x and self.y == other.y
            return False

        def __hash__(self):
            return self.x + 100 * self.y


    def findAllOnlyOneVertex(self, graphDB, outputFrequentVertices):
        self.frequentVertexLabels = []
        labelM = {} 
        for g in graphDB:
            for v in g.getNonPrecalculatedAllVertices():
                if v.getEdgeList():
                    vLabel = v.getLabel()
                    labelM.setdefault(vLabel, set()).add(g.getId())
        for label, tempSupG in labelM.items():                
            sup = len(tempSupG)
            if sup >= self.minSup:
                self.frequentVertexLabels.append(label)
                if outputFrequentVertices:
                    tempD = _ab.DfsCode()
                    tempD.add(_ab.ExtendedEdge(0, 0, label, label, -1))
                    self.savePattern(_ab.FrequentSubgraph(tempD, tempSupG, sup))
            elif TKG.ELIMINATE_INFREQUENT_VERTICES:
                for graphId in tempSupG:
                    g = graphDB[graphId]
                    g.removeInfrequentLabel(label)
                    self.infrequentVerticesRemovedCount += 1

    def removeInfrequentVertexPairs(self, graphDB):

        alreadySeenPair = None
        matrix = None
        mapEdgeLabelToSupport = None
        alreadySeenEdgeLabel = None

        if TKG.ELIMINATE_INFREQUENT_EDGE_LABELS:
            matrix = _ab.SparseTriangularMatrix()
            alreadySeenPair = set()

        if TKG.ELIMINATE_INFREQUENT_EDGE_LABELS:
            mapEdgeLabelToSupport = {}
            alreadySeenEdgeLabel = set()

        for g in graphDB:
            vertices = g.getAllVertices()

            for v1 in vertices:
                labelV1 = v1.getLabel()

                for edge in v1.getEdgeList():
                    v2 = edge.another(v1.getId())
                    labelV2 = g.getVLabel(v2)

                    if TKG.ELIMINATE_INFREQUENT_EDGE_LABELS:
                        pair = self.Pair(labelV1, labelV2)
                        if pair not in alreadySeenPair:
                            matrix.incrementCount(labelV1, labelV2)
                            alreadySeenPair.add(pair)

                    if TKG.ELIMINATE_INFREQUENT_EDGE_LABELS:
                        edgeLabel = edge.getEdgeLabel()
                        if edgeLabel not in alreadySeenEdgeLabel:
                            alreadySeenEdgeLabel.add(edgeLabel)
                            edgeSupport = mapEdgeLabelToSupport.get(edgeLabel, 0)
                            mapEdgeLabelToSupport[edgeLabel] = edgeSupport + 1

            if TKG.ELIMINATE_INFREQUENT_VERTEX_PAIRS:
                alreadySeenPair.clear()
            if TKG.ELIMINATE_INFREQUENT_EDGE_LABELS:
                alreadySeenEdgeLabel.clear()

        if TKG.ELIMINATE_INFREQUENT_VERTEX_PAIRS:
            matrix.removeInfrequentEntriesFromMatrix(self.minSup)

        if TKG.ELIMINATE_INFREQUENT_VERTEX_PAIRS or TKG.ELIMINATE_INFREQUENT_EDGE_LABELS:
            for g in graphDB:
                vertices = g.getAllVertices()

                for v1 in vertices:
                    iterEdges = iter(v1.getEdgeList())
                    for edge in iterEdges:
                        v2 = edge.another(v1.getId())
                        labelV2 = g.getVLabel(v2)
                        count = matrix.getSupportForItems(v1.getLabel(), labelV2)

                        if TKG.ELIMINATE_INFREQUENT_VERTEX_PAIRS and count < self.minSup:
                            v1.removeEdge(edge)
                            self.infrequentVertexPairsRemovedCount += 1

                        elif TKG.ELIMINATE_INFREQUENT_EDGE_LABELS and \
                                mapEdgeLabelToSupport.get(edge.getEdgeLabel(), 0) < self.minSup:
                            v1.removeEdge(edge)
                            self.edgeRemovedByLabel += 1

    def getMemoryRSS(self):
        return self._memoryRSS

    def getMemoryUSS(self):
        return self._memoryUSS

    def getRuntime(self):
        return self.runtime
    
    def getMinSupport(self):
        return self.minSup
    
    def getKSubgraphs(self):
        """ Return the formatted subgraphs as a single string with correct formatting and newlines. """
        subgraphsList = self.getSubgraphsList()  
        sb = [] 
        for i, subgraph in enumerate(subgraphsList):
            subgraphDescription = [f"t # {i} * {subgraph.support}"]  
            dfsCode = subgraph.dfsCode
            if len(dfsCode.eeList) == 1:
                ee = dfsCode.eeList[0]
                subgraphDescription.append(f"v 0 {ee.vLabel1}")
                if ee.edgeLabel != -1:
                    subgraphDescription.append(f"v 1 {ee.vLabel2}")
                    subgraphDescription.append(f"e 0 1 {ee.edgeLabel}")
            else:
                vLabels = dfsCode.getAllVLabels()
                for j, vLabel in enumerate(vLabels):
                    subgraphDescription.append(f"v {j} {vLabel}")
                for ee in dfsCode.eeList:
                    subgraphDescription.append(f"e {ee.v1} {ee.v2} {ee.edgeLabel}")

            # Include graph IDs if the feature is enabled
            if self.outputGraphIds and subgraph.setOfGraphsIds:
                subgraphDescription.append("x " + " ".join(str(ID) for ID in subgraph.setOfGraphsIds))
            sb.append('\n'.join(subgraphDescription)) 
        return '\n\n'.join(sb)  



    def getSubgraphsList(self):
        """Creates a copy of the queue's contents without emptying the original queue."""
        subgraphsList = list(self.kSubgraphs.queue)
        subgraphsList.sort(key=lambda sg: sg.support, reverse=True)
        return subgraphsList


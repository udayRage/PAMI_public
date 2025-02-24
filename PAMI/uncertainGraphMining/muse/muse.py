

from PAMI.uncertainGraphMining.muse import abstract as _ab
class Muse(_ab._MUSE):
    def __init__(self, file_path):
        self.graphCount = None
        self.graphDatabase = self.readGraph(file_path)
        self.F = set()


    def readGraph(self, path):
        with open(path, 'r') as f:
            graphDatabase = []
            vMap = {}
            gId = None

            for line in f:
                line = line.strip()

                if line.startswith("t"):
                    if vMap:  # If vMap is not empty, it means a graph was read
                        graphDatabase.append(_ab.UncertainGraph(gId, vMap))
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
                    eProb = float(items[4])
                    e = _ab.Edge(v1, v2, eLabel, eProb)
                    vMap[v1].addEdge(e)
                    vMap[v2].addEdge(e)

            if vMap:
                graphDatabase.append(_ab.UncertainGraph(gId, vMap))

        self.graphCount = len(graphDatabase)
        return graphDatabase

    def _generateImplicatedGraphs(self):
        implicatedGraphs = []
        for uncertainGraph in self.graphDatabase:
            vMap = uncertainGraph.getVertexMap()
            edges = [(e.v1, e.v2, e.edgeLabel, e.existenceProbability) for v in vMap.values() for e in v.getEdgeList()]
            edges = list(set(edges))  # Remove duplicates

            breakpoint()
            edgeCombinations = list(_ab.itertools.product([0, 1], repeat=len(edges)))

            for combination in edgeCombinations:
                implicatedGraph = {
                    "uncertain_graph_id": uncertainGraph.id,
                    "vertices": {vId: vertex.getLabel() for vId, vertex in vMap.items()},
                    "edges": [],
                    "implication_probability": 1
                }

                implicationProbability = 1
                for i, include_edge in enumerate(combination):
                    v1, v2, eLabel, eProb = edges[i]
                    if include_edge:
                        implicatedGraph["edges"].append((v1, v2, eLabel))
                        implicationProbability *= eProb
                    else:
                        implicationProbability *= (1 - eProb)

                implicatedGraph["implication_probability"] = implicationProbability
                implicatedGraphs.append(implicatedGraph)

        return implicatedGraphs

    def _generateImplicatedDatabase(self):
        allImplicatedGraphs = [self._generateImplicatedGraphs() for _ in self.graphDatabase]

        # Combine implicated graphs across all uncertain graphs using Cartesian product
        implicatedDatabase = {}
        counter = 0

        breakpoint()
        for combination in _ab.itertools.product(*allImplicatedGraphs):
            combinedGraph = {
                "vertices": {},
                "edges": [],
                "implication_probability": 1,
                "component_implicated_graphs": []
            }

            for graph in combination:
                combinedGraph["vertices"].update(graph["vertices"])
                combinedGraph["edges"].extend(graph["edges"])
                combinedGraph["implication_probability"] *= graph["implication_probability"]
                combinedGraph["component_implicated_graphs"].append(graph["uncertain_graph_id"])

            if all(combinedGraph["component_implicated_graphs"][i] < combinedGraph["component_implicated_graphs"][
                i + 1] for i in range(len(combinedGraph["component_implicated_graphs"]) - 1)):
                implicatedDatabase[f'X{counter}'] = combinedGraph
                counter += 1

        return implicatedDatabase

    def _sampleGraph(self, uncertainGraph):
        sampledGraph = _ab.deepcopy(uncertainGraph)
        for vertex in sampledGraph.getVertexMap().values():
            edgesToRemove = []
            for edge in vertex.getEdgeList():
                if _ab.random.random() > edge.existenceProbability:
                    edgesToRemove.append(edge)
            for edge in edgesToRemove:
                vertex.edges.remove(edge)
        return sampledGraph

    def _checkSubgraph(self, graph, subgraph):
        """ Check if subgraph is present in graph using DFS Code for subgraph isomorphism check """
        subgraphCode = _ab.DFSCode()
        subgraphCode.buildCode(subgraph)
        graphCode = _ab.DFSCode()
        graphCode.buildCode(graph)

        return subgraphCode.isSubcodeOf(graphCode)

    def _constructDnfFormula(self, embeddings):
        """ Construct the DNF formula from embeddings """
        dnfFormula = []
        for embedding in embeddings:
            prob = 1
            for edge in embedding.getEdgeList():
                prob *= edge.getExistenceProbability()
            dnfFormula.append(prob)
        return dnfFormula

    def estimateProbability(self, dnfFormula, epsilon, delta, n, minsup):
        """ Estimate the probability using FPRAS """
        epsilonPrime = epsilon * minsup / 2
        N = _ab.math.ceil((4 * n * _ab.math.log(2 / delta)) / (epsilonPrime ** 2))
        Z = sum(dnfFormula)
        X = Y = 0

        for _ in range(N):
            i = _ab.random.randint(0, n - 1)
            Ci = dnfFormula[i]
            Y += Ci
            if all(_ab.random.random() > dnfFormula[j] for j in range(n) if j != i):
                X += Ci

        pHat = (X * Z) / Y if Y > 0 else 0
        return max(0, pHat - epsilonPrime), min(1, pHat + epsilonPrime)

    def _approxOccProb(self, uncertainGraph, subgraph, epsilon, delta, minsup):
        embeddings = []
        for node in uncertainGraph.getVertexMap().values():
            if self._checkSubgraph(uncertainGraph.getVertexMap(), subgraph):
                embeddings.append(node)  # Collect embeddings as Vertex objects

        n = len(embeddings)
        if n == 0:
            return 0, 0

        dnfFormula = self._constructDnfFormula(embeddings)
        return self.estimateProbability(dnfFormula, epsilon, delta, n, minsup)

    def _computeProbabilityFromDnf(self, dnfFormula):
        """ Compute the probability of the DNF formula being true """
        return sum(dnfFormula) / len(dnfFormula) if dnfFormula else 0

    def _approxExpSup(self, subgraph, database, minsup, epsilon, delta):
        l = u = 0
        for Gi in database:
            Xi = [vertex for vertex in Gi.getVertexMap().values() if
                  self._checkSubgraph(Gi.getVertexMap(), subgraph)]
            if len(Xi) > 0 and 2 * len(Xi) - 5 / len(Xi) >= _ab.math.log(2 / delta) / (epsilon * minsup) ** 2:
                alpha, beta = self._approxOccProb(Gi, subgraph, epsilon, delta, minsup)
            else:
                dnfFormula = self._constructDnfFormula(Xi)
                alpha = beta = self._computeProbabilityFromDnf(dnfFormula)
            l += alpha
            u += beta
        n = len(database)
        return l / n, u / n

    def _generateInitialPatterns(self):
        patterns = set()
        for graph in self.graphDatabase:
            vertex_map = graph.getVertexMap()
            for vertex in vertex_map.values():
                for edge in vertex.getEdgeList():
                    pattern = {
                        vertex.getId(): vertex,
                        edge.v2: _ab.Vertex(edge.v2, vertex_map[edge.v2].getLabel())  # Access the label from vertex_map
                    }
                    patterns.add(frozenset(pattern.items()))
        return patterns

    def _generateSuperpatterns(self, pattern):
        superpatterns = set()
        for graph in self.graphDatabase:
            for vertex in graph.getVertexMap().values():
                for edge in vertex.getEdgeList():
                    if (vertex.id, vertex.getLabel()) in pattern:
                        new_pattern = dict(pattern)
                        if edge not in new_pattern[(vertex.id, vertex.getLabel())]:
                            new_pattern[(vertex.id, vertex.getLabel())].append(edge)
                            superpatterns.add(frozenset(new_pattern.items()))
        return superpatterns

    def mine(self, minsup, epsilon, delta):
        T = self._generateInitialPatterns()
        while T:
            S = T.pop()
            S_dict = dict(S)
            embeddings = []
            for Gi in self.graphDatabase:
                if self._checkSubgraph(Gi.getVertexMap(), S_dict):
                    embeddings.append(S_dict)
            l, u = self._approxExpSup(S_dict, self.graphDatabase, minsup, epsilon, delta)
            if l >= (1 - epsilon) * minsup and u >= minsup:
                self.F.add(S)
                superpatterns = self._generateSuperpatterns(S)
                for sp in superpatterns:
                    T.add(sp)

        return self.F

    def parseFrozenset(self, fset):
        vertices = {}
        edges = []

        edge_list = list(fset)
        for eid, vertex in edge_list:
            if vertex.id not in vertices:
                vertices[vertex.id] = vertex.vLabel
            if len(edge_list) > 1:
                for other_eid, other_vertex in edge_list:
                    if other_vertex.id != vertex.id:
                        edges.append((vertex.id, other_vertex.id))

        return vertices, edges
    def save(self, oFile):
        with open(oFile, 'w') as f:
            for tid, fset in enumerate(self.F):
                f.write(f"t # {tid}\n")
                vertices, edges = self.parseFrozenset(fset)
                for vid, label in vertices.items():
                    f.write(f"v {vid} {label}\n")

                for edge in edges:
                    f.write(f"e {edge[0]} {edge[1]}\n")



if __name__ == '__main__':
    muse = Muse('largerDataset')
    epsilon = 0.1
    delta = 0.05
    minsup = 0.3

    frequentPatterns = muse.mine(minsup, epsilon, delta)
    # print(f"Frequent subgraph patterns: {frequentPatterns}")
    for pattern in frequentPatterns:
        print(pattern)
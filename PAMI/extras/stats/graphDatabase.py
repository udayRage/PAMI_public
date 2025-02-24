import networkx as nx
import matplotlib.pyplot as plt

class graphDatabase:


    def __init__(self, iFile):
        self.graphs = []
        current_graph = {'vertices': [], 'edges': []}
        self.edges_per_graph = None
        self.nodes_per_graph = None

        with open(iFile, 'r') as file:
            for line in file:
                if line.startswith('t #'):
                    if current_graph['vertices'] or current_graph['edges']:
                        self.graphs.append(current_graph)
                        current_graph = {'vertices': [], 'edges': []}
                elif line.startswith('v'):
                    _, v_id, label = line.split()
                    current_graph['vertices'].append((int(v_id), int(label)))
                elif line.startswith('e'):
                    _, v1, v2, label = line.split()
                    current_graph['edges'].append((int(v1), int(v2), int(label)))

        if current_graph['vertices'] or current_graph['edges']:
            self.graphs.append(current_graph)

    def printIndividualGraphStats(self):
        for i, graph in enumerate(self.graphs):
            print(f"Graph {i}:")
            num_vertices = len(graph['vertices'])
            num_edges = len(graph['edges'])
            vertex_labels = set(label for _, label in graph['vertices'])
            edge_labels = set(label for _, _, label in graph['edges'])

            print(f"  Number of vertices: {num_vertices}")
            print(f"  Number of edges: {num_edges}")
            print(f"  Unique vertex labels: {vertex_labels}")
            print(f"  Unique edge labels: {edge_labels}")

    def printGraphDatabaseStatistics(self):
        total_nodes = 0
        total_edges = 0
        vertex_labels = set()
        edge_labels = set()
        
        self.nodes_per_graph = [len(graph['vertices']) for graph in self.graphs]
        self.edges_per_graph = [len(graph['edges']) for graph in self.graphs]
        
        for graph in self.graphs:
            total_nodes += len(graph['vertices'])
            total_edges += len(graph['edges'])
            
            for vertex in graph['vertices']:
                vertex_labels.add(vertex[1])  
                
            for edge in graph['edges']:
                edge_labels.add(edge[2])  

        average_nodes = sum(self.nodes_per_graph) / len(self.graphs) if self.graphs else 0
        average_edges = sum(self.edges_per_graph) / len(self.graphs) if self.graphs else 0
        max_nodes = max(self.nodes_per_graph) if self.graphs else 0
        min_nodes = min(self.nodes_per_graph) if self.graphs else 0
        max_edges = max(self.edges_per_graph) if self.graphs else 0
        min_edges = min(self.edges_per_graph) if self.graphs else 0
        total_unique_vertex_labels = len(vertex_labels)
        total_unique_edge_labels = len(edge_labels)

        print(f'average_nodes: {average_nodes}')
        print(f'average_edges: {average_edges}')
        print(f'max_nodes: {max_nodes}')
        print(f'min_nodes: {min_nodes}')
        print(f'max_edges: {max_edges}')
        print(f'min_edges: {min_edges}')
        print(f'total_unique_vertex_labels: {total_unique_vertex_labels}')
        print(f'total_unique_edge_labels: {total_unique_edge_labels}')

    def plotNodeDistribution(self):
        
        plt.figure(figsize=(6, 4))
        plt.hist(self.nodes_per_graph, bins=max(20, len(set(self.nodes_per_graph))), edgecolor='black')
        plt.title('Distribution of Nodes per Graph')
        plt.xlabel('Number of Nodes')
        plt.ylabel('Frequency')
        plt.tight_layout()
        plt.show()

    def plotEdgeDistribution(self):
        
        plt.figure(figsize=(6, 4))
        plt.hist(self.edges_per_graph, bins=max(20, len(set(self.edges_per_graph))), edgecolor='black')
        plt.title('Distribution of Edges per Graph')
        plt.xlabel('Number of Edges')
        plt.ylabel('Frequency')
        plt.tight_layout()
        plt.show()
        

if __name__ == '__main__':
    file_path = 'Chemical_340.txt'
    obj = graphDatabase(file_path)
    obj.printGraphDatabaseStatistics()
    obj.printIndividualGraphStats()
    obj.plotNodeDistribution()
    obj.plotEdgeDistribution()
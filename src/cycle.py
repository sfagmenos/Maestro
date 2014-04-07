from networkx import *

def isCyclicUtil(graph, vertex, visited, recstack):
    if not visited[vertex]:
        visited[vertex] = True
        recstack[vertex] = True
    for des in graph.successors(vertex):
        if not visited[des] and isCyclicUtil(graph,des,visited,recstack):
            return True
        elif recstack[des]:
            return True
    recstack[vertex] = False
    return False

def isCyclic(graph):
    visited={}
    recstack={}
    for node in graph.nodes():
        visited[node] = False
        recstack[node] = False
    for node in graph.nodes():
        if isCyclicUtil(graph,node,visited,recstack):
            return True
    return False

G = DiGraph()
G.add_nodes_from([1,2,3,4,5,6])
G.add_edge(1,2)
G.add_edge(2,3)
G.add_edge(2,5)
G.add_edge(3,4)
G.add_edge(4,6)
#G.add_edge(6,5)
G.add_edge(6,2)
print isCyclic(G)

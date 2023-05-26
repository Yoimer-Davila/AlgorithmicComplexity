import graphviz as gv
import numpy as np
from graphs import AdjacencyList


def from_adjacency_list(adjacency: list[str], weighted=False, sep="|"):
    _list = []
    for item in adjacency:
        if weighted:
            _list.append([tuple(map(int, p.split(sep))) for p in item.strip().split()])
            # line => "1|3 2|5 4|4" ==> [(1, 3), (2, 5), (4, 4)]
        else:
            _list.append(list(map(int, item.strip().split())))  # "1 3 5" => [1, 3, 5]
            # L.append([int(x) for x in line.strip().split()])
    return _list


def from_adjacency_file(filename: str, has_labels=False, weighted=False, sep="|"):
    labels = None
    with open(filename, mode='r', encoding='utf-8') as file:
        if has_labels:
            labels = file.readline().strip().split()
        return from_adjacency_list([_ for _ in file], weighted, sep), labels


def from_adjacency_matrix_file(filename: str):
    return np.loadtxt(filename, dtype=int)


def from_edges_list(edges: list[tuple], size: int):
    graph = [[] for _ in range(size)]

    for u, v in edges:
        graph[u].append(v)

    return graph


def from_topology_names_list(names: list[str], separator=':'):
    labels = []
    _dict = dict()
    info = []
    for name in names:
        node, neighbours = [elem.strip() for elem in name.split(separator)]
        neighbours = neighbours.split()
        _dict[node] = len(labels)
        labels.append(node)
        info.append(neighbours)
    return _dict, info, labels


def from_topology_names_file(filename: str, separator):
    with open(filename, mode='r', encoding='utf-8') as file:
        return from_topology_names_list(file.readlines(), separator)


def from_topology_names(_dict: dict, information):
    graph = []
    for neighbours in information:
        graph.append([_dict[node] for node in neighbours])
    return graph


def adjacency_matrix_graph(matrix, labels=None, directed=False, weighted=False, layout="neato"):
    graph = gv.Digraph("G") if directed else gv.Graph("G")
    graph.graph_attr["layout"] = layout
    graph.node_attr["style"] = "filled"
    graph.node_attr["color"] = "orange"
    n = len(matrix)
    for u in range(n):
        graph.node(str(u), labels[u] if labels else str(u))

    for u in range(n):
        for v in range(0 if directed else u, n):
            if weighted:
                if not np.isnan(matrix[u, v]):
                    graph.edge(str(u), str(v), f"{matrix[u, v]:.0f}")
            else:
                if matrix[u, v] == 1:
                    graph.edge(str(u), str(v))
    return graph


def adjacency_list_graph(adjacency: list | AdjacencyList, labels=None, directed=False, weighted=False, path=None,
                         layout="neato"):
    if path is None:
        path = []
    graph = gv.Digraph("G") if directed else gv.Graph("G")
    graph.graph_attr["layout"] = layout
    graph.edge_attr["color"] = "gray"
    graph.node_attr["color"] = "orangered"
    graph.node_attr["width"] = "0.1"
    graph.node_attr["height"] = "0.1"
    graph.node_attr["fontsize"] = "8"
    graph.node_attr["fontcolor"] = "mediumslateblue"
    graph.node_attr["fontname"] = "monospace"
    graph.edge_attr["fontsize"] = "8"
    graph.edge_attr["fontname"] = "monospace"

    n = len(adjacency)
    for u in range(n):
        graph.node(str(u), labels[u] if labels else str(u))
    added = set()

    for v, u in enumerate(path):
        if u is not None and u >= 0:
            if weighted:
                for vi, w in adjacency[u]:
                    if vi == v:
                        break
                graph.edge(str(u), str(v), str(w), dir="forward", penwidth="1", color="orange")
            else:
                graph.edge(str(u), str(v), dir="forward", penwidth="1", color="orange")
            added.add(f"{u},{v}")
            added.add(f"{v},{u}")

    if weighted:
        for u in range(n):
            for v, w in adjacency[u]:
                if not directed and f"{u},{v}" not in added:
                    added.add(f"{u},{v}")
                    added.add(f"{v},{u}")
                    graph.edge(str(u), str(v), str(w))
                elif directed:
                    graph.edge(str(u), str(v), str(w))
    else:
        for u in range(n):
            for v in adjacency[u]:
                if not directed and f"{u},{v}" not in added:
                    added.add(f"{u},{v}")
                    added.add(f"{v},{u}")
                    graph.edge(str(u), str(v))
                elif directed:
                    graph.edge(str(u), str(v))
    return graph


def show_graph(graph: gv.Graph, name='graph', size: str = '8px,4px'):
    graph.graph_attr['size'] = size
    src = gv.Source(graph.source)
    src.view()


class DisjointSet:
    def __init__(self, size):
        self.set = list(range(size))

    def find(self, node):
        if self.set[node] == node:
            return node
        parent = self.find(self.set[node])
        self.set[node] = parent
        return parent

    def same_set(self, node_a, node_b):
        return self.find(node_a) == self.find(node_b)

    def union(self, node_a, node_b):
        a = self.find(node_a)
        b = self.find(node_b)
        self.set[a] = b


def from_kruskal(size: int, kruskal: list[int]):
    graph = [[] for _ in range(size)]

    for u, v, _ in kruskal:
        graph[u].append(v)
        graph[v].append(u)

    return graph

import copy
import math
import heapq as hq

from graphs import DisjointSet


def dijkstra(graph, source, target=None):
    n = len(graph)  # numero de nodos
    visited = [False] * n  # si el nodo actual ha sido visitado
    path = [-1] * n  # la ruta para cada nodo
    cost = [math.inf] * n  # por defecto el costo mayor es infinito
    cost[source] = 0  # el costo es igual a 0
    queue = [(0, source)]  # cola de elementos a buscar
    while queue:
        g_u, u = hq.heappop(queue)
        if target is not None and u == target:
            return g_u

        if not visited[u]:
            visited[u] = True
            for v, w in graph[u]:  # para cada nodo y cada peso
                f = g_u + w  # sumamos el costo de mi nodo origen + w (el costo del nodo visitado)
                if f < cost[v]:
                    cost[v] = f
                    path[v] = u
                    hq.heappush(queue, (f, v))

    return path, cost


def deep_first_search(graph, source):
    size = len(graph)
    visited = [False] * size
    path = [-1] * size

    def _dfs(u):
        visited[u] = True
        for v in graph[u]:
            if not visited[v]:
                path[v] = u
                _dfs(v)

    _dfs(source)

    return path


def deep_first_search_path(graph, source, target):
    visited = []
    path = []

    def _dfs(start, end):
        visited.append(start)
        if start == end:
            if start not in path and end in graph[start]:
                path.append(start)
            return True
        for neighbor in graph[start]:
            if neighbor not in visited:
                if _dfs(neighbor, end):
                    path.append(start)
                    return True
        path.pop()
        return False

    _dfs(source, target)
    return path


def deep_first_search_stack(graph, source):
    size = len(graph)
    visited = [False] * size
    path = [-1] * size
    stack = [source]
    while stack:
        u = stack.pop()
        if not visited[u]:
            visited[u] = True
            for v in graph[u]:
                if not visited[v]:
                    path[v] = u
                    stack.append(v)

    return path


def __breadth_first_search(graph, source, version=1):
    size = len(graph)
    visited = [False] * size  # si el nodo actual está siendo visitado
    path = [-1] * size  # lista de si visité a los hijos de ese nodo
    nodes = [None] * size
    queue = [source]  # lista de cual es el nodo origen desde donde voy a hacer el recorrido
    visited[source] = True  # considero que estoy visitando primero el nodo s

    def solver(sequence):
        for index in sequence:
            try:
                unit = graph[index, u] == 1
            except TypeError or IndexError:
                unit = True
            if unit and not visited[index]:
                visited[index] = True
                path[index] = u
                nodes[index] = index
                queue.append(index)

    while queue:
        u = queue.pop(0)
        solver(graph[u]) if version == 1 else solver(range(size))
    if version == 1:
        return path
    return path, nodes


def breadth_first_search_al(graph, source) -> list:
    return __breadth_first_search(graph, source)


def breadth_first_search_am(graph, source) -> tuple[list, list]:
    return __breadth_first_search(graph, source, version=2)


def deep_limited_search(graph, source, limit):
    size = len(graph)
    visited = [False] * size
    path = [-1] * size

    def _dls(u, limit):
        if limit > 0 and not visited[u]:
            visited[u] = True
            for v in graph[u]:
                if not visited[v]:
                    path[v] = u
                    _dls(v, limit - 1)

    _dls(source, limit)
    return path


def kosaraju(graph):
    def reverse_graph(_graph: list[list[int]]):
        n = len(_graph)
        _reversed = [[] for _ in range(n)]

        for u in range(n):
            for v in _graph[u]:
                _reversed[v].append(u)

        return _reversed

    def dfs(_graph, u, stack, visited):
        visited[u] = True
        for v in _graph[u]:
            if not visited[v]:
                dfs(_graph, v, stack, visited)

        stack.append(u)

    graph_size = len(graph)
    visited = [False] * graph_size
    f = []

    r_graph = reverse_graph(graph)  # step 1

    for u in range(graph_size):  # step 2
        if not visited[u]:
            dfs(r_graph, u, f, visited)

    visited = [False] * graph_size  # step 3
    scc = []
    for u in reversed(f):
        if not visited[u]:
            cc = []
            dfs(graph, u, cc, visited)
            scc.append(list(reversed(cc)))

    return scc


def toposort(graph):
    n = len(graph)
    visited = [False] * n
    ts = []

    def dfs(u):
        visited[u] = True
        for v in graph[u]:
            if not visited[v]:
                dfs(v)
        ts.append(u)

    for u in range(n):
        if not visited[u]:
            dfs(u)

    return ts


def kruskal(graph):
    size = len(graph)
    edges = []
    for u in range(size):
        for v, w in graph[u]:
            hq.heappush(edges, (w, u, v))

    uf = DisjointSet(size)

    min_graph = []
    weight = 0
    while edges and size > 0:
        w, u, v = hq.heappop(edges)
        if not uf.same_set(u, v):
            weight += w
            uf.union(u, v)
            min_graph.append((u, v, w))
            size -= 1

    return min_graph, weight


def prim(graph, start=(0, 0)):
    n = len(graph)
    visited = [False] * n
    path = [-1] * n
    cost = [math.inf] * n
    q = [start]
    while q:
        _, u = hq.heappop(q)
        if not visited[u]:
            visited[u] = True
            for v, w in graph[u]:
                if not visited[v] and w < cost[v]:
                    cost[v] = w
                    path[v] = u
                    hq.heappush(q, (w, v))

    weight = 0

    for w in cost:
        if w != math.inf:
            weight += w
    return path, weight


def bfs_ff(graph, source, target, parent):
    visited = [False] * len(graph)
    queue = [[source]]  # Almacena caminos en lugar de nodos individuales
    visited[source] = True

    paths = []  # Almacena los caminos encontrados

    while queue:
        path = queue.pop(0)
        u = path[-1]  # Último nodo en el camino actual
        for ind in range(len(graph[u])):
            if visited[ind] is False and graph[u][ind] > 0:
                new_path = path + [ind]  # Agrega el nuevo nodo al camino
                queue.append(new_path)
                visited[ind] = True
                parent[ind] = u
                if ind == target:
                    paths.append(new_path)  # Agrega el camino completo a los caminos encontrados

    return visited[target], paths


def ford_fulkerson(matrix, source, sink):
    graph = matrix.copy()
    parent = [-1] * len(graph)
    max_flow = 0
    paths = []  # Almacena los caminos utilizados

    while True:
        visited, path_list = bfs_ff(graph, source, sink, parent)
        if visited:
            path_flow = float("Inf")
            for path in path_list:
                for i in range(1, len(path)):
                    path_flow = min(path_flow, graph[path[i - 1]][path[i]])
                paths.append((path, path_flow))  # Agrega el camino actual a los caminos utilizados

            for path in path_list:
                for i in range(1, len(path)):
                    graph[path[i - 1]][path[i]] -= path_flow
                    graph[path[i]][path[i - 1]] += path_flow

            max_flow += path_flow
        else:
            break

    return max_flow, paths


def bfs_ff_cost(graph, source, target, parent):
    # Return True if there is node that has not iterated.
    visited = [False] * len(graph)
    queue = [source]
    visited[source] = True

    while queue:
        u = queue.pop(0)
        for ind in range(len(graph[u])):
            if visited[ind] is False and graph[u][ind] > 0:
                queue.append(ind)
                visited[ind] = True
                parent[ind] = u

    return visited[target]


def ford_fulkerson_cost(matrix, source, sink):
    # This array is filled by BFS and to store path
    graph = matrix.copy()
    parent = [-1] * (len(graph))
    max_flow = 0
    while bfs_ff_cost(graph, source, sink, parent):
        path_flow = float("Inf")
        s = sink

        while s != source:
            # Find the minimum value in select path
            path_flow = min(path_flow, graph[parent[s]][s])
            s = parent[s]

        max_flow += path_flow
        v = sink

        while v != source:
            u = parent[v]
            graph[u][v] -= path_flow
            graph[v][u] += path_flow
            v = parent[v]
    return max_flow

import graphs


class __Adjacency:
    def __init__(self):
        self._list: list = None
        self._weighted = None
        self._size = None

    def _value(self, value, weight):
        return (value, weight) if weight is not None and self._weighted else value

    def _connect(self, index, value, weight):
        raise NotImplementedError()

    def connect(self, node_a: int, node_b: int, weight: int = None, bidirectional=False):
        self._connect(node_a, node_b, weight)
        if bidirectional:
            self._connect(node_b, node_a, weight)

    def __getitem__(self, item):
        return self._list[item]

    def __iter__(self):
        return self._list.__iter__()

    def __len__(self):
        return self._size

    def __str__(self):
        return str(self._list)

    def __repr__(self):
        return self._list.__repr__()

    def repr_list(self):
        chars = str(self).replace('],', '],\n')
        return chars

    def copy(self):
        return self._list.copy()


class AdjacencyList(__Adjacency):
    def __init__(self, size: int = None, weighted=False):
        super().__init__()
        self._list = [] if size is None else [[] for _ in range(size)]
        self._weighted = weighted
        self._size = 0 if size is None else size

    def add(self, connections: list = None):
        self._list.append([] if connections is None else connections)
        self._size += 1

    def _connect(self, index, value, weight):
        connection = self._value(value, weight)
        if connection not in self._list[index]:
            self._list[index].append(connection)

    def connect(self, node_a: int, node_b: int, weight: int = None, bidirectional=False):
        if node_a < self._size > node_b:
            super().connect(node_a, node_b, weight, bidirectional)

    def list(self):
        return self._list


class NamedAdjacencyList(AdjacencyList):
    def __init__(self, labels: list[str] = None, weighted=False):
        super().__init__(len(labels) if labels else None, weighted)
        self._labels: list[str] = labels if labels else []

    def add(self, label: str, connections: list = None):
        if label not in self._labels:
            self._labels.append(label)
            super().add(connections)

    def connect(self, label_a: str, label_b: str, weight: int = None, bidirectional=False):
        if label_b in self._labels and label_a in self._labels:
            super().connect(self.label_index(label_a), self.label_index(label_b), weight, bidirectional)

    def labels(self):
        return self._labels

    def label_index(self, label: str):
        if label in self._labels:
            return self._labels.index(label)
        return -1


class AdjacencyMatrix(__Adjacency):
    def __init__(self, size: int = None, weighted=False, not_connected=0):
        super().__init__()
        self._size = 0 if size is None else size
        self._weighted = weighted
        self._not_connected = not_connected
        self._list = [self._zeros_list() for _ in range(self._size)]

    def _zeros_list(self):
        return [self._not_connected] * self._size

    def _init_list(self):
        self._list = [self._zeros_list() for _ in range(self._size)]

    def matrix(self):
        return self._list

    def _connect(self, index_a: int, index_b: int, weight: int):
        self._list[index_a][index_b] = self._value(index_b, weight)

    def connect(self, index_a: int, index_b: int, weight: int = None, bidirectional=False):
        if index_a < self._size > index_b:
            self._connect(index_a, index_b, weight)
            if bidirectional:
                self._connect(index_b, index_a, weight)

    def add(self):
        self._size += 1
        [item.append(self._not_connected) for item in self._list]
        self._list.append(self._zeros_list())

    def copy(self):
        adj = AdjacencyMatrix(self._size, self._weighted, self._not_connected)
        adj._list = [item.copy() for item in self._list]
        return adj


class NamedAdjacencyMatrix(AdjacencyMatrix):
    def __init__(self, labels: list[str] = None, weighted=False, not_connected=0):
        self._labels = [] if labels is None else labels
        super().__init__(len(self._labels), weighted, not_connected)

    def add(self, label: str):
        if label not in self._labels:
            self._labels.append(label)
            super().add()

    def label_index(self, label: str):
        if label in self._labels:
            return self._labels.index(label)
        return -1

    def connect(self, label_a: str, label_b: str, weight: int = None, bidirectional=False):
        if label_b in self._labels and label_a in self._labels:
            super().connect(self.label_index(label_a), self.label_index(label_b), weight, bidirectional)

    def labels(self):
        return self._labels


class MaxFlowMatrix(AdjacencyMatrix):
    def __init__(self, size: int):
        super().__init__(size)

    def _value(self, value, weight):
        return weight

    def connect(self, index_a: int, index_b: int, weight: int, bidirectional=False):
        super().connect(index_a, index_b, weight, bidirectional)


class NamedMaxFlowMatrix(NamedAdjacencyMatrix):
    def __init__(self, labels: list[str]):
        super().__init__(labels)

    def _value(self, value, weight):
        return weight

    def connect(self, label_a: str, label_b: str, weight: int, bidirectional=False):
        super().connect(label_a, label_b, weight, bidirectional)


class DynamicProgrammingList(AdjacencyList):
    def __init__(self, size: int):
        super().__init__(size, weighted=True)
        self._list = []

    def _connect(self, index, value, weight):
        connection = (index,) + self._value(value, weight)
        if connection not in self._list:
            self._list.append(connection)


class NamedDynamicProgrammingList(NamedAdjacencyList):
    def __init__(self, labels: list[str]):
        super().__init__(labels, weighted=True)
        self._list = []

    def _connect(self, index, value, weight):
        connection = (index,) + self._value(value, weight)
        if connection not in self._list:
            self._list.append(connection)


class DynamicProgrammingMatrix(MaxFlowMatrix):
    def __init__(self, size: int):
        super().__init__(size)
        self._not_connected = float("inf")
        self._init_list()

    def _init_list(self):
        self._list = [
            [self._not_connected if index != item else 0 for item in range(self._size)]
            for index in range(self._size)
        ]


class NamedDynamicProgrammingMatrix(NamedMaxFlowMatrix):
    def __init__(self, labels: list[str]):
        super().__init__(labels)
        self._not_connected = float("inf")
        self._init_list()

    def _init_list(self):
        self._list = [
            [self._not_connected if index != item else 0 for item in range(self._size)]
            for index in range(self._size)
        ]

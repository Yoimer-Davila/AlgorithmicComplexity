class AdjacencyList:
    def __init__(self, size: int = None, weighted=False):
        self.__list = [] if size is None else [[] for _ in range(size)]
        self.__weighted = weighted
        self.__size = 0 if size is None else size

    def add(self, connections: list = None):
        self.__list.append([] if connections is None else connections)
        self.__size += 1

    def __value(self, index, value, weight):
        return (value, weight) if weight is not None and self.__weighted else value

    def __connect(self, index, value, weight):
        connection = self.__value(index, value, weight)
        if connection not in self.__list[index]:
            self.__list[index].append(connection)

    def connect(self, node_a: int, node_b: int, weight: int = None, bidirectional=False):
        if node_a < self.__size > node_b:
            self.__connect(node_a, node_b, weight)
            if bidirectional:
                self.__connect(node_b, node_a, weight)

    def list(self):
        return self.__list

    def __getitem__(self, item):
        return self.__list[item]

    def __iter__(self):
        return self.__list.__iter__()

    def __len__(self):
        return self.__size

    def __str__(self):
        return str(self.__list)

    def __repr__(self):
        return self.__list.__repr__()


class NamedAdjacencyList(AdjacencyList):
    def __init__(self, labels: list[str] = None, weighted=False):
        super().__init__(len(labels) if labels else None, weighted)
        self.__labels: list[str] = labels if labels else []

    def add(self, label: str, connections: list = None):
        if label not in self.__labels:
            self.__labels.append(label)
            super().add(connections)

    def connect(self, label_a: str, label_b: str, weight: int = None, bidirectional=False):
        if label_b in self.__labels and label_a in self.__labels:
            super().connect(self.__labels.index(label_a), self.__labels.index(label_b), weight, bidirectional)

    def labels(self):
        return self.__labels

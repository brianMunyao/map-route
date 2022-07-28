class Graph:
    def __init__(self):
        self.nodes = {}

    class Edge:
        def __init__(self, startNode, toNode, weight):
            self.startNode = startNode
            self.toNode = toNode
            self.weight = weight

        def getConnections(self):
            return self.toNode

        def getDetail(self):
            return self.startNode.getId() + " -> " + self.toNode.getId()+", Weight: " + str(self.weight)

    class Node:
        def __init__(self, value):
            self.value = value
            self.edges = []

        def addEdge(self, edge):  # Edge(to, weight)
            self.edges.append(edge)

        def getEdges(self):
            return self.edges

        def getId(self):
            return self.value

    def addNode(self, value):
        node = self.Node(value)
        self.nodes[value] = node
        return node

    def addEdge(self, startNode: Node, toNode: Node, weight=10):
        startNode.addEdge(self.Edge(startNode, toNode, weight))
        toNode.addEdge(self.Edge(toNode, startNode, weight))

    def getNodes(self):
        return self.nodes

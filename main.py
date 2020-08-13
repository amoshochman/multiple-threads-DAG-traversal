from queue import Queue
from threading import Thread


class Graph:
    def __init__(self):
        """
        For a node B, self.edges[B] is the set of nodes B such that exist an edge (A,B).
        """
        self.edges = dict()
        self.q = Queue()

    def add_node(self, node):
        self.edges[node] = set()

    def add_edge(self, node1, node2):
        self.edges[node2].add(node1)

    @staticmethod
    def _visit_node(edges_to_traverse, node):
        """
        Visiting a node means removing it from the dependencies.
        That is, removing it from the sets of values in edges_to_traverse.
        :param edges_to_traverse: The remaining edges.
        :param node: The node to be visited.
        """
        node.func()
        for s in edges_to_traverse.values():
            s.discard(node)

    @staticmethod
    def _get_node_to_visit(edges_to_traverse):
        """
        Returns a node such that there are no remaining dependencies for it,
        if such exist. None otherwise.
        :param edges_to_traverse: The remaining edges to be traversed.
        :return: A node that can be visited, if exist. None otherwise.
        """
        for node, depends_on in edges_to_traverse.items():
            if not depends_on:
                del edges_to_traverse[node]
                return node
        return None

    def traverse(self):
        """
        Traverses the DAG from the root in such a way that every node is visited
        (its associated function is called, in our case) once all its parents were visited.
        """

        edges_to_traverse = self.edges.copy()
        """
        edges_to_traverse are the remaining edges to be traversed. Therefore,
        it's initialized as a copy of the edges.
        Every time a node A is visited, we remove it from all the sets in edges_to_traverse.values.
        At the end of traverse function, edges_to_traverse is empty.
        """

        def pop():
            """
            While there is some node in the queue, the first node in the queue is removed
            and visited.
            """
            while True:
                node = self.q.get()
                self._visit_node(edges_to_traverse, node)
                self.q.task_done()

        for i in range(len(self.edges)):
            """
            We may be using more threads than really needed but this way we ensure
            that there are no delays due to this reason.
            """
            worker = Thread(target=pop)
            worker.setDaemon(True)
            worker.start()

        while edges_to_traverse:
            node_to_visit = self._get_node_to_visit(edges_to_traverse)
            if node_to_visit:
                self.q.put(node_to_visit)

        self.q.join()


class Node:
    def __init__(self, name, func):
        self.name = name
        self.func = func

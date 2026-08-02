class Graph:
    """Undirected graph backed by an adjacency-list (dict of sets)."""

    def __init__(self):
        self._adjacency = {}

    def add_node(self, node):
        """Insert a node with no edges if it does not already exist."""
        if node not in self._adjacency:
            self._adjacency[node] = set()

    def add_edge(self, node_a, node_b):
        """Create an undirected edge (friendship) between two nodes."""
        if node_a == node_b:
            raise ValueError("Self-friendships are not allowed.")
        self.add_node(node_a)
        self.add_node(node_b)
        self._adjacency[node_a].add(node_b)
        self._adjacency[node_b].add(node_a)

    def remove_edge(self, node_a, node_b):
        """Remove an edge if it exists; safe to call if it does not."""
        self._adjacency.get(node_a, set()).discard(node_b)
        self._adjacency.get(node_b, set()).discard(node_a)

    def remove_node(self, node):
        """Completely remove a node and all its incident edges."""
        if node in self._adjacency:
            # Remove node from all neighbors' adjacency sets
            for neighbor in self._adjacency[node]:
                self._adjacency[neighbor].discard(node)
            del self._adjacency[node]

    def has_edge(self, node_a, node_b):
        return node_b in self._adjacency.get(node_a, set())

    def neighbors(self, node):
        """Return the set of nodes directly connected to `node`."""
        return self._adjacency.get(node, set())

    def nodes(self):
        return self._adjacency.keys()

    def degree(self, node):
        """Number of direct connections a node has (used for influence)."""
        return len(self._adjacency.get(node, set()))

    def __len__(self):
        return len(self._adjacency)

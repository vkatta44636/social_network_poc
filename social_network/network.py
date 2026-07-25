from collections import deque

from .graph import Graph
from .user import User


class SocialNetwork:
    """Ties together user profiles (hash table) and friendships (graph)."""

    def __init__(self):
        self._profiles = {}
        self._graph = Graph()

    # Insertion
    
    def add_user(self, user_id, name, bio=""):
        """Register a new user. Raises ValueError on a duplicate id."""
        if user_id in self._profiles:
            raise ValueError(f"User '{user_id}' already exists.")
        self._profiles[user_id] = User(user_id, name, bio)
        self._graph.add_node(user_id)

    def add_friendship(self, user_a, user_b):
        """Create a mutual friendship between two existing users."""
        self._validate_user(user_a)
        self._validate_user(user_b)
        self._graph.add_edge(user_a, user_b)

    # Deletion (partial -- see report, Section: Next Steps)
    
    def remove_friendship(self, user_a, user_b):
        self._validate_user(user_a)
        self._validate_user(user_b)
        self._graph.remove_edge(user_a, user_b)
    
    # Searching
    
    def search_profile(self, user_id):
        """O(1) average-case profile lookup via the hash table."""
        self._validate_user(user_id)
        return self._profiles[user_id]

    def mutual_friends(self, user_a, user_b):
        """Set intersection of two users' neighbor sets."""
        self._validate_user(user_a)
        self._validate_user(user_b)
        return self._graph.neighbors(user_a) & self._graph.neighbors(user_b)

    # Traversal: BFS -> shortest path / degrees of separation
    
    def shortest_path(self, start, goal):
        """
        Breadth-First Search for the shortest friendship path between
        two users. Returns a list of user_ids from start to goal
        (inclusive), or None if no path exists (e.g. disconnected
        components). Runs in O(V + E).
        """
        self._validate_user(start)
        self._validate_user(goal)

        if start == goal:
            return [start]

        visited = {start}
        queue = deque([[start]])

        while queue:
            path = queue.popleft()
            current = path[-1]
            for neighbor in self._graph.neighbors(current):
                if neighbor == goal:
                    return path + [neighbor]
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(path + [neighbor])

        return None

    def degrees_of_separation(self, start, goal):
        path = self.shortest_path(start, goal)
        return None if path is None else len(path) - 1
    
    # Traversal: DFS -> community / connected-component discovery
    
    def find_community(self, start):
        """
        Iterative Depth-First Search (explicit stack, not recursion,
        to avoid Python's recursion-depth limit on large networks).
        Returns every user reachable from `start`, i.e. its connected
        component / community.
        """
        self._validate_user(start)

        visited = set()
        stack = [start]
        community = []

        while stack:
            node = stack.pop()
            if node not in visited:
                visited.add(node)
                community.append(node)
                for neighbor in self._graph.neighbors(node):
                    if neighbor not in visited:
                        stack.append(neighbor)

        return community

    # Internal helpers
    
    def _validate_user(self, user_id):
        if user_id not in self._profiles:
            raise KeyError(f"User '{user_id}' does not exist.")

    def __len__(self):
        return len(self._profiles)

from collections import deque
from .graph import Graph
from .user import User

class SocialNetwork:
    """Ties together user profiles (hash table) and friendships (graph)."""

    def __init__(self):
        self._profiles = {}
        self._graph = Graph()
        self._path_cache = {} # Optimization: Memoization for shortest paths

    def _invalidate_cache(self):
        """Clears the path cache when the graph topology changes."""
        self._path_cache.clear()

    # Insertion & Deletion
    
    def add_user(self, user_id, name, bio=""):
        if user_id in self._profiles:
            raise ValueError(f"User '{user_id}' already exists.")
        self._profiles[user_id] = User(user_id, name, bio)
        self._graph.add_node(user_id)
        self._invalidate_cache()

    def delete_user(self, user_id):
        """Full user deletion as promised in Phase 2."""
        self._validate_user(user_id)
        self._graph.remove_node(user_id)
        del self._profiles[user_id]
        self._invalidate_cache()

    def add_friendship(self, user_a, user_b):
        self._validate_user(user_a)
        self._validate_user(user_b)
        self._graph.add_edge(user_a, user_b)
        self._invalidate_cache()

    def remove_friendship(self, user_a, user_b):
        self._validate_user(user_a)
        self._validate_user(user_b)
        self._graph.remove_edge(user_a, user_b)
        self._invalidate_cache()
    
    # Searching
    
    def search_profile(self, user_id):
        self._validate_user(user_id)
        return self._profiles[user_id]

    def mutual_friends(self, user_a, user_b):
        self._validate_user(user_a)
        self._validate_user(user_b)
        return self._graph.neighbors(user_a) & self._graph.neighbors(user_b)

    # Traversal: BFS -> shortest path / degrees of separation
    
    def shortest_path(self, start, goal):
        self._validate_user(start)
        self._validate_user(goal)

        cache_key = tuple(sorted([start, goal]))
        if cache_key in self._path_cache:
            return self._path_cache[cache_key]

        if start == goal:
            return [start]

        visited = {start}
        queue = deque([[start]])

        while queue:
            path = queue.popleft()
            current = path[-1]
            for neighbor in self._graph.neighbors(current):
                if neighbor == goal:
                    final_path = path + [neighbor]
                    self._path_cache[cache_key] = final_path
                    return final_path
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(path + [neighbor])

        self._path_cache[cache_key] = None
        return None

    def degrees_of_separation(self, start, goal):
        path = self.shortest_path(start, goal)
        return None if path is None else len(path) - 1
    
    # Traversal: DFS -> community / connected-component discovery
    
    def find_community(self, start):
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

    # Advanced Influence Metric
    def compute_pagerank(self, damping=0.85, iterations=20):
        """Advanced influence metric utilizing PageRank algorithm."""
        nodes = list(self._graph.nodes())
        if not nodes:
            return {}
        N = len(nodes)
        pagerank = {node: 1.0 / N for node in nodes}
        
        for _ in range(iterations):
            new_pr = {}
            for node in nodes:
                rank_sum = 0
                for neighbor in self._graph.neighbors(node):
                    if self._graph.degree(neighbor) > 0:
                        rank_sum += pagerank[neighbor] / self._graph.degree(neighbor)
                new_pr[node] = ((1.0 - damping) / N) + (damping * rank_sum)
            pagerank = new_pr
            
        return pagerank

    # Internal helpers
    
    def _validate_user(self, user_id):
        if user_id not in self._profiles:
            raise KeyError(f"User '{user_id}' does not exist.")

    def __len__(self):
        return len(self._profiles)

import heapq

class PriorityManager:
    """Max-priority queue of users, ranked by influence score."""

    def __init__(self):
        self._heap = []
        self._counter = 0
        self._entry_finder = {} # Mapping of tasks to entries
        self._REMOVED = '<removed-user>' # Placeholder for a removed user

    def push(self, user_id, influence_score):
        """Add a new user or update the priority of an existing user."""
        if user_id in self._entry_finder:
            self.remove_user(user_id)
        
        self._counter += 1
        entry = [-influence_score, self._counter, user_id]
        self._entry_finder[user_id] = entry
        heapq.heappush(self._heap, entry)

    def remove_user(self, user_id):
        """Mark an existing user as removed without breaking the heap."""
        entry = self._entry_finder.pop(user_id, None)
        if entry:
            entry[-1] = self._REMOVED

    def top_k(self, k):
        if k < 0:
            raise ValueError("k must be non-negative.")
            
        results = []
        temp_heap = []
        
        while len(results) < k and self._heap:
            neg_score, count, user_id = heapq.heappop(self._heap)
            if user_id is not self._REMOVED:
                results.append((user_id, -neg_score))
                temp_heap.append((neg_score, count, user_id))
                
        # Push items back to preserve the heap for future calls
        for item in temp_heap:
            heapq.heappush(self._heap, item)
            
        return results

    def most_influential(self):
        while self._heap:
            neg_score, _, user_id = self._heap[0]
            if user_id is not self._REMOVED:
                return user_id, -neg_score
            heapq.heappop(self._heap)
        return None

    def __len__(self):
        return len(self._entry_finder)

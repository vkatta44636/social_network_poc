import heapq


class PriorityManager:
    """Max-priority queue of users, ranked by influence score."""

    def __init__(self):
        self._heap = []
        self._counter = 0

    def push(self, user_id, influence_score):
        self._counter += 1
        heapq.heappush(self._heap, (-influence_score, self._counter, user_id))

    def top_k(self, k):
        """Return the k most influential (user_id, score) pairs."""
        if k < 0:
            raise ValueError("k must be non-negative.")
        smallest = heapq.nsmallest(k, self._heap)
        return [(user_id, -neg_score) for neg_score, _, user_id in smallest]

    def most_influential(self):
        """Peek at the single most influential user, or None if empty."""
        if not self._heap:
            return None
        neg_score, _, user_id = self._heap[0]
        return user_id, -neg_score

    def __len__(self):
        return len(self._heap)

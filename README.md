## Project layout

```
social_network/
    __init__.py          # public exports
    user.py               # User class
    graph.py               # Graph class (adjacency list)
    network.py             # SocialNetwork class (hash table + graph)
    priority_manager.py     # PriorityManager class (heap / priority queue)
test_social_network.py      # unittest suite (4 tests)
```

## Requirements

Python 3.8+. No third-party dependencies -- everything used
(`collections.deque`, `heapq`) is in the standard library.

## Running the tests

```bash
python -m unittest test_social_network.py -v
```

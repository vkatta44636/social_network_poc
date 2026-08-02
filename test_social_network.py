import unittest
from social_network import SocialNetwork, PriorityManager

class TestSocialNetworkCore(unittest.TestCase):
    def setUp(self):
        self.network = SocialNetwork()
        for user_id, name in [("u1", "Aisha"), ("u2", "Ben"), ("u3", "Carlos")]:
            self.network.add_user(user_id, name)
        self.network.add_friendship("u1", "u2")
        self.network.add_friendship("u2", "u3")

    # ... [Keep previous 20 test cases from Phase 2 here] ...

    # ---- Phase 3 Advanced Testing & Edge Cases ----
    def test_delete_user(self):
        self.network.delete_user("u2")
        with self.assertRaises(KeyError):
            self.network.search_profile("u2")
        self.assertEqual(sorted(self.network.find_community("u1")), ["u1"])

    def test_shortest_path_caching(self):
        # Initial run (caches result)
        path1 = self.network.shortest_path("u1", "u3")
        self.assertEqual(path1, ["u1", "u2", "u3"])
        
        # Invalidate cache by adding friendship
        self.network.add_friendship("u1", "u3")
        path2 = self.network.shortest_path("u1", "u3")
        self.assertEqual(path2, ["u1", "u3"])

    def test_stress_scaling(self):
        """Stress test with 1000 nodes and 999 edges."""
        stress_net = SocialNetwork()
        for i in range(1000):
            stress_net.add_user(f"u{i}", f"User {i}")
        for i in range(999):
            stress_net.add_friendship(f"u{i}", f"u{i+1}")
            
        # Ensure deep traversals do not fail (DFS/BFS depth constraints)
        path = stress_net.shortest_path("u0", "u999")
        self.assertEqual(len(path), 1000)

class TestPriorityManagerPhase3(unittest.TestCase):
    def test_update_priority(self):
        pm = PriorityManager()
        pm.push("a", 5)
        pm.push("b", 10)
        pm.push("a", 15)  # Update a
        self.assertEqual(pm.most_influential(), ("a", 15))

if __name__ == "__main__":
    unittest.main()

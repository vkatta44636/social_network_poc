import unittest

from social_network import SocialNetwork, PriorityManager


class TestSocialNetworkCore(unittest.TestCase):
    def setUp(self):
        self.network = SocialNetwork()
        for user_id, name in [("u1", "Aisha"), ("u2", "Ben"), ("u3", "Carlos")]:
            self.network.add_user(user_id, name)
        self.network.add_friendship("u1", "u2")
        self.network.add_friendship("u2", "u3")

    # ---- Insertion ----
    def test_add_user(self):
        self.network.add_user("u4", "Deepa")
        self.assertEqual(len(self.network), 4)

    def test_add_duplicate_user_raises(self):
        with self.assertRaises(ValueError):
            self.network.add_user("u1", "Duplicate")

    def test_add_friendship_between_unknown_users_raises(self):
        with self.assertRaises(KeyError):
            self.network.add_friendship("u1", "ghost")

    # ---- Searching ----
    def test_search_profile(self):
        user = self.network.search_profile("u1")
        self.assertEqual(user.name, "Aisha")

    def test_search_missing_profile_raises(self):
        with self.assertRaises(KeyError):
            self.network.search_profile("u99")

    def test_mutual_friends(self):
        self.network.add_user("u4", "Deepa")
        self.network.add_friendship("u1", "u4")
        self.network.add_friendship("u3", "u4")
        self.assertEqual(self.network.mutual_friends("u2", "u4"), {"u1", "u3"})

    # ---- BFS traversal ----
    def test_shortest_path_direct(self):
        self.assertEqual(self.network.shortest_path("u1", "u2"), ["u1", "u2"])

    def test_shortest_path_multi_hop(self):
        self.assertEqual(self.network.shortest_path("u1", "u3"), ["u1", "u2", "u3"])

    def test_shortest_path_same_node(self):
        self.assertEqual(self.network.shortest_path("u1", "u1"), ["u1"])

    def test_shortest_path_disconnected_returns_none(self):
        self.network.add_user("isolated", "Grace")
        self.assertIsNone(self.network.shortest_path("u1", "isolated"))

    def test_degrees_of_separation(self):
        self.assertEqual(self.network.degrees_of_separation("u1", "u3"), 2)

    # ---- DFS traversal ----
    def test_find_community_full_component(self):
        self.assertEqual(sorted(self.network.find_community("u1")), ["u1", "u2", "u3"])

    def test_find_community_isolated_user(self):
        self.network.add_user("isolated", "Grace")
        self.assertEqual(self.network.find_community("isolated"), ["isolated"])

    def test_remove_friendship_splits_community(self):
        self.network.remove_friendship("u2", "u3")
        self.assertEqual(sorted(self.network.find_community("u1")), ["u1", "u2"])
        self.assertEqual(self.network.find_community("u3"), ["u3"])

    # ---- Edge cases ----
    def test_self_friendship_raises(self):
        with self.assertRaises(ValueError):
            self.network.add_friendship("u1", "u1")

    def test_duplicate_friendship_is_idempotent(self):
        self.network.add_friendship("u1", "u2")
        self.assertEqual(self.network._graph.degree("u1"), 1)


class TestPriorityManager(unittest.TestCase):
    def test_top_k_orders_by_score_descending(self):
        pm = PriorityManager()
        pm.push("a", 5)
        pm.push("b", 9)
        pm.push("c", 1)
        self.assertEqual(pm.top_k(2), [("b", 9), ("a", 5)])

    def test_most_influential(self):
        pm = PriorityManager()
        pm.push("a", 3)
        pm.push("b", 7)
        self.assertEqual(pm.most_influential(), ("b", 7))

    def test_empty_manager(self):
        pm = PriorityManager()
        self.assertIsNone(pm.most_influential())
        self.assertEqual(pm.top_k(5), [])

    def test_tie_breaking_does_not_raise(self):
        pm = PriorityManager()
        pm.push("a", 4)
        pm.push("b", 4)
        pm.push("c", 4)
        result = pm.top_k(3)
        self.assertEqual({user_id for user_id, _ in result}, {"a", "b", "c"})


if __name__ == "__main__":
    unittest.main()

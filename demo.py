from social_network import SocialNetwork, PriorityManager


def build_sample_network():
    network = SocialNetwork()

    users = [
        ("u1", "Aisha"),
        ("u2", "Ben"),
        ("u3", "Carlos"),
        ("u4", "Deepa"),
        ("u5", "Elena"),
        ("u6", "Farid"),
        ("u7", "Grace"),
    ]
    for user_id, name in users:
        network.add_user(user_id, name)

    friendships = [
        ("u1", "u2"), ("u1", "u3"), ("u2", "u3"),
        ("u3", "u4"), ("u4", "u5"), ("u5", "u6"),
    ]
    for a, b in friendships:
        network.add_friendship(a, b)

    return network


def run_demo():
    network = build_sample_network()

    print("Search profile: u1 ")
    print(network.search_profile("u1"))

    print("\nMutual friends of u1 and u4 ")
    print(network.mutual_friends("u1", "u4"))

    print("\nBFS shortest path: u1 -> u6 ")
    path = network.shortest_path("u1", "u6")
    print("Path:", path)
    print("Degrees of separation:", network.degrees_of_separation("u1", "u6"))

    print("\nBFS shortest path: u1 -> u7 (disconnected, expect None) ")
    print(network.shortest_path("u1", "u7"))

    print("\nDFS community containing u1 ")
    print(sorted(network.find_community("u1")))

    print("\nDFS community containing u7 (isolated) ")
    print(network.find_community("u7"))

    print("\nInfluence ranking (Priority Queue / heap) ")
    pm = PriorityManager()
    for user_id in network._graph.nodes():
        pm.push(user_id, network._graph.degree(user_id))
    print("Top 3 most influential users:", pm.top_k(3))
    print("Single most influential user:", pm.most_influential())

    print("\nEdge case: search for a user that does not exist ")
    try:
        network.search_profile("u99")
    except KeyError as e:
        print("Caught expected KeyError:", e)

    print("\nEdge case: register a duplicate user id ")
    try:
        network.add_user("u1", "Duplicate Aisha")
    except ValueError as e:
        print("Caught expected ValueError:", e)

    print("\nEdge case: self-friendship ")
    try:
        network.add_friendship("u2", "u2")
    except ValueError as e:
        print("Caught expected ValueError:", e)

    print("\nEdge case: remove a friendship, then re-check community ")
    network.remove_friendship("u3", "u4")
    print("Community containing u1 after removing (u3, u4):",
          sorted(network.find_community("u1")))
    print("Community containing u4 after removing (u3, u4):",
          sorted(network.find_community("u4")))


if __name__ == "__main__":
    run_demo()

from .models import AirportNode


# =========================================================
# BASIC TREE UTILITIES
# =========================================================

def get_all_nodes():
    """
    Returns all nodes in the tree.
    Used for brute-force approaches (e.g., diameter calculation).
    """
    return list(AirportNode.objects.all())


def path_to_root(node):
    """
    Returns path from given node up to the root.
    Order: node → parent → ... → root
    """
    path = []
    while node:
        path.append(node)
        node = node.parent
    return path


# =========================================================
# DISTANCE CALCULATIONS
# =========================================================

def distance_from_root(node):
    """
    Computes total distance from root to given node.

    Walks upward using parent pointers and accumulates edge weights.
    """
    total = 0
    current = node

    while current.parent:
        parent = current.parent

        if parent.left == current:
            total += parent.left_distance or 0
        elif parent.right == current:
            total += parent.right_distance or 0

        current = parent

    return total


def distance_between(node1, node2):
    """
    Computes distance between any two nodes in the tree.

    Steps:
    1. Find path to root for both nodes
    2. Find Lowest Common Ancestor (LCA)
    3. Sum distances from both nodes to LCA
    """
    path1 = path_to_root(node1)
    path2 = path_to_root(node2)

    set_path2 = set(path2)

    # Find LCA
    lca = None
    for n in path1:
        if n in set_path2:
            lca = n
            break

    # node1 → LCA
    dist1 = 0
    curr = node1
    while curr != lca:
        parent = curr.parent
        if parent.left == curr:
            dist1 += parent.left_distance or 0
        else:
            dist1 += parent.right_distance or 0
        curr = parent

    # node2 → LCA
    dist2 = 0
    curr = node2
    while curr != lca:
        parent = curr.parent
        if parent.left == curr:
            dist2 += parent.left_distance or 0
        else:
            dist2 += parent.right_distance or 0
        curr = parent

    return dist1 + dist2


# =========================================================
# PATH CONSTRUCTION
# =========================================================

def path_between(node1, node2):
    """
    Returns the actual path between two nodes.

    Output:
    node1 → ... → LCA → ... → node2
    """
    path1 = path_to_root(node1)
    path2 = path_to_root(node2)

    set_path2 = set(path2)

    # Find LCA
    lca = None
    for n in path1:
        if n in set_path2:
            lca = n
            break

    # node1 → LCA
    path_up = []
    curr = node1
    while curr != lca:
        path_up.append(curr)
        curr = curr.parent
    path_up.append(lca)

    # LCA → node2
    path_down = []
    curr = node2
    while curr != lca:
        path_down.append(curr)
        curr = curr.parent

    return path_up + path_down[::-1]



# =========================================================
# LONGEST ROUTE FROM ROOT
# =========================================================

def longest_from_root(root):
    """
    Finds the longest route starting from the root node.

    This is NOT tree diameter.
    This is simply:
        root → deepest leaf (by total edge weight)

    Returns:
        (max_distance, path)

    Path format:
        root → ... → leaf
    """

    def dfs(node):
        """
        Returns:
            (max_distance_from_this_node, path_from_this_node)
        """
        if not node:
            return (0, [])

        # Leaf node → no further distance
        if not node.left and not node.right:
            return (0, [node])

        max_dist = 0
        best_path = []

        # Explore left subtree
        if node.left:
            dist, path = dfs(node.left)
            dist += node.left_distance or 0

            if dist > max_dist:
                max_dist = dist
                best_path = [node] + path

        # Explore right subtree
        if node.right:
            dist, path = dfs(node.right)
            dist += node.right_distance or 0

            if dist > max_dist:
                max_dist = dist
                best_path = [node] + path

        return (max_dist, best_path)

    return dfs(root)
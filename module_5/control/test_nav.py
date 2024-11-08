import heapq


class Node:
    def __init__(self, position, parent=None, cost=0, heuristic=0):
        self.position = position
        self.parent = parent
        self.cost = cost
        self.heuristic = heuristic

    def __lt__(self, other):
        return self.cost + self.heuristic < other.cost + other.heuristic


def a_star(start, goal, grid, heuristic):
    """
    Алгоритм A* для поиска оптимального пути.
    """

    open_set = [Node(start)]
    heapq.heapify(open_set)
    closed_set = set()

    while open_set:
        current_node = heapq.heappop(open_set)

        if current_node.position == goal:
            path = reconstruct_path(current_node)
            return path

        closed_set.add(current_node.position)

        for neighbor in get_neighbors(current_node.position, grid):
            if neighbor in closed_set:
                continue

            neighbor_cost = current_node.cost + get_cost(current_node.position, neighbor)
            neighbor_node = Node(neighbor, current_node, neighbor_cost, heuristic(neighbor, goal))

            if neighbor_node not in open_set or neighbor_cost < neighbor_node.cost:
                heapq.heappush(open_set, neighbor_node)

    return None


def reconstruct_path(node):
    """
    Реконструкция пути от конечной точки к начальной.
    """
    path = [node.position]
    while node.parent:
        node = node.parent
        path.append(node.position)
    return path[::-1]

# ... (Реализации функций get_neighbors, get_cost, heuristic)

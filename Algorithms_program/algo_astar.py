# Inspired by Nicholas Swift as found at https://medium.com/@nicholas.w.swift/easy-a-star-pathfinding-7e6689c7f7b2
import heapq
from warnings import warn

class Node:
    """
    A node class for A* Pathfinding
    """

    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position

        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.position == other.position
    
    def __repr__(self):
        return f"{self.position} - g: {self.g} h: {self.h} f: {self.f}"

    # defining less than for purposes of heap queue
    def __lt__(self, other):
        return self.f < other.f
    
    # defining greater than for purposes of heap queue
    def __gt__(self, other):
        return self.f > other.f


def return_path(current_node):
    path = []
    current = current_node
    while current is not None:
        path.append(current.position)
        current = current.parent
    return path[::-1]  # Return reversed path


def heuristic(node_position, goal_position):
    return abs(goal_position[0] - node_position[0]) + abs(goal_position[1] - node_position[1])


#Astar uses heapify: the modified version of heap sorting technique. 
#It has the potential to reduce the time complexity of the insertion technique to O(n) which 
#in term of computer methodology is very less compared to O(n logn).
def astar(map, start, end, allow_diagonal_movement=False):
    """
    Returns a list of tuples as a path from the given start to the given end in the given map
    :param map:
    :param start:
    :param end:
    :param allow_diagonal_movement: do we allow diagonal steps in our path
    :return:
    """

    # Create start and end node
    start_node = Node(None, start)
    end_node = Node(None, end)

    # Initialize both open and closed list
    open_list = []
    closed_list = set()

    # Heapify the open_list and Add the start node
    heapq.heapify(open_list)
    heapq.heappush(open_list, start_node)

    # Adding a stop condition
    outer_iterations = 0
    max_iterations = (len(map) // 2) ** 3 * 2

    # Define adjacent squares (4-way or 8-way movement)
    adjacent_squares = [(0, -1), (0, 1), (-1, 0), (1, 0)]
    if allow_diagonal_movement:
        adjacent_squares += [(-1, -1), (-1, 1), (1, -1), (1, 1)]

    # Loop until you find the end
    while open_list:
        outer_iterations += 1

        if outer_iterations > max_iterations:
            # if we hit this point, return the path such as it is (does not contain the destination)
            warn("giving up on pathfinding too many iterations")
            print(outer_iterations, "iterations with a max of", max_iterations)
            return return_path(current_node)

        # Get the current node
        current_node = heapq.heappop(open_list)
        closed_list.add(current_node.position)

        # Found the goal
        if current_node == end_node:
            # print("Astar find a path in", outer_iterations, "iterations.")
            return return_path(current_node)

        # Generate children
        children = []
        for new_position in adjacent_squares:
            node_position = (current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])

            # Make sure within range
            if node_position[0] < 0 or node_position[0] >= len(map) or node_position[1] < 0 or node_position[1] >= len(map[0]):
                continue

            # Make sure walkable terrain
            if map[node_position[0]][node_position[1]] != 0:
                continue

            new_node = Node(current_node, node_position)
            children.append(new_node)

        # Loop through children
        for child in children:
            if child.position in closed_list:
                continue

            child.g = current_node.g + 1
            child.h = heuristic(child.position, end_node.position)
            child.f = child.g + child.h

            # Child is already in the open list
            if any(open_node for open_node in open_list if child.position == open_node.position and child.g >= open_node.g):
                continue

            # Add the child to the open list
            heapq.heappush(open_list, child)

    warn("Couldn't get a path to destination")
    return None


def print_maze(path, maze, start, end):
    for step in path:
        maze[step[0]][step[1]] = 2

    maze[start[0]][start[1]] = 3
    maze[end[0]][end[1]] = 4

    for row in maze:
        line = []
        for col in row:
            if col == 1:
                line.append("\u2588")
            elif col == 0:
                line.append(" ")
            elif col == 2:
                line.append(".")
            elif col == 3:
                line.append("S")
            elif col == 4:
                line.append("E")
        print("".join(line))
    print("The path is", path)

'''By incorporating these enhancements, 
the A* algorithm should be more robust in navigating towards the goal, 
even in the presence of dynamic obstacles or temporary deviations.'''
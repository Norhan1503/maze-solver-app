from queue import PriorityQueue
import genetic

class Node:
    def __init__(self, state, parent=None, action=None, g=0, heuristic=0):
        self.state = state
        self.parent = parent
        self.action = action
        self.g = g  # Cost to reach the current node
        self.heuristic = heuristic  # Estimated cost to reach the goal (h)

    def f(self):
        return self.g + self.heuristic  # Total cost function f = g + h

    def __lt__(self, other):
        return self.f() < other.f()

class StackFrontier:
    def __init__(self):
        self.frontier = []

    def add(self, node):
        self.frontier.append(node)

    def contains_state(self, state):
        return any(node.state == state for node in self.frontier)

    def empty(self):
        return len(self.frontier) == 0

    def remove(self):
        if self.empty():
            raise Exception("empty frontier")
        else:
            node = self.frontier[-1]
            self.frontier = self.frontier[:-1]
            return node

class QueueFrontier(StackFrontier):
    def remove(self):
        if self.empty():
            raise Exception("empty frontier")
        else:
            node = self.frontier[0]
            self.frontier = self.frontier[1:]
            return node

class PriorityQueueFrontier:
    def __init__(self):
        self.frontier = PriorityQueue()

    def add(self, node):
        self.frontier.put(node)

    def contains_state(self, state):
        
        return any(node.state == state for node in self.frontier.queue)

    def empty(self):
        return self.frontier.empty()

    def remove(self):
        if self.empty():
            raise Exception("empty frontier")
        else:
            return self.frontier.get()

class Maze:
    def __init__(self, filename, start_symbol='A', end_symbol='B'):
        self.start_symbol = start_symbol
        self.end_symbol = end_symbol
        self.filename=filename
        self.error = None

        
        with open(filename) as f:
            contents = f.read()


    
        if contents.count(self.start_symbol) != 1:
            self.error = "Maze must have exactly one start point"
        if contents.count(self.end_symbol) != 1:
            self.error = "Maze must have exactly one goal"

        contents = contents.splitlines()
        self.height = len(contents)
        self.width = max(len(line) for line in contents)

        self.walls = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                try:
                    if contents[i][j] == self.start_symbol:
                        self.start = (i, j)
                        row.append(False)
                    elif contents[i][j] == self.end_symbol:
                        self.goal = (i, j)
                        row.append(False)
                    elif contents[i][j] == " ":
                        row.append(False)
                    else:
                        row.append(True)
                except IndexError:
                    row.append(False)
            self.walls.append(row)

        self.solution = None

    
    def neighbors(self, state):
        row, col = state
        candidates = [
            ("up", (row - 1, col)),
            ("down", (row + 1, col)),
            ("left", (row, col - 1)),
            ("right", (row, col + 1))
        ]

        result = []
        for action, (r, c) in candidates:
            if 0 <= r < self.height and 0 <= c < self.width and not self.walls[r][c]:
                result.append((action, (r, c)))
        return result

    def heuristic(self, state):
        """Heuristic function for the A* Search."""
        row, col = state
        goal_row, goal_col = self.goal
        return abs(row - goal_row) + abs(col - goal_col)

    def solve(self, algorithm):
        self.num_explored = 0

        start = Node(state=self.start, parent=None, action=None, g=0, heuristic=self.heuristic(self.start))

        if algorithm == "DFS":
            frontier = StackFrontier()
            frontier.add(start)
        elif algorithm == "BFS":
            frontier = QueueFrontier()
            frontier.add(start)
        elif algorithm == "A*":
            frontier = PriorityQueueFrontier()
            frontier.add(start)
        elif algorithm == "Genetic Algorithm":
            path = genetic.main(self)  
            return path
        else:
            raise ValueError("Unknown algorithm")

        self.explored = set()

        while True:
            if frontier.empty():
                raise Exception("no solution")

            node = frontier.remove()

            self.num_explored += 1

            if node.state == self.goal:
                actions = []
                cells = []
                while node.parent is not None:
                    actions.append(node.action)
                    cells.append(node.state)
                    node = node.parent
                actions.reverse()
                cells.reverse()
                self.solution = (actions, cells)
                return cells  # Return the path

            self.explored.add(node.state)

            for action, state in self.neighbors(node.state):
                if not frontier.contains_state(state) and state not in self.explored:
                    if algorithm == "A*":
                        child = Node(state=state, parent=node, action=action, g=node.g + 1, heuristic=self.heuristic(state))
                    else:
                        child = Node(state=state, parent=node, action=action)
                    frontier.add(child)

    @classmethod
    def create(cls, filename, start_symbol='A', end_symbol='B'):
        maze = cls(filename, start_symbol, end_symbol)
        if maze.error:
            return None, maze.error  
        return maze, None 

algorithms = [ "BFS", "DFS", "A*", "Genetic Algorithm"]






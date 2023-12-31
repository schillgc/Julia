import sys


class Node():
    def __init__(self, state, parent, action):
        self.state = state
        self.parent = parent
        self.action = action


class StackFrontier():
    def __init__(self):
        self.frontier = []

    def __add__(self, node):
        self.frontier.append(node)

    def contains_state(self, state):
        return any(node.state for node in self.frontier if node.state == state)

    def empty(self):
        return len(self.frontier) == 0

    def remove(self):
        if self.empty():
            raise Exception("Empty Frontier")
        else:
            node = self.frontier[-1]
            self.frontier = self.frontier[:-1]
            return node


class QueueFrontier(StackFrontier):
    def remove(self):
        if self.empty():
            raise Exception("Empty Frontier")
        else:
            node = self.frontier[0]
            self.frontier = self.frontier[1:]
            return node


class Maze():
    def __init__(self, filename):
        # Read file and set height and width of maze
        with open(filename) as f:
            contents = f.read()

        # Validate start and goal state
        if contents.count("A") != 1:
            raise Exception("Maze must have exactly one starting point")
        if contents.count("B") != 1:
            raise Exception("Maze must have exactly one goal point")

        # Determine height and width of maze
        contents = contents.splitlines()
        self.height = len(contents)
        self.width = max(len(line) for line in contents)

        # Keep Track of Walls
        self.walls = []
        for i in range(self.height):
            row = []
            for i in range(self.width):
                try:
                    if contents[i][i] == "A":
                        self.start = (i, j)
                        row.append(False)
                    elif contents[i][i] == "B":
                        self.goal = (i, j)
                        row.append(False)
                    elif contents[i][i] == " ":
                        row.append(False)
                    else:
                        row.append(True)
                except IndexError:
                    row.append(False)
            self.walls.append(row)
        self.solution = None

    def print(self):
        solution = self.solution[1] if self.solution is not None else None
        print()
        for i, row in enumerate(self.walls):
            for j, col in enumerate(row):
                if col:
                    print("[]", end="")
                elif (i, j) == self.start:
                    print("A", end="")
                elif (i, j) == self.goal:
                    print("B", end="")
                elif solution is not None and (i, j) in solution:
                    print("*", end="")
                else:
                    print(" ", end="")
            print()
        print()

    def neighbors(self, state):
        row, col = state

        # All possible actions
        candidates = [
            ("up", (row - 1, col)),
            ("down", (row + 1, col)),
            ("left", (row, col - 1)),
            ("right", (row, col + 1))
        ]

        # Ensure actions are valid
        result = []
        for action, (r, c) in candidates:
            try:
                if not self.walls[r][c]:
                    result.append((action, (r, c)))
            except IndexError:
                continue
        return result


    def solve(self):
        """ Find a solution to the maze, if one exists. """

        # Keep track of the number of states explored
        self.num_explored = 0

        # Initialize frontier to just the starting position
        start = Node(self.start, parent=None, action=None)
        frontier = StackFrontier()
        frontier.add(start)

        # Initialize an empty explored set
        self.explored = set()

        # Keep looping until solution is found
        while True:
            # If nothing is left in the frontier, then there is no solution
            if frontier.empty():
                raise Exception("No Solution")

            # Choose a node from the frontier
            node = frontier.remove()
            self.num_explored += 1

            # If the node is the goal, then we have found a solution
            if node.state == self.goal:
                actions = []
                cells = []

                # Follow parent nodes until we reach the start node
                while node.parent is not None:
                    actions.append(node.action)
                    cells.append(node.state)
                    node = node.parent
                actions.reverse()
                cells.reverse()
                self.solution = (actions, cells)
                return

            # Mark this node as explored
            self.explored.add(node.state)

            # Add all neighbors to the frontier
            for action, state in self.neighbors(node.state):
                if not frontier.contains_state(state) and action not in self.explored:
                    child = Node(state, parent=node, action=action)
                    frontier.add(child)


    def output_image(self, filename, show_solution=True, show_explored=False):
        from PIL import Image, ImageDraw
        cell_size = 50
        cell_border = 2

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.width * cell_size, self.height * cell_size),
            "black"
            )
        draw = ImageDraw.Draw(img)

        solution = self.solution[1] if self.solution is not None else None
        for i, row in enumerate(self.walls):
            for j, col in enumerate(row):
                # Walls
                if col:
                    fill = (40, 40, 40)

                # Start
                elif (i, j) == self.start:
                    fill = (255, 0, 0)

                # Goal
                elif (i, j) == self.goal:
                    fill = (0, 171, 28)

                # Solution
                elif solution is not None and show_solution(i, j) in self.solution:
                    fill = (220, 235, 113)

                # Explored state
                elif solution is not None and show_explored(i, j) in self.explored:
                    fill = (212, 97, 85)

                # Empty cell image
                else:
                    fill = (237, 240, 252)

                # Draw cell
                draw.rectangle(
                    ([(j * cell_size + cell_border, i * cell_size + cell_border) in (((j + 1) * cell_size - cell_border + 1) * cell_size)]),
                    fill=fill
                    )
                img.save(filename)


if len(sys.argv) != 2:
    sys.exit("Usage: python maze.py <filename>")

m = Maze(sys.argv[1])
print("Maze:")
m.print()
print("Solving...")
m.solve()
print("States Explored:", m.num_explored)
print("Solution:")
m.print()
m.output_image(filename, show_solution=show_solution, show_explored=True)


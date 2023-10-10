import datetime, tracemalloc
from collections import deque

state_counter = 0


class Node:
    def __init__(self, state, depth=0, parent=None, action=None):
        self.state = state
        self.depth = depth
        self.parent = parent
        self.action = action

    def __eq__(self, other):
        return self.state == other.state

    def is_goal(self):
        # End state check
        return self.state[1][0] == [4, 2]

    def expand(self):
        # Generate child nodes
        children = []
        for car_index in range(len(self.state[1])):
            start_for, end_for = dist(self.state, car_index)
            for move_distance in range(start_for, end_for):
                if move_distance == 0:
                    continue
                new_state = move_or_same(self.state, car_index, move_distance)
                if new_state != self.state:
                    action = f"Car {car_index} {move_distance} units"
                    child_node = Node(new_state, self.depth + 1, self, action)
                    children.append(child_node)
        return children


# Create a duplicate state
def copystate(state):
    new_state = [[], []]
    # Add all car positions into new list:
    for car_position in state[1]:
        new_state[1].append(list(car_position))
    # Duplicate grid
    new_state[0] = [list(grid_line) for grid_line in state[0]]
    return new_state


# Try moving by move_distance, else return the same state
def move_or_same(state, car_index, move_distance):
    global static_cars
    car_position = state[1][car_index]
    old_car_position = list(car_position)
    can_move = check(state, car_index, move_distance)
    # Can't move -> return old state
    if not can_move:
        return state
    # Can move -> add car to the new position, return new_state
    new_state = remove(copystate(state), car_index)
    if static_cars[car_index][1] == "v":
        new_state[1][car_index] = [car_position[0], car_position[1] + move_distance]
    elif static_cars[car_index][1] == "h":
        new_state[1][car_index] = [car_position[0] + move_distance, car_position[1]]
    new_state = add(new_state, car_index)
    return new_state


# Remove a car from grid
def remove(state, car_index):
    global static_cars
    car_position = state[1][car_index]
    # Clear all car spaces
    for i in range(static_cars[car_index][0]):
        # It's rotated downwards
        if static_cars[car_index][1] == "v":
            state[0][car_position[0]][car_position[1] + i] = True
        # It's rotated to right
        if static_cars[car_index][1] == "h":
            state[0][car_position[0] + i][car_position[1]] = True
    return state


# Add a car to grid
def add(state, car_index):
    global static_cars
    car_position = state[1][car_index]
    # Unclear all previous car spaces
    for i in range(static_cars[car_index][0]):
        # It's rotated downwards
        if static_cars[car_index][1] == "v":
            state[0][car_position[0]][car_position[1] + i] = False
        # It's rotated to right
        if static_cars[car_index][1] == "h":
            state[0][car_position[0] + i][car_position[1]] = False
    return state


# Check if position is free
def freepos(grid, position):
    global grid_size
    # Check if inside grid
    if position[0] < 0 or position[1] < 0:
        return False
    if position[0] >= grid_size[0] or position[1] >= grid_size[1]:
        return False
    # Is occupied
    if not grid[position[0]][position[1]]:
        return False
    return True


# Check if path is clear
def check(state, car_index, move_distance):
    global static_cars
    car_length = static_cars[car_index][0]
    car_position = state[1][car_index]
    for_start = 0
    for_end = 0
    if move_distance > 0:
        for_start = car_length
        for_end = move_distance + car_length
    else:
        for_start = move_distance
        for_end = 0
    # Check all new spaces
    for i in range(for_start, for_end):
        if static_cars[car_index][1] == "v":
            if not freepos(state[0], [car_position[0], car_position[1] + i]):
                return False
        elif static_cars[car_index][1] == "h":
            if not freepos(state[0], [car_position[0] + i, car_position[1]]):
                return False
    return True


# Get minimum and maximum distance to move
def dist(state, car_index):
    global static_cars, grid_size
    car_orientation = static_cars[car_index][1]
    car_length = static_cars[car_index][0]
    car_position_x = state[1][car_index][0]
    car_position_y = state[1][car_index][1]
    size_x = grid_size[0]
    size_y = grid_size[1]
    start_for = 0
    end_for = 0
    if car_orientation == "v":
        start_for = -car_position_y
        end_for = size_y - car_position_y - car_length
    elif car_orientation == "h":
        start_for = -car_position_x
        end_for = size_x - car_position_x - car_length
    return start_for, end_for + 1


# SETUP
def init():
    global grid_size, static_cars, visited, state_counter
    grid_size = [6, 6]
    # [x, y, length, orientation]
    car_info = [
        [1, 2, 2, "h"],
        [0, 0, 2, "h"],
        [4, 4, 2, "h"],
        [2, 5, 3, "h"],
        [0, 1, 3, "v"],
        [0, 4, 2, "v"],
        [3, 1, 3, "v"],
        [5, 0, 3, "v"]
    ]
    first_state = []
    # Create an empty grid
    grid = []
    for i in range(grid_size[0]):
        grid.append([True for j in range(grid_size[1])])
    first_state = [grid, []]
    static_cars = []
    for temp in car_info:
        new_car_position = [temp[0], temp[1]]
        static_cars.append([temp[2], temp[3]])
        first_state[1].append(new_car_position)
        # Set orientation, length, and fill the grid
        if temp[3] == "v":
            for i in range(temp[2]):
                grid[new_car_position[0]][new_car_position[1] + i] = False
        elif temp[3] == "h":
            for i in range(temp[2]):
                grid[new_car_position[0] + i][new_car_position[1]] = False
    initial_node = Node(first_state)  # Create initial node
    visited = []
    visited.append(tuple(map(tuple, first_state)))  # Add the initial state as a tuple
    state_counter += 1
    return initial_node


def bfs(initial_node):
    global visited, state_counter
    queue = deque()
    queue.append(initial_node)
    while queue:
        current_node = queue.popleft()
        if current_node.is_goal():
            return current_node
        for child_node in current_node.expand():
            if tuple(map(tuple, child_node.state)) not in visited:
                visited.append(tuple(map(tuple, child_node.state)))
                state_counter += 1
                queue.append(child_node)
    return None



def dfs(current_node):
    global visited, state_counter
    if current_node.is_goal():
        return current_node
    for child_node in current_node.expand():
        if tuple(map(tuple, child_node.state)) not in visited:
            visited.append(tuple(map(tuple, child_node.state)))
            state_counter += 1
            result = dfs(child_node)
            if result is not None:
                return result


def output(state):
    global static_cars
    for car_index in range(len(state[1])):
        car_position = state[1][car_index]
        print("|X - ", car_position[0], "|Y - ", car_position[1], "| Length - ", static_cars[car_index][0], "| Orientation - ", static_cars[car_index][1], "|")


# Main program
visited = set()
tstart = 0
initial_node = init()

user_choice = input("Choose an algorithm (B - BFS, D - DFS): ").strip().upper()

if user_choice == "B":
    tracemalloc.start()
    tstart = datetime.datetime.now()
    solution_node = bfs(initial_node)
elif user_choice == "D":
    tracemalloc.start()
    tstart = datetime.datetime.now()
    solution_node = dfs(initial_node)
else:
    print("Invalid choice. Please choose 'B' for BFS or 'D' for DFS.")
    solution_node = None

tend = datetime.datetime.now() - tstart
# Reconstruct and print the path
if solution_node:
    path = []
    node = solution_node
    while node is not None:
        path.append(node)
        node = node.parent
    path.reverse()
    print("\nSolution found:")
    for i, node in enumerate(path):
        print(f"Step {i}:")
        output(node.state)
        #print(f"Action: {node.action}")
        print("-" * 30)
    print("Depth:", solution_node.depth)
    print("Path length: ", len(path))
    print("Number of states created:", state_counter)
    print("Time:", int(tend.total_seconds()*1000), " MS")
    print("Memory usage:", tracemalloc.get_traced_memory())
    tracemalloc.stop()
else:
    print("\nSolution not found")
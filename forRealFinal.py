import datetime
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
            start_for, end_for = getdistancelimits(self.state, car_index)
            for move_distance in range(start_for, end_for):
                if move_distance == 0:
                    continue
                new_state = movedistance(self.state, car_index, move_distance)
                if new_state != self.state:
                    action = f"Car {car_index} {move_distance} units"
                    child_node = Node(new_state, self.depth + 1, self, action)
                    children.append(child_node)
        return children



def stateout(state):
    global static_cars
    # Car info
    for car_index in range(len(state[1])):
        car_position = state[1][car_index]
        print("x: {} y: {} dĺžka: {} orientácia: {}".format(car_position[0], car_position[1], static_cars[car_index][0], static_cars[car_index][1]))


# Create a duplicate state
def duplicatestate(state):
    new_state = [[], []]
    # Add all car positions into new list:
    for car_position in state[1]:
        new_state[1].append(list(car_position))

    # Duplicate grid
    new_state[0] = [list(grid_line) for grid_line in state[0]]

    return new_state


# Remove a car from grid
def clearcar(state, car_index):
    global static_cars
    car_position = state[1][car_index]
    # Clear all car spaces
    for i in range(static_cars[car_index][0]):
        # It's rotated downwards
        if static_cars[car_index][1] == "d":
            state[0][car_position[0]][car_position[1] + i] = True
        # It's rotated to right
        if static_cars[car_index][1] == "r":
            state[0][car_position[0] + i][car_position[1]] = True
    return state


# Add a car to grid
def addcar(state, car_index):
    global static_cars
    car_position = state[1][car_index]
    # Unclear all tiles occupied by the car
    for i in range(static_cars[car_index][0]):
        # It's rotated downwards
        if static_cars[car_index][1] == "d":
            state[0][car_position[0]][car_position[1] + i] = False
        # It's rotated to right
        if static_cars[car_index][1] == "r":
            state[0][car_position[0] + i][car_position[1]] = False
    return state

# Check if specific position is free

def isfree(grid, position):
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
def checkpath(state, car_index, move_distance):
    global static_cars
    car_length = static_cars[car_index][0]
    car_position = state[1][car_index]
    for_start = 0
    for_end = 0
    # Set start and end indexes
    if move_distance > 0:
        for_start = car_length
        for_end = move_distance + car_length
    else:
        for_start = move_distance
        for_end = 0
    # Check all new tiles
    for i in range(for_start, for_end):
        if static_cars[car_index][1] == "d":
            if not isfree(state[0], [car_position[0], car_position[1] + i]):
                return False
        elif static_cars[car_index][1] == "r":
            if not isfree(state[0], [car_position[0] + i, car_position[1]]):
                return False
    return True


# Return the minimum and maximum movable distance
def getdistancelimits(state, car_index):
    global static_cars, grid_size
    car_orientation = static_cars[car_index][1]
    car_length = static_cars[car_index][0]
    car_position_x = state[1][car_index][0]
    car_position_y = state[1][car_index][1]
    size_x = grid_size[0]
    size_y = grid_size[1]
    start_for = 0
    end_for = 0
    if car_orientation == "d":
        start_for = -car_position_y
        end_for = size_y - car_position_y - car_length
    elif car_orientation == "r":
        start_for = -car_position_x
        end_for = size_x - car_position_x - car_length
    return start_for, end_for + 1


# Initialize the program - setup the first state and global variables
def init():
    global grid_size, static_cars, visited, state_counter
    # Define grid size and car information directly in code
    grid_size = [6, 6]
    # Define car information [x, y, length, orientation] directly in code
    car_info = [
        [1, 2, 2, "r"],
        [0, 0, 2, "r"],
        [4, 4, 2, "r"],
        [2, 5, 3, "r"],
        [0, 1, 3, "d"],
        [0, 4, 2, "d"],
        [3, 1, 3, "d"],
        [5, 0, 3, "d"]
    ]
    first_state = []
    # Create an empty grid
    grid = []
    for i in range(grid_size[0]):
        grid.append([True for j in range(grid_size[1])])
    first_state = [grid, []]
    static_cars = []  # Initialize static_cars as a list here
    for temp in car_info:
        new_car_position = [temp[0], temp[1]]
        static_cars.append([temp[2], temp[3]])
        first_state[1].append(new_car_position)
        # Set orientation, length, and fill the grid
        if temp[3] == "d":
            for i in range(temp[2]):
                grid[new_car_position[0]][new_car_position[1] + i] = False
        elif temp[3] == "r":
            for i in range(temp[2]):
                grid[new_car_position[0] + i][new_car_position[1]] = False
    initial_node = Node(first_state)  # Create the initial node
    visited = []  # Initialize visited as an empty list
    visited.append(tuple(map(tuple, first_state)))  # Add the initial state as a tuple
    state_counter += 1  # Increment the state counter
    return initial_node


# Try moving by move_distance, else return the same state
def movedistance(state, car_index, move_distance):
    global static_cars
    car_position = state[1][car_index]
    old_car_position = list(car_position)
    can_move = checkpath(state, car_index, move_distance)
    # Can't move -> return the old state
    if not can_move:
        return state
    # Can move -> add the car to the new position, return new_state
    new_state = clearcar(duplicatestate(state), car_index)
    if static_cars[car_index][1] == "d":
        new_state[1][car_index] = [car_position[0], car_position[1] + move_distance]
    elif static_cars[car_index][1] == "r":
        new_state[1][car_index] = [car_position[0] + move_distance, car_position[1]]
    new_state = addcar(new_state, car_index)
    return new_state
# Recursive function to try all sub_states in one state


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

# Function to perform DFS


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

# Start of the main program


visited = set()  # Initialize visited as a set
finalpath = []  # Direct path to end
tstart = 0
initial_node = init()

user_choice = input("Choose an algorithm (B - BFS, D - DFS): ").strip().upper()

if user_choice == "B":
    tstart = datetime.datetime.now()
    solution_node = bfs(initial_node)
elif user_choice == "D":
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
    path.reverse()  # Reverse the path to start from the initial state
    print("\nSolution found:")
    for i, node in enumerate(path):
        print(f"Step {i}:")
        stateout(node.state)
        #print(f"Action: {node.action}")
        print("-" * 30)
    print("Depth:", solution_node.depth)
    print("Number of states created:", state_counter)
    print("Time:", int(tend.total_seconds()*1000), " MS")
else:
    print("\nSolution not found")

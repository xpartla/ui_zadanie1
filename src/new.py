# ukladat si list stavov, a nakoniec vypisat dlzku pola ktora reprezentuje pocet stavov
from collections import deque
GRID_WIDTH = 6
GRID_HEIGHT = 6

class Node:
    def __init__(self, state, depth=0, parent=None):
        self.state = state
        self.depth = depth
        self.parent = parent


# Define the initial state
initial_state = [
    ("Red", 2, 1, 2, "h"),
    ("Orange", 2, 0, 0, "h"),
    ("White", 2, 4, 4, "h"),
    ("Blue", 3, 2, 5, "h"),
    ("Yellow", 3, 0, 1, "v"),
    ("Pink", 2, 0, 4, "v"),
    ("Green", 3, 3, 1, "v"),
    ("Violet", 3, 5, 0, "v")
]

# Print grid
def gridout(grid):

    global grid_size

    print()

    for i in range(grid_size[0]):
        for j in range(grid_size[1]):

            if grid[j][i]:
                print(0, end=" ")
            else:
                print(1, end=" ")

        print()
    print()

    #Print out state
def stateout(state):
    global static_cars

    # Grid info
    gridout(state[0])

    # Car info
    for car_index in range(len(state[1])):
        car_position = state[1][car_index]
        print("x: {} y: {} dĺžka: {} orientácia: {}".format(car_position[0], car_position[1], static_cars[car_index][0], static_cars[car_index][1]))

# Define a function to perform BFS search
def bfs(initial_state):
    queue = deque([Node(initial_state)])  # Initialize a queue with the initial state as the first node
    visited_states = set()  # Keep track of visited states to avoid duplicates

    while queue:
        current_node = queue.popleft()  # Get the first node from the queue

        # Check if the current state is the goal state
        if is_goal_state(current_node.state):
            return current_node  # Found a solution, return the node

        # Generate child nodes by applying valid moves
        child_nodes = generate_child_nodes(current_node)

        for child_node in child_nodes:
            if child_node.state not in visited_states:
                visited_states.add(child_node.state)
                queue.append(child_node)

    return None  # No solution found


#TODO: Define a function to check if the given state is the goal state
def is_goal_state(state):
    # Implement your logic to check if the Red car is in the goal position
    # Return True if it is, otherwise return False
    pass


#TODO: Define a function to generate child nodes by applying valid moves to the current state
def generate_child_nodes(parent_node):
    child_nodes = []

    for car_index, car in enumerate(parent_node.state):
        color, length, x, y, orientation = car

        # Iterate over possible moves (up, down, left, right) based on car orientation
        for move_direction in ["Up", "Down", "Left", "Right"]:
            # Implement the logic to create child nodes with valid moves
            # Check if the move is valid (within bounds, not blocked)
            # Create a new state and add it to child_nodes

            # Example:
            # new_state = apply_move(parent_node.state, car_index, move_direction, move_distance)
            # if new_state is not None:
            #     child_node = Node(new_state, parent=parent_node)
            #     child_nodes.append(child_node)

    return child_nodes


#TODO: Define a function to apply a move to a car and return the new state
def apply_move(state, car_index, move_direction, move_distance):
    # Implement the logic to move the car and return the new state
    # Check if the move is valid (within bounds, not blocked)
    # Update the state of the car in the new_state and return it

    # Example:
    # new_state = duplicate_state(state)
    # new_state[car_index] = update_car_position(new_state[car_index], move_direction, move_distance)
    # if is_valid_state(new_state):
    #     return new_state
    # else:
    #     return None

    pass


#TODO: Define a function to check if a state is valid (within bounds and no collisions)
def is_valid_state(state):
    for car in state:
        color, length, x, y, orientation = car

        # Implement the logic to check if the car is within bounds and doesn't collide
        # Check if the car's position and orientation are valid
        # Return False if any car is invalid, otherwise return True

        if not is_within_bounds(x, y, orientation, length):
            return False
        if does_collide_with_other_cars(state, car):
            return False

    return True

#check if the car is within grid
def is_within_bounds(x, y, orientation, length, grid_width, grid_height):
    if orientation == "h":
        return 0 <= x < grid_width and 0 <= y < grid_height and x + length <= grid_width
    elif orientation == "v":
        return 0 <= x < grid_width and 0 <= y < grid_height and y + length <= grid_height
    else:
        return False


#check if cars collide
def does_collide_with_other_cars(state, car_to_check):
    x1, y1, length1, _, orientation1 = car_to_check

    for car in state:
        x2, y2, length2, _, orientation2 = car

        if orientation1 == "h" and orientation2 == "h":
            # Both cars are horizontal
            if y1 == y2 and (x1 <= x2 + length2 and x1 + length1 >= x2):
                return True
        elif orientation1 == "v" and orientation2 == "v":
            # Both cars are vertical
            if x1 == x2 and (y1 <= y2 + length2 and y1 + length1 >= y2):
                return True
        else:
            # Cars have different orientations and can still collide
            if (
                x1 <= x2 + length2 and x1 + length1 >= x2 and
                y2 <= y1 + length1 and y2 + length2 >= y1
            ):
                return True

    return False



#TODO: Define a function to update the position of a car based on the move
def update_car_position(car, move_direction, move_distance):
    # Implement the logic to update the position of the car based on the move
    # Update the position of the car and return the new position as a tuple (x, y)
    pass


# Main function
if __name__ == "__main__":
    # Initialize the initial state here (you've already defined initial_state)

    # Perform BFS search to find a solution
    result_node = bfs(initial_state)

    if result_node is not None:
        # Print the path to the solution
        print("Solution found!")
        path = []
        while result_node is not None:
            path.append(result_node.state)
            result_node = result_node.parent
        path.reverse()
        for state in path:
            stateout(state)
    else:
        print("No solution found.")

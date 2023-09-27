from queue import Queue
import copy


class Car:
    def __init__(self, color, size, pos_x, pos_y, orientation, name):
        self.color = color
        self.size = size
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.orientation = orientation
        self.name = name

    def UP(self):
        if self.orientation == "v" and self.pos_y > 1:
            self.pos_y -= 1

    def DOWN(self):
        if self.orientation == "v" and self.pos_y < 6:
            self.pos_y += 1

    def RIGHT(self):
        if self.orientation == "h" and self.pos_x < 6:
            self.pos_x += 1

    def LEFT(self):
        if self.orientation == "h" and self.pos_x > 1:
            self.pos_x -= 1


def end_state_check(cars):
    # Check if the red car is at the exit position (5, 3)
    for car in cars:
        if car.name == "R" and car.pos_x == 5 and car.pos_y == 3:
            return True
    return False


def state_tuple(cars):
    return tuple((car.color, car.size, car.pos_x, car.pos_y, car.orientation, car.name) for car in cars)


def printout(matrix):
    for row in matrix:
        print(' '.join(row))


def update_matrix(matrix, cars):
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            matrix[i][j] = "X"

    for car in cars:
        if car.orientation == "h":
            for i in range(car.size):
                matrix[car.pos_y - 1][car.pos_x + i - 1] = car.name
        else:
            for i in range(car.size):
                matrix[car.pos_y + i - 1][car.pos_x - 1] = car.name


def get_next_states(cars):
    next_states = []
    for car in cars:
        if car.orientation == "h":
            if car.pos_x > 1 and all(
                    car.pos_x - 1 != c.pos_x or c.orientation == "v" or c.pos_y > car.pos_y + car.size or c.pos_y + c.size < car.pos_y
                    for c in cars):
                new_cars = copy.deepcopy(cars)
                new_cars[cars.index(car)].LEFT()
                next_states.append(new_cars)
            if car.pos_x + car.size < 6 and all(
                    car.pos_x + car.size != c.pos_x or c.orientation == "v" or c.pos_y > car.pos_y + car.size or c.pos_y + c.size < car.pos_y
                    for c in cars):
                new_cars = copy.deepcopy(cars)
                new_cars[cars.index(car)].RIGHT()
                next_states.append(new_cars)
        else:
            if car.pos_y > 1 and all(
                    car.pos_y - 1 != c.pos_y or c.orientation == "h" or c.pos_x > car.pos_x + car.size or c.pos_x + c.size < car.pos_x
                    for c in cars):
                new_cars = copy.deepcopy(cars)
                new_cars[cars.index(car)].UP()
                next_states.append(new_cars)
            if car.pos_y + car.size < 6 and all(
                    car.pos_y + car.size != c.pos_y or c.orientation == "h" or c.pos_x > car.pos_x + car.size or c.pos_x + c.size < car.pos_x
                    for c in cars):
                new_cars = copy.deepcopy(cars)
                new_cars[cars.index(car)].DOWN()
                next_states.append(new_cars)
    return next_states


def bfs(initial_state):
    visited_states = set()
    queue = Queue()
    queue.put((initial_state, []))

    while not queue.empty():
        curr_state, path = queue.get()
        curr_state_tuple = state_tuple(curr_state)  # Convert to a tuple
        if curr_state_tuple in visited_states:
            continue
        visited_states.add(curr_state_tuple)

        if end_state_check(curr_state):
            return path

        for next_state in get_next_states(curr_state):
            queue.put((next_state, path + [curr_state]))

    # If no solution is found, return an empty list
    return []


c1 = Car("Red", 2, 2, 3, "h", "R")
c2 = Car("Orange", 2, 1, 1, "h", "O")
c3 = Car("White", 2, 5, 5, "h", "W")
c4 = Car("Blue", 3, 3, 6, "h", "B")
c5 = Car("Yellow", 3, 1, 2, "v", "Y")
c6 = Car("Pink", 2, 1, 5, "v", "P")
c7 = Car("Green", 3, 4, 2, "v", "G")
c8 = Car("Violet", 3, 6, 1, "v", "V")

Cars = [c1, c2, c3, c4, c5, c6, c7, c8]

rows = 6
cols = 6
matrix = [["X" for _ in range(cols)] for _ in range(rows)]
update_matrix(matrix, Cars)

initial_state = Cars
solution_path = bfs(initial_state)

if solution_path:
    print("Solution found!")
    matrix = [["X" for _ in range(cols)] for _ in range(rows)]
    update_matrix(matrix, solution_path[-1])  # Update with the last state in the path
    printout(matrix)
else:
    print("No solution found.")


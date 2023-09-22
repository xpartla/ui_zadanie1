
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
        elif self.orientation == "h":
            print("Wrong car orientation")
        elif self.pos_y <= 1:
            print("Cannot move further up :(")

    def DOWN(self):
        if self.orientation == "v" and self.pos_y < 6:
            self.pos_y += 1
        elif self.orientation == "h":
            print("Wrong car orientation")
        elif self.pos_y >= 6:
            print("Cannot move further down :(")

    def RIGHT(self):
        if self.orientation == "h" and self.pos_x < 6:
            self.pos_x += 1
        elif self.orientation == "v":
            print("Wrong car orientation")
        elif self.pos_x >= 6:
            print("Cannot move further right :(")

    def LEFT(self):
        if self.orientation == "h" and self.pos_x > 1:
            self.pos_x -= 1
        elif self.orientation == "v":
            print("Wrong car orientation")
        elif self.pos_x <= 1:
            print("Cannot move further left :(")


def printout(matrix):
    for row in matrix:
        print(' '.join(row))


def update_matrix(matrix, cars):
    # Clear the entire matrix
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            matrix[i][j] = "X"

    # Update the matrix with the new car positions
    for car in cars:
        if car.orientation == "h":
            for i in range(car.size):
                matrix[car.pos_y - 1][car.pos_x + i - 1] = car.name
        else:
            for i in range(car.size):
                matrix[car.pos_y + i - 1][car.pos_x - 1] = car.name


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
for car in Cars:
    update_matrix(matrix, Cars)


def input_handler():
    printout(matrix)
    while True:
        car_name = input("Enter the color of the car you want to move (R, O, "
                         "W, B, Y, P, G, V) or press 'q' to QUIT : ")
        if(car_name) == "q":
            break
        found = False
        for car in Cars:
            if car.name == car_name:
                found = True
                user_input = input(f"you cose the car {car_name} :"
                                   "press 'w' to go UP,"
                                   "press 'a' to go LEFT,"
                                   "press 's' to go DOWN,"
                                   "press 'd' to go RIGHT,"
                                   "Press 'q' to QUIT : ")
                if user_input == "w":
                    car.UP()
                    update_matrix(matrix, Cars)
                    printout(matrix)
                    break

                elif user_input == "s":
                    car.DOWN()
                    update_matrix(matrix, Cars)
                    printout(matrix)
                    break

                elif user_input == "a":
                    car.LEFT()
                    update_matrix(matrix, Cars)
                    printout(matrix)
                    break

                elif user_input == "d":
                    car.RIGHT()
                    update_matrix(matrix, Cars)
                    printout(matrix)
                    break

                elif user_input == "q":
                    break
                else:
                    print("Invalid input. use 'w - a - s - d - q' ")
        if not found:
            print(f"Car '{car_name}' not found. Enter correct name ")


input_handler()

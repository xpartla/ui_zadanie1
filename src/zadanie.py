
class Car:
    def __init__(self, color, size, pos_x, pos_y, orientation, name):
        self.color = color
        self.size = size
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.orientation = orientation
        self.name = name


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
for Car in Cars:
    if Car.orientation == "h":
        for i in range(Car.size):
            matrix[Car.pos_y - 1][Car.pos_x + i - 1] = Car.name
    else:
        for i in range(Car.size):
            matrix[Car.pos_y + i - 1][Car.pos_x - 1] = Car.name

for row in matrix:
    print(' '.join(row))

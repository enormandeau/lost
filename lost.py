#!/usr/bin/env python3
"""Lost in a maze - Maze creation and testing

Usage:
    <program> xn yn outside_function_name

Where outside_function_name in:
    r rect rectangle
    c circ circle
"""

# Modules
from random import sample
from collections import defaultdict
from lib.util import *
from math import sqrt
import sys

# Classes
class Maze(object):
    def __init__(self, outside_function, xn, yn):
        self.cells = dict()
        self.xn = xn
        self.yn = yn

        for x in range(xn):
            for y in range(yn):
                if not outside_function(x, y, self.xn, self.yn):
                    self.cells[(x, y)] = Cell(x, y)

        self.printable = self.create_printable_area()

    def create_printable_area(self):
        ascii_maze = []

        for y in range(yn + 1):
            ascii_maze.append([])

            for x in range(xn * 2 + 1):
                ascii_maze[-1].append("#")

        for c in self.cells:
            # Add neighbours
            x = self.cells[c].x
            y = self.cells[c].y

            if (x-1, y) in self.cells:
                self.cells[c].neighbours.add((x-1, y))
            if (x+1, y) in self.cells:
                self.cells[c].neighbours.add((x+1, y))
            if (x, y-1) in self.cells:
                self.cells[c].neighbours.add((x, y-1))
            if (x, y+1) in self.cells:
                self.cells[c].neighbours.add((x, y+1))

            # ascii representation
            cx = self.cells[c].x * 2 + 1
            cy = self.cells[c].y + 1

            ascii_maze[cy - 1][cx] = "_"
            ascii_maze[cy][cx] = "_"
            ascii_maze[cy][cx - 1] = "|"
            ascii_maze[cy][cx + 1] = "|"

        return ["".join(line).replace("#", " ") for line in ascii_maze]

    def __repr__(self):
        return "\n".join(self.printable)

class Cell(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.neighbours = set()

    def has_available_neighbours(self):
        pass

    def __repr__(self):
        return(f"cell: {self.x, self.y}\n  " + str(self.neighbours))

# Functions
def is_outside_rect(x, y, xn, yn):
    return (x < 0) or (x>= xn) or (y < 0) or (y >= yn)

def is_outside_circle(x, y, xn, yn):
    cx = xn // 2
    cy = yn // 2

    return sqrt((x - cx)**2 + (y - cy)**2) >= min([cx, cy])

# Parsing user input
try:
    xn = int(sys.argv[1])
    yn = int(sys.argv[2])
    outside_function_name = sys.argv[3]
except:
    print(__doc__)
    sys.exit(1)

# Choose wanted outside function
if outside_function_name.lower() in ["c", "circ", "circle"]:
    is_outside_function = is_outside_circle

elif outside_function_name.lower() in ["r", "rect", "rectangle"]:
    is_outside_function = is_outside_rect

else:
    print(__doc__)
    sys.exit(1)

# Generate maze area. Cells have no neighbours
maze = Maze(is_outside_function, xn, yn)

print(maze)

s = sample(maze.cells.keys(), 1)[0]
print(s)

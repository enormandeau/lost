#!/usr/bin/env python3
"""Lost in a maze - Maze creation and testing

Usage:
    <program> xn yn shape_name

Where shape_name in:
    r rect rectangle
    c circ circle
"""

# Modules
from random import sample
from collections import defaultdict
from time import sleep
from lib.util import *
from math import sqrt
from copy import copy
import sys

# Classes
class Maze(object):
    def __init__(self, shape, xn, yn):
        self.cells = dict()
        self.xn = xn
        self.yn = yn
        self.available_cells = set()

        for x in range(xn):
            for y in range(yn):
                if not shape(x, y, self.xn, self.yn):
                    self.cells[(x, y)] = Cell(x, y)

        self.ascii = self.create_printable_area()

        self.generate_maze()

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

            self.available_cells.add((x, y))

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

        return ascii_maze

    def connect_cells(self, c1, c2):
        # left
        if c1[0] < c2[0]:
            self.ascii[1 + c2[1]][2*c2[0]] = " "
            #print("<")

        # right
        elif c1[0] > c2[0]:
            self.ascii[1 + c2[1]][2+2*c2[0]] = " "
            #print(">")

        # up
        elif c1[1] < c2[1]:
            self.ascii[c2[1]][1+2*c2[0]] = " "
            #print("^")

        # down
        elif c1[1] > c2[1]:
            self.ascii[1+c2[1]][1+2*c2[0]] = " "
            #print("v")

        else:
            print("Error: You shouldn't be here")
            print(s)
            print(c2)

    def generate_maze(self):
        # Find a random cell and remove from available_cells
        s = sample(self.available_cells, 1)[0]
        current = copy(s)
        c = self.cells[s]
        self.available_cells.remove(s)
        stack = [s]
        count = 0

        while len(self.available_cells) > 0:
            count = (count + 1) % 10

            # Find an available neighbour and remove from available
            available_neighbours = c.get_available_neighbours(self)

            # Backtrack if no available_neighbours
            while not available_neighbours:
                stack.pop()
                c = self.cells[stack[-1]]
                current = stack[-1]
                available_neighbours = c.get_available_neighbours(self)

            s = sample(available_neighbours, 1)[0]
            stack.append(s)
            c = self.cells[s]
            self.available_cells.remove(s)

            # Display progress
            #print(self, flush=True)
            #sleep(0.05)

            # Connect them and remove wall between them
            self.connect_cells(s, current)
            current = copy(s)

    def __repr__(self):
        return "\n".join(["".join(line).replace("#", " ") for line in self.ascii])

class Cell(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.neighbours = set()

    def get_available_neighbours(self, maze):
        """Return empty list if none
        """
        n_avail = 0
        return [n for n in self.neighbours if n in maze.available_cells]

    def __repr__(self):
        return(f"cell: {self.x, self.y}\n  " + str(self.neighbours))

# Functions
def shape_rect(x, y, xn, yn):
    return (x < 0) or (x>= xn) or (y < 0) or (y >= yn)

def shape_circle(x, y, xn, yn):
    cx = xn // 2
    cy = yn // 2

    return sqrt((x - cx)**2 + (y - cy)**2) >= min([cx, cy])

def shape_donut(x, y, xn, yn):
    cx = xn // 2
    cy = yn // 2

    return (sqrt((x - cx)**2 + (y - cy)**2) >= min([cx, cy])) or (sqrt((x - cx)**2 + (y - cy)**2) <= min([cx, cy]) / 2.2)

def shape_triangle(x, y, xn, yn):
    return (x + y < xn) or (x - y > 0)

# Parsing user input
try:
    xn = int(sys.argv[1])
    yn = int(sys.argv[2])
    shape_name = sys.argv[3]
except:
    print(__doc__)
    sys.exit(1)

# Choose wanted outside function
if shape_name.lower() in ["c", "circ", "circle"]:
    shape = shape_circle

elif shape_name.lower() in ["r", "rect", "rectangle"]:
    shape = shape_rect

elif shape_name.lower() in ["d", "don", "donut"]:
    shape = shape_donut

elif shape_name.lower() in ["t", "tri", "triangle"]:
    shape = shape_triangle

else:
    print(__doc__)
    sys.exit(1)

# Generate maze area. Cells have no neighbours
maze = Maze(shape, xn, yn)
print(maze)

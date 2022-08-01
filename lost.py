#!/usr/bin/env python3
"""Lost in a maze - Maze creation and testing

Usage:
    <program> row col
"""

# Modules
from lib.util import *
import sys

# Parsing user input
try:
    row = int(sys.argv[1])
    col = int(sys.argv[2])
except:
    print(__doc__)
    sys.exit(1)

# Initialize walls
walls = set()
test_area = []
for n in range(row + 2):
    test_area.append([])

    for m in range(col + 2):
        test_area[-1].append(".")

    walls.add((n,       0))
    walls.add((n, col + 1))

for m in range(col + 2):
    walls.add((0,       m))
    walls.add((row + 1, m))

for n, m in sorted(walls):
    test_area[n][m] = "#"

for t in test_area:
    print("".join(t))

# Initialize maze area

# Generate maze
pass

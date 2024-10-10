import numpy as np
import random

# Takes in user size to build the sudoku array
a_size = int(input("Enter the size you want the Sudoku to be (ie. Enter 3 for a 3x3 square set resulting in a 9x9 board): "))
border_val = a_size + 1



# Creates the grid with zeros as placeholders
sudoku_array = [["0" for _ in range(a_size**2 + border_val)] for _ in range(a_size**2 + border_val)]

# Adds in barriers
for row in range(len(sudoku_array)):
    for  col in range(len(sudoku_array[0])):
        if (col == 0 or col == len(sudoku_array[0]) - 1 or col % border_val == 0):
            sudoku_array[row][col] = "|"
        if (row == 0 or row == len(sudoku_array) - 1 or row % border_val == 0):
            sudoku_array[row][col] = "-"

    
# Random numbers entered into array
# for row in sudoku_array:
#     for col in row:
#         sudoku_array[row][col]

# # Random empty slots
# for row in sudoku_array:
#     for col in row:
#         sudoku_array[row][col]

# Prints the Grid
for row in sudoku_array:
    for col in row:
        print(col, end=' ')
    print()
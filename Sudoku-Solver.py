import numpy as np
import random

def main():
    global a_size, border_val, total_game_len

    # Takes in user size to build the sudoku array
    a_size = int(input("Enter the size you want the Sudoku to be (ie. Enter 3 for a 3x3 square set resulting in a 9x9 board): "))
    border_val = a_size + 1
    total_game_len = a_size**2

    start_or_restart()
    print_board()

# Initializes empty board
def initialize_empty_board():
    global sudoku_board, total_game_len, border_val

    # Creates the grid with zeros as placeholders
    sudoku_array = [["0" for _ in range(total_game_len + border_val)] for _ in range(total_game_len + border_val)]

    # Adds in barriers
    for row in range(len(sudoku_array)):
        for col in range(len(sudoku_array[0])):
            if (col == 0 or col == len(sudoku_array[0]) - 1 or col % border_val == 0):
                sudoku_array[row][col] = "|"
            if (row == 0 or row == len(sudoku_array) - 1 or row % border_val == 0):
                sudoku_array[row][col] = "-"
    
    # Update the global sudoku_board
    sudoku_board = sudoku_array

# Fills board in
def fill_board():
    pass

# Adds blank spots, ensuring at least one blank per row and column in each individual square
def add_blanks():
    global sudoku_board, total_game_len, a_size

    # Loop through each subgrid (3x3 if a_size = 3)
    for square_row in range(0, total_game_len, a_size):  # Start row of each subgrid
        for square_col in range(0, total_game_len, a_size):  # Start column of each subgrid

            available_cols = list(range(a_size))  # List of available columns within the subgrid

            # For each row in the subgrid
            for row_offset in range(a_size):
                # Randomly choose a column within the subgrid for this row
                random_col_offset = random.choice(available_cols)
                available_cols.remove(random_col_offset)  # Ensure no two blanks in the same column

                # Map to the actual board coordinates, accounting for borders
                actual_row = square_row + row_offset + (square_row // a_size + 1)  # Adjust for border rows
                actual_col = square_col + random_col_offset + (square_col // a_size + 1)  # Adjust for border columns

                # Place a blank (underscore) in the chosen position, ensuring no border is replaced
                sudoku_board[actual_row][actual_col] = "_"

# Starts/resets the game
def start_or_restart():
    initialize_empty_board()
    fill_board()
    add_blanks()

# AI solver
def start_solve():
    pass

# Prints the Grid
def print_board():
    global sudoku_board
    
    print()
    print("Here is the Board:")
    print()
    for row in sudoku_board:
        for col in row:
            print(col, end=' ')
        print()

main()
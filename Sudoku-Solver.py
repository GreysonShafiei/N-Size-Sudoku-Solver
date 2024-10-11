import numpy as np
import random

def main():
    global a_size, border_val, total_game_len, answer_arr, blank_locations

    # Takes in user size to build the sudoku array
    a_size = int(input("Enter the size you want the Sudoku to be (ie. Enter 3 for a 3x3 square set resulting in a 9x9 board): "))
    border_val = a_size + 1
    total_game_len = a_size**2

    start_or_restart()
    print_board()

# Initializes empty board
def initialize_empty_board():
    global sudoku_board, total_game_len, border_val, answer_arr

    # Creates the grid with zeros as placeholders
    sudoku_array = [["0" for _ in range(total_game_len + border_val)] for _ in range(total_game_len + border_val)]
    answer_arr = [["0" for _ in range(total_game_len + border_val)] for _ in range(total_game_len + border_val)]

    # Adds in barriers
    for row in range(len(sudoku_array)):
        for col in range(len(sudoku_array[0])):
            if (col == 0 or col == len(sudoku_array[0]) - 1 or col % border_val == 0):
                sudoku_array[row][col] = "|"
            if (row == 0 or row == len(sudoku_array) - 1 or row % border_val == 0):
                sudoku_array[row][col] = "-"

    for row in range(len(answer_arr)):
        for col in range(len(answer_arr[0])):
            if (col == 0 or col == len(answer_arr[0]) - 1 or col % border_val == 0):
                answer_arr[row][col] = "|"
            if (row == 0 or row == len(answer_arr) - 1 or row % border_val == 0):
                answer_arr[row][col] = "-"
    
    # Update the global sudoku_board
    sudoku_board = sudoku_array

# Fills board in randomly with numbers 1 through a_size**2
def fill_board():
    global sudoku_board, total_game_len, a_size
    # Loop through each of the subgrids
    for square_row in range(0, total_game_len, a_size):
        for square_col in range(0, total_game_len, a_size):

            available_cols = list(range(a_size))
            available_num = list(range(1, total_game_len + 1))

            for row_offset in range (a_size):
                for col_offset in range(a_size):
                    random_num = random.choice(available_num) # Randomly generates a number 1 through the total_game_len (a_size ** 2)
                    available_num.remove(random_num)

                    # Map to the actual board coordinates, accounting for borders
                    actual_row = square_row + row_offset + (square_row // a_size + 1)  # Adjust for border rows
                    actual_col = square_col + col_offset + (square_col // a_size + 1)  # Adjust for border columns

                    # Place a value in the chosen position, ensuring no border is replaced
                    sudoku_board[actual_row][actual_col] = f"{random_num}"
        print()
    print("Here is the Filled Board:")
    print()
    for row in sudoku_board:
        for col in row:
            print(col, end=' ')
        print()

            
             



# Adds blank spots, ensuring at least one blank per row and column in each individual square
def add_blanks():
    global sudoku_board, total_game_len, a_size, answer_arr, blank_locations

    blank_locations = []
    blank_num = 1

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

                # Saves the answers into a board replacing 0's with the answer where the blanks will be placed
                answer_arr[actual_row][actual_col] = sudoku_board[actual_row][actual_col]

                # Saves the indexes of the blanks into a list
                blank_locations.append([[actual_row, actual_col], sudoku_board[actual_row][actual_col], blank_num])  # Append the blank location
                blank_num += 1  # Increment blank number


                # Place a blank (underscore) in the chosen position, ensuring no border is replaced
                sudoku_board[actual_row][actual_col] = "_"

    print(f"Here are the blank locations: {blank_locations}")

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
    global sudoku_board, answer_arr
    
    print()
    print("Here is the Board:")
    print()
    for row in sudoku_board:
        for col in row:
            print(col, end=' ')
        print()
    
    print()
    print("Here is the Answer Board:")
    print()
    for row in answer_arr:
        for col in row:
            print(col, end=' ')
        print()

main()
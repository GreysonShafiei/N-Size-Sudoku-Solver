import random

def main():
    global a_size, border_val, total_game_len, answer_arr, blank_locations

    # Takes in user size to build the sudoku array
    a_size = int(input("Enter the size you want the Sudoku to be (ie. Enter 3 for a 3x3 square set resulting in a 9x9 board): "))
    border_val = a_size + 1
    total_game_len = a_size**2

    sudoku_board_start = start_or_restart()
    correct_board = sudoku_board_start
    sudoku_board_start = sudoku_board
    
    print_board()

    AISolve = input("Would you like AI to solve the problem? (Y/N): ")

    if AISolve == "Y" or AISolve == "y":
        start_solve()

    print()

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

    # Retry mechanism to attempt filling the board multiple times if needed
    while True:
        try:
            # Initialize sets to track numbers used in each row and column
            used_in_rows = [set() for _ in range(total_game_len + border_val)]
            used_in_cols = [set() for _ in range(total_game_len + border_val)]
            
            # Initialize an empty board before each attempt
            initialize_empty_board()
            
            # Loop through each of the subgrids
            for square_row in range(0, total_game_len, a_size):
                for square_col in range(0, total_game_len, a_size):

                    available_num = list(range(1, total_game_len + 1))  # List of available numbers for the subgrid

                    for row_offset in range(a_size):
                        for col_offset in range(a_size):
                            # Map to the actual board coordinates, accounting for borders
                            actual_row = square_row + row_offset + (square_row // a_size + 1)
                            actual_col = square_col + col_offset + (square_col // a_size + 1)

                            # Try to find a valid number for this position
                            valid_num = None
                            random.shuffle(available_num)  # Shuffle to randomize selection
                            for num in available_num:
                                # Check if the number is already used in the current row or column
                                if num not in used_in_rows[actual_row] and num not in used_in_cols[actual_col]:
                                    valid_num = num
                                    break

                            if valid_num is not None:
                                # Place the number on the board and update tracking sets
                                sudoku_board[actual_row][actual_col] = f"{valid_num}"
                                used_in_rows[actual_row].add(valid_num)
                                used_in_cols[actual_col].add(valid_num)
                                available_num.remove(valid_num)  # Remove it from available numbers for this subgrid
                            else:
                                # If no valid number found, break and restart the board generation
                                raise ValueError("No valid number available for this position.")

            # If the board is successfully filled, exit the retry loop
            break
        except ValueError:
            # If a conflict is found, restart the process
            continue  # This will trigger a new attempt to generate the board

    # print()
    # print("A Solution was found")
    # print()
    # print("Here is the Filled Board:")
    # print()
    # for row in sudoku_board:
    #     for col in row:
    #         print(col, end=' ')
    #     print()

            
             



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
                #blank_locations.append([[actual_row, actual_col], sudoku_board[actual_row][actual_col], blank_num])  # Append the blank location
                blank_locations.append([actual_row, actual_col])
                blank_num += 1  # Increment blank number


                # Place a blank (underscore) in the chosen position, ensuring no border is replaced
                sudoku_board[actual_row][actual_col] = "_"

# Starts/resets the game
def start_or_restart():
    initialize_empty_board()
    fill_board()
    add_blanks()

# AI solver using backtracing
def start_solve():
    global sudoku_board, total_game_len, a_size, blank_locations

    while True:
        try:
            # Initialize lists of sets to track numbers used in each row and column
            used_in_row = [set() for _ in range(total_game_len + border_val)]
            used_in_col = [set() for _ in range(total_game_len + border_val)]
            
            for square_row in range(0, total_game_len, a_size):
                for square_col in range(0, total_game_len, a_size):

                    available_num = list(range(1, total_game_len + 1))

                    for row_offset in range(a_size):
                        for col_offset in range(a_size):
                            actual_row = square_row + row_offset + (square_row // a_size + 1)
                            actual_col = square_col + col_offset + (square_col // a_size + 1)
                            
                            # Try to find a valid number for this cell
                            random.shuffle(available_num)
                            valid_num = None
                            for num in available_num:
                                if num not in used_in_row[actual_row] and num not in used_in_col[actual_col]:
                                    valid_num = num
                                    break

                            if valid_num is not None:
                                # Place the valid number and update the used sets
                                sudoku_board[actual_row][actual_col] = f"{valid_num}"
                                used_in_row[actual_row].add(valid_num)
                                used_in_col[actual_col].add(valid_num)
                                available_num.remove(valid_num)
                            else:
                                # If no valid number is found, raise an error to trigger a restart
                                raise ValueError("No valid number found for this position.")

            # Break the loop if the board is successfully solved
            break

        except ValueError:
            # If a conflict occurs, restart the solving process
            continue

    print()
    print("Here is a solution to the Board:")
    print()
    for row in sudoku_board:
        for col in row:
            print(col, end=' ')
        print()


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
    
    print(f"Here are the blank locations: {blank_locations}")
    for _ in range(len(f"Here are the blank locations: {blank_locations}")):
        print('_', end='')
    print()
    print()

main()

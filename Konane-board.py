# CSCI 1913
# Project 1
# Name: Amro Abu-atieh

import random

print('Hello, welcome to the Konane Game, this is the Hawaiian version of Checkers.')

def generate_board(an_int):
    if an_int <= 0:
        return []

    board_size = []

    for row in range(an_int):
        row_list = []
        for col in range(an_int):
            if (row + col) % 2 == 0:
                row_list.append(1)
            else:
                row_list.append(2)

        board_size.append(row_list)

    return board_size

def generate_board_r(an_int_row, an_int_col):
    if an_int_row <= 0 or an_int_col <= 0:
        return []

    board_size = []

    for row in range(an_int_row):
        row_list = []
        for col in range(an_int_col):
            if (row + col) % 2 == 0:
                row_list.append(1)
            else:
                row_list.append(2)

        board_size.append(row_list)

    return board_size

def get_board_as_string(board):
    if not board:
        return ''
    board_str = ''

    num_columns = len(board[0])
    header = ' '

    for i in range(num_columns):
        header += f' {i % 10}'
    header += '\n'

    board_str += header

    for row_board in range(len(board)):
        board_str += ' ' + '+-' * len(board[0]) + '+\n'
        board_str += f'{row_board % 10}|'
        for cell in board[row_board]:
            if cell == 1:
                board_str += '○|'
            elif cell == 2:
                board_str += '●|'
            else:
                board_str += ' |'

        board_str += '\n'
    board_str += ' ' + '+-' * len(board[0]) + '+'
    return board_str


def prep_board_human(board, player):
    print(get_board_as_string(board))

    while True:
        print(get_board_as_string(board))

        try:
            # Get input for the first and second positions
            row_one, col_one = map(int, input(f"Player {player} Enter first row and first column: ").split(', '))
            row_two, col_two = map(int, input(f"Player {player} Enter second row and second column: ").split(', '))
        except ValueError:
            print("Invalid input. Please enter two integers for each position.")
            continue

        # Validate that positions are within the board's bounds
        if (0 <= row_one < len(board) and 0 <= col_one < len(board[0]) and
                0 <= row_two < len(board) and 0 <= col_two < len(board[0])):

            # Ensure the selected piece belongs to the current player
            if board[row_one][col_one] == player:
                # Calculate the position of the piece being jumped over
                middle_row = (row_one + row_two) // 2
                middle_col = (col_one + col_two) // 2

                # Check if the middle position is occupied by the opponent
                if (0 <= middle_row < len(board) and 0 <= middle_col < len(board[0]) and
                        board[middle_row][middle_col] != 0 and
                        board[middle_row][middle_col] != player):

                    # Calculate the direction of the initial jump
                    row_direction = row_two - row_one
                    col_direction = col_two - col_one

                    # Perform the jump
                    board[row_two][col_two] = player  # Move player's piece to the new location
                    board[row_one][col_one] = 0  # Remove the piece from the old location
                    board[middle_row][middle_col] = 0  # Remove the jumped-over opponent's piece
                    print("The jump was successful.")

                    # Check for a possible double jump
                    while True:
                        print(get_board_as_string(board))
                        try:
                            double_jump = input("Do you want to make another jump? (y/n): ").lower()
                            if double_jump == 'y':
                                # Get the next position for the double jump
                                row_two_next, col_two_next = map(int, input(
                                    f"Player {player} Enter next row and column: ").split(', '))

                                # Calculate the direction of the next jump
                                new_row_direction = row_two_next - row_two
                                new_col_direction = col_two_next - col_two

                                # Ensure the next jump is in the same direction as the first jump
                                if new_row_direction == row_direction and new_col_direction == col_direction:
                                    # Calculate the new middle piece to jump over
                                    new_middle_row = (row_two + row_two_next) // 2
                                    new_middle_col = (col_two + col_two_next) // 2

                                    # Validate that the second jump is legal
                                    if (0 <= row_two_next < len(board) and 0 <= col_two_next < len(board[0]) and
                                            0 <= new_middle_row < len(board) and 0 <= new_middle_col < len(board[0]) and
                                            board[new_middle_row][new_middle_col] != 0 and
                                            board[new_middle_row][new_middle_col] != player):

                                        # Perform the second jump
                                        board[row_two_next][col_two_next] = player
                                        board[row_two][col_two] = 0
                                        board[new_middle_row][new_middle_col] = 0

                                        # Update the new position
                                        row_two, col_two = row_two_next, col_two_next
                                        print("The second jump was successful.")
                                    else:
                                        print("Invalid second jump. Ending turn.")
                                        break
                                else:
                                    print("Invalid second jump. Must be in the same direction.")
                                    break
                            else:
                                print("Ending turn.")
                                break
                        except ValueError:
                            print("Invalid input. Ending turn.")
                            break

                    player = 3 - player  # Switch player after the jumps
                else:
                    print("Invalid jump. The middle piece must belong to the opponent.")
            else:
                print("You must select a piece that belongs to you.")
        else:
            print("Please enter valid board positions.")

    print(get_board_as_string(board))


def is_valid_move(board, move):
    valid_row, valid_col = move

    if not (0 <= valid_row < len(board) and 0 <= valid_col < len(board[0])):
        return False
    if board[valid_row][valid_col] == 0:
        return False
    return True

def get_valid_moves_for_stone(board, stone):
    valid_row, valid_col = stone

    if not is_valid_move(board, stone):
        return []

    valid_moves = []
    directions = [(-2,0), (2,0), (0,-2), (0,2)]

    for d in directions:
        dvalid_row, dvalid_col = d
        new_row = dvalid_row + valid_row
        new_col = dvalid_col + valid_col

        if is_valid_move(board, (new_row, new_col)):
            valid_moves.append((new_row, new_col))

            for d in directions:
                dvalid_row2, dvalid_col2 = d
                next_row = new_row + dvalid_row2
                next_col = new_col + dvalid_col2

                if is_valid_move(board, (next_row, next_col)):
                    valid_moves.append((next_row, next_col))

    return valid_moves

def get_valid_moves(board, player):

    valid_moves = []

    for row in range(len(board)):
        for col in range(len(board[0])):

            if board[row][col] != 0:

                if get_valid_moves_for_stone(board,(row, col)):
                    valid_moves.append((row, col))

    return valid_moves

def human_player(board, player):

    print(get_board_as_string(board))
    valid_moves = get_valid_moves(board, player)

    if not valid_moves:
        return ()
    while True:
        try:
            row_valid, col_valid = map(int, input(f"Player {player}, enter your move (row and column): ").split(', '))
            if (row_valid, col_valid) in valid_moves:
                return row_valid, col_valid
            else:
                print('Invalid move. Enter a valid move to continue')
        except Exception as e:
            print(f"Error, {e}. Please enter valid numbers.")

def random_player(board, player):
    valid_moves = get_valid_moves(board, player)

    if not valid_moves:
        return ()
    return random.choice(valid_moves)

def ai_player(board, player):
    valid_moves = get_valid_moves(board, player)

    if not valid_moves:
        return ()
    return valid_moves[0]


def first_move(board, player):
    print(get_board_as_string(board))

    while True:
        try:
            row, col = map(int, input(f"Player {player}, choose your first piece (row, column): ").split(', '))
        except ValueError:
            print("Invalid input. Please enter two valid integers, separated with a comma.")
            continue

        if (0 <= row < len(board) and 0 <= col < len(board[0])):

            if board[row][col] == player:
                print(f"Player {player} selected piece at ({row}, {col}).")
                board[row][col] = 0
                return
            else:
                print("That's not your peice, please pick one of your peices.")
        else:
            print("Please enter a valid location.")

def play_game(ai_black, ai_white, board = None):

    if board == None:
        board = generate_board(7)

    print(get_board_as_string(board))
    first_player = random.choice([1,2])

    second_player = 3 - first_player

    first_move(board, first_player)
    first_move(board, second_player)

    print(f"The first player is {first_player}.")

    while True:
        prep_board_human(board, first_player)

        if first_player == 1:
            move = ai_black(board, first_player)

            if not move:
                print(f"Player {3 - first_player} wins!")
                return 3 - first_player
        else:
            move = ai_white(board, first_player)
            if not move:
                print(f"Player {3 - first_player} wins!")
                return 3 - first_player

        if move == ():
            print(f"Player {3 - first_player} wins!")
            return 3 - first_player

        row, col = move
        board[row][col] = 0

        first_player, second_player = second_player, first_player

        print(get_board_as_string(board))

play_game(random_player, random_player)

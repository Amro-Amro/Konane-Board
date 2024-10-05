
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

def prep_board_human(board):
    print(get_board_as_string(board))

    valid_input = False

    while True:
        try:
            row_one, col_one = map(int, input("Enter first row and first column: ").split())
            row_two, col_two = map(int, input("Enter second row and second column: ").split())
        except ValueError:
            print("Invalid input. Please enter two integers for each position.")
            continue
        if (0 < row_one < len(board) - 1 and 0 < col_one < len(board[0]) - 1 and
                0 < row_two < len(board) - 1 and 0 < col_two < len(board[0]) - 1):
            if board[row_one][col_one] != board[row_two][col_two] and board[row_one][col_one] != 0 and board[row_two][col_two] != 0:

                board[row_one][col_one] = 0
                board[row_two][col_two] = 0

                print("The tokens were removed successfully.")
                valid_input = True
            else:
                print("Please try again; you might have picked the same place, or the wrong color")

        else:
            print("Please enter a valid location")

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

    valid_moves = [
        check_move
        for row in range(len(board))
        for col in range(len(board[0]))
        if board[row][col] == player
        for check_move in get_valid_moves_for_stone(board, (row, col))
    ]

    return valid_moves

def human_player(board, player):

    print(get_board_as_string(board))
    valid_moves = get_valid_moves(board, player)

    if not valid_moves:
        return ()
    while True:
        try:
            row_valid, col_valid = map(int, input(f"Player {player}, enter your move (row and column): ").split())
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

def play_game(ai_black, ai_white, board = None):

    if board == None:
        board = generate_board(10)

    print(get_board_as_string(board))
    first_player = random.choice([1,2])

    print(f"The first player is {first_player}.")

    while True:
        if first_player == 1:
            move = ai_black(board, first_player)
            if not move:
                return 2
        else:
            move = ai_white(board, first_player)

        if move == ():
            print(f"Player {3 - first_player} wins!")
            return 3 - first_player

        row, col = move
        board[row][col] = 0

        print(get_board_as_string(board))
        first_player = 3 - first_player

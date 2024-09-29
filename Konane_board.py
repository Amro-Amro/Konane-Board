import random

def generate_board(an_int):
    '''First this function will see if the input is empty and if it is it will output
    and empty set. Then it will take an argument an_int, and go through an iteration to
    make a list full of all the numbers that are needed. '''
    if an_int <= 0:
        return []

    board_size = []

    for row in range(an_int):
        row_list = []
        for col in range(an_int):
            if(row + col) % 2 == 0:
                row_list.append(1)
            else:
                row_list.append(2)

        board_size.append(row_list)

    for i in board_size:
        print(i)
# board_len_and_width = int(input('How big do you want the board to be?'))
# generate_board(board_len_and_width)
def generate_board_r(an_int_row, an_int_col):
    '''This is the same as the last function, but the differenece is that it takes two arguments,
    and with those  two arguments its goes in two for loops to print out a board with the qaulifications
    of the width and the length.'''
    if an_int_row <= 0 and an_int_col <= 0:
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

    for i in board_size:
        print(i)

def get_board_as_string(board):
    '''This function will take the board that you put in it, and will first check
    if its empty then it will go through all the numbers 1, and 2 in this list and based
    on the numbers it will print either a black dot or a white dot, and if empty nothing.'''
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
    '''This function first prints the board. This will then check if the input
    is in the range of the board excluding the sides. I did this by using the try
    except function, adn also originally putting valid_input eqaul to false.'''
    print(get_board_as_string(board))
    valid_input = False
    while True:
        try:
            row_one, col_one = map(int, input("Enter first row and first column: ").split())
            row_two, col_two = map(int, input("Enter second row and second column: ").split())
        except ValueError:
            print("Invalid input. Please enter two integers for each position.")
            continue
        if row_one > 0 and row_one < len(board) - 1 and col_one > 0 and col_one < len(board[0]) - 1 and \
                row_two > 0 and row_two < len(board) - 1 and col_two > 0 \
                and col_two < len(board[0]) - 1:

            if board[row_one][col_one] != board[row_two][col_two] and board[row_one][col_one] != 0 \
                    and board[row_two][col_two] != 0:
                board[row_one][col_one] = 0
                board[row_two][col_two] = 0

                print("The tokens were removed successfully.")
                valid_input = True

            else:
                print("Please try agian, you might have picked the same place, or the color")
        else:
            print("Please enter a valid location")

    print(get_board_as_string(board))

def is_valid_move(board, move):
    '''This function wil; check if the move is valid, by taking the argument, and
    returning either true or false.'''
    valid_row, valid_col = move
    if 0 <= valid_row >= len(board):
        return False
    if 0 <= valid_col >= len(board[0]):
        return False
    if board[valid_row][valid_col] == 0:
        return False

    return True

def get_valid_moves_for_stone(board, stone):
    '''This function will check for valid moves for the stones. If there are no
    stones then an empty list will be returned. '''
    valid_row, valid_col = stone
    if not is_valid_move(board, stone):
        return []
    valid_move = []
    directions = [(-1,0), (1,0), (0,-1), (0,1)]

    for d in directions:
        dvalid_row, dvalid_col = d
        new_row = dvalid_row + valid_row
        new_col = dvalid_col + valid_col

        if is_valid_move(board, (new_row, new_col)):
            valid_move.append((new_row, new_col))

    return valid_move

def get_valid_moves(board, player):
    '''This function will accept a board and an integer representing a "Black" or "White" player.
    The function will return a list of the valid moves for that player given the current
    board state.'''
    valid_moves = [
        move
        for row in range(len(board))
        for col in range(len(board[0]))
        if board[row][col] == player
        for move in get_valid_moves_for_stone(board, (row, col))
    ]
    return valid_moves

def human_player(board, player):
    '''This function first prints the board as a string, then checks for valid moves with the
    get_valid_moves function. If it's not valid it executes an empty tuple. Next it goes into a while loop
    that executes until the game is finished. This while loop checks if the moves are valid, and
    make sure the game runs smoothly'''
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
    '''This function will make a computer that uses the random module to make moves. If there is no
    valid moves an empty tuple will be outputted.'''
    valid_moves = get_valid_moves(board, player)
    if not valid_moves:
        return ()
    return random.choice(valid_moves)

def ai_player(board, player):
    '''This function asks us to build an AI. What I did is firt checked if the move is
    valid, and if it's empty. If valid the AI will pick the first option it has for a move. '''
    valid_moves = get_valid_moves(board, player)
    if not valid_moves:
        return ()
    return valid_moves[0]

def play_game(ai_black, ai_white, board):
    '''This function will play a game with two AI's. It first randomly picks between 1 and 2
    to see which AI goes first. Then after that, the game starts and until there is an empty list,
    the game will continue to play. When the empty list happens the winner will be the other player
    aka 3 - first_player.'''
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

        row,col = move
        board[row][col] = 0

        print(get_board_as_string(board))

        first_player = 3 - first_player

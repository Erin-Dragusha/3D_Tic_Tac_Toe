#!/usr/bin/python3

# Dimensions of the board
BOARD_SIZE = 4

# Blank placeholder
BLANK = '_'

# Player tokens
PLAYERS = ['1', '2', '3']

# The game board
board = [[[BLANK] * BOARD_SIZE for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]

# Turn tracker
turn = 0

#
# PURPOSE:
# Prints out the board to stdout
#
def print_board():
    for layer in board:
        for row in layer:
            for cell in row:
                print(cell, end = '')
            print()
        print()

#
# PURPOSE:
# Returns the board contents in form of a string
# Each row is newline-terminated, and each layer is also newline-terminated
#
def encode_board():
    encoded_board = ''
    for layer in board:
        for row in layer:
            for cell in row:
                encoded_board += cell
            encoded_board += '\n'
        encoded_board += '\n'

    return encoded_board
#
# PURPOSE:
# Places a token at the given position
#
# PARAMETERS:
# layer - the target layer of the board
# row - the target row of the board
# cell - the target column of the board
# token - the token to be placed on the board
#
# RETURNS:
# True if the token was placed successfully
# False if the position was out of range, the token was placed out of turn, or the cell is not blank
#
def place_token(layer, row, column, token):
    if token != PLAYERS[turn]:
        return False
    
    try:
        if board[layer][row][column] != BLANK:
            return False
        board[layer][row][column] = token
        return True
    except IndexError as e:
        return False

#
# PURPOSE:
# Checks whether or not a given token has won
#
# PARAMETERS:
# token - the token to be checked
#
# RETURNS:
# True if the token won, False otherwise
#
def token_wins(token):
    layer_bottom_left_top_right_diagonal_count = 0
    layer_top_left_bottom_right_diagonal_count = 0
    layer_bottom_right_top_left_diagonal_count = 0
    layer_top_right_bottom_left_diagonal_count = 0
    for i in range(BOARD_SIZE):
        top_left_diagonal_count = 0
        bottom_left_diagonal_count = 0
        layer_row_top_left_diagonal_count = 0
        layer_row_bottom_left_diagonal_count = 0
        layer_column_top_diagonal_count = 0
        layer_column_bottom_diagonal_count = 0
        for j in range(BOARD_SIZE):
            row_count = 0
            col_count = 0
            layer_col_count = 0
            for k in range(BOARD_SIZE):
                # Check row within a layer
                if board[i][j][k] == token:
                    row_count += 1
                if row_count == BOARD_SIZE:
                    #print('Row found at board', i, 'row', j)
                    return True
                
                # Check column within a layer
                if board[i][k][j] == token:
                    col_count += 1
                if col_count == BOARD_SIZE:
                    #print('Column found at board', i, 'column', j)
                    return True
                
                # Check column between layers
                if board[k][i][j] == token:
                    layer_col_count += 1
                if layer_col_count == BOARD_SIZE:
                    #print('Layer-spanning column found at row', i, 'col', j)
                    return True
        
            # Check top left to bottom right diagonal within a layer
            if board[i][j][j] == token:
                top_left_diagonal_count += 1
            if top_left_diagonal_count == BOARD_SIZE:
                #print('Top left diagonal found at board', i)
                return True
            
            # Check bottom left to top right diagonal within a layer
            if board[i][BOARD_SIZE - 1 - j][j] == token:
                bottom_left_diagonal_count += 1
            if bottom_left_diagonal_count == BOARD_SIZE:
                #print('Bottom left diagonal found at board', i)
                return True
            
            # Check top left to bottom right diagonal between layers, but within a row
            if board[BOARD_SIZE - 1 - j][i][j] == token:
                layer_row_top_left_diagonal_count += 1
            if layer_row_top_left_diagonal_count == BOARD_SIZE:
                #print('Layer-spanning top left diagonal found at row', i)
                return True

            # Check bottom left to top right diagonal between layers, but within a row
            if board[j][i][j] == token:
                layer_row_bottom_left_diagonal_count += 1
            if layer_row_bottom_left_diagonal_count == BOARD_SIZE:
                #print('Layer-spanning bottom left diagonal found at row', i)
                return True

            # Check top to bottom diagonal between layers
            if board[j][BOARD_SIZE - 1 - j][i] == token:
                layer_column_top_diagonal_count += 1
            if layer_column_top_diagonal_count == BOARD_SIZE:
                #print('Layer-spanning top to bottom diagonal found at column', i)
                return True

            # Check bottom to top diagonal between layers
            if board[j][j][i] == token:
                layer_column_bottom_diagonal_count += 1
            if layer_column_bottom_diagonal_count == BOARD_SIZE:
                #print('Layer-spanning bottom to top diagonal found at column', i)
                return True

        # Check bottom left to top right diagonal between layers
        if board[i][i][i] == token:
            layer_bottom_left_top_right_diagonal_count += 1
        if layer_bottom_left_top_right_diagonal_count == BOARD_SIZE:
            #print('Layer-spanning bottom left to top right diagonal found')
            return True

        # Check bottom right to top left diagonal between layers
        if board[i][i][BOARD_SIZE - 1 - i] == token:
            layer_bottom_right_top_left_diagonal_count += 1
        if layer_bottom_right_top_left_diagonal_count == BOARD_SIZE:
            #print('Layer-spanning bottom right to top left diagonal found')
            return True

        # Check top right to bottom left diagonal between layers
        if board[i][BOARD_SIZE - 1 - i][i] == token:
            layer_top_right_bottom_left_diagonal_count += 1
        if layer_top_right_bottom_left_diagonal_count == BOARD_SIZE:
            #print('Layer-spanning top right to bottom left diagonal found')
            return True

        # Check top left to bottom right diagonal between layers
        if board[i][BOARD_SIZE - 1 - i][BOARD_SIZE - 1 - i] == token:
            layer_top_left_bottom_right_diagonal_count += 1
        if layer_top_left_bottom_right_diagonal_count == BOARD_SIZE:
            #print('Layer-spanning top left to bottom right diagonal found')
            return True

    return False

#
# PURPOSE:
# Determines whose turn it is
#
# RETURNS:
# The token whose turn it is
#
def whose_turn():
    return PLAYERS[turn]

#
# PURPOSE:
# Switches to the next player
#
def take_turn():
    global turn
    turn = (turn + 1) % len(PLAYERS)

#
# PURPOSE:
# Clears the board and resets the turn to player 0
#
def clear_board():
    global board
    global turn
    board = [[[BLANK] * BOARD_SIZE for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
    turn = 0

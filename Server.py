#!/usr/bin/python3

import GameBoard
import socket
import logging
import logging.handlers
import threading

# Set up logging
logger = logging.getLogger('Server.py')
logger.setLevel(logging.DEBUG)
handler = logging.handlers.SysLogHandler(address = '/dev/log')
logger.addHandler(handler)

# Set up threading
lock = threading.Semaphore()

# The maximum size of the receive buffer
BUF_SIZE = 1024

# The interface that is being listened to
HOST = ''

# The maximum number of connections
MAX_CONNECTIONS = 3

# The port that is being listened to
PORT = 12345

# Where the command is found in the incoming string
COMMAND_INDEX = 0

# Where the board is found (if applicable) in the incoming string
BOARD_INDEX = 1

# Where the row is found (if applicable) in the incoming string
ROW_INDEX = 2

# Where the column is found (if applicable) in the incoming string
COLUMN_INDEX = 3

# Where the player token is found (if applicable) in the incoming string
PLAYER_TOKEN_INDEX = 4

# The clear command
CLEAR_REQUEST = 'C'

# The length of the clear command
CLEAR_REQUEST_LEN = 1

# The get command
GET_REQUEST = 'G'

# The length of the get command
GET_REQUEST_LEN = 1

# The put command
PUT_REQUEST = 'P'

# The length of the put command
PUT_REQUEST_LEN = 5

# The end marker of a network request
END_MARKER = '*'

# The error flag
ERR_RESPONSE = 'E'

# The OK flag
OK_RESPONSE = 'O'

# The rejection response
REJECTION_RESPONSE = 'R'

# The name of the winner, if any
winner = ''

#
# PURPOSE:
# Gets an END_MARKER-terminated string from the network and decodes it
# If no newline is found within BUF_SIZE bytes, the first BUF_SIZE bytes are returned
# Errors are caught and result in an error message being logged
#
# PARAMETERS:
# sc - the connection from which to receive data
#
# RETURNS:
# The received data in the form of a string, or '' in case of an error
#
def get_request(sc):
    data = ''
    try:
        while len(data) < BUF_SIZE:
            incoming = sc.recv(1).decode()
            if len(data) > 0 and incoming == END_MARKER:
                return data
            data += incoming
    except Exception as e:
        logger.critical(str(e), exc_info = 1)
        return ''

#
# PURPOSE:
# Processes a request and returns a response
# In case of an error, the failure is shown in the response
#
# PARAMETERS:
# req - the request to be fulfilled
# id - the id of the requestor
#
# RETURNS:
# The response to the request
#
def process_request(req, id):
    global winner

    logger.debug('Client ' + str(id) + ': ' + req)
    with lock:
        try:
            if len(req) == 0:
                return ERR_RESPONSE + END_MARKER
            elif req[COMMAND_INDEX] == CLEAR_REQUEST and len(req) == CLEAR_REQUEST_LEN:
                GameBoard.clear_board()
                winner = ''
                return OK_RESPONSE + END_MARKER
            elif req[COMMAND_INDEX] == GET_REQUEST and len(req) == GET_REQUEST_LEN:
                response = GameBoard.encode_board()
                if winner == '':
                    response = response + 'Player ' + GameBoard.whose_turn() + '\'s turn'
                else:
                    response = response + 'Player ' + winner + ' wins'
                return response + END_MARKER
            elif req[COMMAND_INDEX] == PUT_REQUEST and len(req) == PUT_REQUEST_LEN and req[1:PUT_REQUEST_LEN - 1].isdigit() and req[PLAYER_TOKEN_INDEX] == str(id) and winner == '':
                if not GameBoard.place_token(int(req[BOARD_INDEX]), int(req[ROW_INDEX]), int(req[COLUMN_INDEX]), (req[PLAYER_TOKEN_INDEX])):
                    return ERR_RESPONSE + END_MARKER

                current_player = GameBoard.whose_turn()
                if GameBoard.token_wins(current_player):
                    winner = current_player
                else:
                    GameBoard.take_turn()

                return OK_RESPONSE + END_MARKER
            else:
                return ERR_RESPONSE + END_MARKER
        except Exception as e:
            logger.critical(str(e), exc_info = 1)
            return ERR_RESPONSE + END_MARKER

#
# PURPOSE:
# Given a connection, gets a request, processes it, and sends a response, ad infinitum
# Errors are caught and result in an error message being logged and the connection being closed
#
# PARAMETERS:
# sc - the socket connection to use
# id - the id of the connection; if it is not in [1, MAX_CONNECTIONS], a rejection message will be sent and the connection will be closed
#
def process_connection(sc, id):
    try:
        with sc:
            logger.debug('Client ' + str(id) + ': ' + str(sc.getpeername()))
            if id < 1 or MAX_CONNECTIONS < id:
                response = REJECTION_RESPONSE + END_MARKER
                sc.sendall(response.encode())
                return
            while True:
                request = get_request(sc)
                reponse = process_request(request.strip(), id)
                sc.sendall(reponse.encode()) 
    except Exception as e:
        logger.critical(str(e), exc_info = 1)

try:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 
        sock.bind((HOST, PORT)) 
        sock.listen(1) 
        logger.debug('Server: ' + str(sock.getsockname()))
        i = 1
        while True:
            sc, sockname = sock.accept() 
            threading.Thread(target = process_connection, args = (sc, i, )).start()
            i = i + 1
except Exception as e:
    logger.critical(str(e), exc_info = 1)

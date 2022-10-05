#!/usr/bin/python3
import socket
BUF_SIZE = 1024
HOST = ''
PORT = 12345
board = [[["_" for _ in range(4)] for _ in range(4)] for _ in range(4)]
turn = 1


def getBoard():
	boardString = ""
	for level in board:
		for row in level:
			for col in row:
				boardString += col
			boardString += "\n"
		boardString += "\n"
	return boardString

def displayError(sc):
	sc.sendall("E\n".encode())

def displaySuccess(sc):
	sc.sendall("O\n".encode())

def displayMessage(sc, message):
	sc.sendall((message+"\n").encode())

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock: # TCP socket
	sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # Details later
	sock.bind((HOST, PORT)) # Claim messages sent to port "PORT"
	sock.listen(1) # Enable server to receive 1 connection at a time
	print('Server:', sock.getsockname()) # Source IP and port
	while True:
		sc, sockname = sock.accept() # Wait until a connection is established
		with sc:
			print('Client:', sc.getpeername()) # Dest. IP and p
			data = sc.recv(BUF_SIZE) # recvfrom not needed since address is known
			decodedData = data.decode()
			print(list(decodedData))
			COMMAND = decodedData[0]

			if COMMAND == 'G':
				displayMessage(sc, getBoard())
			elif COMMAND == 'P':

				if len(decodedData) != 6:
					displayError(sc)
					print("Invalid number of inputs!")
					continue

				
				level = decodedData[1]
				row = decodedData[2]
				col = decodedData[3]
				inputRecord = decodedData[4]

				if not level.isnumeric() or not row.isnumeric() or not col.isnumeric() or not inputRecord.isnumeric():			
					displayError(sc)
					print("One of the arguments is NaN")
					continue

				level = int(level)	
				row = int(row)	
				col = int(col)
				inputRecord = int(inputRecord)

				if inputRecord != turn:
					displayError(sc)
					print("Not your turn!")
					continue	

				try:
					board[level][row][col]
				except IndexError:
					displayError(sc)
					print("Out of bounds!")
					continue

				if board[level][row][col] != '_':
					displayError(sc)
					print("Section occupied!")
					continue

				board[level][row][col] = str(inputRecord)
				displaySuccess(sc)
				print("Sucessfully placed on board!")

				if turn == 3:
					turn = 1
				else:
					turn+=1
			elif COMMAND == 'C':
				turn = 1
				board = [[["_" for _ in range(4)] for _ in range(4)] for _ in range(4)]
				displaySuccess(sc)
				print("Board cleared!")
			else:
				displayError(sc)
				print("Unknown command!")

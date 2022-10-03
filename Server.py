#!/usr/bin/python3
import socket
BUF_SIZE = 1024
HOST = ''
PORT = 12345
board = [[["_" for _ in range(4)] for _ in range(4)] for _ in range(4)]
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock: # TCP socket
	sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # Details later
	sock.bind((HOST, PORT)) # Claim messages sent to port "PORT"
	sock.listen(1) # Enable server to receive 1 connection at a time
	print('Server:', sock.getsockname()) # Source IP and port
	while True:
		sc, sockname = sock.accept() # Wait until a connection is established
		with sc:
			print('Client:', sc.getpeername()) # Dest. IP and p
			responseMessage = ''
			data = sc.recv(BUF_SIZE) # recvfrom not needed since address is known
			decodedData = data.decode()
			print(list(decodedData))
			result = ''

			if decodedData[0] == 'G':
				for row in board:
					result += '\n'
					for ro in row:
						result += '\n'
						for r in ro:
							result += r
				result += '\n'
			elif decodedData[0] == 'P':

				if not decodedData[1].isnumeric() or not decodedData[2].isnumeric() or not decodedData[3].isnumeric():
					responseMessage = "Invalid input!"
				else:

					inputRecord = decodedData[4]
					firstPosition = int(decodedData[1])
					secondPosition = int(decodedData[2])
					thirdPosition = int(decodedData[3])

					if firstPosition > 3:
						responseMessage += "First position is out of bounds!"

					if secondPosition > 3:
						responseMessage += "Second position is out of bounds!"

					if thirdPosition > 3:
						responseMessage += "Third position is out of bounds!"

					if responseMessage == '':
						if board[firstPosition][secondPosition][thirdPosition] == "_":
							board[firstPosition][secondPosition][thirdPosition] = inputRecord
							responseMessage = "OK"
						else:
							responseMessage = "ERROR! This section is occupied!"

			print(responseMessage)
			sc.sendall(result.encode())


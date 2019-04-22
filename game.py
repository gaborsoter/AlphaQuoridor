import numpy as np

# the game

class Game:

	def __init__(self):
		self.currentPlayer = 0 # 0:A, 1:B
		self.gameState = 0
		self.A_position = 5
		self.B_position = 116
		self.A_walls = [-1] * 10 # each element of the array represents the position of a given wall, -1 if it's off the board
		self.B_walls = [-1] * 10
		self.bottom = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
		self.left = [0, 11, 22, 33, 44, 55, 66, 77, 88, 99, 110]
		self.right = [10, 21, 32, 43, 54, 65, 76, 87, 98, 109, 120]
		self.top = [110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120]

	def allowedMoves(self, position, position_opponent):
		allowed_moves = []

		# moving down
		if position not in self.bottom:
			if position + 99 not in self.A_walls and position + 99 not in self.B_walls:
				if position_opponent != position - 11:
					allowed_moves.append(position - 11)
				elif position_opponent + 99 not in self.A_walls and position_opponent + 99 not in self.B_walls:
					allowed_moves.append(position - 22)

		# moving up
		if position not in self.top:
			if position + 110 not in self.A_walls and position + 110 not in self.B_walls:
				if position_opponent != position + 11:
					allowed_moves.append(position + 11)
				elif position_opponent + 110 not in self.A_walls and position_opponent + 110 not in self.B_walls:
					allowed_moves.append(position + 22)

		# moving right
		if position not in self.right and position_opponent not in self.right:
			if position - int(position/11) not in self.A_walls and position - int(position/11) not in self.B_walls:
				if position_opponent != position + 1:
					allowed_moves.append(position + 1)
				elif position_opponent - int(position/11) not in self.A_walls and position_opponent - int(position/11) not in self.B_walls:
					allowed_moves.append(position + 2)

		# moving left
		if position not in self.left and position_opponent not in self.left:
			if position - int(position/11) - 1 not in self.A_walls and position - int(position/11) - 1 not in self.B_walls:
				if position_opponent != position - 1:
					allowed_moves.append(position - 1)
				elif position_opponent - int(position/11) - 1 not in self.A_walls and position_opponent - int(position/11) - 1 not in self.B_walls:
					allowed_moves.append(position - 2)

		return allowed_moves

	def convertTo2D(self, state):
		# for visualisation
		board = np.zeros([11, 11])
		return

game = Game()

game.A_walls[0] = 71
game.B_walls[5] = 177

print(game.allowedMoves(78, 77))

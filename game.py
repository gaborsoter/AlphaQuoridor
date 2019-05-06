import numpy as np

# the game class
class Game:
	def __init__(self):
		self.currentPlayer = 0 # 0:A, 1:B
		self.gameState = 0
		self.A_position = 5
		self.B_position = 116
		self.A_walls = np.full((10, 2), -1) # each element of the array represents the position of a given wall, -1 if it's off the board
		self.B_walls = np.full((10, 2), -1)
		self.bottom = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
		self.left = [0, 11, 22, 33, 44, 55, 66, 77, 88, 99, 110]
		self.right = [10, 21, 32, 43, 54, 65, 76, 87, 98, 109, 120]
		self.top = [110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120]
		self.walls = []
		self.set_bottom = set(self.bottom)
		self.set_top = set(self.top)

	# allowed moves of the figures
	def allowedMoves(self, position, position_opponent):
		allowed_moves = []

		# moving down
		if position not in self.bottom:
			if position + 99 not in self.A_walls.flatten() and position + 99 not in self.B_walls.flatten():
				if position_opponent != position - 11:
					allowed_moves.append(position - 11)
				elif position_opponent + 99 not in self.A_walls.flatten() and position_opponent + 99 not in self.B_walls.flatten():
					allowed_moves.append(position - 22)

		# moving up
		if position not in self.top:
			if position + 110 not in self.A_walls.flatten() and position + 110 not in self.B_walls.flatten():
				if position_opponent != position + 11:
					allowed_moves.append(position + 11)
				elif position_opponent + 110 not in self.A_walls.flatten() and position_opponent + 110 not in self.B_walls.flatten():
					allowed_moves.append(position + 22)

		# moving right
		if position not in self.right and position_opponent not in self.right:
			if position - int(position/11) not in self.A_walls.flatten() and position - int(position/11) not in self.B_walls.flatten():
				if position_opponent != position + 1:
					allowed_moves.append(position + 1)
				elif position_opponent - int(position/11) not in self.A_walls.flatten() and position_opponent - int(position/11) not in self.B_walls.flatten():
					allowed_moves.append(position + 2)

		# moving left
		if position not in self.left and position_opponent not in self.left:
			if position - int(position/11) - 1 not in self.A_walls.flatten() and position - int(position/11) - 1 not in self.B_walls.flatten():
				if position_opponent != position - 1:
					allowed_moves.append(position - 1)
				elif position_opponent - int(position/11) - 1 not in self.A_walls.flatten() and position_opponent - int(position/11) - 1 not in self.B_walls.flatten():
					allowed_moves.append(position - 2)

		return allowed_moves

	# outputs the crossing pair of a wall
	def crossingWallPair(self, wall):
		if wall[0] >= 110:
			pair = self.walls[self.walls.index(wall) + 100]
		else:
			pair = self.walls[self.walls.index(wall) - 100]

		return pair

	# removing wall positions that are not allowed
	def allowedWalls(self):
		allowed_walls = np.copy(self.walls).tolist()
		allowed_walls.pop(allowed_walls.index(self.crossingWallPair(list(self.A_walls[0]))))
		for i in range(10):
			if self.A_walls[i][0] != -1:
				if self.A_walls[i][0] >= 110:
					try:
						allowed_walls.pop(allowed_walls.index([self.A_walls[i][1] , self.A_walls[i][1] + 1]))
						allowed_walls.pop(allowed_walls.index([self.A_walls[i][0] - 1 , self.A_walls[i][0] ]))
						allowed_walls.pop(allowed_walls.index(self.crossingWallPair(list(self.A_walls[i]))))
					except:
						pass
				else:
					try:
						allowed_walls.pop(allowed_walls.index([self.A_walls[i][1] , self.A_walls[i][1] + 11]))
						allowed_walls.pop(allowed_walls.index([self.A_walls[i][0] - 11 , self.A_walls[i][0] ])) 
						allowed_walls.pop(allowed_walls.index(self.crossingWallPair(list(self.A_walls[i]))))
					except:
						pass
			if self.B_walls[i][0] != -1:
				allowed_walls.pop(allowed_walls.index([self.B_walls[i][0], self.B_walls[i][1]]))
				if self.B_walls[i][0] >= 110:
					try:
						allowed_walls.pop(allowed_walls.index([self.B_walls[i][1] , self.B_walls[i][1] + 1]))
						allowed_walls.pop(allowed_walls.index([self.B_walls[i][0] - 1 , self.B_walls[i][0] ]))
						allowed_walls.pop(allowed_walls.index(self.crossingWallPair(list(self.A_walls[i]))))
					except:
						pass
				else:
					try:
						allowed_walls.pop(allowed_walls.index([self.B_walls[i][1] , self.B_walls[i][1] + 11]))
						allowed_walls.pop(allowed_walls.index([self.B_walls[i][0] - 11 , self.B_walls[i][0] ]))
						allowed_walls.pop(allowed_walls.index(self.crossingWallPair(list(self.A_walls[i]))))
					except:
						pass

		return allowed_walls

	# initialising walls
	def initWalls(self):
		for j in range(10):
			for i in range(10):
				self.walls.append([110+j*11+i,111+j*11+i])

		for i in range(10):
			for j in range(10):
				self.walls.append([0+i*10+j,10+i*10+j])
		return

	def convertTo2D(self, state):
		# for visualisation
		board = np.zeros([11, 11])
		return

	# There should be at least one path that connects the figures and the opposite row.
	# The algorithm takes one step at each iteration and collects all the possible moves.
	# After the collection, it checks whether there is any position that is in the opposite line.
	def connected(self):
		connected = True
		#-----------------------------------
		# player A
		pmoves = [self.A_position] # this is neccessary to start the algorithm
		# collect all the possible moves, usually takes 15-20 iteration
		for i in range(20):
			for j in range(len(pmoves)):
				a = game.allowedMoves(pmoves[j], 39)
				for k in range(len(a)):
					if a[k] not in pmoves:
						pmoves.append(a[k])	

		# check whether there is a possible route to the top or bottom rows
		set_pmoves = set(pmoves)
		intersect_top = list(self.set_top.intersection(set_pmoves))
		intersect_bottom = list(self.set_bottom.intersection(set_pmoves))

		if len(intersect_top) == 0 or len(intersect_bottom) == 0:
			connected = False

		#-----------------------------------
		# player B - same as player A
		pmoves = [self.B_position]
		for i in range(20):
			for j in range(len(pmoves)):
				a = game.allowedMoves(pmoves[j], 39)
				for k in range(len(a)):
					if a[k] not in pmoves:
						pmoves.append(a[k])	

		set_pmoves = set(pmoves)
		intersect_top = list(self.set_top.intersection(set_pmoves))
		intersect_bottom = list(self.set_bottom.intersection(set_pmoves))

		if len(intersect_top) == 0 or len(intersect_bottom) == 0:
			connected = False

		return connected

game = Game()

game.initWalls()

game.A_walls[0] = [154, 155]

game.A_walls[0] = [4, 14]
game.A_walls[1] = [126, 127]
game.A_walls[2] = [6, 16]

allowedmoves = [90]

a = game.connected()

print(a)

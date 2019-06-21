import numpy as np
import time
import matplotlib.pyplot as plt

# the game class
class Game:
	def __init__(self):
		self.boardSize = 4 # number of positions = boardSize ** 2
		self.currentPlayer = 0 # 0:A, 1:B
		self.A_position = 5 # position of player A
		self.B_position = 1 # position of player B
		self.A_walls = np.full((self.boardSize - 1, 2), -1) # each element of the array represents the position of a given wall, -1 if it's off the board
		self.B_walls = np.full((self.boardSize - 1, 2), -1)
		self.bottom = [i for i in range(self.boardSize)] # field numbering - bottom
		self.left = [self.boardSize * i for i in range(self.boardSize)] # field numbering - left
		self.right = [self.boardSize - 1 + self.boardSize * i for i in range(self.boardSize)] # field numbering - right
		self.top = [self.boardSize ** 2 - self.boardSize + i for i in range(self.boardSize)] # field numbering - top
		self.walls = [] # list of walls placed on the board
		self.set_bottom = set(self.bottom)
		self.set_top = set(self.top)

	# outputs the neighbouring wall numbers of a position
	def wallnumber(self, position, direction):
		if direction == 'bottom':
			return self.boardSize * (self.boardSize - 1) + (int(position / self.boardSize) -1 ) * self.boardSize + position % self.boardSize
		elif direction == 'top':
			return self.boardSize * (self.boardSize - 1) + int(position / self.boardSize) * self.boardSize + position % self.boardSize
		elif direction == 'right':
			return int(position / self.boardSize) * (self.boardSize - 1) + position % self.boardSize
		elif direction == 'left':
			return int(position / self.boardSize) * (self.boardSize - 1) + position % self.boardSize - 1
		else:
			raise ValueError('invalid direction')

	# allowed moves of the figures given the position, the position of the opponent and the walls on the board
	def allowedMoves(self, position, position_opponent):
		allowed_moves = []

		# moving down
		if position not in self.bottom:
			if self.wallnumber(position, 'bottom') not in self.A_walls.flatten() and self.wallnumber(position, 'bottom') not in self.B_walls.flatten():
				if position_opponent != position - self.boardSize:
					allowed_moves.append(position - self.boardSize)
				elif position_opponent not in self.bottom and self.wallnumber(position_opponent, 'bottom') not in self.A_walls.flatten() and self.wallnumber(position_opponent, 'bottom') not in self.B_walls.flatten():
					allowed_moves.append(position - 2 * self.boardSize)

		# moving up
		if position not in self.top:
			if self.wallnumber(position, 'top') not in self.A_walls.flatten() and self.wallnumber(position, 'top') not in self.B_walls.flatten():
				if position_opponent != position + self.boardSize:
					allowed_moves.append(position + self.boardSize)
				elif position_opponent not in self.top and self.wallnumber(position_opponent, 'top') not in self.A_walls.flatten() and self.wallnumber(position_opponent, 'top') not in self.B_walls.flatten():
					allowed_moves.append(position + 2 * self.boardSize)

		# moving right
		if position not in self.right:
			if self.wallnumber(position, 'right') not in self.A_walls.flatten() and self.wallnumber(position, 'right') not in self.B_walls.flatten():
				if position_opponent != position + 1:
					allowed_moves.append(position + 1)
				elif position_opponent not in self.right and self.wallnumber(position_opponent, 'right') not in self.A_walls.flatten() and self.wallnumber(position_opponent, 'right') not in self.B_walls.flatten():
					allowed_moves.append(position + 2)

		# moving left
		if position not in self.left:
			if self.wallnumber(position, 'left') not in self.A_walls.flatten() and self.wallnumber(position, 'left') not in self.B_walls.flatten():
				if position_opponent != position - 1:
					allowed_moves.append(position - 1)
				elif position_opponent not in self.left and self.wallnumber(position_opponent, 'left') not in self.A_walls.flatten() and self.wallnumber(position_opponent, 'left') not in self.B_walls.flatten():
					allowed_moves.append(position - 2)

		return allowed_moves

	# outputs the crossing pair of a wall
	def crossingWallPair(self, wall): 
		if wall[0] >= (self.boardSize ** 2 - self.boardSize):
			pair = self.walls[self.walls.index(wall) + (self.boardSize-1) ** 2]
		else:
			pair = self.walls[self.walls.index(wall) - (self.boardSize-1) ** 2]

		return pair

	# There should be at least one path that connects the figures and the opposite row.
	# The algorithm takes one step at each iteration and collects all the possible moves.
	# After the collection, it checks whether there is any position that is in the opposite line.
	def connected(self):
		connected = True
		
		#-----------------------------------
		# player A

		pmoves = [None] * self.boardSize ** 2 # possible moves
		pmoves[0] = self.A_position # initialising with the first one
		none = self.boardSize ** 2 - 1
		count = 0

		for i in range(20): # 20 iterations are usually enough to walk through the whole board, probably depends on boardSize
			for j in range(self.boardSize ** 2 - none): # iterate through the array that contains that possible moves
				if pmoves[j] is not None:
					a = self.allowedMoves(pmoves[j], self.B_position) # calculate the allowed moves
					for k in a:
						if k not in pmoves: # if the algorithm found a new valid position, add it to pmoves
							pmoves[self.boardSize ** 2 - none] = k
							none -= 1

		# check whether there is a possible route to the top or bottom rows
		set_pmoves = set(pmoves)
		intersect_top = list(self.set_top.intersection(set_pmoves))
		intersect_bottom = list(self.set_bottom.intersection(set_pmoves))

		if len(intersect_top) == 0 or len(intersect_bottom) == 0: 
			connected = False

		#-----------------------------------
		# player B

		pmoves = [None] * self.boardSize ** 2 # possible moves
		pmoves[0] = self.B_position # initialising with the first one
		none = self.boardSize ** 2 - 1
		count = 0

		for i in range(20): # 20 iterations are usually enough to walk through the whole board, probably depends on boardSize
			for j in range(self.boardSize ** 2 - 1): # iterate through the array that contains that possible moves
				if pmoves[j] is not None:
					a = self.allowedMoves(pmoves[j], self.A_position) # calculate the allowed moves
					for k in a:
						if k not in pmoves: # if the algorithm found a new valid position, add it to pmoves
							pmoves[self.boardSize ** 2 - none] = k
							none -= 1

		# check whether there is a possible route to the top or bottom rows
		set_pmoves = set(pmoves)
		intersect_top = list(self.set_top.intersection(set_pmoves))
		intersect_bottom = list(self.set_bottom.intersection(set_pmoves))

		if len(intersect_top) == 0 or len(intersect_bottom) == 0: 
			connected = False

		return connected

	# removing wall positions that are not allowed
	def allowedWalls(self):
		self.initWalls()
		allowed_walls = np.copy(self.walls).tolist() # copy the array of walls placed on the board

		for i in range(self.boardSize - 1): # number of available walls for each player
			if self.A_walls[i][0] != -1:
				if self.A_walls[i][0] >= self.boardSize * (self.boardSize - 1):
					try:
						allowed_walls.pop(allowed_walls.index([self.A_walls[i][0] , self.A_walls[i][1]]))
					except:
						pass
					try:
						allowed_walls.pop(allowed_walls.index([self.A_walls[i][1] , self.A_walls[i][1] + 1]))
					except:
						pass
					try:
						allowed_walls.pop(allowed_walls.index([self.A_walls[i][0] - 1 , self.A_walls[i][0]]))
					except:
						pass
					try:
						allowed_walls.pop(allowed_walls.index(self.crossingWallPair(list(self.A_walls[i]))))
					except:
						pass
				else:
					try:
						allowed_walls.pop(allowed_walls.index([self.A_walls[i][0] , self.A_walls[i][1]]))
					except:
						pass
					try:
						allowed_walls.pop(allowed_walls.index([self.A_walls[i][1] , self.A_walls[i][1] + self.boardSize - 1]))
					except:
						pass
					try:
						allowed_walls.pop(allowed_walls.index([self.A_walls[i][0] - self.boardSize + 1 , self.A_walls[i][0]]))
					except:
						pass
					try:
						allowed_walls.pop(allowed_walls.index(self.crossingWallPair(list(self.A_walls[i]))))
					except:
						pass
				if self.B_walls[i][0] >= self.boardSize * (self.boardSize - 1):
					try:
						allowed_walls.pop(allowed_walls.index([self.B_walls[i][0] , self.B_walls[i][1]]))
					except:
						pass
					try:
						allowed_walls.pop(allowed_walls.index([self.B_walls[i][1] , self.B_walls[i][1] + 1]))
					except:
						pass
					try:
						allowed_walls.pop(allowed_walls.index([self.B_walls[i][0] - 1 , self.B_walls[i][0]]))
					except:
						pass
					try:
						allowed_walls.pop(allowed_walls.index(self.crossingWallPair(list(self.B_walls[i]))))
					except:
						pass
				else:
					try:
						allowed_walls.pop(allowed_walls.index([self.B_walls[i][0] , self.B_walls[i][1]]))
					except:
						pass
					try:
						allowed_walls.pop(allowed_walls.index([self.B_walls[i][1] , self.B_walls[i][1] + self.boardSize - 1]))
					except:
						pass
					try:
						allowed_walls.pop(allowed_walls.index([self.B_walls[i][0] - self.boardSize + 1 , self.B_walls[i][0]]))
					except:
						pass
					try:
						allowed_walls.pop(allowed_walls.index(self.crossingWallPair(list(self.B_walls[i]))))
					except:
						pass

		# Check whether the walls block the path between the players and the top or bottom rows

		counter = 0
		start = time.time()
		for i in range(len(allowed_walls)):
			try:	
				if self.A_walls[i][0] == -1: # check whether A has any unused walls
					self.A_walls[i] = allowed_walls[i - counter] # modify the board
					if self.connected() == False: # check whether move is allowed
						allowed_walls.pop(i-counter) # throw it away if blocks the path
						counter += 1
					self.A_walls[i] = [-1, -1] # restore the board
				else:
					self.B_walls[i] = allowed_walls[i-counter] # modify the board
					if self.connected() == False: # check whether move is allowed
						allowed_walls.pop(i-counter) # throw it away if blocks the path
						counter += 1
					self.B_walls[i] = [-1, -1] # restore the board
			except:
				pass
		end = time.time()

		# print('duration: ', start - end)

		return allowed_walls

	# initialising walls
	def initWalls(self):
		for j in range(self.boardSize - 1):
			for i in range(self.boardSize - 1):
				self.walls.append([(self.boardSize ** 2 - self.boardSize) + j * self.boardSize + i, (self.boardSize ** 2 - self.boardSize) + 1 + j * self.boardSize + i])

		for i in range(self.boardSize - 1):
			for j in range(self.boardSize - 1):
				self.walls.append([0 + i * (self.boardSize - 1) + j, (self.boardSize - 1) + i * (self.boardSize - 1) + j])
		return

game = Game()

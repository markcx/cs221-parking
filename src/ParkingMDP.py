from operator import itemgetter

class SmartParkingMDP(util.MDP):
	def __init__(self, P_dist, P_leave_params, Lots):
		"""
		The user will input 
		(estimated time of arrival, final destination, 
			max_dist of walking, max_price willing to pay, preference for shortest dist or cheapest lot)
		Solving this MDP formulation will estimate the value of choosing closest lot or cheapest lot

		P_dist: preference (probability) for closest lot to current lot. 
			1-P_dist = preference for next cheapest lot

		leave_params: (c1, c2), such that 
			lambda_leave = c1/AvailNum + c2/Price
		Lots: list of lots, 
			each lot is (lot_id, loc, AvailNum, Price, Dist to final dest)
			This list of lots is derived from the ML algorithm, which predicts (AvailNum, Price)
			for each lot, and we filter for only the lots which satisfy <= 
		"""
		self.P_dist = P_dist
		self.leave_params = leave_params
		self.Lots = Lots 		# list of tuples
		self.min_dist_index = 4
		self.min_price_index = 3

		self.Rewards = {
			'Leave': -1, 
			'Leave, no more lots', -1000,
			'Stay, but left', -10,
			'Stay, and stayed', 100
		}

	def getNextClosestLot(self, state):
		'''
		Returns the index of next closest lot to the destination that has not been visited
		'''
		Visited, IsEnd = state
		if sum(Visited) == len(Visited):
			return []	# all the lots have been visited

		min_dist = -1

		for i, lot in enumerate(self.Lots):
			if not Visited:
				if lot[self.min_dist_index] < min_dist or min_dist == -1:
					min_dist = lot[self.min_dist_index]
					min_index = i
		return min_index

	def getNextCheapestLot(self, state):
		'''
		Returns the next cheapest lot that has not been visited
		'''
		Visited, IsEnd = state
		if sum(Visited) == len(Visited):
			return []	# all the lots have been visited

		min_price = -1

		for i, lot in enumerate(self.Lots):
			if not Visited:
				if lot[self.min_price_index] < min_price or min_price == -1:
					min_price = lot[self.min_price_index]
					min_index = i
		return min_index

		# lot = min(self.Unvisited, key=itemgetter(self.min_price_index))
		# return lot

	def startState(self):
		'''
		Defines the starting state based on whether the user prefers
		closest lot to destination or cheapest lot. 

		State = (Visited, IsEnd)
		Visited = tuple of binary values indicating whether Lot[i] has been visited
		isEnd = 0 for not end state, 1 for end state
		'''
		# if P_dist > .5:		# min_dist_lot
		# 	index = getNextClosestLot()
		# else:	# min_price_lot
		# 	index = getNextCheapestLot()


		Visited = (0,)*len(self.Lots)
		return (Visited, 0)

	def actions(self, state):
		'''
		Return set of actions possible from |state|.
		'''
		return ['Leave', 'Stay']

	def changeState(self, Visited, Index):
		'''
		Given |Index| and bit tuple Visited, turn on the bit of Visited[Index]
		and return (result, IsEnd=0)
		'''
		_l = list(Visited)
		_l[Index] = 1
		return (tuple(_l),0)

	def succAndProbReward(self, state, action):
		'''
		Return a list of (newState, prob, reward) tuples corresponding to edges
		coming out of |state|.  Indicate a terminal state by setting state[1]=1
		'''
		Visited, IsEnd = state
		if IsEnd:	# terminal state
			return []
		
		closestLotIndex = getNextClosestLot(state)
		cheapestLotIndex = getNextCheapestLot(state)
		if action == 'Leave':
			if sum(Visited) == len(Visited):	# all the lots have been visited
				newState = (None, 1)
				reward = self.Rewards['Leave, no more lots']
				return [(newState, 1, reward)]

			succAndProbReward_closestLot = (changeState(Visited, closestLotIndex),self.P_dist, self.Rewards['Leave'])
			succAndProbReward_cheapestLot = (changeState(Visited, cheapest), 1-self.P_dist, self.Rewards['Leave'])

			return [succAndProbReward_closestLot, succAndProbReward_cheapestLot]

		else:	# action == 'Stay'

			

			if sum(Visited) == len(Visited):	# all the lots have been visited
				newState = (None, 1)
				reward = self.Rewards['Leave, no more lots']
				return [(newState, 1, reward)]

			succAndProbReward_closestLot = (changeState(Visited, closestLotIndex),self.P_dist, self.Rewards['Leave'])
			succAndProbReward_cheapestLot = (changeState(Visited, cheapest), 1-self.P_dist, self.Rewards['Leave'])

			return [succAndProbReward_closestLot, succAndProbReward_cheapestLot]




	def discount(self):
		return 1













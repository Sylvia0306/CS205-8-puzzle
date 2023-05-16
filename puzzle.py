import queue
import copy as cp
import math
import time


class Node:

	def __init__(self, state):
		self.state = state
		self.gn = 0
		self.hn = 0
		self.fn = 0

	def __repr__(self):
		return str(self.state)

	def getState(self):
		return self.state

	def setGn(self, gn):
		self.gn = gn

	def getGn(self):
		return self.gn

	def setHn(self, hn):
		self.hn = hn

	def getHn(self):
		return self.hn

	def setFn(self, fn):
		self.fn = fn

	def getFn(self):
		return self.fn

	def __lt__(self, otherNode):
		return self.fn < otherNode.fn


class Problem:

	def __init__(self, initState):
		self.goal = [1,2,3,4,5,6,7,8,0]
		self.initState = initState
		self.map = set()
		self.test(self.initState)
		self.count = 0

	def blank(self, state):
		for blankIndex, value in enumerate(state):
			if value == 0:
				return blankIndex

	def initialState(self):
		return self.initState

	def test(self, state):	
		if self.goal == state:
			return True
		else:
			return False
		

	def testMove(self, tState):
		if tuple(tState) in self.map:
			return False
		else:
			self.map.add(tuple(tState))
			return True

	def nodeCount(self):
		return self.count

	def operators(self, state):
		Curstate = state.getState()
		blankID = self.blank(Curstate)
		self.count += 1

		operator = list()

		# move left (except id 0,3,6)
		if blankID%3 != 0:
			nodeLeft = cp.deepcopy(Curstate)
			temp = nodeLeft[blankID]
			nodeLeft[blankID] = nodeLeft[blankID-1]
			nodeLeft[blankID-1] = temp
			nodeLeft = Node(nodeLeft)
			nodeLeft.setGn(state.getGn()+1)
			if self.testMove(nodeLeft.getState()):
				operator.append(nodeLeft)

		# move right (except id 2,5,8)
		if blankID%3 != 2:
			nodeRight = cp.deepcopy(Curstate)
			temp = nodeRight[blankID]
			nodeRight[blankID] = nodeRight[blankID+1]
			nodeRight[blankID+1] = temp
			nodeRight = Node(nodeRight)
			nodeRight.setGn(state.getGn()+1)
			if self.testMove(nodeRight.getState()):
				operator.append(nodeRight)

		# move up (except id 0,1,2)
		if blankID > 2:
			nodeUp = cp.deepcopy(Curstate)
			temp = nodeUp[blankID]
			nodeUp[blankID] = nodeUp[blankID-3]
			nodeUp[blankID-3] = temp
			nodeUp = Node(nodeUp)
			nodeUp.setGn(state.getGn()+1)
			if self.testMove(nodeUp.getState()):
				operator.append(nodeUp)

		# move down (except id 6,7,8)
		if blankID < 6:
			nodeDown = cp.deepcopy(Curstate)
			temp = nodeDown[blankID]
			nodeDown[blankID] = nodeDown[blankID+3]
			nodeDown[blankID+3] = temp
			nodeDown = Node(nodeDown)
			nodeDown.setGn(state.getGn()+1)
			if self.testMove(nodeDown.getState()):
				operator.append(nodeDown)
		return operator



def general_search(problem, queueFunc):
	initNode = Node(problem.initialState())
	initNode.setGn(0)
	initNode.setHn(0)
	initNode.setFn(0)
	nodes = queue.PriorityQueue()
	nodes.put(initNode)
	print("first node")
	printNode(initNode)
	maxSize = nodes.qsize()

	start = time.time()
	while(1):
		if nodes.empty():
			return "failure"

		node = nodes.get()

		if problem.test(node.getState()):
			print("Goal State!!!!!!")
			print("Solution depth was {depth}".format(depth = node.getGn()))
			print("Number of nodes expanded: {total}".format(total = problem.nodeCount()))
			print("Max queue size: {max}".format(max = maxSize))
			end = time.time()
			exeTime = round((end-start),4)
			print("execution time was {t}".format(t = exeTime))
			return node

		testSize = nodes.qsize()
		if testSize > maxSize:
			maxSize = testSize

		print("The best state to expand with a g(n) = {gn} and h(n) = {hn} is ...".format(gn=node.getGn(), hn=node.getHn()))
		printNode(node)
		print()
		nodes = queueFunc(nodes, problem.operators(node))


def uniform(nodes, nodes2):
	sortNode = nodes
	for node in nodes2:
		node.setHn(0)
		node.setFn(node.getGn() + 0)
		sortNode.put(node)
	return sortNode


def manhattan_distance(test):
	goal = [1,2,3,4,5,6,7,8,0]
	distance = 0
	for index, (test,goal) in enumerate(zip(test,goal)):
		if test == goal or test == 0:
			continue
		else:
			num = test - 1
			
			tRow = num/3
			tCol = num % 3

			idRow = index/3
			idCol = index % 3

			rowDist = math.floor(tRow) - math.floor(idRow)
			colDist = tCol - idCol

			if rowDist < 0:
				rowDist = -1*rowDist

			if colDist < 0:
				colDist = -1*colDist

			dist = rowDist + colDist
			distance += dist

	return distance


def aStar_manhattan(nodes, nodes2):
	sortNode = nodes
	for node in nodes2:
		dist = manhattan_distance(node.getState())
		node.setHn(dist)
		node.setFn(node.getGn() + node.getHn())
		sortNode.put(node)
	return sortNode


def misplaced_distance(test):
	goal = [1,2,3,4,5,6,7,8,0]
	distance = 0
	for test,goal in zip(test, goal):
		if test == 0:
			continue
		if test != goal:
			distance += 1
	return distance


def aStar_misplaced(nodes, nodes2):
	sortNode = nodes
	for node in nodes2:
		distance = misplaced_distance(node.getState())
		node.setHn(distance)
		node.setFn(node.getGn() + distance)
		sortNode.put(node)
	return sortNode


def start():
	puzzle = []
	gaol = [1,2,3,4,5,6,7,8,0]
	defaultPuzzle = [1,3,6,5,0,2,4,7,8]

	intro = "Welcome to Yin-Yu's 8-puzzle solver.\n Type '1' to use a default puzzle, or '2' to enter your own one." 
	print(intro)
	option = int(input())

	if option == 1:
		puzzle = defaultPuzzle
		print(puzzle)

	elif option == 2:
		text = "Enter your own puzzle from left to right and top to down, and use 0 to represent the blank."
		print(text)
		ownPuzzle = [int(num) for num in input().split()]
		puzzle = ownPuzzle
		print(puzzle)

	text2 = "Select a algorithm.\n 1. Uniform Cost Search\n 2. A* with the Misplaced Tile heuristic\n 3. A* with the Manhattan distance heuristic"
	print(text2)
	algorithmChoose = str(input())
	algorithm = {'1': uniform, '2': aStar_misplaced, '3': aStar_manhattan}
	problem = Problem(puzzle)
	node = general_search(problem, algorithm[algorithmChoose])
	return node


def printNode(pNode):
	for index, num in enumerate(pNode.getState()):
		print(num, end=' ')
		if index % 3 == 2:
			print()


if __name__ == '__main__':
	start()
	

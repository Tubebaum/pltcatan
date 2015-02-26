from collections import deque

types = ["lumber", "ore", "gold", "wool"]


def BFS_gen(node, depth):
	def connect(node1, node2, ang):
		if (node2 == None):
			return
		node1.adjlist[ang] = node2
		node2.adjlist[(ang+3)%6] = node1

	queue = deque()
	queue.append(node)
	queue.append("lvl++")
	lvl = 1
	while(True):
		node = queue.popleft()
		if (node == "lvl++"):
			lvl += 1
			# print "lvl = " + str(lvl)
			queue.append("lvl++")
			if(lvl > depth):
				return
			continue

		for idx in range(6):
			if (node.adjlist[idx] == None):
				new_node = Node()
				connect(node, new_node, idx)
				connect(new_node, node.adjlist[(idx+1)%6], (idx+2)%6)
				connect(new_node, node.adjlist[(idx-1)%6], (idx-2)%6)
				queue.append(new_node)

class Node:
	def __init__(self):
		self.data = None
		self.adjlist = list(None for i in range(6))

class Game:

	def __init__(self, nplayers, boardsize=3):
		self.players = []
		self.boardsize = boardsize


	def gen_board(self):
		self.center = Node()
		BFS_gen(self.center, 2)

	# Intended for testing
	def count_nodes(self):
		return len(list(self.nodes()))

	# Python generator returning each node
	def nodes(self):
		visited = set()
		queue = deque()
		queue.append(self.center)
		visited.add(self.center)
		while(len(queue) != 0):
			node = queue.popleft()
			for neig in node.adjlist:
				# print neig
				if (neig != None and neig not in visited):
					queue.append(neig)
					visited.add(neig)
			yield node
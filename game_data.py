from collections import deque

types = ["lumber", "ore", "gold", "wool"]


def BFS_gen(node, depth):
	queue = deque()
	queue.append(node)
	queue.append("lvl++")
	lvl = 1
	while(True):
		node = queue.popleft()
		if (node == "lvl++"):
			lvl += 1
			queue.append("lvl++")
			if(lvl > depth):
				return
			continue

		for neig_idx in range(len(node.adjlist)):
			neig = node.adjlist[neig_idx]
			if (neig == None):
				neig = Node()
				neig.adjlist[(neig_idx+3)%6]
				queue.append(neig)


def 

class Node:
	def __init__(self):
		print Node.cont
		self.data = None
		self.adjlist = list(None for i in range(6))

class Game:

	def __init__(self, nplayers, boardsize=3):
		self.players = []
		self.boardsize = boardsize


	def gen_board(self):
		center = Node()
		BFS_gen(center, 2)
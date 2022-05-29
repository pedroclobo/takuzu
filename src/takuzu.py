# Grupo 41:
# 99079 Guilherme Pascoal
# 99115 Pedro Lobo

from sys import stdin
import numpy as np
from search import (
    Problem,
    Node,
    compare_searchers,
    astar_search,
    breadth_first_graph_search,
    breadth_first_tree_search,
    depth_first_graph_search,
    depth_first_tree_search,
    greedy_search,
    iterative_deepening_search,
    uniform_cost_search,
)


class TakuzuState:
	state_id = 0

	def __init__(self, board):
		self.board = board
		self.id = TakuzuState.state_id
		TakuzuState.state_id += 1

	def __lt__(self, other):
		return len(self.board.get_free_positions()) < \
		       len(other.board.get_free_positions())

	def __eq__(self, other):
		return self.board == other.board

	def __hash__(self):
		return self.id

	def get_board(self):
		return self.board.copy()

	# TODO: outros metodos da classe


class Board:
	"""Internal representation of Takuzu board."""

	def __init__(self, board):
		self.board = np.array(board)
		self.dimension = len(self.board)

		# Compute free positions
		self.free = []
		for i in range(self.dimension):
			for j in range(self.dimension):
				if self.get_number(i, j) == 2:
					self.free.append((i, j))

	def get_number(self, row: int, col: int) -> int:
		"""Return value in given position."""
		return self.board[row, col]

	def adjacent_vertical_numbers(self, row: int, col: int) -> (int, int):
		"""Return values under and above the given position."""
		first = self.get_number(row + 1, col) if row != self.dimension - 1 else None
		sec = self.get_number(row - 1, col) if row != 0 else None

		return (first, sec)

	def adjacent_horizontal_numbers(self, row: int, col: int) -> (int, int):
		"""Return values to left and to the right of the given position."""
		first = self.get_number(row, col - 1) if col != 0 else None
		sec = self.get_number(row, col + 1) if col != self.dimension - 1 else None

		return (first, sec)

	@staticmethod
	def parse_instance_from_stdin():
		"""Reads input from stdin and returns a new Board instance."""
		dimension = int(input())
		board = []

		while dimension > 0:
			board += [[int(x) for x in stdin.readline().strip().split("\t")]]
			dimension -= 1

		return Board(board)

	def copy(self):
		"""Return copy of Board instance."""
		return Board(self.board)

	def place_number(self, row: int, col: int, number: int):
		"""Place number on board instance."""
		self.board[row][col] = number
		self.free = [el for el in self.free if el != (row, col)]

	def get_free_positions(self):
		"""Return coordinates of free position."""
		return self.free

	def check_count_criteria(self):
		"""Check if specified row or column has an equal amount of 0 and 1,
		or an amount differing by 1 if the board's dimension is odd."""
		for i in range(self.dimension):
			zeros = np.count_nonzero(self.board[i, ] == 0)
			ones = np.count_nonzero(self.board[i, ] == 1)

			if (self.dimension % 2 == 0 and zeros != ones) or \
			   (self.dimension % 2 != 0 and \
			   (zeros != ones + 1 or zeros + 1 != ones)):
				return False

		for j in range(self.dimension):
			zeros = np.count_nonzero(self.board[:, j] == 0)
			ones = np.count_nonzero(self.board[:, j] == 1)

			if (self.dimension % 2 == 0 and zeros != ones) or \
			   (self.dimension % 2 != 0 and \
			   (zeros != ones + 1 or zeros + 1 != ones)):
				return False

		return True

	def check_adjacency_criteria(self):
		"""Check if there aren't more than 2 adjacent numbers."""
		for i in range(self.dimension):
			for j in range(self.dimension):
				number = self.get_number(i, j)
				adjacent_h = self.adjacent_horizontal_numbers(i, j)
				adjacent_v = self.adjacent_vertical_numbers(i, j)

				if (adjacent_h + (number, )).count(number) == 3 or \
				   (adjacent_v + (number, )).count(number) == 3:
					return False

		return True

	def check_vector_inequality_criteria(self):
		"""Check if all rows are different and if all columns are different."""
		return not (self.board == self.board[0]).all() and \
		       not (self.board.T == self.board.T[0]).all()

	def check_resolved_board(self):
		"""Check if board is resolved."""
		return self.is_full() and \
		       self.check_count_criteria() and \
		       self.check_adjacency_criteria() and \
		       self.check_vector_inequality_criteria()

	def __eq__(self, other):
		return (self.board == other.board).all()

	def __str__(self):
		"""Board representation."""
		string = ""

		for i in range(self.dimension):
			for j in range(self.dimension):
				string += str(self.get_number(i, j))
				if j != self.dimension - 1:
					string += "\t"

			if i != self.dimension - 1:
				string += "\n"

		return string

	def is_valid_play(self, play):
		"""Check if play respects the game rules."""
		row, col, number = play
		self.place_number(row, col, number)

		# Check count criteria
		zeros_r = np.count_nonzero(self.board[row, ] == 0)
		ones_r = np.count_nonzero(self.board[row, ] == 1)
		zeros_c = np.count_nonzero(self.board[:, col] == 0)
		ones_c = np.count_nonzero(self.board[:, col] == 1)

		if self.dimension % 2 == 0:
			if zeros_r > self.dimension / 2 or ones_r > self.dimension / 2 or \
			   zeros_c > self.dimension / 2 or ones_c > self.dimension / 2:
				return False

		else:
			if zeros_r > self.dimension // 2 + 1 or ones_r > self.dimension // 2 + 1 or \
			   zeros_c > self.dimension // 2 + 1 or ones_c > self.dimension // 2 + 1:
				return False

		# Check adjacency criteria
		if self.adjacent_vertical_numbers(row, col).count(number) > 2 or \
		   self.adjacent_horizontal_numbers(row, col).count(number) > 2:
			return False

		# Check for different rows and columns
		return self.check_vector_inequality_criteria()

	def is_full(self):
		return len(self.free) == 0

	def restrictions(self, row, col):
		return len([el for el in self.adjacent_vertical_numbers(row, col) if el != None and el != 2]) + \
		       len([el for el in self.adjacent_horizontal_numbers(row, col) if el != None and el != 2])

	# TODO: outros metodos da classe


class Takuzu(Problem):

	def __init__(self, board: Board):
		"""Constructor specifies initial state."""
		super().__init__(TakuzuState(board))
		self.state = TakuzuState(board)

	def actions(self, state: TakuzuState):
		"""Return a collection of actions which can be executed from the given state."""
		actions = []
		board = state.get_board()

		for (row, col) in board.get_free_positions():
			for number in (0, 1):
				action = (row, col, number)
				if board.is_valid_play(action):
					actions += [action, ]

		# Order actions using degree heuristic
		actions.sort(key=lambda tup: board.restrictions(tup[0], tup[1]), reverse=True)

		return actions

	def result(self, state: TakuzuState, action):
		"""Returns the state obtained from executing 'action' in 'state'."""
		(row, col, number) = action
		board = state.get_board()
		board.place_number(row, col, number)

		return TakuzuState(board)

	def goal_test(self, state: TakuzuState):
		"""Return True if 'state' if a goal state."""
		return state.board.check_resolved_board()

	def h(self, node: Node):
		"""Heuristic for A*."""
		board = node.state.board

		# Number of free positions
		h1 = len(board.get_free_positions())

		return max(h1, 0)

	# TODO: outros metodos da classe


if __name__ == "__main__":
	board = Board.parse_instance_from_stdin()

	searchers = [
	    astar_search,
	    breadth_first_graph_search,
	    breadth_first_tree_search,
	    depth_first_graph_search,
	    depth_first_tree_search,
	    greedy_search,
	    iterative_deepening_search,
	    uniform_cost_search
	]

	compare_searchers([Takuzu(board)], "", searchers)

	#node = astar_search(Takuzu(board))
	#node = breadth_first_graph_search(Takuzu(board))
	#node = breadth_first_tree_search(Takuzu(board))
	#node = depth_first_graph_search(Takuzu(board))
	#node = depth_first_tree_search(Takuzu(board))
	#node = greedy_search(Takuzu(board))
	#node = iterative_deepening_search(Takuzu(board))
	#node = uniform_cost_search(Takuzu(board))

	#print(node.state.board)

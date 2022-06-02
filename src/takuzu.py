# Grupo 41:
# 99079 Guilherme Pascoal
# 99115 Pedro Lobo

from sys import stdin
import numpy as np
from search import (
    Problem,
    Node,
    depth_first_tree_search,
)


class TakuzuState:
	state_id = 0

	def __init__(self, board):
		self.board = board
		self.id = TakuzuState.state_id
		TakuzuState.state_id += 1

	def __lt__(self, other):
		return len(self.board.free_positions()) < len(other.board.free_positions())

	def get_board(self):
		return self.board.copy()


class Board:
	"""Internal representation of Takuzu board."""

	def __init__(self, board):
		self.board = np.array(board)
		self.dimension = len(self.board)

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

	def copy(self):
		"""Return copy of Board instance."""
		return Board(self.board)

	def get_number(self, row: int, col: int) -> int:
		"""Return value in given position."""
		return self.board[row, col]

	def place_number(self, row: int, col: int, number: int):
		"""Place number on board instance."""
		self.board[row, col] = number

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

	def check_adjacency(self, row, col):
		number = self.get_number(row, col)

		if self.adjacent_horizontal_numbers(row, col).count(number) == 2 or \
		   self.adjacent_vertical_numbers(row, col).count(number) == 2:
			return False

		return True

	def vector_count(self, index, el, row):
		"""Count the number of occurrences of an element in a row or column."""
		return np.count_nonzero(self.board[index, ] == el) if row else \
		       np.count_nonzero(self.board[:, index] == el)

	def free_positions(self):
		"""Return coordinates of free position."""
		(row, col) = np.where(self.board == 2)
		return list(zip(row, col))

	@staticmethod
	def parse_instance_from_stdin():
		"""Reads input from stdin and returns a new Board instance."""
		dimension = int(input())
		board = []

		while dimension > 0:
			board.append([int(x) for x in stdin.readline().split("\t")])
			dimension -= 1

		return Board(board)

	def check_resolved_board(self):
		"""Check if board is resolved."""

		def is_full(self):
			"""Check if board in completely filled."""
			return np.count_nonzero(self.board == 2) == 0

		def equality_rule(self):
			"""Check if specified row or column has an equal amount of 0 and 1,
			or an amount differing by 1 if the board's dimension is odd."""
			for i in range(self.dimension):
				zeros_row = self.vector_count(i, 0, True)
				ones_row = self.vector_count(i, 1, True)
				zeros_col = self.vector_count(i, 0, False)
				ones_col = self.vector_count(i, 1, False)

				if self.dimension % 2 == 0:
					if zeros_row != ones_row or zeros_col != ones_col:
						return False
				else:
					if (zeros_row != ones_row + 1 and zeros_row + 1 != ones_row) or \
					   (zeros_col != ones_col + 1 and zeros_col + 1 != ones_col):
						return False

			return True

		def adjacency_rule(self):
			"""Check if there aren't more than 2 adjacent numbers."""
			for i in range(self.dimension):
				for j in range(self.dimension):
					if self.check_adjacency(i, j) == False:
						return False

			return True

		def uniqueness_rule(self):
			"""Check if all rows are different and if all columns are different."""
			return len(np.unique(self.board, axis=0)) == self.dimension and \
			       len(np.unique(self.board.T, axis=0)) == self.dimension

		return is_full(self) and uniqueness_rule(self) and \
		       equality_rule(self) and adjacency_rule(self)


class Takuzu(Problem):

	def __init__(self, board: Board):
		"""Constructor specifies initial state."""
		self.initial = TakuzuState(board)

	def actions(self, state: TakuzuState):
		"""Return a collection of actions which can be executed from the given state."""

		def infer_number(board, row, col):
			adjacent_h = board.adjacent_horizontal_numbers(i, j)
			adjacent_v = board.adjacent_vertical_numbers(i, j)

			if adjacent_h.count(0) == 2 or adjacent_v.count(0) == 2:
				return 1
			elif adjacent_h.count(1) == 2 or adjacent_v.count(1) == 2:
				return 0

			if board.vector_count(row, 0, True) >= board.dimension / 2 or \
			   board.vector_count(col, 0, False) >= board.dimension / 2:
				return 1
			elif board.vector_count(row, 1, True) >= board.dimension / 2 or \
			     board.vector_count(col, 1, False) >= board.dimension / 2:
				return 0

			return None

		board = state.board

		for i in range(board.dimension - 1, -1, -1):
			for j in range(board.dimension - 1, -1, -1):
				if board.get_number(i, j) == 0:
					adjacent_h = board.adjacent_horizontal_numbers(i, j)
					adjacent_v = board.adjacent_vertical_numbers(i, j)

					if adjacent_h == (2, 0):
						return [(i, j - 1, 1)]
					elif adjacent_h == (0, 2):
						return [(i, j + 1, 1)]
					elif adjacent_v == (2, 0):
						return [(i + 1, j, 1)]
					elif adjacent_v == (0, 2):
						return [(i - 1, j, 1)]

				elif board.get_number(i, j) == 1:
					adjacent_h = board.adjacent_horizontal_numbers(i, j)
					adjacent_v = board.adjacent_vertical_numbers(i, j)

					if adjacent_h == (2, 1):
						return [(i, j - 1, 0)]
					elif adjacent_h == (1, 2):
						return [(i, j + 1, 0)]
					elif adjacent_v == (2, 1):
						return [(i + 1, j, 0)]
					elif adjacent_v == (1, 2):
						return [(i - 1, j, 0)]

				elif board.get_number(i, j) == 2:
					number = infer_number(board, i, j)
					if number != None:
						return [(i, j, number)]

		for i in range(board.dimension - 1, -1, -1):
			for j in range(board.dimension - 1, -1, -1):
				if board.get_number(i, j) == 2:
					return [(i, j, 0), (i, j, 1)]

		return []

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
		return len(node.state.board.free_positions())


if __name__ == "__main__":
	board = Board.parse_instance_from_stdin()

	node = depth_first_tree_search(Takuzu(board))
	print(node.state.board)

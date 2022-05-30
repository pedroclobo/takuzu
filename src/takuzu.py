# Grupo 41:
# 99079 Guilherme Pascoal
# 99115 Pedro Lobo

from sys import stdin
import numpy as np
from search import (
    Problem,
    Node,
    astar_search,
    breadth_first_tree_search,
    depth_first_tree_search,
    greedy_search,
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

	# TODO: outros metodos da classe


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

	def vector_count(self, index, el, row):
		"""Count the number of occurrences of an element in a row or column."""
		return np.count_nonzero(self.board[index, ] == el) if row else \
		       np.count_nonzero(self.board[:, index] == el)

	def free_positions(self):
		"""Return coordinates of free position."""
		positions = ()

		for i in range(self.dimension):
			for j in range(self.dimension):
				if self.get_number(i, j) == 2:
					positions += ((i, j), )

		return positions

	def get_row(self, index):
		return self.board[index, ]

	def get_col(self, index):
		return self.board[:, index]

	@staticmethod
	def parse_instance_from_stdin():
		"""Reads input from stdin and returns a new Board instance."""
		dimension = int(input())
		board = []

		while dimension > 0:
			board += [[int(x) for x in stdin.readline().strip().split("\t")]]
			dimension -= 1

		return Board(board)

	def uniqueness_rule(self):
		"""Check if all rows are different and if all columns are different."""
		return len(np.unique(self.board, axis=0)) == self.dimension and \
		       len(np.unique(self.board.T, axis=0)) == self.dimension

	def check_resolved_board(self):
		"""Check if board is resolved."""

		def is_full(self):
			"""Check if board in completely filled."""
			return np.count_nonzero(self.board == 2) == 0

		def equality_rule(board):
			"""Check if specified row or column has an equal amount of 0 and 1,
			or an amount differing by 1 if the board's dimension is odd."""
			for i in range(board.dimension):
				zeros = np.count_nonzero(board.board[i, ] == 0)
				ones = np.count_nonzero(board.board[i, ] == 1)

				if board.dimension % 2 == 0:
					if zeros != ones:
						return False
				else:
					if zeros != ones + 1 and zeros + 1 != ones:
						return False

			for j in range(board.dimension):
				zeros = np.count_nonzero(board.board[:, j] == 0)
				ones = np.count_nonzero(board.board[:, j] == 1)

				if board.dimension % 2 == 0:
					if zeros != ones:
						return False
				else:
					if zeros != ones + 1 and zeros + 1 != ones:
						return False

			return True

		def adjacency_rule(board):
			"""Check if there aren't more than 2 adjacent numbers."""
			for i in range(board.dimension):
				for j in range(board.dimension):
					number = board.get_number(i, j)
					adjacent_h = board.adjacent_horizontal_numbers(i, j)
					adjacent_v = board.adjacent_vertical_numbers(i, j)

					if (adjacent_h + (number, )).count(number) == 3 or \
					   (adjacent_v + (number, )).count(number) == 3:
						return False

			return True

		return is_full(self) and equality_rule(self) and \
               adjacency_rule(self) and self.uniqueness_rule()

	def is_valid_play(self, play):
		"""Check if play respects the game rules."""
		row, col, number = play
		self.place_number(row, col, number)

		# Equality rule
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

		# Adjacency rule
		if self.adjacent_vertical_numbers(row, col).count(number) >= 2 or \
		   self.adjacent_horizontal_numbers(row, col).count(number) >= 2:
			return False

		# Uniqueness rule
		return self.uniqueness_rule()

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

		def infer_number(board, row, col):
			if board.adjacent_horizontal_numbers(row, col).count(0) == 2 or \
			   board.adjacent_vertical_numbers(row, col).count(0) == 2:
				return 1
			elif board.adjacent_horizontal_numbers(row, col).count(1) == 2 or \
			     board.adjacent_vertical_numbers(row, col).count(1) == 2:
				return 0

			if board.vector_count(row, 0, True) >= board.dimension / 2 or \
			   board.vector_count(col, 0, False) >= board.dimension / 2:
				return 1
			elif board.vector_count(row, 1, True) >= board.dimension / 2 or \
			     board.vector_count(col, 1, False) >= board.dimension / 2:
				return 0

			return None

		actions = []
		board = state.get_board()

		tup = (1, 0)
		for i in range(board.dimension):
			row = board.get_row(i)
			for j in range(board.dimension):
				row_comp = board.get_row(j)
				comp = (row == row_comp)
				if np.count_nonzero(comp == False) == 1:
					position = np.where(comp == False)[0][0]
					number = row_comp[position]

					if number == 2:
						number = tup[row[position]]
						return [(j, position, number)]
					elif row[position] == 2:
						number = tup[row_comp[position]]
						return [(i, position, number)]

		for i in range(board.dimension):
			col = board.get_col(i)
			for j in range(board.dimension):
				col_comp = board.get_col(j)
				comp = (col == col_comp)
				if np.count_nonzero(comp == False) == 1:
					position = np.where(comp == False)[0][0]
					number = col_comp[position]

					if number == 2:
						number = tup[col[position]]
						return [(position, j, number)]
					elif col[position] == 2:
						number = tup[col_comp[position]]
						return [(position, i, number)]

		for i in range(board.dimension):
			for j in range(board.dimension):
				if board.get_number(i, j) == 0:
					if board.adjacent_horizontal_numbers(i, j) == (2, 0):
						return [(i, j - 1, 1)]
					elif board.adjacent_horizontal_numbers(i, j) == (0, 2):
						return [(i, j + 1, 1)]
					elif board.adjacent_vertical_numbers(i, j) == (2, 0):
						return [(i + 1, j, 1)]
					elif board.adjacent_vertical_numbers(i, j) == (0, 2):
						return [(i - 1, j, 1)]

				elif board.get_number(i, j) == 1:
					if board.adjacent_horizontal_numbers(i, j) == (2, 1):
						return [(i, j - 1, 0)]
					elif board.adjacent_horizontal_numbers(i, j) == (1, 2):
						return [(i, j + 1, 0)]
					elif board.adjacent_vertical_numbers(i, j) == (2, 1):
						return [(i + 1, j, 0)]
					elif board.adjacent_vertical_numbers(i, j) == (1, 2):
						return [(i - 1, j, 0)]

				elif board.get_number(i, j) == 2:
					number = infer_number(board, i, j)
					if number != None:
						return [(i, j, number)]


		for (row, col) in board.free_positions():
			for number in (0, 1):
				action = (row, col, number)
				if board.is_valid_play(action):
					actions.append(action)

		# Degree heuristic
		actions.sort(key=lambda tup: board.restrictions(tup[0], tup[1]),
		             reverse=True)

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
		return len(node.state.board.free_positions())

	# TODO: outros metodos da classe


if __name__ == "__main__":
	board = Board.parse_instance_from_stdin()

	searchers = [
	    astar_search,
	    breadth_first_tree_search,
	    depth_first_tree_search,
	    greedy_search,
	]

	node = depth_first_tree_search(Takuzu(board))

	print(node.state.board)

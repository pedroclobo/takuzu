# takuzu.py: Template para implementação do projeto de Inteligência Artificial 2021/2022.
# Devem alterar as classes e funções neste ficheiro de acordo com as instruções do enunciado.
# Além das funções e classes já definidas, podem acrescentar outras que considerem pertinentes.

# Grupo 41:
# 99115 Pedro Lobo
# 99079 Guilherme Pascoal

from sys import stdin
import numpy as np
from search import (
    Problem,
    Node,
    astar_search,
    breadth_first_tree_search,
    depth_first_tree_search,
    greedy_search,
    recursive_best_first_search,
)


class TakuzuState:
	state_id = 0

	def __init__(self, board):
		self.board = board
		self.id = TakuzuState.state_id
		TakuzuState.state_id += 1

	def __lt__(self, other):
		return self.id < other.id

	def get_board(self):
		return self.board.copy()

	# TODO: outros metodos da classe


class Board:
	"""Representação interna de um tabuleiro de Takuzu."""

	def __init__(self, board):
		self.board = np.array(board)
		self.dimension = len(self.board)

	def get_number(self, row: int, col: int) -> int:
		"""Devolve o valor na respetiva posição do tabuleiro."""
		return self.board[row][col]

	def adjacent_vertical_numbers(self, row: int, col: int) -> (int, int):
		"""Devolve os valores imediatamente abaixo e acima, respectivamente."""
		first = self.board[row + 1][col] if row != self.dimension - 1 else None
		sec = self.board[row - 1][col] if row != 0 else None

		return (first, sec)

	def adjacent_horizontal_numbers(self, row: int, col: int) -> (int, int):
		"""Devolve os valores imediatamente à esquerda e à direita, respectivamente."""
		first = self.board[row][col - 1] if col != 0 else None
		sec = self.board[row][col + 1] if col != self.dimension - 1 else None

		return (first, sec)

	@staticmethod
	def parse_instance_from_stdin():
		"""Lê o test do standard input (stdin) que é passado como argumento
        e retorna uma instância da classe Board.

        Por exemplo:
            $ python3 takuzu.py < input_T01

            > from sys import stdin
            > stdin.readline()
        """
		dimension = int(input())
		board = []

		while dimension > 0:
			board += [[int(x) for x in stdin.readline().strip().split("\t")]]
			dimension -= 1

		return Board(board)

	def copy(self):
		return Board(self.board)

	def place_number(self, row: int, col: int, number: int):
		self.board[row][col] = number

	def is_free_position(self, row: int, col: int):
		return self.get_number(row, col) == 2

	def get_free_positions(self):
		positions = ()
		for i in range(self.dimension):
			for j in range(self.dimension):
				if self.is_free_position(i, j):
					positions += ((i, j), )

		return positions

	def check_numbers(self):
		# Line check
		for i in range(self.dimension):
			zeros = np.count_nonzero(self.board[i, ] == 0)
			ones = np.count_nonzero(self.board[i, ] == 1)

			if self.dimension % 2 == 0:
				if zeros != ones:
					return False
			else:
				if zeros > ones + 1 or ones > zeros + 1:
					return False


        # Column check
		for j in range(self.dimension):
			zeros = np.count_nonzero(self.board[:, j] == 0)
			ones = np.count_nonzero(self.board[:, j] == 1)

			if self.dimension % 2 == 0:
				if zeros != ones:
					return False
			else:
				if zeros > ones + 1 or ones > zeros + 1:
					return False

		return True

	def check_adjacency(self):
		for i in range(self.dimension):
			for j in range(self.dimension):
				number = self.get_number(i, j)
				adjacent_h = self.adjacent_horizontal_numbers(i, j)
				adjacent_v = self.adjacent_vertical_numbers(i, j)

				if (adjacent_h + (number, )).count(number) == 3 or \
				   (adjacent_v + (number, )).count(number) == 3:
					return False

		return True

	def check_vector_difference(self):
		return not (self.board == self.board[0]).all() and \
		       not (self.board.T == self.board.T[0]).all()

	def check_finished_board(self):
		return self.check_numbers() and \
		       self.check_adjacency() and \
		       self.check_vector_difference() and \
		       2 not in self.board

	def __str__(self):
		string = ""

		for i in range(self.dimension):
			for j in range(self.dimension):
				string += str(self.get_number(i, j))
				if j != self.dimension - 1:
					string += "\t"

			if i != self.dimension - 1:
				string += "\n"

		return string

	# TODO: outros metodos da classe


class Takuzu(Problem):

	def __init__(self, board: Board):
		"""O construtor especifica o estado inicial."""
		super().__init__(TakuzuState(board))
		self.state = TakuzuState(board)

	def actions(self, state: TakuzuState):
		"""Retorna uma lista de ações que podem ser executadas a
        partir do estado passado como argumento."""
		actions = ()

		for (row, col) in state.get_board().get_free_positions():
			for number in (0, 1):
				actions += ((row, col, number), )

		return actions

	def result(self, state: TakuzuState, action):
		"""Retorna o estado resultante de executar a 'action' sobre
        'state' passado como argumento. A ação a executar deve ser uma
        das presentes na lista obtida pela execução de
        self.actions(state)."""
		(row, col, number) = action
		board = state.get_board()
		board.place_number(row, col, number)

		return TakuzuState(board)

	def goal_test(self, state: TakuzuState):
		"""Retorna True se e só se o estado passado como argumento é
        um estado objetivo. Deve verificar se todas as posições do tabuleiro
        estão preenchidas com uma sequência de números adjacentes."""
		return state.get_board().check_finished_board()

	def h(self, node: Node):
		"""Função heuristica utilizada para a procura A*."""
		# TODO
		pass

	# TODO: outros metodos da classe


if __name__ == "__main__":
	board = Board.parse_instance_from_stdin()

	#node = breadth_first_tree_search(Takuzu(board))
	node = depth_first_tree_search(Takuzu(board.copy()))
	#node = greedy_search(Takuzu(board))
	#node = astar_search(Takuzu(board))

	solution = node.solution()

	for (row, col, number) in solution:
		board.place_number(row, col, number)

	print(board)

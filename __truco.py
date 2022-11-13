import numpy as np
from truco import Algoritmo, Game
from abc import ABC, abstractmethod

class AlogritmoMonteCarloTreeSearch(Algoritmo):

    #apenas para o autocomplete
    game: Game
    
    def getJogada(self, jogadaAdversario=None):
        state = TrucoState(self.game)
        node = Node(state)
        mcts = MonteCarloTreeSearch(node)
        return mcts.best_action(1000)


class MonteCarloTreeSearch:
    def __init__(self, node):
        self.root = node

    def best_action(self, simulations_number=None):
        for _ in range(0, simulations_number):            
            v = self._tree_policy()
            reward = v.rollout()
            v.backpropagate(reward)

        return self.root.best_child(c_param=0.)

    def _tree_policy(self): # selects node to run rollout/playout for
        current_node = self.root
        while not current_node.is_terminal_node():
            if not current_node.is_fully_expanded():
                return current_node.expand()
            else:
                current_node = current_node.best_child()
        return current_node



class TwoPlayersAbstractGameState(ABC):

    @abstractmethod
    def game_result(self):
        """
        this property should return:

         1 if player #1 wins
        -1 if player #2 wins
         0 if there is a draw
         None if result is unknown
        """
        pass

    @abstractmethod
    def is_game_over(self):
        """
        boolean indicating if the game is over,
        simplest implementation may just be
        `return self.game_result() is not None`
        """
        pass

    @abstractmethod
    def move(self, action):
        """
        consumes action and returns resulting TwoPlayersAbstractGameState
        """
        pass

    @abstractmethod
    def get_legal_actions(self):
        """
        returns list of legal action at current game state
        Returns
        """
        pass

class TrucoState(TwoPlayersAbstractGameState):
    def __init__(self, state, next_to_move=1, win=None):
        if len(state.shape) != 2 or state.shape[0] != state.shape[1]:
            raise ValueError("Only 2D square boards allowed")
        self.board = state
        self.board_size = state.shape[0]
        if win is None:
            win = self.board_size
        self.win = win
        self.next_to_move = next_to_move

    @property
    def game_result(self):
        # check if game is over
        for i in range(self.board_size - self.win + 1):
            rowsum = np.sum(self.board[i:i+self.win], 0)
            colsum = np.sum(self.board[:,i:i+self.win], 1)
            if rowsum.max() == self.win or colsum.max() == self.win:
                return self.x
            if rowsum.min() == -self.win or colsum.min() == -self.win:
                return self.o
        for i in range(self.board_size - self.win + 1):
            for j in range(self.board_size - self.win + 1):
                sub = self.board[i:i+self.win,j:j+self.win]
                diag_sum_tl = sub.trace()
                diag_sum_tr = sub[::-1].trace()        
                if diag_sum_tl == self.win or diag_sum_tr == self.win:
                    return self.x
                if diag_sum_tl == -self.win or diag_sum_tr == -self.win:
                    return self.o

        # draw
        if np.all(self.board != 0):
            return 0.

        # if not over - no result
        return None

    def is_game_over(self):
        return self.game_result is not None

    def is_move_legal(self, move):
        # check if correct player moves
        if move.value != self.next_to_move:
            return False

        # check if inside the board on x-axis
        x_in_range = (0 <= move.x_coordinate < self.board_size)
        if not x_in_range:
            return False

        # check if inside the board on y-axis
        y_in_range = (0 <= move.y_coordinate < self.board_size)
        if not y_in_range:
            return False

        # finally check if board field not occupied ye
        return self.board[move.x_coordinate, move.y_coordinate] == 0

    def move(self, move):
        if not self.is_move_legal(move):
            raise ValueError(
                "move {0} on board {1} is not legal". format(move, self.board)
            )
        new_board = np.copy(self.board)
        new_board[move.x_coordinate, move.y_coordinate] = move.value
        if self.next_to_move == self.x:
            next_to_move = self.o
        else:
            next_to_move = self.x
        return type(self)(new_board, next_to_move, self.win)

    def get_legal_actions(self):
        indices = np.where(self.board == 0)
        aux = [
            TicTacToeMove(coords[0], coords[1], self.next_to_move)
            for coords in list(zip(indices[0], indices[1]))
        ]
        print(aux)
        return aux

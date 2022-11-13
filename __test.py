import numpy as np
from __nodes import TwoPlayersGameMonteCarloTreeSearchNode
from __search import MonteCarloTreeSearch
from monte_carlo import TrucoGameState

initial_board_state = TrucoGameState(state = state, next_to_move=1)

root = TwoPlayersGameMonteCarloTreeSearchNode(state = initial_board_state)
mcts = MonteCarloTreeSearch(root)
best_node = mcts.best_action(10000)
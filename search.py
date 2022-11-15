import time
class MonteCarloTreeSearch(object):

    def __init__(self, node):
        self.root = node

    def getBestAction(self, simulations_number=None, total_simulation_seconds=None):
        if simulations_number is None :
            assert(total_simulation_seconds is not None)
            end_time = time.time() + total_simulation_seconds
            while True:
                v = self.treeExpand()
                reward = v.rollout()
                v.backpropagate(reward)
                if time.time() > end_time:
                    break
        else :
            for _ in range(0, simulations_number):            
                v = self.treeExpand()
                reward = v.rollout()
                v.backpropagate(reward)

        return self.root.best_child(c_param=0.)

    def treeExpand(self): # selects node to run rollout/playout for
        current_node = self.root
        while not current_node.is_terminal_node():
            if not current_node.is_fully_expanded():
                return current_node.expand()
            else:
                current_node = current_node.best_child()
        return current_node

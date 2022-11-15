from abc import ABC, abstractmethod

class AbstractGameState(ABC):

    @abstractmethod
    def game_result(self):
        pass

    @abstractmethod
    def isGameOver(self):
        pass

    @abstractmethod
    def doAction(self, action):
        pass

    @abstractmethod
    def getLegalActions(self):
        pass


class AbstractAction(ABC):
    pass

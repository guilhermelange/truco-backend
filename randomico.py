from truco import Algoritmo, Game
import random

class AlgoritmoRandomico(Algoritmo):

    #apenas para o autocomplete
    game: Game

    def getJogada(self, jogadaAdversario=None):
        return self.play(self.popCarta(random.choice(self.hand)))

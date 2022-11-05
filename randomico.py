from truco import Algoritmo
import random

class AlgoritmoRandomico(Algoritmo):

    def getJogada(self, cartaAdversario=None):
        return self.play(self.hand.pop(random.randint(0,  len(self.hand) - 1)))

from truco import Algoritmo, Game
import random

class AlgoritmoRandomico(Algoritmo):

    #apenas para o autocomplete
    game: Game

    def getJogada(self, jogadaAdversario=None):

        if jogadaAdversario != None and jogadaAdversario['type'] == 'TRUCO':
            if random.randint(0,1) == 1:
                return self.accept(self.popCarta(random.choice(self.hand)))
            else:
                return self.run()

        randomChoice = random.randint(0, 10)

        if randomChoice <= 1 and jogadaAdversario == None:
            return self.truco(self.popCarta(random.choice(self.hand)))
        elif randomChoice == 2:
            return self.run()
        else:
            return self.play(self.popCarta(random.choice(self.hand)))

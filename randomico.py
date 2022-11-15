from truco import Algorithm, Game
import random

class RandomAlgorithm(Algorithm):

    #apenas para o autocomplete
    game: Game

    def getJogada(self, jogadaAdversario=None):

        if len(self.game.jogadas) and self.game.jogadas[-1]['type'] == 'TRUCO':
            if random.randint(0,1) == 1:
                return self.accept()
            else:
                return self.run()

        randomChoice = random.randint(0, 20)

        if randomChoice <= 2 and jogadaAdversario == None and self.isTrucoPermited():
            return self.truco()
        elif randomChoice == 2:
            return self.run()
        else:
            return self.play(self.popCarta(random.choice(self.hand)))

from truco import Algoritmo, Game


class AlgoritmoBaseline(Algoritmo):

    #apenas para o autocomplete
    game: Game

    def getJogada(self, jogadaAdversario=None):

        #Se o adversario pediu truco
        #verificar se tem carta "forte" (indice alto de força (>=1 <=3) ou manilha)
        #caso sim, aceita,
        #caso não corre 
        cartas = self.handOrderedByPower()
        if jogadaAdversario != None and jogadaAdversario['type'] == 'TRUCO':
            if int(cartas[0].split('_')[0]) >= 1 or self.hasManilha():
                return self.accept()
            else:
                return self.run()

        #se ja fez a primeira tenta empaxar a segunda ou a terceira se possivel

        #Nunca sair com a carta mais forte
        # talvez: se tiver 3 ou mais, lançar na saída;
        if jogadaAdversario == None and self.game.turn == 0:
            carta = int(cartas[0].split('_')[0])
            if (carta == 3 or self.isManilha(cartas[0])):
                return self.play(self.popCarta(cartas[0]))
            elif not self.isManilha(cartas[len(cartas) - 1]):
                    return self.play(self.popCarta(cartas.pop()))
        
        #Priorizar "Matar" carta do adversário com cartas que não são manilha antes de usar a manilha
        if jogadaAdversario != None and jogadaAdversario['type'] == 'PLAY':
            for carta in cartas:
                #if not self.isManilha(carta) and self.game.cardWins(carta, jogadaAdversario['card']):
                if self.game.cardWins(carta, jogadaAdversario['card']):
                    return self.play(self.popCarta(carta))

 
        #Se tem carta boa (>=1 <=3 ou manilha) e estiver na seguinda ou terceira rodada pede truco
        if jogadaAdversario == None and self.game.turn >= 1:
            if int(cartas[0].split('_')[0]) >= 1 and self.hasManilha() and self.isTrucoPermited():
                return self.truco()

        return self.play(cartas.pop())


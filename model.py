import random
from abc import abstractmethod

class Deck:
    def __init__(self):
        self.cartas = []
        self.criaCartas()
        self.shuffle()
        self.manilha = None
        

    def criaCartas(self):
        validNumbers = [1,2,3,4,5,6,7,10,11,12];
        validNaipes = ['MOLES', 'ESPADAS', 'COPAS', 'PAUS']

        for number in validNumbers:
            for naipe in validNaipes:
                self.cartas.append(str(number) + '_' + naipe)

    def shuffle(self):
        random.shuffle(self.cartas)

    def getMao(self):
        return [self.cartas.pop(), self.cartas.pop(), self.cartas.pop()]

    def getManilha(self):
        if self.manilha == None:
            self.manilha = self.cartas.pop()
        return self.manilha


class Algoritmo:
    def __init__(self, id):
        self.id = id

    @abstractmethod
    def getJogada(self, cartaAdversario = None):
        #return(carta, truco)
        pass

    def setHand(self, hand):
        self.hand = hand

    def setHandAdversario(self, hand):
        self.handAdversario = hand
    
    def setManilha(self, manilha):
        self.manilha = manilha

class Partida:
    def __init__(self, algoritmoA : Algoritmo, algoritmoB: Algoritmo):
        self.algoritmoA = algoritmoA
        self.algoritmoB = algoritmoB
        self.deck = Deck()

        handA = self.deck.getMao()
        handB = self.deck.getMao()
        manilha = self.deck.getManilha()

        self.algoritmoA.setHand(handA)
        self.algoritmoA.setHandAdversario(handB)
        self.algoritmoA.setManilha(manilha)

        self.algoritmoB.setHand(handB)
        self.algoritmoB.setHandAdversario(handA)
        self.algoritmoB.setManilha(manilha)


    def play(self):
        turn = random.randint(0,1)
        jogadas = []
        for i in range(3):
            if turn == 1:
                jogadaA = self.algoritmoA.getJogada()
                jogadaB = self.algoritmoB.getJogada(jogadaA['carta'])
                jogadas.append({"id_jogador" : self.algoritmoA.id, "carta" : jogadaA['carta'], "truco" : jogadaA['truco']})
                jogadas.append({"id_jogador" : self.algoritmoB.id, "carta" : jogadaB['carta'], "truco" : jogadaB['truco']})
                turn = 0
            else:
                jogadaB = self.algoritmoB.getJogada()
                jogadaA = self.algoritmoA.getJogada(jogadaB['carta'])
                jogadas.append({"id_jogador" : self.algoritmoB.id, "carta" : jogadaB['carta'], "truco" : jogadaB['truco']})
                jogadas.append({"id_jogador" : self.algoritmoA.id, "carta" : jogadaA['carta'], "truco" : jogadaA['truco']})
                turn = 1

        return jogadas


class AlgoritmoRandomico(Algoritmo):

    def getJogada(self, cartaAdversario=None):
        print(self.hand)
        return {'carta': self.hand.pop(random.randint(0,  len(self.hand) - 1)), 'truco': False}








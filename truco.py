import random
import uuid
from abc import abstractmethod
import json

realizedMatches = []


class Deck:

    def __init__(self):
        self.cartas = []
        self.criaCartas()
        self.shuffle()
        self.manilha = None

    def criaCartas(self):
        validNumbers = [1, 2, 3, 4, 5, 6, 7, 10, 11, 12]
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

    hand: list

    def __init__(self, id):
        self.id = id

    @abstractmethod
    def getJogada(self, jogadaAdversario=None):
        # return(carta, truco)
        pass

    # joga uma carta
    def play(self, carta):
        return {"type": "PLAY", "card": carta, "player": self.id}

    # pede truco (jogando a carta)
    def truco(self):
        self.game.last_player_truco = self.id
        return {"type": "TRUCO", "player": self.id}

    # aceita o truco (jogando a carta)
    def accept(self):
        return {"type": "ACCEPT","player": self.id}

    # corre
    def run(self):
        return {"type": "RUN", "player": self.id}

    def popCarta(self, carta):
        return self.hand.pop(self.hand.index(carta))

    def setHand(self, hand):
        self.hand = hand

    def setHandAdversario(self, hand):
        self.handAdversario = hand

    def setManilha(self, manilha):
        self.manilha = manilha

    def setGame(self, game):
        self.game = game

    def isTrucoPermited(self):
        return self.game.last_player_truco != self.id


# Classe que representa uma "Rodada" da partida, constituida por 3 jogadas de cada player


class Game:

    def __init__(self, algoritmoA: Algoritmo, algoritmoB: Algoritmo):
        self.algoritmoA = algoritmoA
        self.algoritmoB = algoritmoB
        self.deck = Deck()

        self.handA = self.deck.getMao()
        self.handB = self.deck.getMao()
        self.manilha = self.deck.getManilha()

        self.algoritmoA.setHand(self.handA)
        self.algoritmoA.setHandAdversario(self.handB)
        self.algoritmoA.setManilha(self.manilha)

        self.algoritmoB.setHand(self.handB)
        self.algoritmoB.setHandAdversario(self.handA)
        self.algoritmoB.setManilha(self.manilha)

        self.algoritmoA.setGame(self)
        self.algoritmoB.setGame(self)

        self.last_player_truco = 0

    # Joga um game, constituido de 3 rodadas
    def play(self):
        turn = random.randint(0, 1)
        jogadas = []
        run = False
        win_counts = []
        
        #TODO Necessário tratar empachada
        # realiza as rodadas
        for i in range(3):
            if not run:
                if turn == 1:
                    algoritmos = [self.algoritmoA, self.algoritmoB]
                else:
                    algoritmos = [self.algoritmoB, self.algoritmoA]

                playersRunOrPlay = [False, False]
                while (any(playersRunOrPlay) == False):
                    jogadaA = algoritmos[0].getJogada()
                    jogadas.append(jogadaA)
                    playersRunOrPlay[0] = playersRunOrPlay[0] or (jogadaA['type'] == 'RUN' or jogadaA['type'] == 'PLAY')
                    if jogadaA['type'] == 'RUN':
                        run = True
                        break
                    
                    jogadaB = algoritmos[1].getJogada(jogadaA)
                    jogadas.append(jogadaB)
                    playersRunOrPlay[1] = playersRunOrPlay[1] or (jogadaB['type'] == 'RUN' or jogadaB['type'] == 'PLAY')
                    
                    if jogadaB['type'] == 'RUN':
                        run = True
                        break

                # No proximo turno, quem joga é quem ganhou o último
                if not(run):
                    if self.cardWins(jogadaA['card'], jogadaB['card']):
                        win_counts.append(jogadaA['player'])
                    else:
                        win_counts.append(jogadaB['player'])
                        if turn == 1:
                            turn = 0
                        else:
                            turn = 1
                else:
                    if jogadaA['type'] == 'RUN':
                        win_counts.append(jogadaA['player'])
                    elif jogadaB['type'] == 'RUN':
                        win_counts.append(jogadaA['player'])

                if(win_counts.count(self.algoritmoA.id) == 2 or win_counts.count(self.algoritmoB.id) == 2):
                    break

                run = jogadaA['type'] == 'RUN' or jogadaB['type'] == 'RUN'

        # conta rodadas ganhas


        accept_count = 0
        for jogada in jogadas:
            if jogada['type'] == 'ACCEPT':
                accept_count += 1

        win_points = 1
        if accept_count == 1:
            win_points = 3

        if accept_count > 1:
            win_points = (accept_count * 3)

        # Correu
        if any(jogada['type'] == 'RUN' for jogada in jogadas):
            jog = next(jogada for jogada in jogadas if jogada['type'] == 'RUN')
            if jog['player'] == self.algoritmoA.id:
                jogadas.append({
                    'type': 'WIN',
                    'player': self.algoritmoB.id,
                    'points': win_points
                })
                self.winner = self.algoritmoB.id
            else:
                jogadas.append({
                    'type': 'WIN',
                    'player': self.algoritmoA.id,
                    'points': win_points
                })
                self.winner = self.algoritmoA.id

        # Conta jogo ganho normal (quem ganhou mais rodadas)
        elif win_counts.count(self.algoritmoA.id) > win_counts.count(self.algoritmoB.id):
            jogadas.append({
                'type': 'WIN',
                'player': self.algoritmoA.id,
                'points': win_points
            })
            self.winner = self.algoritmoA.id
        else:
            jogadas.append({
                'type': 'WIN',
                'player': self.algoritmoB.id,
                'points': win_points
            })
            self.winner = self.algoritmoB.id

        self.totalPoints = win_points

        return jogadas

    # Verica se a carta A ganha da carta B
    def cardWins(self, cartaA, cartaB):
        powerOrderNumbers = [
            '4', '5', '6', '7', '10', '11', '12', '1', '2', '3'
        ]
        powerOrderNaipe = ['MOLES', 'ESPADAS', 'COPAS', 'PAUS']
        numeroA = cartaA.split('_')[0]
        naipeA = cartaA.split('_')[1]
        numeroB = cartaB.split('_')[0]
        naipeB = cartaB.split('_')[1]

        if numeroA == self.deck.getManilha().split('_')[0]:
            if numeroB == self.deck.getManilha().split('_')[0]:
                return powerOrderNaipe.index(naipeA) > powerOrderNaipe.index(
                    naipeB)
            else:
                return True

        return powerOrderNumbers.index(numeroA) > powerOrderNumbers.index(
            numeroB)

    # verifica se as cartas "Empaxam"
    def cardEquals(self, cartaA, cartaB):
        numeroA = cartaA.split('_')[0]
        numeroB = cartaB.split('_')[0]
        numeroManilha = self.deck.getManilha().split('_')[0]
        return numeroA == numeroB and numeroA != numeroManilha and numeroB != numeroManilha


class Match:

    def __init__(self, algoritmoA: Algoritmo, algoritmoB: Algoritmo):
        self.algoritmoA = algoritmoA
        self.algoritmoB = algoritmoB

    # Joga uma partida, realizando games até que alguem atinja a pontuação final de 12 pontos
    def playMatch(self):
        totalPoints = 0
        pointsA = 0
        pointsB = 0
        matches = []

        #while (pointsA < 12 and pointsB < 12):
        # DESCOMENTAR DEPOIS
        game = Game(self.algoritmoA, self.algoritmoB)
        handA = game.handA.copy()
        handB = game.handB.copy()
        jogadas = game.play()
        totalPoints = totalPoints + game.totalPoints
        mtch = {
            'joker': game.manilha,
            'winner': game.winner,
            'match_id': str(uuid.uuid4())[0:8],
            'points': game.totalPoints,
            'player_1': handA,
            'player_2': handB,
            'plays': jogadas
        }

        if game.winner == self.algoritmoA.id:
            pointsA = pointsA + game.totalPoints
        else:
            pointsB = pointsB + game.totalPoints

        matches.append(mtch)

        if pointsA >= 12:
            winner = self.algoritmoA.id
        else:
            winner = self.algoritmoB.id

        mt = {
            'winner': winner,
            "points": [pointsA, pointsB],
            "matches": matches
        }

        realizedMatches.append(mt)
        return mt

import random
import uuid
from abc import abstractmethod

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
    def truco(self, carta):
        self.game.last_player_truco = self.id
        return {"type": "TRUCO", "card": carta, "player": self.id}

    # aceita o truco (jogando a carta)
    def accept(self, carta):
        return {"type": "ACCEPT", "card": carta, "player": self.id}

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

        #TODO Necessário tratar empachada
        # realiza as rodadas
        for i in range(3):
            if not run:
                if turn == 1:
                    jogadaA = self.algoritmoA.getJogada()
                    jogadas.append(jogadaA)
                    if jogadaA['type'] == 'RUN':
                        run = True
                        break
                    jogadaB = self.algoritmoB.getJogada(jogadaA)
                    jogadas.append(jogadaB)
                    turn = 0

                else:
                    jogadaB = self.algoritmoB.getJogada()
                    jogadas.append(jogadaB)
                    if jogadaB['type'] == 'RUN':
                        run = True
                        break
                    jogadaA = self.algoritmoA.getJogada(jogadaB)
                    jogadas.append(jogadaA)
                    turn = 1

                # No proximo turno, quem joga é quem ganhou o último
                if 'card' in jogadaA and 'card' in jogadaB and not self.cardEquals(
                        jogadaA['card'], jogadaB['card']):
                    if self.cardWins(jogadaA['card'], jogadaB['card']):
                        turn = 1
                    else:
                        turn = 0

                run = jogadaA['type'] == 'RUN' or jogadaB['type'] == 'RUN'

        # conta rodadas ganhas
        counts = []
        for jogada in jogadas:
            index = jogadas.index(jogada)
            if index % 2 == 0 and index < len(jogadas) - 1:
                jogadaA = jogada
                jogadaB = jogadas[index + 1]

                if jogadaB['type'] == 'RUN':
                    counts.append(jogadaA['player'])
                elif jogadaA['type'] == 'RUN':
                    counts.append(jogadaB['player'])
                else:
                    if 'card' in jogadaA and 'card' in jogadaB:
                        if self.cardWins(jogadaA['card'], jogadaB['card']):
                            counts.append(jogadaA['player'])
                        else:
                            counts.append(jogadaB['player'])

        # Ganhou com truco
        #TODO Ajustar para poder pedir truco de 6 ou mais
        if any(jogada['type'] == 'TRUCO'
               for jogada in jogadas) and any(jogada['type'] == 'ACCEPT'
                                              for jogada in jogadas):
            if counts.count(self.algoritmoA.id) > counts.count(
                    self.algoritmoB.id):
                jogadas.append({
                    'type': 'WIN',
                    'player': self.algoritmoA.id,
                    'points': 3
                })
                self.winner = self.algoritmoA.id
            else:
                jogadas.append({
                    'type': 'WIN',
                    'player': self.algoritmoB.id,
                    'points': 3
                })
                self.winner = self.algoritmoB.id

        # Correu
        elif any(jogada['type'] == 'RUN' for jogada in jogadas):
            jog = next(jogada for jogada in jogadas if jogada['type'] == 'RUN')
            if jog['player'] == self.algoritmoA.id:
                jogadas.append({
                    'type': 'WIN',
                    'player': self.algoritmoB.id,
                    'points': 1
                })
                self.winner = self.algoritmoB.id
            else:
                jogadas.append({
                    'type': 'WIN',
                    'player': self.algoritmoA.id,
                    'points': 1
                })
                self.winner = self.algoritmoA.id

        # Conta jogo ganho normal (quem ganhou mais rodadas)
        elif counts.count(self.algoritmoA.id) > counts.count(
                self.algoritmoB.id):
            jogadas.append({
                'type': 'WIN',
                'player': self.algoritmoA.id,
                'points': 1
            })
            self.winner = self.algoritmoA.id
        else:
            jogadas.append({
                'type': 'WIN',
                'player': self.algoritmoB.id,
                'points': 1
            })
            self.winner = self.algoritmoB.id

        self.totalPoints = jogadas[len(jogadas) - 1]['points']

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

        while (pointsA < 12 and pointsB < 12):
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

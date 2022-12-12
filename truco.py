import random
import uuid
from abc import abstractmethod
import copy

realizedMatches = []


class Deck:

    def __init__(self):
        self.cartas = []
        self.criaCartas()
        self.shuffle()
        self.manilha = None
        self.num_manilha = None

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

    def getNumeroManilha(self):
        if self.num_manilha == None:
            man = int(self.getManilha().split('_')[0])
            if man == 12:
                man = 1
            elif man == 7:
                man = 10
            else:
                man += 1
            self.num_manilha = man
        return self.num_manilha


class Algorithm:

    def __init__(self, id):
        self.hand = []
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
        return {"type": "ACCEPT", "player": self.id}

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

    def handOrderedByPower(self):
        powerOrderNumbers = [
            '4', '5', '6', '7', '10', '11', '12', '1', '2', '3'
        ]
        powerOrderNumbers.remove(str(self.game.num_manilha))
        powerOrderNumbers.append(str(self.game.num_manilha))

        ordered = sorted(
            self.hand.copy(),
            key=lambda a: powerOrderNumbers.index(a.split('_')[0]))

        ordered.reverse()
        return ordered

    def hasManilha(self):
        for carta in self.hand:
            if int(carta.split('_')[0]) == self.game.num_manilha:
                return True
        return False

    def popManilha(self):
        for carta in self.hand:
            if int(carta.split('_')[0]) == self.game.num_manilha:
                return self.hand.pop(self.hand.index(carta))
        return False

    def isManilha(self, carta):
        return int(carta.split('_')[0]) == self.game.num_manilha


# Classe que representa uma "Rodada" da partida, constituida por 3 jogadas de cada player


class Game:

    def __init__(self, algoritmoA: Algorithm, algoritmoB: Algorithm, default_deck):
        self.algoritmoA = algoritmoA
        self.algoritmoB = algoritmoB
        if default_deck == None:
            self.deck = Deck()
        else:
            self.deck = default_deck

        self.handA = self.deck.getMao()
        self.handB = self.deck.getMao()
        self.manilha = self.deck.getManilha()
        self.num_manilha = self.deck.getNumeroManilha()

        self.algoritmoA.setHand(self.handA)
        self.algoritmoA.setHandAdversario(self.handB)
        self.algoritmoA.setManilha(self.manilha)

        self.algoritmoB.setHand(self.handB)
        self.algoritmoB.setHandAdversario(self.handA)
        self.algoritmoB.setManilha(self.manilha)

        self.algoritmoA.setGame(self)
        self.algoritmoB.setGame(self)

        self.winner = -1
        self.last_player_truco = 0
        self.current_player = -1
        self.jogadas = []

    # Joga um game, constituido de 3 rodadas1
    def play(self, turn):
        run = False
        self.win_counts = []
        empate = [False, False, False]
        jogadaB = {}
        jogadaA = {}
        jogadasCard = []
        self.jogadas = []
        self.turn = 0

        # realiza as rodadas
        temp = str(uuid.uuid4())[0:8]
        for i in range(3):
            self.turn = i
            if not run:
                if turn == 1:
                    algoritmos = [self.algoritmoA, self.algoritmoB]
                else:
                    algoritmos = [self.algoritmoB, self.algoritmoA]

                playersRunOrPlay = [False, False]
                jogadasCard = [None, None]
                #while (any(playersRunOrPlay) == False):
                while (playersRunOrPlay[0] == False
                       or playersRunOrPlay[1] == False):
                    self.current_player = algoritmos[0].id

                    jogadaA = algoritmos[0].getJogada()
                    self.jogadas.append(jogadaA)

                    playersRunOrPlay[0] = playersRunOrPlay[0] or (
                        jogadaA['type'] == 'RUN' or jogadaA['type'] == 'PLAY')
                    if jogadaA['type'] == 'RUN':
                        jogadaB = {'player': algoritmos[1].id}
                        run = True
                        break
                    elif jogadaA['type'] == 'PLAY':
                        jogadasCard[jogadaA['player']] = jogadaA

                    self.current_player = algoritmos[1].id
                    jogadaB = algoritmos[1].getJogada(jogadaA)
                    self.jogadas.append(jogadaB)
                    playersRunOrPlay[1] = playersRunOrPlay[1] or (
                        jogadaB['type'] == 'RUN' or jogadaB['type'] == 'PLAY')

                    if jogadaB['type'] == 'RUN':
                        run = True
                        break
                    elif jogadaB['type'] == 'PLAY':
                        jogadasCard[jogadaB['player']] = jogadaB

                # No proximo turno, quem joga é quem ganhou o último
                if not (run):
                    # Verifica empaxe e lança evento; (TEMOS CARTAS AQUI)
                    empate[i] = self.cardEquals(
                        jogadasCard[jogadaA['player']]['card'],
                        jogadasCard[jogadaB['player']]['card'])
                    if empate[i]:
                        self.jogadas.append({'type': 'TIE'})
                        pass
                    elif self.cardWins(jogadasCard[jogadaA['player']]['card'],
                                       jogadasCard[jogadaB['player']]['card']):
                        self.win_counts.append(jogadaA['player'])
                    else:
                        self.win_counts.append(jogadaB['player'])
                        if turn == 1:
                            turn = 0
                        else:
                            turn = 1
                else:
                    if jogadaA['type'] == 'RUN':
                        self.win_counts.append(jogadaB['player'])
                        self.winner = jogadaB['player']
                        break
                    elif jogadaB['type'] == 'RUN':
                        self.win_counts.append(jogadaA['player'])
                        self.winner = jogadaA['player']
                        break

                if self.win_counts.count(self.algoritmoA.id) == 2:
                    self.winner = self.algoritmoA.id
                    break

                if self.win_counts.count(self.algoritmoB.id) == 2:
                    self.winner = self.algoritmoB.id
                    break

                # Verifica empate
                if empate == [True, False, False]:
                    if i == 1:
                        self.winner = self.win_counts[-1]
                        break

                elif empate == [False, True, False]:
                    if i == 1:
                        self.winner = self.win_counts[0]
                        break

                elif empate == [True, True, False]:
                    if i == 2:
                        self.winner = self.win_counts[-1]
                        break

                elif empate == [False, False, True]:
                    if i == 2:
                        self.winner = self.win_counts[0]
                        break

                elif empate == [True, True, True]:
                    pass

                # Desnecessário calcular aqui, e pode estar errado e rodar mais uma vez, causando erro
                #run = jogadaA['type'] == 'RUN' or jogadaB['type'] == 'RUN'

        # conta rodadas ganhas

        accept_count = 0
        for jogada in self.jogadas:
            if jogada['type'] == 'ACCEPT':
                accept_count += 1

        if self.winner == -1:
            win_points = 0
            self.jogadas.append({'type': 'TIED_MATCH', 'points': win_points})
        else:
            win_points = 1
            if accept_count == 1:
                win_points = 3

            if accept_count > 1:
                win_points = (accept_count * 3)

            self.jogadas.append({
                'type': 'WIN',
                'player': self.winner,
                'points': win_points
            })

        self.totalPoints = win_points

        return self.jogadas, turn

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

        numeroManilha = self.deck.getNumeroManilha()
        if int(numeroA) == numeroManilha:
            if int(numeroB) == numeroManilha:
                return powerOrderNaipe.index(naipeA) > powerOrderNaipe.index(
                    naipeB)
            else:
                return True
        elif int(numeroB) == numeroManilha:
            return False

        return powerOrderNumbers.index(numeroA) > powerOrderNumbers.index(
            numeroB)

    # verifica se as cartas "Empaxam"
    def cardEquals(self, cartaA, cartaB):
        numeroA = cartaA.split('_')[0]
        numeroB = cartaB.split('_')[0]
        numeroManilha = self.deck.getNumeroManilha()
        return numeroA == numeroB and int(numeroA) != numeroManilha and int(
            numeroB) != numeroManilha


class Match:

    def __init__(self, algoritmoA: Algorithm, algoritmoB: Algorithm, deck_cache: any):
        self.algoritmoA = algoritmoA
        self.algoritmoB = algoritmoB
        self.deck_cache = deck_cache

    # Joga uma partida, realizando games até que alguem atinja a pontuação final de 12 pontos
    def playMatch(self):
        totalPoints = 0
        pointsA = 0
        pointsB = 0
        matches = []
        currentTurn = random.randint(0, 1)

        #while (pointsA < 12 and pointsB < 12):
            # DESCOMENTAR DEPOIS
        if len(self.deck_cache) > 0:
            game = Game(self.algoritmoA, self.algoritmoB, copy.deepcopy(self.deck_cache[len(matches)]))
        else:
            game = Game(self.algoritmoA, self.algoritmoB, None)

        handA = game.handA.copy()
        handB = game.handB.copy()
        jogadas, currentTurn = game.play(currentTurn)
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

        winner = -1

        if pointsA >= 12:
            winner = self.algoritmoA.id

        if pointsB >= 12:
            winner = self.algoritmoB.id

        if winner == -1:
            if pointsA >= pointsB:
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

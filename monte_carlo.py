import numpy as np
import copy
from truco import Algoritmo, Game
from __common import TwoPlayersAbstractGameState
from __common import AbstractGameAction
from __nodes import TwoPlayersGameMonteCarloTreeSearchNode
from __search import MonteCarloTreeSearch
import session

def otherPlayer(playerIndex):
    if playerIndex == 0:
        return 1
    else:
        return 0

class AlogritmoMonteCarloTreeSearch(Algoritmo):

    #apenas para o autocomplete
    game: Game

    def getJogada(self, jogadaAdversario=None):
        cartas = [{},{}]
        cartas[self.id] = self.hand
        cartas[otherPlayer(self.id)] = self.handAdversario

        # print(cartas)
        rodadaJogadas = [jogada for jogada in self.game.jogadas if jogada['type'] != 'TIE']
        state = {
            'jogadas': rodadaJogadas,
            'cartas': cartas,
            'manilha': self.game.num_manilha
        }
        
        game_state = TrucoGameState(state, next_to_move=self.id)

        root = TwoPlayersGameMonteCarloTreeSearchNode(state=game_state)
        mcts = MonteCarloTreeSearch(root)
        best_node = mcts.best_action(simulations_number=1000)

        resultado = best_node.state.dados['jogadas'][-1]

        if resultado['type'] =='PLAY':
           self.popCarta(resultado['card'])

        return resultado

class TrucoGameState(TwoPlayersAbstractGameState):

    def __init__(self, state, next_to_move=1, win=None):
        self.dados = state
        self.next_to_move = next_to_move

    def cardEquals(self, cartaA, cartaB):
        numeroA = cartaA.split('_')[0]
        numeroB = cartaB.split('_')[0]
        numeroManilha = self.dados['manilha']
        return numeroA == numeroB and int(numeroA) != numeroManilha and int(
            numeroB) != numeroManilha

    def cardWins(self, cartaA, cartaB):
        powerOrderNumbers = [
            '4', '5', '6', '7', '10', '11', '12', '1', '2', '3'
        ]
        powerOrderNaipe = ['MOLES', 'ESPADAS', 'COPAS', 'PAUS']
        numeroA = cartaA.split('_')[0]
        naipeA = cartaA.split('_')[1]
        numeroB = cartaB.split('_')[0]
        naipeB = cartaB.split('_')[1]

        numeroManilha = self.dados['manilha']
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

    @property
    def game_result(self):
        # check if game is over
        # 1 = player1
        # 0 = empate
        # -1 = player2
        # None = não definido
        partidaEmpate = False
        empate = False
        self.winner = None
        jogadas = self.dados['jogadas']
        jogadas_empate = [False, False, False]
        acceptedCount = 0

        user_jogadas = [0, 0]
        win_count = [0, 0]
        win_counts = []
        self.plays_count = 0
        player = None
        varOtherPlayer = None
        rodada = 0

        for jogada in jogadas:
            if jogada['type'] != 'TIE':
                player = jogada['player']
                varOtherPlayer = otherPlayer(player)

                if jogada['type'] == 'PLAY':
                    self.plays_count += 1
                    empate = False
                    user_jogadas[jogada['player']] = jogada
                elif jogada['type'] == 'RUN':
                    empate = False
                    self.winner = varOtherPlayer
                    break
                elif jogada['type'] == 'TRUCO':
                    empate = False
                elif jogada['type'] == 'ACCEPT':
                    acceptedCount += 1
                    empate = False
                elif jogada['type'] == 'TIE':
                    empate = True
                elif jogada['type'] == 'TIED_MATCH':
                    empate = True
                elif jogada['type'] == 'WIN':
                    empate = False

                if self.plays_count == 2:
                    self.plays_count = 0
                    
                    # if user_jogadas[0] == 0 or user_jogadas[1] == 0:
                    #     pass

                    # GLL REVER
                    # try:
                    #isEqual = self.cardEquals(user_jogadas[player]['card'], user_jogadas[varOtherPlayer]['card'])
                    # except: 
                    #     isEqual = False
                    #     print('jogadas abaixo: ')
                    #     print(self.dados['jogadas'])

                    if self.cardEquals(user_jogadas[player]['card'], user_jogadas[varOtherPlayer]['card']):
                        jogadas_empate[rodada] = True
                    elif self.cardWins(user_jogadas[player]['card'], user_jogadas[varOtherPlayer]['card']):
                        win_count[player] += 1
                        win_counts.append(user_jogadas[player])
                    else:
                        win_count[varOtherPlayer] += 1
                        win_counts.append(user_jogadas[varOtherPlayer])

                    user_jogadas = [0, 0]
                    rodada += 1


        if player != None and win_count[player] >= 2:
            self.winner = player
        elif varOtherPlayer != None and win_count[varOtherPlayer] >= 2:
            self.winner = varOtherPlayer

        if self.winner == None:
            # Verifica empate
            if jogadas_empate == [True, False, False]:
                if rodada == 1 and len(win_counts) > 0:
                    self.winner = win_counts[-1]

            elif jogadas_empate == [False, True, False]:
                if rodada == 1  and len(win_counts) > 0:
                    self.winner = win_counts[0]

            elif jogadas_empate == [True, True, False]:
                if rodada == 2  and len(win_counts) > 0:
                    self.winner = win_counts[-1]

            elif jogadas_empate == [False, False, True]:
                if rodada == 2  and len(win_counts) > 0:
                    self.winner = win_counts[0]

            elif jogadas_empate == [True, True, True]:
                partidaEmpate = True

        if partidaEmpate:
            return None

        if empate:
            return None

        if self.winner == None:
            return None

        currentMatchPoints = 0
        if acceptedCount == 0:
            currentMatchPoints = 1
        elif acceptedCount == 1:
            currentMatchPoints = 3
        elif acceptedCount > 1:
            currentMatchPoints = currentMatchPoints * 3

        session.update_match_points(currentMatchPoints)

        return 1 if self.winner == 0 else -1

    def is_game_over(self):
        return self.game_result is not None

    def move(self, move):
        newState = copy.deepcopy(self.dados)
        newState['jogadas'].append(move.jogada)

        if 'card' in move.jogada:
            indexCarta = newState['cartas'][self.next_to_move].index(move.jogada['card'])
            newState['cartas'][self.next_to_move].pop(indexCarta)
        
        return type(self)(newState, otherPlayer(self.next_to_move))

    def get_legal_actions(self):
        jogadas = self.dados['jogadas']
        moves = []

        if len(jogadas) > 0 and jogadas[-1]['type'] == 'TRUCO':
            moves.append(TrucoMove({"type": "ACCEPT", "player": self.next_to_move}))
            moves.append(TrucoMove({"type": "RUN", "player": self.next_to_move}))
        else:
            for carta in self.dados['cartas'][self.next_to_move]:
                moves.append(TrucoMove({"type": "PLAY", "card": carta, "player": self.next_to_move}))

            if len(jogadas) > 0 and jogadas[-1]['player'] != self.next_to_move: #and turnoPar: GLL AQUI
                moves.append(TrucoMove({"type": "TRUCO", "player": self.next_to_move}))

        return moves


class TrucoMove(AbstractGameAction):
    def __init__(self, jogada):
        jogada['monte_carlo'] = True
        self.jogada = jogada
        self.card = None
        self.player = None

        if 'card' in jogada:
            self.card = jogada['card']

        if 'player' in jogada:
            self.player = jogada['player']

    def __repr__(self):
        return "type:{0} card:{1} player:{2}".format(
            self.jogada['type'],
            self.card,
            self.player
        )
        

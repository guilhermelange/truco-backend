import copy
from truco import Algorithm, Game
from state import AbstractGameState
from state import AbstractAction
from mcts import MonteCarloTreeSearchNode
from search import MonteCarloTreeSearch

import session

def otherPlayer(playerIndex):
    if playerIndex == 0:
        return 1
    else:
        return 0

def getMatchPlayer(playerIndex):
    if playerIndex == 0:
        return -1
    else:
        return 1

class MonteCarloTreeSearchAlgorithm(Algorithm):

    #apenas para o autocomplete
    game: Game

    def getJogada(self, jogadaAdversario=None):
        cartas = [{},{}]
        cartas[self.id] = self.hand
        cartas[otherPlayer(self.id)] = self.handAdversario
        
        rodadaJogadas = [jogada for jogada in self.game.jogadas if jogada['type'] != 'TIE']
        state = {
            'jogadas': rodadaJogadas,
            'cartas': cartas,
            'manilha': self.game.num_manilha
        }
        
        game_state = TrucoGameState(state, next_to_move=self.id, matchPlayer=getMatchPlayer(self.id))

        root = MonteCarloTreeSearchNode(state=game_state)
        mcts = MonteCarloTreeSearch(root)
        best_node = mcts.getBestAction(simulations_number=5000)

        resultado = best_node.state.dados['jogadas'][-1]

        if resultado['type'] =='PLAY':
           self.popCarta(resultado['card'])

        return resultado

class TrucoGameState(AbstractGameState):

    def __init__(self, state, next_to_move=1, matchPlayer=None):
        self.dados = state
        self.next_to_move = next_to_move
        self.matchPlayer = matchPlayer

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
        partidaEmpate = False
        empate = False
        self.winner = None
        jogadas = self.dados['jogadas']
        self.jogadas_empate = [False, False, False]
        acceptedCount = 0

        user_jogadas = [0, 0]
        win_count = [0, 0]
        win_counts = []
        self.plays_count = 0
        self.player_truco = None
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
                    #print('Passo1: ' +  str(type(self.winner)))
                    break
                elif jogada['type'] == 'TRUCO':
                    self.player_truco = jogada['player']
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

                    if self.cardEquals(user_jogadas[player]['card'], user_jogadas[varOtherPlayer]['card']):
                        self.jogadas_empate[rodada] = True
                    elif self.cardWins(user_jogadas[player]['card'], user_jogadas[varOtherPlayer]['card']):
                        win_count[player] += 1
                        win_counts.append(user_jogadas[player]['player'])
                    else:
                        win_count[varOtherPlayer] += 1
                        win_counts.append(user_jogadas[varOtherPlayer]['player'])

                    user_jogadas = [0, 0]
                    rodada += 1

        rodada -= 1
        if player != None and win_count[player] >= 2:
            self.winner = player
            #print('Passo2: ' +  str(type(self.winner)))
        elif varOtherPlayer != None and win_count[varOtherPlayer] >= 2:
            self.winner = varOtherPlayer
            #print('Passo3: ' +  str(type(self.winner)))

        if self.winner == None:
            # Verifica empate
            if self.jogadas_empate == [True, False, False]:
                if rodada == 1 and len(win_counts) > 0:
                    self.winner = win_counts[-1]
                    #print('Passo4: ' +  str(type(self.winner)))

            elif self.jogadas_empate == [False, True, False]:
                if rodada == 1  and len(win_counts) > 0:
                    self.winner = win_counts[0]
                    #print('Passo5: ' + str(type(self.winner)))

            elif self.jogadas_empate == [True, True, False]:
                if rodada == 2  and len(win_counts) > 0:
                    self.winner = win_counts[-1]
                    #print('Passo6: ' + str(type(self.winner)))

            elif self.jogadas_empate == [False, False, True]:
                if rodada == 2  and len(win_counts) > 0:
                    self.winner = win_counts[0]
                    #print('Passo7: ' + str(type(self.winner)))

            elif self.jogadas_empate == [True, True, True]:
                partidaEmpate = True

        rodada += 1
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

        #print('Winner: ' + str(self.winner))
        #print(' ')
        #print(' ')
        if self.winner == 0:
            return -1
        else:
            return 1

    def isGameOver(self):
        return self.game_result is not None

    def doAction(self, move):
        newState = copy.deepcopy(self.dados)
        newState['jogadas'].append(move.jogada)

        if 'card' in move.jogada:
            indexCarta = newState['cartas'][self.next_to_move].index(move.jogada['card'])
            newState['cartas'][self.next_to_move].pop(indexCarta)
        
        return type(self)(newState, otherPlayer(self.next_to_move), self.matchPlayer)

    def getLegalActions(self):
        jogadas = self.dados['jogadas']
        moves = []

        if len(jogadas) > 0 and jogadas[-1]['type'] == 'TRUCO':
            moves.append(TrucoMove({"type": "ACCEPT", "player": self.next_to_move}))
            moves.append(TrucoMove({"type": "RUN", "player": self.next_to_move}))
        else:
            for carta in self.dados['cartas'][self.next_to_move]:
                moves.append(TrucoMove({"type": "PLAY", "card": carta, "player": self.next_to_move}))

            # if len(jogadas) > 0 and jogadas[-1]['player'] != self.next_to_move:
            #     if self.player_truco == None:
            #         moves.append(TrucoMove({"type": "TRUCO", "player": self.next_to_move}))
            #     elif self.player_truco != self.next_to_move:
            #         moves.append(TrucoMove({"type": "TRUCO", "player": self.next_to_move}))

        return moves


class TrucoMove(AbstractAction):
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
        

from flask import Flask, request, jsonify
import json
from truco import Match
from randomico import AlgoritmoRandomico
from monte_carlo import AlogritmoMonteCarloTreeSearch
from baseline import AlgoritmoBaseline

app = Flask(__name__)


@app.post('/match')
def match_post_route():
    data = json.loads(request.data)
    return jsonify(runMatch(data[0], data[1]))


def runMatch(algorithmA, algorithmB):
    match = Match(getAlgorithm(algorithmA), getAlgorithm(algorithmB))
    return match.playMatch()


def getAlgorithm(algorithm):
    if algorithm['algorithm'] == 'RANDOM':
        return AlgoritmoRandomico(algorithm['id'])
    elif algorithm['algorithm'] == 'BASELINE':
        return AlgoritmoBaseline(algorithm['id'])
    else:
        return AlogritmoMonteCarloTreeSearch(algorithm['id'])


# 1 - Ativar o virtual_envoroment rodando o env/Scripts/Activate.ps1 no powerShell
# 2 - rodar "flask --app server run" no terminal para iniciar o server de desenvolvimento

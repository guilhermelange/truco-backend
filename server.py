from flask import Flask, request, jsonify
import json
from model import AlgoritmoRandomico, Match

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
        return None #Retornar Baseline aqui
    else:
        return None #Retornar Monte Carlo Tree Search aqui

    

# 1 - Ativar o virtual_envoroment rodando o env/Scripts/Activate.ps1 no powerShell
# 2 - rodar "flask --app server run" no terminal para iniciar o server de desenvolvimento